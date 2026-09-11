# Pass 1 — Evidence-tree integrity (results/)

## Summary

**14 CONFIRMED, 4 REJECTED, 2 BLOCKED-ON-MISSING-ARTIFACT; 0 SUSPECTED.**

The most serious confirmed defect was an outdated evidence index: the active Table 1b BWTandem row still selected the more favourable native rerun after C-2 adopted post-hoc filtering. The S4 TRF row also attributed the corrected JSON to the scorer that discarded its periods. Both mappings are corrected. These are evidence-index defects, not newly discovered failures of the deposited numerical measurements.

The substantive checks pass: CEN180 has 66,683 filtered / 68,840 raw coordinates, strictly nested; the three release-build runtime ratios are 1.818251 / 1.770577 / 1.772200 (mean 1.787009); S4's TRF period-exact value is 63.53%; and the three headline whole-genome runtimes and memories reproduce from sacct. All 197 repository checksum paths and 80 external paths exist. All 20 sampled hashes matched **before edits**, including the largest file in each list and the latest modified file in each list. No checksum file was rewritten.

Coverage: all 137 manifest rows, all 12 READMEs, the other evidence prose, checksum inventories, ground-truth counts, the three compressed BEDs, the 40 inherited competitor logs, accounting records, paired range logs, all 15 current S4 JSONs, and the tuning ledger. The surviving tuning files are deposited, but they retain 17 pending decisions. Exact original audit-image reproduction and raw accounting for nine later tasks remain unsupported by deposited artifacts.

Baseline for claim citations is **`3e728cce5be3a530d75b8e3501d5bdb8409e1f43`**, before this pass's edits. Unless expressly labelled current, `file:line` claim locations below refer to that baseline, recoverable with `git show 3e728cc:FILE | nl -ba`. Counter-evidence commands run from the repository root. No withdrawn or REJECTED finding in quarantine.md is reopened.

Supporting audit artifacts:

- `pass1-checks.py`: read-only checks; examples below use its full repository-relative path.
- `pass1-checksum-sample.json`: all 20 pre-edit expected/observed full hashes, file sizes and outcomes.
- `pass1-manifest-audit-before.json` and `pass1-manifest-audit-after.json`: per-row source/scorer checks, current hashes, and matching historical script revisions. The after report additionally records source prefix/size and commit-resolution results.

No manuscript, todo or quarantine edits were made by this pass. Concurrent manuscript changes belong to the parallel Methods pass. No pipeline rerun, scheduler submission, commit, staging, branch operation or rehash script was used.

## Findings

### P1-01 — Checksum coverage and sampled content

**Verdict: REJECTED** — no missing listed path, omitted tracked results artifact, or sampled pre-edit hash mismatch.

**Claim:** `results/manifest.sha256:1` and `results/external_evidence.sha256:1` index the deposited evidence.

**Evidence:** 197 repository entries and 80 external entries exist; every tracked results artifact other than the two checksum indexes is listed. Every absolute `source_bed` path is in the external index. The only other filesystem files excluded from the results index are two untracked `__pycache__` files, not deposited evidence. All 20 sample hashes match. The sample includes the largest repository file, `bwtandem_human.bed.gz` (59,840,593 bytes), and largest external file, human mreps BED (679,004,376 bytes); the latest entries were `manifest.tsv` and `rangerep0363/rep2_p2000.bed` respectively.

**Check:**

```bash
python3 docs/2026-09-05-astra-review/pass1-checks.py inventory
python3 docs/2026-09-05-astra-review/pass1-checks.py sample
```

The second command now deliberately reports differences for sampled prose/TSV files edited in this pass. The JSON snapshot preserves the all-match pre-edit result. This was a representative sample, not a full checksum recomputation of all 277 entries.

**Fix applied:** None to either checksum file. Human rehash is required for the files listed below.

### P1-02 — Incorrect scorer hash prefixes, distinct from valid historical hashes

**Verdict: CONFIRMED.**

**Claim:** `results/manifest.tsv:2,25,36` and repeated rows identify their scorers by hash.

**Evidence:** Three recorded prefixes fail direct SHA-256 comparison and match no version of their named script in reachable git history:

| Scorer | Incorrect prefix | Observed prefix | Affected baseline lines |
|---|---|---|---|
| score_table1_regen.py | b85820c724137549 | b85820bebdd1f139 | 2, 8, 13, 16–19, 46, 83 |
| score_colcen.py, regenerated row | 585d55ba96cb380a | 585d55558609d6e5 | 25 |
| rescore_tables_3bc.py, original external producer | 39d308a0799f7e1f | 39d30894d5a5c295 | 36, 41, 57, 85, 86 |

The last case needs a version distinction: `results/regen/table3bc_provenance.json:3` explicitly names the external original. Its repository copy hashes to `e5202778dcf4a149…`; a diff shows the later change makes input paths configurable. The manifest now names the original hash and explicitly identifies both versions, rather than claiming the deposited copy produced the old report byte-for-byte. The template-only rescoring row at line 53 also now identifies the current LABEL:PATH scorer instead of its predecessor.

All 14 named Python scorers exist on disk. Other current-file differences are legitimate historical versions: Col-CEN `60d20caf…` and maize `33c8c795…` at `bf20dce`; S4 `3e84c976…`, `06fa03a1…`, `91338484…` at `0c3c982`, `43543da`, `5e68f78`; 2026 wrapper `179e77b6…` at `7b2113d`. Those historical hashes were preserved. TRF's corrected arm is handled separately in P1-11.

**Check:**

```bash
python3 docs/2026-09-05-astra-review/pass1-checks.py manifest
sha256sum scripts/scoring/score_table1_regen.py scripts/scoring/score_colcen.py scripts/scoring/rescore_tables_3bc.py
sha256sum /data/gpfs/assoc/pgl/devel/exp1_human/regen/maize_rescore/rescore_tables_3bc.py
diff -u /data/gpfs/assoc/pgl/devel/exp1_human/regen/maize_rescore/rescore_tables_3bc.py scripts/scoring/rescore_tables_3bc.py
```

**Fix applied:** Corrected prefixes in TSV, explained the external producer/repository reproducer distinction, and preserved the historical versions. These corrections identify verifiable files, not a new scoring execution. Diagnostic rows 58, 59 and 84 still have no execution-time scorer hash; none was invented.

### P1-03 — The manifest and provenance prose promise more than their schema records

**Verdict: CONFIRMED.**

**Claim:** `results/README.md:44–48,100–103` promises complete executable accuracy provenance and says the run JSONs record SLURM accounting; `results/beds/README.md:6` promises scoring without cluster access. `results/manifest.tsv:87` uses `this evidence commit` as a commit identifier.

**Evidence:** The source check finds 129 existing file references and eight deliberate non-file entries: five failed-job placeholders, two same-source aliases and one retired flank diagnostic. No concrete named interval file is missing. The baseline has eight distinct resolvable commit IDs, but `0e17d1a+outputfixes` (five rows) is an execution-state description, `this evidence commit` is not a ref, and two competitor attempts use `—`. The detection pin and scorer revision also have different meanings: several scorer wrappers were deposited after `0363d8b`.

The run JSONs positively identify their alternative accounting fields, e.g. `results/regen/regen_human.provenance.json:10–11` has `elapsed_wall_s=45489.16` and `max_rss_kb=18212700`, whereas the raw sacct record gives 45522 seconds and 29447952 KiB. The JSON contains the command but not the configuration-selecting environment variables. Human truth and most comparator BEDs remain external; the gzip deposit alone does not make the invocation self-contained.

**Check:**

```bash
python3 docs/2026-09-05-astra-review/pass1-checks.py manifest
cat results/regen/regen_human.provenance.json
python3 docs/2026-09-05-astra-review/pass1-checks.py sacct
git log --all --format='%h %s' -- scripts/scoring/score_maize_regen_evidence.py
```

**Fix applied:** Qualified README coverage; distinguished detection and scoring commits, wait4 and sacct, and external inputs. Replaced `this evidence commit` with the scorer's deposited commit `33f3ab6`. Retained the historical composite descriptions and missing-hash placeholders with their limitations; no unsupported execution commit or environment was reconstructed. This carries forward prior R3-4/R3-8 limitations, not a new assertion that the measurements are wrong.

### P1-04 — Active Table 1b and S2 mappings retain retired inputs

**Verdict: CONFIRMED.**

**Claim:** `results/manifest.tsv:89` maps Table 1b to the native p100 F output; line 59 labels the old-build unique-call characterization `S2`. `results/regen/README.md:27` still treats the native runs as the Table 1b source.

**Evidence:** C-2 in `todo.md` explicitly adopted post-hoc filtering. In `results/regen/score_table1_p100.txt:46–57`, the full-BED BWTandem matched-range baseline is **78.87% recall / 50.13% precision**, while native F is **79.88% / 50.62%**. `results/figures/paper_figs/data/fig1c_overlap_rules.csv` uses the post-hoc baseline. The old S2 source has 3,991,847 calls, whereas `results/regen/s2_F_p100.txt:1–2` names the new F BED and **3,993,151** calls, and the P control names its own new BED.

**Check:**

```bash
sed -n '46,57p' results/regen/score_table1_p100.txt
head -n 3 results/regen/s2_F_p100.txt results/regen/s2_P_p100.txt
sed -n '59p;89,93p' results/manifest.tsv
```

**Fix applied:** Table 1b now points to the deposited full-range BED with the post-hoc rule and the score-report block. Native F remains in Table 1d and is explicitly a sensitivity analysis for Table 1b. The old S2 row is labelled superseded and points readers to both current reports. Updated the regen README. No accuracy artifact was altered.

### P1-05 — CEN180 nesting, other truth counts, and compressed BED integrity

**Verdict: REJECTED** — the specified counts and coordinate nesting are correct.

**Claim:** `results/README.md:22–35`, `results/beds/README.md:10–12`.

**Evidence:** Filtered/raw coordinate multisets contain **66,683 / 68,840** records, all individually unique; zero filtered coordinates are absent from raw and exactly **2,157** raw coordinates were dropped. This is a strict subset on `(chrom,start,end)`, not on complete six-column lines: the raw file has `.` identity and strand. The other truth counts are five centromeres, 25 knob180 arrays, 17 TR-1 arrays and 17 CentC arrays. The consensus query is 177 bases.

Decompressing the three BWTandem BEDs gives **161,330 / 4,014,108 / 2,406,800** calls (Col-CEN/human/maize), byte counts **9,167,462 / 211,949,715 / 166,077,178**, and full SHA-256 values exactly matching each run JSON. Col-CEN includes 156 ChrC and 291 ChrM calls; its nuclear-only scored count is consequently 160,883. This is not a conflict with Table 2.

**Check:**

```bash
python3 docs/2026-09-05-astra-review/pass1-checks.py cen180
python3 docs/2026-09-05-astra-review/pass1-checks.py beds
wc -l results/ground_truth/*.bed
python3 -c "from pathlib import Path; print(sum(len(s) for s in Path('results/ground_truth/CEN178_consensus.fa').read_text().splitlines() if not s.startswith('>')))"
```

**Fix applied:** Clarified that the subset claim concerns coordinates. The already disclosed missing BLAST invocation and raw identity values remain limitations; they are not evidence that the coordinates are wrong. Quarantine §6.27 is not reopened.

### P1-06 — Forty inherited log files are not forty complete GNU-time records

**Verdict: CONFIRMED.**

**Claim:** `results/competitor_logs/README.md:5–12` says each file contains command, wall clock, MaxRSS and exit status; `results/README.md:75` extends the coverage to every competitor cost cell.

**Evidence:** There are 40 `.log` files: TRASH 12; ULTRA, TRF, tantan and mreps six each; NCRF four. Only **37** contain all four timing fields. Both mreps maize `*_a_exp_run.log` and `*_b_exp_run.log` are zero bytes. `trash__GCA_022117705.1_Zm-Mo17-REFERENCE-CAU-T2T-assembly_genomic_trash_denovo_exp3C_centc_run.log` is a 3,864-byte progress log ending during sequence analysis, with no timing footer. The 2026 per-arm `.time` files are also outside this directory. These concrete contents refute the universal inventory description; they do not prove any unsupported cost value false.

**Check:**

```bash
python3 docs/2026-09-05-astra-review/pass1-checks.py logs
```

**Fix applied:** Corrected the 40-files/37-complete-records distinction in both READMEs and narrowed the universal claim in `comparator_baselines.md`. This extends the already-confirmed quarantine §3.6 coverage defect with concrete additional inventory evidence.

### P1-07 — The current sacct deposit is a subset, with updated counts

**Verdict: CONFIRMED.**

**Claim:** `results/sacct_provenance.txt:1` says it covers every manifest job. The earlier 34-job deposit count appears in `todo.md` D and historical summaries.

**Evidence:** The September 4 recapture contains **120 accounting rows**, representing **40 top-level job/array-task records** and **37 distinct allocations** when the four 6129408 array tasks are collapsed. The earlier **34 allocations** plus the three range jobs gives 37; the historical 34 figure was correct for the earlier deposit, not an erroneous original count. Nine current producer tasks are absent, listed in P1-08. All current range pairs and all three headline whole-genome jobs are present.

**Check:**

```bash
python3 docs/2026-09-05-astra-review/pass1-checks.py sacct
```

**Fix applied:** Corrected only the sacct prose header to give scope, counts and missing tasks. All raw accounting rows are byte-for-byte unchanged. **DESTINATION: todo.md, append-only integration note** — distinguish the completed September 3 deposit (34 allocations) from its September 4 recapture (37 allocations/40 job-task records).

### P1-08 — Nine native-panel/sweep cgroup cells cannot be checked against deposited sacct

**Verdict: BLOCKED-ON-MISSING-ARTIFACT.**

**Claim:** `results/manifest.tsv:89–98` records elapsed/cgroup values for native p100 and identity-sweep tasks (the old line 89 mapping has now been replaced).

**Evidence:** `6141841_0`, `6143150_1..3` and `6143151_0..4` have run JSONs and interval outputs but no raw rows in `results/sacct_provenance.txt`. Their wrapper JSONs hold process-accounting values, which cannot substitute for the cgroup peaks. This pass has not established that any of the printed cgroup values is wrong.

**Check:**

```bash
python3 docs/2026-09-05-astra-review/pass1-checks.py sacct
cat results/regen/bwt_human_F_p100_0363.provenance.json
```

**Fix applied:** Disclosed the scope limit in README/header. Left the values unchanged. **DESTINATION: todo.md** — recover/deposit the original accounting for these nine tasks or state explicitly that those cgroup cells have no deposited raw support. No scheduler query or new run was performed.

### P1-09 — Headline accounting and release-build range ratios reproduce

**Verdict: REJECTED** — no numerical contradiction in these measurements.

**Claim:** `results/manifest.tsv:2,25,30,133–138`; `results/range_cost_0363d8b/README.md:19–28`.

**Evidence:**

| Whole-genome job | Elapsed | Hours | MaxRSS / 1024², GiB |
|---|---|---:|---:|
| 6110900, Col-CEN | 00:40:11 | 0.669722 | 2.163788 → 2.16 |
| 6110901, human | 12:38:42 | 12.645000 | 28.083755 → 28.08 |
| 6124640, maize | 15:51:03 | 15.850833 | 28.449993 → 28.45 |

| Pair job | p100 seconds | p2000 seconds | Ratio |
|---|---:|---:|---:|
| 6147698 | 14,465 | 26,301 | 1.818250951 |
| 6147699 | 14,798 | 26,201 | 1.770577105 |
| 6147700 | 14,482 | 25,665 | 1.772199972 |

Mean ratio **1.787009343**, rounding to **1.79**. All six arms exit 0, with 3,993,151 p100 and 4,014,108 p2000 calls. Pair logs and the submitted sbatch identify `0363d8b`, sequential arms and the same node within each job. The older `07ad6fa` manifest rows are already explicitly superseded; the figure source/data and both inspected Figure 2 PNG copies use the replacement measurements. Old 1.30–1.41 values survive only as labelled history in the active evidence prose/figure caption.

**Check:**

```bash
python3 docs/2026-09-05-astra-review/pass1-checks.py sacct
python3 docs/2026-09-05-astra-review/pass1-checks.py range
python3 docs/2026-09-05-astra-review/pass1-checks.py figures
rg -n '1\.30|1\.41|07ad6fa|superseded' results/range_cost_0363d8b/README.md results/manifest.tsv results/figures/paper_figs/plot_fig2_range_cost.py
```

**Fix applied:** Strengthened the comparison-table heading to call its old arm superseded. No runtime, interval output or figure was regenerated.

### P1-10 — RSS schema description and several transcriptions disagree with raw accounting

**Verdict: CONFIRMED.**

**Claim:** `results/README.md:55–58` says active range rows contain per-arm GNU-time RSS, while `results/manifest.tsv:133–138` explicitly records job-level cgroup peaks. Col-CEN 2026 cells at lines 124–126 retain 0.07/0.07/0.50 after their README correction. Superseded range rows 45 and 60–65 use inconsistent RSS conversions.

**Evidence:** The active range column correctly repeats **41.09/42.67/44.62 GiB** over each pair; per-arm GNU-time values are **17.21–17.38 GiB** in the notes/logs. The 2026 Col-CEN GNU-time counts are **66,020 / 66,340 / 503,968 KiB**, rounding to **0.06 / 0.06 / 0.48 GiB**. They must remain labelled GNU-time, not sacct. Historical range sacct rows give corrected GiB values **35.29** (job 5983772), and **36.75 / 41.81 / 36.31 / 41.01 / 38.11 / 36.55** (jobs 6076848–53), rather than 35.28 and 38.53/43.85/38.07/43.00/39.96/38.32.

**Check:**

```bash
python3 docs/2026-09-05-astra-review/pass1-checks.py range
python3 - <<'PY'
import csv
for r in csv.DictReader((l for l in open('results/sacct_provenance.txt') if not l.startswith('#')), delimiter='|'):
    if r['JobID'] in [str(j)+'.batch' for j in [5983772,6076848,6076849,6076850,6076851,6076852,6076853]]:
        print(r['JobID'], r['MaxRSS'], round(int(r['MaxRSS'][:-1])/1024**2,2))
PY
rg 'Maximum resident set size' /data/gpfs/assoc/pgl/devel/exp1_human/tools2026/runs/*colcen*.time
```

**Fix applied:** Corrected the three 2026 and seven historical TSV cells; retained old historical transcriptions in explicit correction notes. Corrected README schema language and marked all 2026 TSV costs as per-arm GNU-time. Relabelled four remaining memory GB entries in `comparator_baselines.md` to GiB. Active range cgroup values were already correct and were preserved.

### P1-11 — S4 summaries and provenance did not fully follow the TRF correction

**Verdict: CONFIRMED.**

**Claim:** `results/one_to_one/README.md:105,117,122,127,150–162`; `results/manifest.tsv:115,119`.

**Evidence:** The README simultaneously says 63.53% in prose and leaves TRF's table cell blank; it calls BWTandem lowest despite tantan **3.42% < 8.68%**, and its ordering omits TRF. The corrected TRF JSON is still indexed with `06fa03a1…` / `43543da`, even though its scorer is `1972ef4727de1613…` / `903245c`. The split-band TRF JSON retains old zero period fields. Compared with the earlier deposited unsplit JSON at `903245c`, the current file changes all five period fields **and adds `strata_spec` metadata**. Its matched counts, sensitivities, precisions, boundaries and strata are unchanged. The split-band files were produced by job 6146343, not job 6146229.

**Check:**

```bash
python3 docs/2026-09-05-astra-review/pass1-checks.py s4
sha256sum scripts/scoring/score_one_to_one.py
git show 903245c:scripts/scoring/score_one_to_one.py | sha256sum
sed -n '115p;119p' results/manifest.tsv
```

**Fix applied:** Corrected README table, ranking, metadata-change description and job attribution; corrected the single regenerated TRF manifest row; explicitly marked the split-band period statistics superseded while retaining its valid matching/stratum evidence. No JSON changed. **DESTINATION: manuscript pass 3/4** — S4's global `43543da`/6146229 and “metric-identical” split-run provenance need the same TRF-only exception; the numerical S4 correction is already present. **DESTINATION: todo.md/quarantine.md, append-only integration** — C-10 JSON replacement is complete; only the five numerical fields changed, but there was also a metadata addition.

### P1-12 — Current S4 numerical rows are internally consistent

**Verdict: REJECTED** — no mismatch between the current unsplit JSON values and S4's numerical rows.

**Claim:** `results/one_to_one/one_to_one_trf_annot_r50.json:7,46–51` and the corresponding S4 row.

**Evidence:** All 15 current JSONs satisfy `sensitivity=100*matched/truth_records` and `precision=100*matched/pred_records`. The ten unsplit JSONs reproduce the S4 matched counts and rounded sensitivity/precision values. Annotation period-exact rates are **tantan 73.54, TRF 63.53, ULTRA 59.61, BWTandem 58.66, TRASH 33.41**. TRF has **518,719** scored period pairs, 29.063079% sensitivity and 53.874020% precision. Split-band matching/strata agree with unsplit results after relabelling the long band; the pre-fix TRF period fields are the disclosed exception in P1-11.

**Check:**

```bash
python3 docs/2026-09-05-astra-review/pass1-checks.py s4
```

**Fix applied:** None to JSONs or manuscript cells. This checks arithmetic and deposited summaries; it is not a rerun of full-genome bipartite matching.

### P1-13 — C-3 deposit is complete, but its selection ledger is not a final decision record

**Verdict: CONFIRMED.**

**Claim:** `results/tuning_ledger/README.md:6–10` describes a campaign that chose the configuration, with accept/reject decisions and selection state. C-3 and the deposit are marked complete in todo.md.

**Evidence:** Both deposited files are byte-identical to their surviving `exp1_human/loop/` originals. There are 44 scored evaluations, **22 `config` and 22 `code`**, with decisions **7 accept / 14 reject / 3 near-reject / 3 near / 17 pending**. The eventual copies≥3 candidate `f_cp3` at `ledger.tsv:34` remains pending. `best.json:17–19` marks an earlier cAB configuration final, and its subsequent catch-all frontiers do not resolve the final copies≥3 choice. Code-labelled rows have environment strings/notes, not per-row code revisions. Many records predate the native alignment correction and cannot be cited as current benchmark measurements under quarantine §1.2.

**Check:**

```bash
python3 docs/2026-09-05-astra-review/pass1-checks.py ledger
cmp results/tuning_ledger/ledger.tsv /data/gpfs/assoc/pgl/devel/exp1_human/loop/ledger.tsv
cmp results/tuning_ledger/best.json /data/gpfs/assoc/pgl/devel/exp1_human/loop/best.json
```

**Fix applied:** README now gives the exact categories, pending-state limit, historical-value restriction, and links the original acceptance/stopping plan and revised objective. Raw ledger and best.json preserved. **DESTINATION: todo.md / manuscript pass 3/4** — distinguish completed minimal disclosure/deposit from a fully traceable final selection rule; resolve or explain pending decisions only from surviving records, without inventing retrospective accept/reject outcomes.

### P1-14 — Figure READMEs contradict existing files and current range-cost figures

**Verdict: CONFIRMED.**

**Claim:** `results/figures/README.md:3–7,19–20` says the CSV is a pending non-numeric placeholder. `results/README.md:6` attributes this curve to the identity sweep. `results/figures/paper_figs/README.md:3,10,48,62` says six figures, Figure 2 rerender pending, and that plot scripts write into rendered/.

**Evidence:** `figure_curve_data.csv` has four numeric native P/B/F/H rows plus four competitor rows; the completed jobs are indexed at `manifest.tsv:90–93`. There are seven PNG/PDF pairs under rendered/. Both copies of Figure 2 were visually inspected and are byte-identical, displaying **1.77–1.82×**, with the old ratios explicitly superseded in the caption. `git log` attributes the renders to `da9e484`. The plotting scripts save relative filenames into the working directory, rather than rendered/.

**Check:**

```bash
python3 docs/2026-09-05-astra-review/pass1-checks.py figures
sha256sum results/figures/paper_figs/{,rendered/}fig2_range_cost.{png,pdf}
git log -1 --format='%h %s' -- results/figures/paper_figs/rendered/fig2_range_cost.png
rg -n 'savefig' results/figures/paper_figs/plot_*.py
```

**Fix applied:** Corrected both READMEs and the root figure-source sentence. No renderer, CSV or binary was changed or rerun. **DESTINATION: pass 3/4** — Figure 5 placement remains an existing open manuscript task, not an unfinished Figure 2 rerender.

### P1-15 — Competitor-attempt README retains claims corrected in its manifest

**Verdict: CONFIRMED.**

**Claim:** `results/range_cost_attempts/README.md:12,15,34,61,73,93`; `results/comparator_baselines.md:9,42`; the former conflicts with the already corrected `manifest.tsv:67`.

**Evidence:** The ULTRA partial contains a header, **138,425 complete nine-field records**, and **one six-field fragment** without a final newline. There are 138,426 newline characters. The last complete endpoint is **124,785,432**, while the fragment ends at **124,786,615**. Last emitted coordinates do not measure the fraction processed or the location of a stall. The manifest already distinguishes binary files and accession headers; the README still says unqualified version/input matching. Contrary to “no artifacts beyond its partial file,” TRF has a cancellation record in the deposited sacct table. Ratios against completed baseline runs are lower bounds, not speed ratios or proofs that a rerun is infeasible.

**Check:**

```bash
python3 docs/2026-09-05-astra-review/pass1-checks.py ultra
rg -n '^6076847|^6145581' results/sacct_provenance.txt
sed -n '66,67p' results/manifest.tsv
```

**Fix applied:** Corrected complete/fragment accounting, inference limits, matching terminology, cancellation framing and surviving-accounting inventory in results prose; made the TRF TSV lower-bound qualification explicit. This propagates previously adjudicated R1-3/R1-5/R1-15 corrections. **DESTINATION: pass 3/4** — search remaining manuscript statements about percentage processed, version matching, and cancelled-run cost ratios.

### P1-16 — Competitor-log README still presents the retired TRASH template contract as current

**Verdict: CONFIRMED.**

**Claim:** `results/competitor_logs/README.md:27–29` says the template row uses all three runs and both rows use the CEN159 cost.

**Evidence:** `results/regen/colcen_trash_template_scored.txt:8–14` documents the replacement **397-record template-only union**, **31:41:09 / 2.63 GiB**, and separate de novo **5:47:30 / 1.29 GiB**. The BED has 397 records and `manifest.tsv:53` points to it. This is the applied quarantine §6.1 correction, not a new challenge to the union result. The human TRASH nonzero exit is also already disclosed in the manuscript; README tense had not followed the correction.

**Check:**

```bash
wc -l results/regen/colcen_trash_template_union.bed
sed -n '1,26p' results/regen/colcen_trash_template_scored.txt
rg 'Elapsed|Maximum resident|Exit status' results/competitor_logs/trash__Col-CEN*.log
```

**Fix applied:** Replaced the current-tense retired account with the corrected contract, cost arithmetic and historical pointer. Preserved the unfavorable nonzero-exit information.

### P1-17 — 2026 comparator prose overstates what its evidence establishes

**Verdict: CONFIRMED.**

**Claim:** `results/comparators2026/README.md:15,80,106–114` claims cost comparability, says `adj_rules` is used nowhere before its loop, infers a mechanistic reason for zero overlap, and describes BWTandem output as per-copy records.

**Evidence:** The accounting difference is explicit in P1-10. `scripts/scoring/score_table1.py:403` reads `adj_rules` for an informational note before line 408's numerical loop. The deposited maize log reports zero longdust overlap, without identifying the mechanism. `results/beds/README.md:20–28` and the BED format define one array per row with aggregate copy count. These are the previously confirmed R1-8/R1-16/R1-18/R1-19 issues, still live on this surface.

**Check:**

```bash
sed -n '400,409p' scripts/scoring/score_table1.py
cat results/comparators2026/score_2026_maize.txt
sed -n '18,32p' results/beds/README.md
```

**Fix applied:** Qualified accounting comparability, corrected the informational branch description, removed the unsupported mechanistic attribution, and changed per-copy to per-array. No scoring code or results changed. The human crashed/clean score logs were also checked: their scored bodies are equal; the timestamp/host and traceback differences remain legitimate provenance differences.

### P1-18 — Audit summary mixes denominators and names a sampler as an image reproducer

**Verdict: CONFIRMED.**

**Claim:** `results/audit11/README.md:18–22` pairs 1.0% with a definitive-verdict CI and says the sampler deterministically regenerates the images.

**Evidence:** The sheet, key and verdict file each have 400 matching sample IDs. After case normalization and the disclosed SUUPORTED typo correction, counts are **4 supported / 346 unsupported / 50 unsure**. Thus 4/400 = **1.0%**, while 4/350 = **1.142857%** is the definitive-verdict estimate to which the reported Wilson CI belongs. The sequence lengths agree with the call spans plus flanks. `scripts/scoring/sample_specificity_audit.py:127–154` writes a sheet and key, not an image. This positively refutes the named reproduction procedure; it does not invalidate the recorded reader judgments.

**Check:**

```bash
python3 docs/2026-09-05-astra-review/pass1-checks.py audit
sed -n '123,160p' scripts/scoring/sample_specificity_audit.py
cat results/audit11/aggregate_reviewer2_20260831.txt
```

**Fix applied:** Separated the two denominators and stated the original-renderer limitation. Raw reader files and verdicts were preserved. The remaining artifact question is P1-19.

### P1-19 — Exact original visual audit cannot be reproduced from the deposit

**Verdict: BLOCKED-ON-MISSING-ARTIFACT.**

**Claim:** `results/audit11/README.md:21–22` promises regeneration of the original visual audit.

**Evidence:** The deposit contains the sampler-linked sheet, key, verdicts and aggregate, but no original 400 images or rendering implementation/settings. P1-18 demonstrates that the named sampler does not fill that role. New plots could be made from the sequence-bearing sheet, but they would not establish what the reader originally saw. The original population BED and reader attestation also remain outside this small deposit. No conclusion about the validity of the 400 judgments follows from those absences.

**Check:**

```bash
rg --files results/audit11
rg -n 'open\(|write\(|savefig|png|dot' scripts/scoring/sample_specificity_audit.py
```

**Fix applied:** Corrected the promise in README, but did not invent or regenerate substitute evidence. **DESTINATION: todo.md** — recover original images, renderer/settings and reader/population provenance if exact visual replication is claimed. Prior R2-6/R3-2 remains an artifact limitation; this pass does not promote missing images into an erroneous scientific result.

### P1-20 — Failed-job supersession is correct; an asserted failure cause is not supported by its cited accounting

**Verdict: CONFIRMED**, limited to the causal wording.

**Claim:** `results/manifest.tsv:8,16–19` marks the old PENDING attempt superseded and attributes its startup failure to out-of-memory.

**Evidence:** Supersession agrees with todo.md and with completed replacement rows; the literal PENDING strings are historical placeholders, not active unfinished runs. In the raw accounting, all four batch/job records are **FAILED** after 0–1 seconds with a 1,544 KiB batch maximum. Their `.extern` rows say OUT_OF_MEMORY, but that state also appears on extern rows of completed headline jobs. The cited deposit establishes startup failure; it does not isolate an out-of-memory cause for the batch process.

**Check:**

```bash
rg -n '^6129408|^611090[01]' results/sacct_provenance.txt
sed -n '8p;16,19p;90,93p' results/manifest.tsv
```

**Fix applied:** Preserved supersession and historical placeholders; replaced the asserted cause with the exact batch/extern distinction. The replacement native-panel outputs remain valid. No withdrawn quarantine item is reopened and no failed job was rerun.

## REHASH REQUIRED

Every results/ file touched by this pass:

- `results/README.md`
- `results/audit11/README.md`
- `results/beds/README.md`
- `results/comparator_baselines.md`
- `results/comparators2026/README.md`
- `results/competitor_logs/README.md`
- `results/figures/README.md`
- `results/figures/paper_figs/README.md`
- `results/manifest.tsv`
- `results/one_to_one/README.md`
- `results/range_cost_0363d8b/README.md`
- `results/range_cost_attempts/README.md`
- `results/regen/README.md`
- `results/sacct_provenance.txt` — comment header only; accounting rows unchanged
- `results/tuning_ledger/README.md`

`results/manifest.sha256`, `results/external_evidence.sha256`, and `results/beds/SHA256SUMS` remain byte-identical to the baseline. No `.sha256` file was edited. The human must rehash after all results edits and then run the deposit guards; a checksum guard now would correctly detect the authorized prose/TSV changes.

## Not fixed, and why

- **Raw data and images:** no BED, JSON, reader verdict, ledger, CSV, figure binary or measured runtime log was rewritten. The obsolete TRF split-band period fields are explicitly marked, not silently replaced with a fabricated rerun. Exact original audit-image reproduction remains blocked (P1-19).
- **Missing accounting:** nine task-level raw sacct records remain missing. Their reported costs were not changed merely because support is absent (P1-08).
- **Historical provenance:** retained legitimate old scorer hashes and the `0e17d1a+outputfixes` execution-state labels. The external Table 3BC original remains a dependency; the repository version has different path configuration. Unrecorded diagnostic execution hashes were not fabricated (P1-02/P1-03).
- **Tuning decisions:** preserved pending states, old final markers and pre-fix tuning scores as history. A completed deposit is not a completed decision ledger; any later decisions require evidence, not retrospective inference (P1-13).
- **Manuscript / todo / quarantine destinations:** P1-07, P1-08, P1-11, P1-13, P1-14, P1-15 and P1-19 explicitly mark integration work for the later passes. In particular, qualify S4's corrected-arm provenance, preserve cancellation lower bounds, and distinguish historical deposit counts and C-10 status from their current state. None of these three files was edited by this pass.
- **Verification limits:** checks establish file integrity, accounting arithmetic and consistency of deposited summaries. They do not rerun real-genome detection, full S4 matching, or the historical tuning campaign. The CEN180 generation command/BLAST version remains unavailable as already disclosed; the fixed truth coordinates themselves pass the requested integrity checks.

Final validation: per-row source byte counts and recorded first-megabyte prefixes have no mismatches; all concrete source paths and named scorer files exist; every unchanged historical scorer prefix resolves to its matching git version or to the explicitly identified external Table 3BC producer. All 15 current S4 JSONs pass their count-fraction arithmetic checks. Targeted diff whitespace checks pass. Raw sacct data rows and all checksum files were compared against the baseline and are unchanged. Full deposit guards are intentionally deferred until the human rehashes.
