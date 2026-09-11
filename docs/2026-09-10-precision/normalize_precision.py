#!/usr/bin/env python3
"""Normalise reported measurements in manuscript.md to two decimal places.

Rule (CLAUDE.md "Numeric presentation"): every *measured* quantity in a table or
in prose is printed with exactly two decimals, computed from the deposited
artifact — never by appending a digit to an already-rounded value. Parameters,
thresholds and counts keep their native form.

Source of cell→artifact mapping: docs/2026-09-05-astra-review/pass3-table-cells.tsv
(columns: table, manuscript_line, row, column, printed, artifact_value, verdict, source).

Usage: normalize_precision.py [--apply]   (default: dry run — writes *.dryrun.json/.md only, never touches the live edit log)
Outputs (docs/2026-09-10-precision/):
  precision-edits.json   old/new/line/source per edit (same shape as pass3-edits.json)
  precision-report.md    what changed, what was left and why
"""
import csv, io, json, os, re, sys
from decimal import Decimal, ROUND_HALF_UP
Q2 = Decimal("0.01")
def fmt2(v):
    """Decimal ROUND_HALF_UP to two places (author decision 2026-09-10; NOT float :.2f)."""
    return str(Decimal(str(v)).quantize(Q2, rounding=ROUND_HALF_UP))
from collections import defaultdict, Counter

ROOT = os.path.expanduser("~/scratch/devel/bwt-algorithm")
os.chdir(ROOT)
OUT = "docs/2026-09-10-precision"; os.makedirs(OUT, exist_ok=True)
TSV = "docs/2026-09-05-astra-review/pass3-table-cells.tsv"
APPLY = "--apply" in sys.argv

def to_hours(s):
    """'33.7294', '03:12:24', '1-02:03:04' → float hours; None if not parseable."""
    s = s.strip()
    m = re.fullmatch(r"(?:(\d+)-)?(\d{1,2}):(\d{2}):(\d{2})", s)
    if m:
        d, h, mi, se = (int(x) if x else 0 for x in m.groups())
        return Decimal(d*86400 + h*3600 + mi*60 + se) / Decimal(3600)
    try: return Decimal(s.replace(",", ""))
    except ValueError: return None

lines = io.open("manuscript.md", encoding="utf-8").read().split("\n")
rows = list(csv.DictReader(open(TSV), delimiter="\t"))
is1dp = lambda s: re.fullmatch(r"-?[\d,]+\.\d", s or "") is not None

edits, skipped = [], []
# ---------- 1. table cells ----------
cell_map = defaultdict(set)   # (printed, unit) -> {new}
for r in rows:
    if not is1dp(r["printed"]): continue
    v = to_hours(r["artifact_value"])
    if v is None:
        skipped.append((r["manuscript_line"], r["column"], r["printed"], "artifact not numeric: " + r["artifact_value"][:30])); continue
    if ":" not in r["artifact_value"] and -v.as_tuple().exponent < 2:
        skipped.append((r["manuscript_line"], r["column"], r["printed"], "artifact has fewer than two decimals — do not append a digit (CLAUDE.md rule 3)")); continue
    if abs(v - Decimal(r["printed"].replace(",", ""))) > Decimal("0.05"):
        skipped.append((r["manuscript_line"], r["column"], r["printed"], f"guard: artifact {v:.4f} is not within 0.05 of printed")); continue
    new = fmt2(v)
    ln = int(r["manuscript_line"]) - 1
    line = lines[ln]
    if not any(part.strip().split(" (")[0][:8] in line for part in r["row"].split("/")):
        skipped.append((r["manuscript_line"], r["column"], r["printed"], "row label not on that line")); continue
    cells = line.split("|")
    hits = [i for i, c in enumerate(cells) if c.strip() == r["printed"]]
    if len(hits) != 1:
        skipped.append((r["manuscript_line"], r["column"], r["printed"], f"{len(hits)} cells equal printed on line")); continue
    cells[hits[0]] = cells[hits[0]].replace(r["printed"], new)
    old_line = line; lines[ln] = "|".join(cells)
    unit = "h" if "Runtime" in r["column"] else ("bp" if "Offset" in r["column"] else r["column"])
    cell_map[(r["printed"], unit)].add(new)
    edits.append({"line": ln+1, "kind": "table", "table": r["table"], "row": r["row"], "column": r["column"],
                  "old": r["printed"], "new": new, "artifact_value": r["artifact_value"], "source": r["source"],
                  "check": f"python3 -c \"from decimal import *; print(Decimal('{v}').quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))\"  # from {r['source'][:60]}"})

# ---------- 2. prose mirrors of table cells (hours only; unambiguous values) ----------
hour_pat = re.compile(r"(?<![\w.])(\d+\.\d)(?=(?:\s?h\b|\s?hours?\b|-hour\b))")
prose_ambiguous = Counter()
for ln, line in enumerate(lines):
    if line.startswith("|"): continue
    def sub(m):
        old = m.group(1); news = cell_map.get((old, "h"), set())
        if len(news) == 1:
            new = next(iter(news))
            edits.append({"line": ln+1, "kind": "prose", "old": old, "new": new, "context": line[max(0,m.start()-40):m.end()+20],
                          "source": "same artifact as the table cell printing " + old + " h"})
            return new
        if len(news) > 1: prose_ambiguous[old] += 1
        return old
    lines[ln] = hour_pat.sub(sub, line)

# ---------- 2b. explicit contextual edits: ambiguous '5.5' (TRF maize 3B 5.51 vs 3C 5.48) and core-hours ----------
EXPLICIT = [
    ("while TRF's rose from 5.2 to 5.5 h", "while TRF's rose from 5.22 to 5.51 h",
     "Table 3A TRF 5.216944 h (6 bp) → Table 3B TRF 5.514167 h (500 bp); competitor_logs trf__GCA_022117705.1"),
    ("was flat, at 5.22 h, 5.5 h and 5.5 h", "was flat, at 5.22 h, 5.51 h and 5.48 h",
     "Tables 3A/3B/3C TRF runtimes 5.216944 / 5.514167 / 5.482222 h; at two decimals the three are not identical"),
    ("in 12 h 39 m (25.3 core-hours over two threads)", "in 12 h 39 m (25.29 core-hours over two threads)",
     "12.645 h (sacct 6110901.batch) × 2 threads = 25.29"),
    ("took 29.78 h (59.6 core-hours)", "took 29.78 h (59.56 core-hours)",
     "29.780278 h (competitor_logs ultra__GRCh38) × 2 threads = 59.56"),
    ("giving 25.3, 59.6 and 33.7 core-hours", "giving 25.29, 59.56 and 33.73 core-hours",
     "12.645×2, 29.780278×2, 33.729444×1 (thread counts stated in the same sentence)"),
]
for old, new, src in EXPLICIT:
    hits = [i for i, l in enumerate(lines) if old in l]
    if len(hits) == 1:
        lines[hits[0]] = lines[hits[0]].replace(old, new, 1)
        edits.append({"line": hits[0]+1, "kind": "prose-explicit", "old": old, "new": new, "source": src})
    else:
        skipped.append(("prose", "explicit", old, f"{len(hits)} matches"))

# ---------- 3. inventory of remaining 1-dp prose tokens (not changed) ----------
left = []
tok = re.compile(r"(?<![\w.])(\d{1,3}(?:,\d{3})*|\d+)\.(\d)(?![\w.])")
for ln, line in enumerate(lines):
    if line.startswith("|"): continue
    for m in tok.finditer(line):
        before = line[max(0, m.start()-12):m.start()]
        if re.search(r"(Section|Sections|Table|Tables|Figure|Fig\.|S|v|version)\s*$", before): continue
        left.append((ln+1, m.group(0), line[max(0,m.start()-30):m.end()+25].replace("|"," ")))

# ---------- write ----------
SUF = "" if APPLY else ".dryrun"
json.dump(edits, io.open(f"{OUT}/precision-edits{SUF}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
rep = io.open(f"{OUT}/precision-report{SUF}.md", "w", encoding="utf-8")
rep.write("# Precision normalisation — 2026-09-10\n\n")
rep.write(f"Mode: {'APPLIED' if APPLY else 'DRY RUN'}. Rule: measurements at two decimals, computed from the deposited artifact named per edit.\n\n")
rep.write(f"## Table cells changed: {sum(1 for e in edits if e['kind']=='table')}\n\n| line | table | row | column | old | new | artifact | source |\n|---|---|---|---|---|---|---|---|\n")
for e in edits:
    if e["kind"]=="table": rep.write(f"| {e['line']} | {e['table']} | {e['row'][:28]} | {e['column']} | {e['old']} | **{e['new']}** | {e['artifact_value'][:14]} | {e['source'][:50]} |\n")
rep.write(f"\n## Prose mirrors changed: {sum(1 for e in edits if e['kind']=='prose')}\n\n")
for e in edits:
    if e["kind"]=="prose": rep.write(f"- L{e['line']}: `{e['old']}` → **{e['new']}** — …{e['context'].strip()}…\n")
rep.write(f"\n## Skipped table cells: {len(skipped)}\n\n")
for s in skipped: rep.write(f"- L{s[0]} {s[1]} `{s[2]}`: {s[3]}\n")
rep.write(f"\n## Ambiguous prose values (same printed value, different artifacts): {dict(prose_ambiguous)}\n\n")
rep.write("These need the row context to resolve; see the todo entry.\n")
rep.write(f"\n## Remaining 1-dp tokens in prose, not changed (no table-cell artifact): {len(left)}\n\n")
for l in left: rep.write(f"- L{l[0]} `{l[1]}` …{l[2].strip()}…\n")
rep.close()
if APPLY:
    io.open("manuscript.md", "w", encoding="utf-8").write("\n".join(lines))
print(f"{'APPLIED' if APPLY else 'DRY RUN'}: table edits={sum(1 for e in edits if e['kind']=='table')} prose edits={sum(1 for e in edits if e['kind']=='prose')} skipped={len(skipped)} ambiguous={dict(prose_ambiguous)} remaining_prose_1dp={len(left)}")
