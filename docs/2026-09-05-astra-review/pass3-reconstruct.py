#!/usr/bin/env python3
"""Regenerate the "Table sweep" section of pass3-results-tables.md from the
pass-3 cell-comparison TSVs. Read-only. Run from the repository root:

    python3 docs/2026-09-05-astra-review/pass3-reconstruct.py            # after-edit sweep
    python3 docs/2026-09-05-astra-review/pass3-reconstruct.py --before   # pre-edit sweep

In these TSVs `REJECTED` means the suspicion that a cell is wrong was rejected,
i.e. the printed cell equals the artifact value at the printed precision
(pass3-table-cells.py, ROUND_HALF_UP). `CONFIRMED` means printed != artifact.
"""
import csv, sys
from collections import Counter, OrderedDict
from pathlib import Path

HERE = Path(__file__).resolve().parent
name = "pass3-table-cells-before.tsv" if "--before" in sys.argv else "pass3-table-cells.tsv"
rows = list(csv.DictReader((HERE / name).open(), delimiter="\t"))

tables = OrderedDict()
for r in rows:
    t = tables.setdefault(r["table"], {"n": 0, "v": Counter(), "lines": [], "sources": Counter()})
    t["n"] += 1
    t["v"][r["verdict"]] += 1
    t["lines"].append(int(r["manuscript_line"]))
    t["sources"][r["source"].split(";")[0].strip()] += 1

tot = Counter(r["verdict"] for r in rows)
print(f"Source: `{name}` ({len(rows)} cells, {len(tables)} tables). "
      f"Verdicts: {tot.get('REJECTED', 0)} match (`REJECTED`), "
      f"{tot.get('CONFIRMED', 0)} mismatch (`CONFIRMED`), "
      f"{tot.get('BLOCKED-ON-MISSING-ARTIFACT', 0)} `BLOCKED-ON-MISSING-ARTIFACT`.")
print()
print("| Table | Manuscript lines | Cells | Match | Mismatch | Blocked | Primary artifact(s) |")
print("|---|---|---:|---:|---:|---:|---|")
for k, t in tables.items():
    src = "; ".join(f"`{s}` ({c})" for s, c in t["sources"].most_common(3))
    print(f"| {k} | {min(t['lines'])}–{max(t['lines'])} | {t['n']} | {t['v'].get('REJECTED', 0)} | "
          f"{t['v'].get('CONFIRMED', 0)} | {t['v'].get('BLOCKED-ON-MISSING-ARTIFACT', 0)} | {src} |")
print()
odd = [r for r in rows if r["verdict"] != "REJECTED"]
if odd:
    print("Cells not matching, or blocked:")
    print()
    print("| Table | Line | Row | Column | Printed | Artifact value | Verdict | Source |")
    print("|---|---|---|---|---|---|---|---|")
    for r in odd:
        print(f"| {r['table']} | {r['manuscript_line']} | {r['row']} | {r['column']} | {r['printed']} | "
              f"{r['artifact_value']} | {r['verdict']} | {r['source']} |")
