#!/usr/bin/env python3
"""Switch the 2026-09-10 precision edits from Python :.2f (binary float) to
decimal ROUND_HALF_UP (author decision 2026-09-10), and audit every table cell
in pass3-table-cells.tsv against the half-up rule."""
import csv, io, json, os, re
from decimal import Decimal, ROUND_HALF_UP
os.chdir(os.path.expanduser("~/scratch/devel/bwt-algorithm"))
OUT="docs/2026-09-10-precision"; TSV="docs/2026-09-05-astra-review/pass3-table-cells.tsv"
Q=Decimal("0.01")
def dec(s):
    s=s.strip()
    m=re.fullmatch(r"(?:(\d+)-)?(\d{1,2}):(\d{2}):(\d{2})", s)
    if m:
        d,h,mi,se=(int(x) if x else 0 for x in m.groups())
        return (Decimal(d*86400+h*3600+mi*60+se)/Decimal(3600))
    try: return Decimal(s.replace(",",""))
    except Exception: return None
hu=lambda d: str(d.quantize(Q, rounding=ROUND_HALF_UP))
f2=lambda d: f"{float(d):.2f}"

lines=io.open("manuscript.md",encoding="utf-8").read().split("\n")
edits=json.load(io.open(f"{OUT}/precision-edits.json",encoding="utf-8"))
changed=[]; hu_map={}
for e in edits:
    if e["kind"]!="table": continue
    d=dec(e["artifact_value"]); new_hu=hu(d)
    hu_map[(e["old"], "h" if "Runtime" in e["column"] else "x")]=new_hu
    e["rounding"]="half-up"; e["new_f2"]=e["new"]
    if new_hu!=e["new"]:
        ln=e["line"]-1; cells=lines[ln].split("|")
        hits=[i for i,c in enumerate(cells) if c.strip()==e["new"]]
        assert len(hits)==1, (e["line"], e["new"], hits)
        cells[hits[0]]=cells[hits[0]].replace(e["new"], new_hu); lines[ln]="|".join(cells)
        changed.append((e["line"],"table",e["row"],e["column"],e["new"],new_hu,e["artifact_value"])); e["new"]=new_hu
for e in edits:
    if e["kind"]!="prose": continue
    new_hu=hu_map.get((e["old"],"h"))
    e["rounding"]="half-up"; e["new_f2"]=e["new"]
    if new_hu and new_hu!=e["new"]:
        ln=e["line"]-1
        pat=re.compile(r"(?<![\w.])"+re.escape(e["new"])+r"(?=(?:\s?h\b|\s?hours?\b|-hour\b))")
        lines[ln],n=pat.subn(new_hu, lines[ln], count=1); assert n==1,(e["line"],e["new"])
        changed.append((e["line"],"prose",e.get("context","")[:40],"",e["new"],new_hu,"mirror of table cell")); e["new"]=new_hu
# explicit edits: recompute stated formulas under half-up
EXPL={"25.29":Decimal("12.645")*2, "59.56":Decimal("29.780278")*2, "33.73":Decimal("33.729444"), "5.51":Decimal("5.514167"), "5.48":Decimal("5.482222"), "5.22":Decimal("5.216944")}
for e in edits:
    if e["kind"]!="prose-explicit": continue
    e["rounding"]="half-up"
    for tok,val in EXPL.items():
        if tok in e["new"] and hu(val)!=tok: changed.append((e["line"],"explicit",tok,"",tok,hu(val),"CHECK"))
# ---- audit: all numeric cells in the TSV vs half-up and vs :.2f ----
rows=list(csv.DictReader(open(TSV),delimiter="\t"))
mism_hu=[]; f2_vs_hu=[]
for r in rows:
    d=dec(r["artifact_value"]);
    if d is None or not re.fullmatch(r"-?[\d,]+\.\d\d", r["printed"] or ""): continue
    p=r["printed"].replace(",","")
    if hu(d)!=p: mism_hu.append((r["manuscript_line"],r["table"],r["row"][:25],r["column"],p,hu(d),f2(d),r["artifact_value"][:16],r["source"][:45]))
    if hu(d)!=f2(d): f2_vs_hu.append((r["manuscript_line"],r["column"],p,hu(d),f2(d),r["artifact_value"][:16]))
io.open("manuscript.md","w",encoding="utf-8").write("\n".join(lines))
json.dump(edits, io.open(f"{OUT}/precision-edits.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
rep=io.open(f"{OUT}/precision-report.md","a",encoding="utf-8")
rep.write("\n\n# Addendum 2026-09-10 — rounding convention changed to decimal ROUND_HALF_UP (author decision)\n\n")
rep.write(f"Re-applied over the 94 edits. Values that differ between `:.2f` and half-up: {len(changed)}\n\n| line | kind | row | column | :.2f | half-up | artifact |\n|---|---|---|---|---|---|---|\n")
for c in changed: rep.write(f"| {c[0]} | {c[1]} | {c[2]} | {c[3]} | {c[4]} | **{c[5]}** | {c[6]} |\n")
rep.write(f"\n## Audit of pre-existing two-decimal table cells against half-up: {len(mism_hu)} mismatches\n\n")
rep.write("| line | table | row | column | printed | half-up | :.2f | artifact | source |\n|---|---|---|---|---|---|---|---|---|\n")
for m in mism_hu: rep.write("| "+" | ".join(str(x) for x in m)+" |\n")
rep.write(f"\n## Cells where :.2f and half-up disagree at all (informational): {len(f2_vs_hu)}\n\n")
for m in f2_vs_hu: rep.write(f"- L{m[0]} {m[1]}: printed {m[2]}, half-up {m[3]}, :.2f {m[4]}, artifact {m[5]}\n")
rep.close()
print("changed:",len(changed)); [print("  ",c) for c in changed]
print("pre-existing 2dp cells mismatching half-up:",len(mism_hu)); [print("  ",m) for m in mism_hu]
print("f2 vs half-up disagreements total:",len(f2_vs_hu))
