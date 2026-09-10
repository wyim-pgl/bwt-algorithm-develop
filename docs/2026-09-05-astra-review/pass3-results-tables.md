# Pass 3 — Results and tables vs deposited artifacts (RECONSTRUCTED 2026-09-10)

> ⚠️ This report was reconstructed on 2026-09-10 from the pass's artifacts and transcript
> after the pass was cut off at 21:41 on 2026-09-05 (quarantine.md §1.4). The reviewer
> never wrote it. Every verdict below is either quoted from pass3.log (with the log line
> number) or derived from pass3-table-cells.tsv; nothing is inferred beyond that.

The pass prompt (pass3.log:37) named the intended report `pass3-results-vs-artifacts.md`; that file was never created. This reconstruction is written under the name the author chose. The transcript ran with `reasoning summaries: none` (pass3.log:10), so the reviewer's rationale exists only in five short narrative blocks (pass3.log:38, 2861, 4442, 6494, 7506), in the comments of the edit script it wrote (pass3.log:7813–7923), and in the command outputs. Where none of those covers an edit, the edit is listed as `APPLIED-RATIONALE-NOT-RECOVERED`.

## Summary

**13 CONFIRMED, 1 REJECTED, 1 BLOCKED-ON-MISSING-ARTIFACT, 1 APPLIED-RATIONALE-NOT-RECOVERED (covering 5 edits); 0 SUSPECTED.**

The most serious thing the artifacts show is that, before the pass, eight table cells did not equal their deposited artifacts: three Table 1a unique-region counts for TRF, ULTRA and tantan (18,900 / 518,405 / 518,443 printed against 18,904 / 518,440 / 518,488 in the deposited full-range BEDs), one Table 2 TRF runtime (131.9 against an exact 131.95 h), three tantan memory cells (0.09 / 0.50 / 0.50 against sacct cgroup peaks of 0.10 / 0.48 / 0.37 GiB) and one Table 3C AniAnn's fragmentation score (0.22 against 0.21). All eight were corrected, and the after-edit sweep matches all 586 checkable cells. The single most serious unfinished item is that the reviewer's independent `bedtools intersect -v` cross-check of the new TRF unique count never completed (see "Where the log stopped"), so the three Table 1a counts rest on one method, `pass3-checks.py human`.

Beyond the cells, the pass corrected one false superlative (AniAnn's was not the highest banded recall on CEN180: ULTRA leads the 150–400 band and TRASH leads the 150–200 band), one contradiction (Table 1c prose said AniAnn's had no row while its row was present), three rounding statements derived from already-rounded cells (0.02→0.03 pp, 0.13→0.14 pp, 15.18→15.17 pp), and it placed Figures 2–5, S1 and S2 with captions written against the deposited figure data. No edit improved a BWTandem number; every numeric change moved a competitor value or widened a gap against BWTandem.

Table sweep coverage: 590 numeric cells across 16 tables (1a–1e, 2, 3A, 3A-b, 3B, 3B-b, 3C, 3C-b, S2, S3, S4a, S4b); 586 match the artifact at the printed precision, 4 are `BLOCKED-ON-MISSING-ARTIFACT`. Table S1 (commands/versions) was deliberately excluded from the sweep (pass3-table-cells.py:128, "audited against logs by pass 2"). In the sweep TSVs, `REJECTED` means the suspicion that a cell is wrong was rejected, i.e. the cell matches.

Baseline for claim citations is **`3e728cce5be3a530d75b8e3501d5bdb8409e1f43`**. Pre-pass text is recoverable with `git show 3e728cc:manuscript.md | sed -n 'Np'`. "Current line" numbers refer to manuscript.md as of 2026-09-10; note that the 2026-09-10 precision pass (`docs/2026-09-10-precision/precision-edits.json`, 94 cells) has since rewritten many numeric cells to two decimals, so current table rows may not read byte-for-byte as pass 3 left them. Those precision edits are not pass-3 edits.

Supporting artifacts, all in `docs/2026-09-05-astra-review/`:

- `pass3-edits.json`: the 46 {old,new} replacements applied by `/tmp/pass3-edit.py` (pass3.log:7813–7925, "Applied 46 targeted replacements"). 45 are in the current manuscript; E21 is not, because E22 replaced it within the same script (E22's `old` equals E21's `new`). A 47th manuscript edit was applied outside this JSON (pass3.log:8123; see P3-16).
- `pass3-table-cells.py`, `pass3-table-cells.tsv`, `pass3-table-cells-before.tsv`: cell-by-cell sweep after and before the edits (the before-snapshot was `/tmp/astra-pass3-manuscript-before.md`, pass3.log:5788).
- `pass3-checks.py` with modes `colcen`, `maize`, `costs`, `fig5`, `human`, and their outputs `pass3-colcen.json`, `pass3-maize.json`, `pass3-costs.json`, `pass3-fig5.jsonl`, `pass3-human.json`. `pass3-maize3a-extra.json` (NCRF and TRASH TAG-substring metrics, written at pass3.log:7517) is read by the sweep for the Table 3A rows (pass3.log:7941).
- `pass3-reconstruct.py` (added 2026-09-10): regenerates the "Table sweep" section from the TSVs.

No `results/`, `todo.md` or `quarantine.md` file was edited by pass 3 (see REHASH REQUIRED).

### Edit inventory

Verdict column: C = CONFIRMED (rationale located in the log), N = APPLIED-RATIONALE-NOT-RECOVERED. "Log" is the line of the applying statement in the edit script; "rationale" points to the narrative block, script comment or command output that justifies it.

| Edit | Baseline line → current | Change (gist) | Log | Rationale | Finding | V |
|---|---|---|---|---|---|---|
| E01 | 123 → 129 | Table 1a TRF unique regions 18,900 → 18,904 | 7828–7830 | comment 7827; `pass3-human.json` (7694) | P3-01 | C |
| E02 | 125 → 131 | Table 1a ULTRA unique regions 518,405 → 518,440 | 7828–7830 | comment 7827; 7722 | P3-01 | C |
| E03 | 127 → 133 | Table 1a tantan unique regions 518,443 → 518,488 | 7828–7830 | comment 7827; 7750 | P3-01 | C |
| E04 | 113 → 115 | recall gap to ULTRA 0.02 → 0.03 pp "(after rounding)" | 7831–7832 | computed from `pass3-human.json` | P3-02 | C |
| E05 | 169 → 175 | high-recall span 79.80% → 79.82% | 7833 | score_table1_p100.txt (3936) | P3-02 | C |
| E06 | 119 → 125 | 2026 cost cells: scope matches BWTandem; GNU-time RSS ≠ cgroup peak; 2024 rows larger FASTA | 7834 | .time vs sacct (6233–6451); fig2 caption 3.92% (6290) | P3-10 | C |
| E07 | 144 → 150 | Table 1c: AniAnn's row is present, enters under prediction-period rule | 7835 | narrative 4442 | P3-05 | C |
| E08 | 111 → 113 | "range all tools shared" → "common output-period band (with FASTA scope differences)" | 7837 | comment 7836 | P3-10 | C |
| E09 | 133 → 139 | adds: output band ≠ execution range or FASTA scope; competitors processed unplaced sequence | 7838 | comment 7836; 6290 | P3-10 | C |
| E10 | 109 → 111 | "ranges and implementations" → "ranges, FASTA scopes and implementations" | 7839 | comment 7836 | P3-10 | C |
| E11 | 182 → 188 | TRF Col-CEN 131.9 → 131.95 hours (prose) | 7841 | comment 7840; costs 6392 | P3-03 | C |
| E12 | 197 → 205 | Table 2 TRF runtime 131.9 → 131.95 | 7842–7843 | same | P3-03 | C |
| E13 | 201 → 209 | Table 2 tantan memory 0.09 → 0.10 | 7844–7847 | narrative 6494; sacct 6085141 | P3-03 | C |
| E14 | 253 → 263 | Table 3B tantan memory 0.50 → 0.48 | 7844–7847 | sacct 6085142 | P3-03 | C |
| E15 | 300 → 310 | Table 3C tantan memory 0.50 → 0.37 | 7844–7847 | sacct 6085143 | P3-03 | C |
| E16 | 182 → 188 | tantan 0.09 → 0.10 GiB; "one twenty-fourth" → "about one twenty-third (unrounded)" | 7848 | 2.1638/0.0960 = 22.5 (`pass3-costs.json`) | P3-03 | C |
| E17 | 184 → 190 | tantan 0.10 GiB; two longdust runs 0.06 GiB | 7849 | .time files 6446–6447 | P3-03 | C |
| E18 | 184 → 190 | "twenty-four times the memory" → "twenty-three times (unrounded)" | 7850 | as E16 | P3-03 | C |
| E19 | 182 → 188 | TRF runtime: "upper bound… no plausible correction reverses" → "different period ceiling, observed not matched" | 7851 | none beyond group comment 7840 | P3-16 | N |
| E20 | 188 → 194 | AniAnn's no longer "highest banded recall"; ULTRA leads wide band, TRASH 99.39% leads narrow | 7853 | comment 7852; narrative 4442, 6494; `pass3-colcen.json` | P3-04 | C |
| E21 | 260 → (superseded) | band-loss sentence, first rewrite | 7854 | comment 7855 (replaced by E22) | P3-07 | C |
| E22 | (E21) → 270 | "smallest losses among the four tools with banded rows here in each class" | 7856 | comment 7855; `pass3-maize.json` losses | P3-07 | C |
| E23 | 260 → 270 | 2026 maize rows: no banded scoring artifact deposited | 7857 | `pass3-maize.json` banded=null (7350) | P3-07 | C |
| E24 | 242 → 250 | TR-1 baselines 4,282 bp (merged) vs 770.65 bp (raw) are different definitions | 7859 | comment 7858; narrative 7506; 4240, 7036 | P3-08 | C |
| E25 | 21 → 21 | Abstract: "within 0.13 pp" → "0.14 pp below" | 7861–7862 | narrative 7506; computed 0.1359 | P3-06 | C |
| E26 | 284 → 294 | "within 0.18 points of each other" → "span approximately 0.18 points" | 7863 | group comment 7860 only; 0.18 not recomputed | P3-16 | N |
| E27 | 284 → 294 | leading-group claim scoped to original tools; AniAnn's higher coverage in every class | 7864 | `pass3-maize.json` (7192–7342) | P3-09 | C |
| E28 | 286 → 296 | TRASH losses stated per class: 0.34 / 0.03 / 18.57 (rounded from unrounded) | 7865–7867 | narrative 7506; `pass3-maize.json` | P3-06 | C |
| E29 | 286 → 296 | TRF knob180 lead 15.18 → 15.17 | 7868–7869 | narrative 7506; computed 15.1743 | P3-06 | C |
| E30 | 302 → 312 | Table 3C AniAnn's Frag. score 0.22 → 0.21 | 7870 | `pass3-maize.json` frag 0.21 (7347) | P3-06 | C |
| E31 | 292 → 302 | Table 3C caption: original rows ordered by coverage, 2026 appended | 7872 | comment 7871 | P3-09 | C |
| E32 | 246 → 256 | Table 3B caption: "unfiltered coverage can only rise with range" → filtering/native-rerun distinction | 7873, 7878–7882 | comment 7871 | P3-10 | C |
| E33 | 292 → 302 | same sentence in Table 3C caption | 7878–7882 | comment 7871 | P3-10 | C |
| E34 | 182 → 188 | "98 times the core-hours" → "98.5" | 7885–7886 | computed 131.95/(2×0.6697)=98.51 | P3-03 | C |
| E35 | 182 → 188 | adds: ULTRA/TRF runs not range-matched | 7887 | none | P3-16 | N |
| E36 | 504 → 520 | S2: outside-catalog fractions "both round to 91.3%" | 7889 | comment 7888; s2_*_p100.txt (exec 4361) | P3-11 | C |
| E37 | 527 → 543 | S4: names corrected TRF arm, scorer commit 903245c | 7890 | comment 7888; P1-11; 2922, 3027 | P3-11 | C |
| E38 | 527 → 543 | S4: job 6146343 "metric-identical" → identical for matching/stratum counts, TRF periods superseded | 7891 | comment 7888; P1-11 | P3-11 | C |
| E39 | 527 → 543 | S4: no truth-period stratum validates period assignment above 500 bp | 7892 | group comment 7888 only | P3-16 | N |
| E40 | 154 → 160 | Figure 1 caption rewritten: three panels, 2026 points full-range, sources named | 7894–7896 | comment 7893; plot script 6253–6262 | P3-12 | C |
| E41 | 107 → 107–109 | Figure 2 placed and captioned (1.77–1.82, mean 1.79) | 7898–7899 | comment 7897; pass1-checks range (7556–7633) | P3-12 | C |
| E42 | 115 → 119–121 | Figure 3 placed (4/346/50; 4/400 = 1.0%; 4/350 = 1.1%; Wilson 0.4–2.9%) | 7900–7901 | pass1-checks audit (7556) | P3-12 | C |
| E43 | 190 → 196 | Figure 4 placed; TRASH and 2026 absent from panel C | 7902–7903 | comment 7897; `pass3-maize.json` banded=null | P3-12 | C |
| E44 | 242 → 250 | Figure S2 placed; gap-zero merge ≠ raw-call baseline | 7904–7905 | as E24 | P3-12 | C |
| E45 | 113 → 115 | Figure S1 placed; series is post-filtered full-range output | 7906–7907 | comment 7897 | P3-12 | C |
| E46 | 317 → 327 | Figure 5 placed with caption and text reference | 7909–7918 | comment 7908; `pass3-checks.py fig5` (6506–6508) | P3-13 | C |
| E47 | — → 496 | `\| BWTandem-F \| 1b, 1d \|` → `\| BWTandem-F \| 1b sensitivity analysis, 1d \|` (not in pass3-edits.json) | 8123 | none | P3-16 | N |

Re-runnable check for the whole inventory (45 of 46 JSON entries present; E21 superseded; E47 present):

```bash
/data/gpfs/assoc/pgl/bin/conda/conda_envs/bwtandem/bin/python - <<'PY'
import json
E=json.load(open('docs/2026-09-05-astra-review/pass3-edits.json')); s=open('manuscript.md').read()
miss=[i+1 for i,e in enumerate(E) if e['new'] not in s]
print(len(E),'edits; not present verbatim:',miss)   # expect [21] plus rows the 2026-09-10 precision pass reformatted
print('E22 old == E21 new:', E[21]['old']==E[20]['new'])
print('E47 present:', '| BWTandem-F | 1b sensitivity analysis, 1d |' in s)
PY
sed -n '8120,8127p' docs/2026-09-05-astra-review/pass3.log
```

Note: E01–E03, E14 and E15 are not present verbatim today only because the 2026-09-10 precision pass rewrote other cells on the same rows; the pass-3 values (18,904; 518,440; 518,488; 0.48; 0.37) are in current lines 129, 131, 133, 263 and 310.

## Findings

### P3-01 — CONFIRMED — Table 1a unique-region counts were stale for TRF, ULTRA and tantan

- **Claim:** manuscript.md:123,125,127 (baseline) printed 18,900 / 518,405 / 518,443 unique regions; current lines 129, 131, 133.
- **Evidence:** `pass3-checks.py human` (pass3.log:7449–7519, output 7654–7811) counted unique unfiltered regions from the deposited BEDs named in `results/manifest.tsv` Table 1a rows: TRF 18,904, ULTRA 518,440, tantan 518,488 (`pass3-human.json`, pass3.log:7694, 7722, 7750). The reviewer's script comment: "Table 1: derive from the current, deposited full-range BED, not the old comparator union" (pass3.log:7827). The pre-edit sweep records all three as `CONFIRMED` mismatches (`pass3-table-cells-before.tsv`, rows 1a/Unique Regions); the after-edit sweep records them as matching. The older figure-input table `unique_regions_human.tsv` was also read (pass3.log:6664–6719) and is the likely origin of the old values; the log does not state this explicitly.
- **Check:**

```bash
python3 -c "import json;h=json.load(open('docs/2026-09-05-astra-review/pass3-human.json'));print({t:h[t]['unique_unfiltered'] for t in ['TRF','ULTRA','tantan']})"
grep -P '\tUnique Regions\t' docs/2026-09-05-astra-review/pass3-table-cells-before.tsv
/data/gpfs/assoc/pgl/bin/conda/conda_envs/bwtandem/bin/python docs/2026-09-05-astra-review/pass3-checks.py human   # slow; regenerates pass3-human.json
```

- **Fix applied:** yes (E01–E03). All three competitor counts went up; BWTandem's own count was not changed. The independent `bedtools intersect -v` cross-check of the TRF count was started and never finished (see "Where the log stopped").

### P3-02 — CONFIRMED — Human prose rounded from rounded cells

- **Claim:** manuscript.md:113 "gap to ULTRA is 0.02 percentage points (81.60 versus 81.62)"; manuscript.md:169 "span 79.80% to 87.98%".
- **Evidence:** ULTRA ≤100 bp region recall 81.62185 and native-H recall 81.59546 (`pass3-human.json`) differ by 0.0264, which rounds to 0.03, not to the 0.02 obtained from the rounded cells (pass3.log:7831–7832 computes `gap` from the JSON). The 79.82% lower bound is BWTandem's recall in `results/regen/score_table1_p100.txt` (pass3.log:3936).
- **Check:** `python3 -c "import json;h=json.load(open('docs/2026-09-05-astra-review/pass3-human.json'));print(h['ULTRA']['scores']['le100']['recall']-h['native-H']['recall'])"`; `grep -n '79.82' results/regen/score_table1_p100.txt`.
- **Fix applied:** yes (E04, E05); the gap against BWTandem widened.

### P3-03 — CONFIRMED — Cost cells did not equal their accounting sources

- **Claim:** manuscript.md:182,197 TRF Col-CEN 131.9 h; manuscript.md:201,253,300 tantan memory 0.09 / 0.50 / 0.50 GiB; manuscript.md:182,184 the derived ratios "one twenty-fourth", "twenty-four times", "98 times the core-hours".
- **Evidence:** `pass3-checks.py costs` (`pass3-costs.json`, pass3.log:6263, printed 6336–6452): `trf__Col-CEN_v1.2_run.log` gives 475,020 s = 131.95 h exactly, a rounding tie the reviewer chose to keep at the hundredth ("retain an exact hundredth-hour at the TRF rounding tie", pass3.log:7840). sacct MaxRSS for the tantan reruns: 6085141 0.09599 GiB, 6085142 0.48378 GiB, 6085143 0.37294 GiB, which `results/manifest.tsv` already listed as 0.10 / 0.48 / 0.37 (pass3.log:6462–6464). Narrative: "the widened tantan rows retain older memory values rather than the cgroup peaks recorded for those reruns" (pass3.log:6494). BWTandem Col-CEN peak 2.16379 GiB / 0.09599 = 22.5, hence "about one twenty-third"; 131.95 / (2 × 0.66972 h) = 98.51 core-hour ratio (pass3.log:7885). longdust Col-CEN RSS 0.06296 and 0.06327 GiB from the two `.time` files (pass3.log:6446–6447).
- **Check:**

```bash
python3 -c "import json;c=json.load(open('docs/2026-09-05-astra-review/pass3-costs.json'));[print(k,c[k]) for k in ['results/competitor_logs/trf__Col-CEN_v1.2_run.log','sacct:6085141.batch','sacct:6085142.batch','sacct:6085143.batch','sacct:6110900.batch']]"
grep -P '\tMemory \(GiB\)\t0\.(09|50)\t' docs/2026-09-05-astra-review/pass3-table-cells-before.tsv
```

- **Fix applied:** yes (E11–E18, E34). Every changed memory value is a competitor's; two went down.

### P3-04 — CONFIRMED — CEN180 banded-recall superlative was false

- **Claim:** manuscript.md:188 "AniAnn's … the highest banded recall of any tool here".
- **Evidence:** `pass3-checks.py colcen` recomputed every Table 2 cell and the band recalls (`pass3-colcen.json`, pass3.log:6336–6355): AniAnn's 99.154% in both bands; ULTRA 99.786% in 150–400; TRASH (de novo and template) 99.388% in both bands. Narrative: "the CEN180 text calls AniAnn's the banded-recall leader even though ULTRA is higher in the wider band" (pass3.log:4442) and "TRASH ahead of AniAnn's in the narrow band" (pass3.log:6494); script comment "The superlative is false both in the wider band (ULTRA) and narrow band (TRASH)" (pass3.log:7852).
- **Check:** `python3 -c "import json;c=json.load(open('docs/2026-09-05-astra-review/pass3-colcen.json'));print({k:v['band_recall'] for k,v in c.items() if 'band_recall' in v})"`.
- **Fix applied:** yes (E20).

### P3-05 — CONFIRMED — Table 1c prose contradicted its own rows

- **Claim:** manuscript.md:144 "The 2026 tools likewise have no rows" while an AniAnn's row is present in Table 1c (current lines 154–158, 5 cells sourced from `results/comparators2026/score_2026_human.txt: STRATUM`).
- **Evidence:** narrative pass3.log:4442 ("Table 1c still says AniAnn's has no row, although its row is present"); the sweep's Table 1c rows.
- **Check:** `grep -P '^1c\t' docs/2026-09-05-astra-review/pass3-table-cells.tsv | grep AniAnn`; `sed -n '150,158p' manuscript.md`.
- **Fix applied:** yes (E07).

### P3-06 — CONFIRMED — Maize prose differences rounded from rounded cells

- **Claim:** manuscript.md:21 "within 0.13 percentage points"; manuscript.md:286 "TRF leading BWTandem by 15.18"; manuscript.md:302 AniAnn's fragmentation 0.22; manuscript.md:286 TRASH "0.34 or less … though 18.57".
- **Evidence:** `pass3-checks.py maize` rescored raw calls (`pass3-maize.json`, pass3.log:6763, printed 7001–7354): CentC TRASH-template 58.6845 − BWTandem 58.5486 = 0.1359 → 0.14; knob180 banded TRF 79.3767 − BWTandem 64.2023 = 15.1743 → 15.17; AniAnn's CentC frag 0.21 (pass3.log:7347); TRASH losses de novo knob180 0.3412, template CentC 0.0318, de novo TR-1 18.5651. Narrative pass3.log:7506: "BWTandem trails the original CentC leader by 0.136 points, which rounds to 0.14, and TRF's banded knob180 lead is 15.17 points. The band-loss cells themselves reproduce correctly."
- **Check:**

```bash
python3 - <<'PY'
import json;m=json.load(open('docs/2026-09-05-astra-review/pass3-maize.json'))
print(m['3C/TRASH-template/CentC']['unfiltered']['coverage']-m['3C/BWTandem/CentC']['unfiltered']['coverage'])
print(m['3B/TRF/knob180']['banded']['coverage']-m['3B/BWTandem/knob180']['banded']['coverage'])
print(m["3C/AniAnn's (2026)/CentC"]['unfiltered']['frag'], [ (k,m[k]['loss']) for k in m if 'TRASH' in k])
PY
```

- **Fix applied:** yes (E25, E28, E29, E30). E26 in the same block is listed under P3-16 because 0.18 was not recomputed in the log.

### P3-07 — CONFIRMED — Band-loss comparison mixed classes; 2026 maize banded scores are not deposited

- **Claim:** manuscript.md:260 compared TRASH's knob180 and TR-1 banded losses across classes, and said the 2026 tools "cannot enter the banded rule".
- **Evidence:** script comment "Use a cleaner per-class comparison rather than a spurious across-class comparison" (pass3.log:7855; E21 was written at 7854 and immediately replaced by E22 at 7856, which is why E21 is absent from the manuscript). For the 2026 rows `pass3-maize.json` records `"banded": null` (pass3.log:7350) and `results/manifest.tsv` maps AniAnn's maize rows to `anianns_maize.bed` with no banded scoring output (pass3.log:5044–5047), so the correct statement is that no banded artifact is deposited, not that the tools are ineligible.
- **Check:** `python3 -c "import json;m=json.load(open('docs/2026-09-05-astra-review/pass3-maize.json'));print({k:m[k]['banded'] for k in m if '2026' in k})"`; `git show 3e728cc:manuscript.md | sed -n '260p'`.
- **Fix applied:** yes (E22, E23).

### P3-08 — CONFIRMED — Two TR-1 offset baselines have different definitions

- **Claim:** manuscript.md:242 and Table 3B present TR-1 offsets of 4,282 bp and 770.65 bp without saying they are different call sets.
- **Evidence:** 4,282 bp is the gap-zero baseline after coordinate merging in `results/regen/table3bc_replacement.md` / `maize_extra_evidence.json` (pass3.log:4240, 5273); 770.65 bp is the raw-call outer-endpoint offset (`pass3-maize.json` `3B/BWTandem/TR-1` offset, pass3.log:7036). Narrative pass3.log:7506: "valid but different definitions: raw calls versus coordinate-merged calls". Merge semantics read at pass3.log:6510–6570 (`score_maize_postmerge.py`).
- **Check:** `grep -n '4,282\|4282' results/regen/table3bc_replacement.md`; `python3 -c "import json;print(json.load(open('docs/2026-09-05-astra-review/pass3-maize.json'))['3B/BWTandem/TR-1']['unfiltered']['offset'])"`.
- **Fix applied:** yes (E24; Figure S2 caption E44 repeats the distinction).

### P3-09 — CONFIRMED — Maize leading-group claim ignored AniAnn's

- **Claim:** manuscript.md:284 "within the leading group on coverage in all three [classes]"; manuscript.md:292 caption on row order.
- **Evidence:** `pass3-maize.json` unfiltered coverage: AniAnn's 87.61 (knob180), 67.98 (TR-1), 81.42 (CentC) against BWTandem 79.79, 50.34, 58.55 (pass3.log:7192–7342). Script comment "Scope of count/coverage claims" (pass3.log:7871).
- **Check:** `python3 -c "import json;m=json.load(open('docs/2026-09-05-astra-review/pass3-maize.json'));print({k:round(m[k]['unfiltered']['coverage'],2) for k in m if 'AniAnn' in k or 'BWTandem' in k})"`.
- **Fix applied:** yes (E27, E31).

### P3-10 — CONFIRMED — Range and FASTA scope stated at the point of comparison

- **Claim:** manuscript.md:109,111,119,133,246,292 compare tools "within the range all tools shared" without stating output-band versus execution-range versus FASTA-scope differences at that point.
- **Evidence:** the pass prompt required scope at the point of comparison (pass3.log:31). The 2026 tools' memory comes from GNU-time `.time` files while BWTandem's is sacct cgroup MaxRSS (pass3.log:6233–6238, 6440–6451); the original competitor FASTA carries 3.92% more sequence (fig2 caption source, pass3.log:6290). Script comments "Scope at the immediate comparisons" (pass3.log:7836) and "Scope of count/coverage claims" (pass3.log:7871). The replaced sentence "unfiltered coverage can only rise with range" was applied separately to the Table 3B and 3C captions (pass3.log:7878–7882). These are wording-scope corrections; no number changed.
- **Check:** `git show 3e728cc:manuscript.md | sed -n '109p;111p;119p;133p;246p;292p'`; `sed -n '6272,6279p;6290p' docs/2026-09-05-astra-review/pass3.log`.
- **Fix applied:** yes (E06, E08, E09, E10, E32, E33).

### P3-11 — CONFIRMED — S2 and S4 text brought in line with pass-1 corrections

- **Claim:** manuscript.md:504 "unchanged by whether the periodicity pass is enabled … likewise 91.3%"; manuscript.md:527 S4 provenance called job 6146343 "metric-identical" and omitted the corrected TRF arm.
- **Evidence:** script comment "S2 and S4 carry pass-1's corrected artifact distinctions forward" (pass3.log:7888). S2 sources `results/regen/s2_F_p100.txt` and `s2_P_p100.txt` were printed at pass3.log:4361–4436 and both fractions round to 91.3%, so "unchanged" was replaced by "both round to". The S4 changes restate pass1-evidence.md P1-11 (corrected TRF annotation-period arm, scorer commit `903245c`, whose hash the reviewer verified at pass3.log:2922, 3027).
- **Check:** `grep -n 'catalog' results/regen/s2_F_p100.txt results/regen/s2_P_p100.txt`; `git show 903245c:scripts/scoring/score_one_to_one.py | sha256sum`; `sed -n '543p' manuscript.md`.
- **Fix applied:** yes (E36, E37, E38). E39 is under P3-16.

### P3-12 — CONFIRMED — Figure captions rewritten against deposited data; Figures 2–4, S1, S2 placed

- **Claim:** manuscript.md:154 Figure 1 caption described a two-panel figure; Figures 2, 3, 4, S1 and S2 existed under `results/figures/paper_figs/` with no manuscript reference.
- **Evidence:** the plot scripts' own captions were read (pass3.log:6064–6135, 6266–6322; Figure 1 has a panel C, pass3.log:6272–6279) together with `prep_data.py` (pass3.log:4664–4909). Numbers placed in the new captions were verified from artifacts in the log: range ratios 1.818 / 1.771 / 1.772 (mean 1.787) via `pass1-checks.py range` and audit counts 4 / 346 / 50 with the Wilson interval via `pass1-checks.py audit` (both at pass3.log:7556–7653); the absence of 2026 banded maize scores as in P3-07. Script comments pass3.log:7893 and 7897.
- **Check:** `python3 docs/2026-09-05-astra-review/pass1-checks.py audit; python3 docs/2026-09-05-astra-review/pass1-checks.py range`; `grep -n '^ Figure\|^!\[Figure' manuscript.md`.
- **Fix applied:** yes (E40–E45). No figure was regenerated.

### P3-13 — CONFIRMED — Figure 5 placed; its three intervals are contained in deposited calls

- **Claim:** the pass prompt (pass3.log:32) required Figure 5 to be placed or its exclusion explained.
- **Evidence:** `pass3-checks.py fig5` (pass3.log:6491, output 6506–6508, `pass3-fig5.jsonl`) found each plotted region inside deposited BWTandem calls with the same period: chr1:122,257,803–122,317,803 (1,866 bp), Chr4:4,985,644–5,045,644 (178 bp), CM039157.1:53,652,014–53,678,133 (155 bp; 26,119 bp long). Script comment pass3.log:7908. The caption states the panels are k-mer similarity illustrations, not validation.
- **Check:** `cat docs/2026-09-05-astra-review/pass3-fig5.jsonl`; `python3 docs/2026-09-05-astra-review/pass3-checks.py fig5`.
- **Fix applied:** yes (E46).

### P3-14 — BLOCKED-ON-MISSING-ARTIFACT — Four Table 1d runtime cells

- **Claim:** manuscript.md (current) 166–169, Runtime (h) for BWTandem-P/B/F/H: 3.2 / 4.5 / 5.4 / 4.1.
- **Evidence:** `results/manifest.tsv` lists elapsed 03:12:24 / 04:31:17 / 05:22:09 / 04:04:46 for producer jobs 6141841_0 and 6143150_1/2/3, but the original sacct records are absent from `results/sacct_provenance.txt` (`pass3-table-cells.py`, pass3.log:8064; TSV source "original sacct absent for …"). This is the same gap pass 1 recorded as P1-08. Reconstruction note, not the reviewer's: the manifest elapsed values convert to 3.21 / 4.52 / 5.37 / 4.08 h, consistent with the printed cells, but a manifest transcription is not the raw accounting.
- **Check:** `grep BLOCKED docs/2026-09-05-astra-review/pass3-table-cells.tsv`; `grep -c '6143150\|6141841' results/sacct_provenance.txt`.
- **Fix applied:** none; absence of the artifact is not an error.

### P3-15 — REJECTED — All other numeric table cells match their artifacts

- **Claim:** every numeric cell of Tables 1a–1e, 2, 3A/3A-b, 3B/3B-b, 3C/3C-b, S2, S3, S4a, S4b.
- **Evidence:** `pass3-table-cells.tsv`: 586 of 590 cells equal the artifact value at the printed precision under ROUND_HALF_UP; before the edits 578 matched and the 8 mismatches are exactly the cells of P3-01, P3-03 and P3-06 (E01–E03, E12–E15, E30). The reviewer's first sweep reported 33 blocked cells (pass3.log:8085) because the parser ran into the Supplementary parameter tables after Table 3C-b; the fix at pass3.log:8122 stops parsing at "4. Discussion", leaving the 4 cells of P3-14.
- **Check:** `python3 docs/2026-09-05-astra-review/pass3-reconstruct.py`; `python3 docs/2026-09-05-astra-review/pass3-reconstruct.py --before | head -3`.
- **Fix applied:** not applicable.

### P3-16 — APPLIED-RATIONALE-NOT-RECOVERED — Five edits whose justification is not in the transcript

The author should judge these on their text. Old → new for each is in `pass3-edits.json` (E47 excepted).

- **E19** (baseline 182 → current 188): "Its runtime was measured on a shared node and is an upper bound rather than a matched figure, but no plausible correction to it reverses the direction." → "Its runtime was measured on a shared node under a different period ceiling, so this is an observed cost comparison rather than a matched measurement." Only the group comment "Cost source corrections" (pass3.log:7840) precedes it.
- **E26** (284 → 294): "The top three sit within 0.18 points of each other" → "The top three span approximately 0.18 points". Group comment "Unrounded maize differences" (pass3.log:7860); the 0.18 span itself was not recomputed in the log.
- **E35** (182 → 188): appends "These runs consumed the same assembly but searched different period ranges; their observed costs are not a range-matched comparison." No comment (pass3.log:7887).
- **E39** (527 → 543): "the paper's evidence above 500 bp is the satellite experiments (Tables 2, 3B–3C) and the prediction-side stratum of Table 1c." → "the satellite panels and Table 1c contain predictions above 500 bp, but neither is a truth-period stratum validating period assignment above that ceiling." Group comment pass3.log:7888 only.
- **E47** (current 496, Supplementary parameter table): `| BWTandem-F | 1b, 1d |` → `| BWTandem-F | 1b sensitivity analysis, 1d |`, applied at pass3.log:8123 inside the command that repaired the sweep parser, and **not recorded in pass3-edits.json**. The log gives no reason for the manuscript change.

**Check:** `git show 3e728cc:manuscript.md | sed -n '182p;284p;527p'`; `sed -n '8120,8127p' docs/2026-09-05-astra-review/pass3.log`; `grep -n 'BWTandem-F | 1b' manuscript.md`.

## Table sweep

Generated by `pass3-reconstruct.py` from `pass3-table-cells.tsv` (after edits). Verdicts: 586 match (`REJECTED`), 0 mismatch (`CONFIRMED`), 4 `BLOCKED-ON-MISSING-ARTIFACT`. The pre-edit sweep (`--before`) gives 578 / 8 / 4; the 8 pre-edit mismatches are E01–E03, E12–E15 and E30. Table S1 is excluded by design; manuscript lines are as of 2026-09-05 21:41.

| Table | Manuscript lines | Cells | Match | Mismatch | Blocked | Primary artifact(s) |
|---|---|---:|---:|---:|---:|---|
| 1a | 129–137 | 68 | 68 | 0 | 0 | `results/regen/score_table1_p100.txt` (BASELINE/published support, 35); `results/comparators2026/score_2026_human.txt` (15); human TRF/ULTRA/tantan/TRASH competitor logs and sacct |
| 1b | 143–148 | 30 | 30 | 0 | 0 | `score_table1_p100.txt: MATCHED RANGE` (25); `score_2026_human.txt: MATCHED` (5) |
| 1c | 154–158 | 25 | 25 | 0 | 0 | `score_table1_p100.txt: STRATUM` (15), `STRATUM tantan-w2000` (5); `score_2026_human.txt: STRATUM` (5) |
| 1d | 166–173 | 56 | 52 | 0 | 4 | `score_table1_p100.txt` native BWT-P/B/F/H-p100 and matched/banded blocks; runtimes from `results/manifest.tsv` (blocked, see P3-14) |
| 1e | 179–183 | 10 | 10 | 0 | 0 | `score_table1_p100.txt: full-range support blocks` |
| 2 | 205–215 | 77 | 77 | 0 | 0 | deposited Col-CEN BEDs rescored by `pass3-checks.py colcen`; competitor logs and sacct for cost cells |
| 3A | 228–234 | 42 | 42 | 0 | 0 | `results/regen/maize_extra_evidence.json: table3a/*` |
| 3A-b | 240–243 | 16 | 16 | 0 | 0 | `maize_extra_evidence.json: table3a/*/band_1_6` |
| 3B | 260–268 | 57 | 57 | 0 | 0 | deposited maize BEDs (`results/beds/bwtandem_maize.bed.gz`, TRF/ULTRA/tantan/TRASH/AniAnn's) rescored by `pass3-checks.py maize`; sacct/logs for costs |
| 3B-b | 274–291 | 54 | 54 | 0 | 0 | same BEDs, banded rule |
| 3C | 306–312 | 40 | 40 | 0 | 0 | same, CentC |
| 3C-b | 318–325 | 28 | 28 | 0 | 0 | same, CentC banded |
| S2 | 524–531 | 16 | 16 | 0 | 0 | `results/regen/s2_F_p100.txt`, `s2_P_p100.txt` |
| S3 | 537–541 | 10 | 10 | 0 | 0 | `results/regen/score_table1_idsweep.txt: BASELINE` |
| S4a | 549–553 | 15 | 15 | 0 | 0 | `results/one_to_one/one_to_one_{ultra,bwtandem,trf,tantan,trash}_r50.json` |
| S4b | 559–563 | 46 | 46 | 0 | 0 | `results/one_to_one/one_to_one_*_annot_r50.json` |

Blocked rows (all Table 1d, column Runtime (h)):

| Line | Row | Printed | Artifact value | Source |
|---|---|---|---|---|
| 166 | BWTandem-P (catch-all off) | 3.2 | 03:12:24 | results/manifest.tsv; original sacct absent for 6141841_0 |
| 167 | BWTandem-B (id 0.76) | 4.5 | 04:31:17 | results/manifest.tsv; original sacct absent for 6143150_1 |
| 168 | BWTandem-F (id 0.72, ≥3 copies) | 5.4 | 05:22:09 | results/manifest.tsv; original sacct absent for 6143150_2 |
| 169 | BWTandem-H (id 0.72) | 4.1 | 04:04:46 | results/manifest.tsv; original sacct absent for 6143150_3 |

Rerun: `python3 docs/2026-09-05-astra-review/pass3-reconstruct.py` (full per-table source lists), or regenerate the TSV itself with `python3 docs/2026-09-05-astra-review/pass3-table-cells.py > /tmp/cells.tsv` after refreshing the `pass3-*.json` snapshots with `pass3-checks.py`. Regenerating against today's manuscript will report the precision-pass cells at two decimals; that is expected.

## REHASH REQUIRED

None from pass 3. The transcript contains no write to `results/` (59 exec blocks; the only files written are `/tmp/pass3-edit.py`, `/tmp/astra-pass3-manuscript-before.md`, `/tmp/astra-pass3-results-diff.sha256`, `manuscript.md`, and `docs/2026-09-05-astra-review/pass3-*`). The reviewer recorded the SHA-256 of `git diff -- results/` at pass3.log:5789 before touching anything, and its opening statement was "leave `results/` untouched" (pass3.log:39). The 15 modified `results/` files in `git diff --stat -- results/` are therefore pass 1's; see pass1-evidence.md "REHASH REQUIRED". No `.sha256` file was edited by any pass.

## Not fixed, and why

- **Table 1d runtime cells (P3-14):** four cells blocked on missing sacct records; the values were left as printed.
- **Independent TRF unique-count cross-check:** `bedtools intersect -v` over the human TRF BED against the BWTandem, ULTRA, tantan and TRASH BEDs (pass3.log:8128–8137) was the last command and produced no output: **not completed, no result**. P3-01's 18,904 therefore has a single supporting computation. quarantine.md §1.4 suspects this command caused the host OOM; sacct does not attribute it.
- **Old figure-input unique-region table:** `wp0/figure_inputs/unique_regions/unique_regions_human.tsv` (pass3.log:6664–6719) still carries the superseded counts; it is outside `results/` and was not edited.
- **Sweep verdict wording:** in the TSVs `REJECTED` means "matches". The reviewer's script used the brief's vocabulary for the suspicion, not the cell; this reconstruction keeps the TSVs unchanged and explains the convention above.
- **The pass never produced its own findings file**, so nothing here carries the reviewer's severity ranking; the order above is the reconstruction's.

## Where the log stopped

The last exec block starts at pass3.log:8128 (command lines 8129–8137) and has no status line; the file ends at line 8138 (8,137 lines plus a trailing newline, 672,942 bytes, mtime 2026-09-05 21:41). The command:

```python
cmd=['/data/gpfs/assoc/pgl/bin/bedtools2/bin/bedtools','intersect','-v','-a',src('TRF'),'-b']+[src(n) for n in ['BWTandem','ULTRA','tantan','TRASH']]
# ... count stdout lines; print('Independent bedtools TRF unique:',n)
```

where `src()` reads `source_bed` for the Table 1a rows of `results/manifest.tsv`. The block immediately before it (pass3.log:8120–8127) had just repaired the sweep parser, applied E47, and regenerated both sweep TSVs (both files mtime 21:41). The pass was cut off before writing its report; quarantine.md §1.4 records the host job's `OUT_OF_MEMORY` end at 2026-09-06 06:49:57.


> ✏️ **Note added 2026-09-10 (after reconstruction):** the precision pass referenced above now stands at **88** effective edits — six Supplementary Table S2 cells were reverted to one decimal because their deposited summary carries only one decimal (Codex ledger review L-09, `docs/2026-09-10-precision/precision-report.md` addendum 2).

> ✅ **Author decision 2026-09-10:** all five P3-16 edits (E19, E26, E35, E39, E47) are **accepted**. Basis per edit is recorded in `docs/2026-09-10-ledger-review/p3-16-decision.md`. E26 follow-up: drop "approximately" — the deposited coverages give 58.6845 − 58.5042 = 0.1803, exactly 0.18 at two decimals (todo.md §0-4).
