# Pass 2 — Methods vs code

## Summary

24 findings: **17 CONFIRMED, 4 REJECTED, 3 BLOCKED-ON-MISSING-ARTIFACT, 0 SUSPECTED**. Confirmed manuscript defects were corrected within Section 2 and Supplementary Methods. Code, results/, todo.md and quarantine.md were not edited by this pass.

The most serious defect was the account of the supplementary periodicity passes: S1.4 specified a different identity statistic from the implementation, conflated two denominators, and described the catch-all endpoint as though it were the satellite endpoint. These passes contribute to the published accuracy, so this affects the operational definition of the method, not just terminology. The other central correction is computational: per-copy DP is not quadratic in megabase array length, and occurrence sorting must be included when discussing seeding cost.

The central mechanism is a **mixed pipeline**. Published Tier 1 runs the direct scanner and additive FM-index enumeration; Tier 2 runs LCP candidate extraction and indexed k-mer lookup in both sub-scans; Tier 3 uses indexed k-mer lookup, extension and either anchor verification or DP. Satellite fill and catch-all are periodicity scans without index queries or DP refinement. The existing Discussion 4.3 correction is right on this distinction. Nothing found establishes that replacing an exhaustive aligner with FM-index queries causes the measured range-cost result.

References below use manuscript line numbers after this pass; edits preserved its line structure. For an original claim, `git show HEAD:manuscript.md | sed -n 'LINEp'` retrieves the pre-pass wording. The parallel results pass may change results prose; evidence here is the code, deposited numeric records, and explicitly identified external launch records read during this pass.

No benchmark metric was numerically changed. Added algorithm constants are transcriptions from the **deposited benchmark source snapshot `0363d8b:src/…`**, not new measurements. Their extraction commands appear below. Recovered competitor flags come from deposited GNU-time logs, and the ablation configuration from deposited manifest rows. No genome was reprocessed.

## Findings

### P2-01 — CONFIRMED — Per-query complexity was presented as seeding complexity

- **Claim:** manuscript.md:46 says the candidate period is read from occurrences at linear cost, with no sequence scan; it also calls suffix construction near-linear in practice. S1.5, manuscript.md:459, gives a checkpoint storage estimate without distinguishing it from the native representation.
- **Evidence:** bwtandem/bwt_seed.py:177–195 samples the sequence and caches queried k-mers; :232 sorts occurrences; :235 invokes the adjacent-gap scan. bwtandem/bwt_core.py:281–334 uses pydivsufsort with a NumPy prefix-doubling fallback; :358–396 constructs checkpoints, and :398–435 retains another flattened checkpoint array for C queries. Rank/search costs are O(k) only at fixed checkpoint spacing; extracting a suffix-array slice is O(occ). Sorting is O(occ log occ) worst case. Text, LCP, masks, Python objects and temporaries also occupy memory.
- **Check:** `nl -ba bwtandem/bwt_seed.py | sed -n '177,238p'; nl -ba bwtandem/bwt_core.py | sed -n '281,334p;358,435p;444,550p'`.
- **Fix applied:** yes. Distinguished derived per-query bounds, sampling and sorting; removed the unmeasured practical scaling assertion and qualified the checkpoint estimate. Kept cited suffix-construction complexity as a stated bound. CLAUDE.md's shared-seeder description and code agree that sampling precedes occurrence analysis; the original manuscript omitted that work in this cost sentence.

### P2-02 — CONFIRMED — Tier 1 native scan and extension were oversimplified

- **Claim:** manuscript.md:50 describes construction of a boolean vector and says Tier 1 does not use the index; :52 describes a strict cumulative fraction below 20%.
- **Evidence:** bwtandem/tier1.py:211–244 dispatches to `find_period_runs` when the C scanner loads; only the fallback materializes the vector. bwtandem/c_extensions/tier1_scan.c:33–85 directly scans valid-base equalities. bwtandem/accelerators.py:81–91 and :127–195, mirrored by _accelerators.pyx:188–207 and :419–509, use a fixed seed motif, extend right then left, and accept an integer budget `max(1, ceil(rate * period * copies))`, so the literal percentage is not a strict ceiling for short seeds. Tier-1 callers take the whole-copy `full_start/full_end` fields; they do not use the separately returned partial flank coordinates.
- **Check / numeric source:** `git show 0363d8b:src/accelerators.py | nl -ba | sed -n '81,91p;127,195p'; nl -ba bwtandem/tier1.py | sed -n '211,244p;267,300p'`.
- **Fix applied:** yes. Specified the native match indicator, per-period candidate-buffer cap (tier1.py:212; C scanner stops when the buffer fills), and integer extension budget, and scoped direct comparison to the initial stage. The cap is transcribed from `git show 0363d8b:src/tier1.py | sed -n '211,230p'`. The two-copy extension setting for periods ≤3, five-copy library default, longest-first order, and length/score gates otherwise agree with code. The C and Cython paths were inspected separately rather than inferred from comments.

### P2-03 — CONFIRMED — FM enumeration exclusion, gap terminology and sampling cap

- **Claim:** manuscript.md:54,421 says the enumeration scans only residual sequence; S1.1 describes gaps of two copies and both passages claim a subsample of *up to* two million bases.
- **Evidence:** tier1.py:469–481 queries the whole index and sorts its suffix-array interval. :513–518 checks only run start, midpoint and final base against the exclusion mask, after ranking by LLR within each descending period. :397–402 permits a separation of `(max_gap_copies + 1) * p`, i.e. two **skipped** copies, not a maximum separation of two copies. `_base_freqs`, :364–366, uses floor division for its stride and can visit more than two million positions.
- **Check:** `nl -ba bwtandem/tier1.py | sed -n '359,421p;465,518p'`; run the executable function-body checks below. Calling the actual extracted `_base_freqs` body on a counting object with n=3,000,000 visits **3,000,000** positions, not two million. No genome input is needed.
- **Prior disposition explicitly reopened:** `docs/2026-09-03-finding-dispositions.md`, R3-14 (REJECTED). New concrete evidence is an executed count of the actual loop, not a missing artifact or an alternative inferred implementation. The earlier rejection equated `n // 2_000_000` with a hard sampling cap; it is not one. No chromosome sampling measurement was invented.
- **Fix applied:** yes. Removed the numerical cap wording, specified skipped copies, and explained whole-index queries plus pointwise exclusion. Primitive rotations, periods 1–6, minimum three occurrences, span 20, density 0.45, LLR 6 and per-query occurrence cap 20,000,000 match the constructor and S2 overrides. Their values were not changed.

### P2-04 — CONFIRMED — Tier 2 copy requirements and jitter need phase-specific disclosure

- **Claim:** manuscript.md:60,425 gives a uniform 3% progression tolerance and leaves “sufficient copies” unspecified; S1.2's last sentence assigns k-mer seeding to one sub-scan and LCP to the other.
- **Evidence:** finder.py:198–231 calls both long-unit and general scans; tier2.py:183–184,247–258 and :348–350,413–424 show LCP then k-mer seeding in **both**. Long-unit passes two copies through refinement. General LCP extension uses `short_req_copies=2`, but :395–396 calls refinement without overriding the default three-copy requirement (:70,109–122). General k-mer seeding also uses three (:419). The shared occurrence cap is 5,000 (bwt_seed.py:116); long-unit LCP DP is capped at 8,192 (tier2.py:97–99,203). _accelerators.pyx:759–763 and accelerators.py:239 use `max(1 bp, first_gap * tolerance_ratio)`. Thus gaps 10 and 11 can belong to the same run at nominal 3% tolerance.
- **Check / numeric source:** `git show 0363d8b:src/tier2.py | nl -ba | sed -n '70,122p;198,258p;381,439p'; git show 0363d8b:src/bwt_seed.py | sed -n '107,118p'; git show 0363d8b:src/_accelerators.pyx | sed -n '713,785p'`. Function-body check below returns `[(0, 21, 10)]` for positions `[0,10,21]`.
- **Fix applied:** yes. Added the one-base floor, copy gates, occurrence cap and DP bound, and made the two sub-scan descriptions consistent. Confirmed unchanged: long-unit periods 20–MAXP, general periods 10–50, k=10/9, stride=10/5, LCP thresholds=10/8, extension mismatch=0.30. CLAUDE.md's phase summary is incomplete; its tuning section and code agree that the short-copy override exists, but that override does not lower the general refinement gate.

### P2-05 — CONFIRMED — Primitive-period tests were called the wrong statistic and incompletely specified

- **Claim:** manuscript.md:58,423 describes the 2% approximate test as autocorrelation and reduces the whole refinement account to divisibility plus that test.
- **Evidence:** motif_utils.py:916–923 compares each character against a repetition of `s[:p]`; approximate p need not divide the motif length. The C equivalent is in c_extensions/tier2_accel.c. `refine_repeat`, :777–807, additionally invokes region autocorrelation for small unreduced consensuses, and `_detect_satellite_period`, :846–890, searches a separate window with a much looser identity floor. This can change reported period independently of the 2% template test.
- **Check / numeric source:** `git show 0363d8b:src/motif_utils.py | nl -ba | sed -n '777,807p;846,925p'; rg -n 'smallest_period_str_approx|template|text\[i\]' bwtandem/c_extensions/tier2_accel.c`.
- **Fix applied:** yes. Described template matching and the subsequent short/satellite autocorrelation branches, with their actual thresholds and exclusive upper-bound handling. This closes the already confirmed R3-11 and the unresolved definition part of R3-6; it does not claim that every emitted call is reduced, because anchor and supplementary calls bypass this path.

### P2-06 — CONFIRMED — Tier 3 DP cost, refinement settings and anchor statistics

- **Claim:** manuscript.md:68 says anchor verification avoids quadratic DP costs on megabase arrays. S1.3, :451, gives only band-cell work and omits the full-width allocations/initialization and branch-specific settings.
- **Evidence:** tier3.py:174 selects anchors at >100 copies or >10,000 bp; :184–195 verifies against the seed and computes consensus from at most the first 20 complete copies; the anchor branch never calls `refine_repeat`. :235–242 uses fixed 0.20 mismatch and 0.10 indel settings for smaller calls, separately from GC-dependent seed extension. motif_utils.py:677–700 updates consensus sequentially. c_extensions/align_accel.c:59–107 retains a full traceback matrix, :137–138 initializes full-width rows; _accelerators.pyx:814–856 and motif_utils.py:317–332 also allocate full tables. Work and DP memory per copy are quadratic in period; copy count is a linear factor at fixed period.
- **Check / numeric source:** `git show 0363d8b:src/tier3.py | nl -ba | sed -n '37,39p;172,242p'; git show 0363d8b:src/c_extensions/align_accel.c | nl -ba | sed -n '59,145p'; nl -ba bwtandem/motif_utils.py | sed -n '626,705p'; nl -ba bwtandem/_accelerators.pyx | sed -n '788,858p'`.
- **Fix applied:** yes. Corrected the total-array complexity implication; labelled cost bounds as derived; specified semi-global edit-distance alignment, fixed refinement mismatch, anchor consensus sampling and absence of primitive refinement. Adaptive k, stride, occurrence budgets, GC mismatch, anchor limits and MAXP-dependent jitter remain unchanged. CLAUDE.md's “banded Smith-Waterman” label disagrees with the implementation; the manuscript's earlier “Needleman-Wunsch” label was also less precise than the semi-global prefix alignment actually used.

### P2-07 — CONFIRMED — Coverage masks and post-merge statistics were incompletely described

- **Claim:** manuscript.md:48 limits masks to detected regions; :70 describes consolidation without the statistics cutoff.
- **Evidence:** bwt_seed.py:293–295 marks a raw candidate before the caller attempts refinement. Thus a rejected candidate can suppress later seeds (also explicitly noted in tier2.py:457–460). finder.py:366–388 uses consensus motifs preferentially, not necessarily the primitive motif field; :422–429 updates merged coordinates and copies but recomputes statistics only at ≤50,000 bp. Longer merged records inherit earlier statistics. :801–825 and :311 apply requested bounds at registration and at the end.
- **Check / numeric source:** `git show 0363d8b:src/finder.py | nl -ba | sed -n '349,437p;801,825p'; nl -ba bwtandem/bwt_seed.py | sed -n '283,295p'; nl -ba bwtandem/coverage.py`.
- **Fix applied:** yes. Disclosed speculative masking, consensus-based merging and retained statistics. Verified unchanged: gaps max(10,p),10p,100p at boundaries 20/100; fuzzy canonical match from length 50 at ≤10% Hamming distance; >half-shorter overlap suppression against the last retained record; ≥0.55 satellite merge gate only if gap>p and gap≥2p, otherwise direct mismatch gate; merge/filter, up to two fill/remerge cycles, catch-all/remerge, then bounds. An unchanged call count, rather than identity of records, stops the second fill cycle (finder.py:294).

### P2-08 — CONFIRMED — Autocorrelation denominator, endpoint and scan-domain mismatch

- **Claim:** manuscript.md:72,74,453–457 defines identity as raw equalities/(w−p), describes a valid-*base* gate, places entire blocks within 50 kb, and gives the catch-all the endpoint of the last passing window.
- **Evidence:** autocorr.py:51–79 computes valid-match/valid-comparison identity, returning zero below an 80% valid-pair floor. finder.py:539–541 separately checks block valid bases. Satellite segmentation (:611–650) and catch-all (:696–738) divide matches by the **full comparison window**, with ambiguous pairs contributing no support. For a passing start run `[a,b)`, satellite end is `b−1+q+p` (clipped); catch-all end is `b+q` (clipped). Catch-all computes whole-sequence counts, masks covered starts, then rejects >30% covered candidates. Block proximity uses `any(near_satellite[block])`, so intersection with the neighborhood suffices; period nomination is also bounded by less than half the sampled window. Supplementary period windows do not read CLI period limits. Initial satellite mismatch is one minus mean passing-window support; catch-all uses maximum support. Neither is whole-call DP identity.
- **Check / numeric source:** `git show 0363d8b:src/autocorr.py | nl -ba | sed -n '43,79p;112,152p'; git show 0363d8b:src/finder.py | nl -ba | sed -n '519,590p;609,659p;679,750p'`. Executable check below: on `AAAAAAAAAAN` at lag 1, scalar identity=1.0 while full-window support=0.9.
- **Fix applied:** yes. Replaced the equation, separated the two denominators/gates and endpoint formulas, qualified proximity, and disclosed whole-chromosome/per-period scanning, independent scan bounds and mismatch summaries. The previous 70%→80% correction is retained; this completes the statistic definition rather than reopening that corrected value.

### P2-09 — CONFIRMED — Assertions still presented as established observations

- **Claim:** manuscript.md:62 explains disabling approximate Tier-2 seeding by an unreported efficacy result; :66,435 calls parameter clamps “empirically validated”.
- **Evidence:** the former statement is already retired by quarantine.md §3.7; tier2.py:78,453–469 establishes only the opt-in branch, not its biological performance. tier3.py:61–69 establishes hard-coded clamp limits, not empirical validation of each endpoint. The brief explicitly requires asserted Methods cost/scaling claims to be labelled or removed; P2-01/P2-06 handle the cost assertions.
- **Check:** `sed -n '/### 3.7/,/### 3.8/p' quarantine.md; nl -ba bwtandem/tier2.py | sed -n '74,85p;448,469p'; nl -ba bwtandem/tier3.py | sed -n '61,69p'`.
- **Fix applied:** yes. Removed the already-retired efficacy explanation, kept the fact that the mode was disabled, and changed the clamps to “implementation-defined”, and limited the statement about the GC formula not attaining its ceiling to the benchmark chromosomes rather than all real sequence. This does **not** newly confirm that the claimed efficacy result is false; its magnitude remains unsupported by a deposited experiment. No new performance number was supplied.

### P2-10 — CONFIRMED — A reported ablation used an unnamed environment switch

- **Claim:** manuscript.md:461,488 presents S2 as the full configuration account but never names the seeding-ablation switch used for Section 3.1.
- **Evidence:** results/manifest.tsv:78–79 explicitly distinguishes `BWT_SEED_KTUPLE=0/1`, four workers, Col-CEN, periods 1–2,000, commit 294f8ac. bwt_seed.py:82 reads it at module import and :204–226 changes the occurrence provider. The table is built and sorted (:41–61), cached by (index,k), and leaves index construction and Tier 1 enumeration in place. CLAUDE.md:238–249 agrees with this limited scope.
- **Check / numeric source:** `sed -n '78,79p' results/manifest.tsv; nl -ba bwtandem/bwt_seed.py | sed -n '41,93p;197,238p'`. External supplementary check: `cat /data/gpfs/assoc/pgl/devel/exp1_human/wp0/fixcampaign/run_seedablation.sbatch` confirms the Arabidopsis gates in both arms.
- **Fix applied:** yes. Named the switch, import timing, separate historical build/worker settings and restricted ablation scope. Removed the implication that the main configuration table enumerates every historical ablation. This is a genuine omitted run-dependent knob, unlike unused optional controls.

### P2-11 — REJECTED — Phantom manuscript knobs or undisclosed main-run detection overrides

- **Claim tested:** whether a named S2/S3 knob is nonexistent/misspelled, or the surviving main-run environment sets an extra detection control not disclosed by the paper.
- **Evidence:** applying tests/test_env_var_docs.py's source/name regexes to manuscript.md gives an empty phantom set before and after edits. All shared overrides have actual readers. The three external whole-genome launch logs print the detection-variable environment, which matches the shared base, short gate and genome-specific catch-all blocks. The deposited range-pair wrapper matches F. The external p100/identity launchers also match P/B/F/H and S3; they do not print the full inherited environment, a narrower limitation retained in P2-22.
- **Check:** environment audit below; `sed -n '24,35p' results/range_cost_0363d8b/run_rangerep0363.sbatch`; `sed -n '1,28p' /data/gpfs/assoc/pgl/devel/exp1_human/regen/logs/regen_regen_human_6110901.out` (also maize_6124640 and colcen_6110900). `cat /data/gpfs/assoc/pgl/devel/exp1_human/regen/maize_rescore/run_human_{p100,idsweep}_0363.sbatch`.
- **Fix applied:** none to values. TIER1_FMSCAN is disclosed and enabled. Extra names read by code are mostly optional/default controls, not evidence that the reported runs secretly set them. P2-10 is the specific exception for the separately reported ablation.

### P2-12 — CONFIRMED — Launch wrappers do more than schedule jobs

- **Claim:** manuscript.md:488 says launch wrappers add scheduling directives only and that the blocks are a complete configuration.
- **Evidence:** scripts/benchmark/regen_345.sbatch:34–91 pins interpreter/repository, exports the detection environment, checks the commit and captures provenance. results/range_cost_0363d8b/run_rangerep0363.sbatch:10–35 selects PATH/compiler and exports the gates. The p100/identity launchers additionally put the benchmark interpreter ahead of PATH; none sanitizes all inherited tuning variables. A JSON command alone therefore does not encode the run's environment.
- **Check:** `nl -ba scripts/benchmark/regen_345.sbatch | sed -n '34,91p'; nl -ba results/range_cost_0363d8b/run_rangerep0363.sbatch | sed -n '10,35p'; sed -n '53,105p' scripts/benchmark/run_with_provenance.sh`.
- **Fix applied:** yes. Described the actual wrapper responsibilities, pointed to deposited launchers and instructed reproduction with unspecified tuning variables unset. This does not assert that contamination happened. The older R3-4 assertion that no launcher is deposited is no longer true for the whole-genome or current range-pair launchers.

### P2-13 — CONFIRMED — The release environment files freeze only the later environment

- **Claim:** manuscript.md:82,474 distinguishes earlier and later versions, but does not connect that distinction to the environment files offered for reproduction. environment.yml:6, environment.core.lock.yml:1 and Dockerfile:16 describe their freeze as that used for the published numbers without this qualification.
- **Evidence:** both YAMLs pin Python 3.11.15/numpy 2.4.6; Dockerfile installs the core lock. Whole-genome JSON records report 3.11.14/2.3.1; p100/S3 JSONs report 3.11.15/2.4.6. pyproject.toml allows Python≥3.11/numpy≥2.0 and pins pydivsufsort=0.0.20; it is not an exact environment. Docker LABEL version=v1.0 also differs from package version=0.9.0, but the manuscript makes no corresponding BWTandem version claim.
- **Check:** `cat environment.yml environment.core.lock.yml Dockerfile pyproject.toml`; JSON audit below.
- **Fix applied:** yes, added the scope of the freezes to S2 and distinguished the release Dockerfile from the original competitor sandbox. **No version number was changed.** The previously adjudicated distinction between whole-genome and later panel environments is preserved. Library availability is not a benchmark execution proof; see P2-22/P2-24.

### P2-14 — CONFIRMED — Container exception count and incomplete competitor commands

- **Claim:** manuscript.md:490 says only two exceptions to the container, while :76 correctly names both 2026 additions plus the ULTRA attempt. S1 omits widened tantan flags, maize TRASH `--def`, and says mreps/NCRF invocations were not preserved.
- **Evidence:** results/comparators2026/README.md:11–12 records local installs for both additions. Original competitor logs retain complete multiline mreps/NCRF commands: human mreps uses `-fasta -res 5 -allowsmall`; original Arabidopsis band attempt uses `-minperiod 150 -maxperiod 400 -res 10` and records missing input files. NCRF maize 3A uses `--minlength=200`, 3B/3C `--minlength=500`; maize TRASH adds `--def`. Manifest :68–71 records widened tantan `-w` values. The original failed Arabidopsis mreps attempt must not be mistaken for the later successful Table 2 run (sacct :19–20).
- **Check / numeric source:** `rg -n 'mreps -fasta|minlength=|Command being timed' results/competitor_logs/{mreps,ncrf}*`; `rg -n 'Command being timed' results/competitor_logs/trash*`; `sed -n '68,71p' results/manifest.tsv`; `sed -n '7,12p' results/comparators2026/README.md`; `sed -n '19,20p' results/sacct_provenance.txt`.
- **Fix applied:** yes. Aligned the caption with Section 2.2, restored flags and specified original-vs-rerun status. TRF positional/scoring flags and MAXP assignments, original ULTRA flags, maize ULTRA `--read_all -i 3 -d 3 --bed`, original tantan `-f4`, and AniAnn's `-j 2 -q` otherwise agree with available commands. No tool version was inferred from an unversioned command.

### P2-15 — CONFIRMED — Thread/allocation and cost-provenance prose overgeneralizes

- **Claim:** manuscript.md:80 calls BWTandem workers threads, assigns four to the main matched-range Table 1b even though its main row now filters the two-worker whole-genome BED, says every remaining tool uses two, and limits later competitor accounting to two exceptions. :82 says every competitor log is in results/competitor_logs/. :99 calls costs comparable solely because input scope matches and retains a ~5% larger-input claim.
- **Evidence:** main.py:164–180 uses ProcessPoolExecutor. Main JSON commands specify two, native panel commands four. The current Table 1b main row and caption describe post-filtered whole-genome calls; the F native row is a sensitivity analysis. results/manifest.tsv:68–71 identifies later tantan jobs, allocated two CPUs but one active thread. comparators2026/README.md:22–29 labels later costs GNU time. Their input scope does not turn that into BWTandem's cgroup maximum. The methods' own Section 2.2.2 has already corrected the assembly-base difference.
- **Check:** `nl -ba bwtandem/main.py | sed -n '164,180p'; sed -n '127,145p' manuscript.md; sed -n '68,71p' results/manifest.tsv; sed -n '22,29p' results/comparators2026/README.md`; JSON audit below.
- **Fix applied:** yes. Distinguished worker counts, active-thread settings and allocations; scoped inherited costs/log deposits; kept separate later accounting; narrowed input comparability and removed the stale approximate input percentage. No cost or worker numeral was recomputed without evidence. CLAUDE.md's process-accounting explanation (:258–261) and code agree; the old Methods terminology did not.

### P2-16 — CONFIRMED — Stopped-run cost ratios and output coordinates overstated processing

- **Claim:** manuscript.md:78 describes ULTRA as having “covered a twenty-fifth of the input”, treats stopped-run ratios without a completion-bound label, and calls ceased output growth a zero processing rate.
- **Evidence:** results/range_cost_attempts/ultra_p2000/ultra_h_p2000_6145581.log records a cancelled attempt, not input progress instrumentation. results/range_cost_attempts/README.md explains the last complete output record and lower-bound status. This is the already-established R1-5/R1-15 distinction, not a new assertion about where computation stopped.
- **Check:** `cat results/range_cost_attempts/README.md; tail -25 results/range_cost_attempts/ultra_p2000/ultra_h_p2000_6145581.log; sed -n '78p' manuscript.md`.
- **Fix applied:** yes. Kept numbers unchanged, called the rate an output-coordinate rate, removed the inferred processed fraction, and labelled completion-cost bounds in their respective environments.

### P2-17 — CONFIRMED — Methods still says the raw BLAST hit set was not retained

- **Claim:** manuscript.md:90 first names the deposited raw hits, then says that raw hit set was not retained.
- **Evidence:** results/ground_truth/colcen_cen180_raw_blast_hits.bed exists; the same Methods paragraph correctly distinguishes the absent identity field from the present coordinates. This is a stale provenance sentence, not a defect in the truth coordinates or headline recall.
- **Check:** `head -2 results/ground_truth/colcen_cen180_raw_blast_hits.bed; sed -n '90p' manuscript.md`.
- **Fix applied:** yes. Specified that raw coordinates survive while their identities do not. No coordinate, count, threshold or metric changed.

### P2-18 — CONFIRMED — CLAUDE.md architecture summaries drift from both code and Methods

- **Claim/evidence comparison:** CLAUDE.md:322 says a 10 Mb threshold selects canonical FM enumeration vs sliding scanning. Actual tier1.py:194–203,331–333 selects explicit modes 0/1/2, independent of chromosome size, and :346–357 enumerates every primitive rotation. **Code and manuscript agree**, CLAUDE.md architecture disagrees (its tuning section correctly describes the switch). CLAUDE.md:328 gives fixed Tier-3 k=20/stride=100; code and manuscript use adaptive values. CLAUDE.md:348 gives only gap≤max(10,p) and unconditional overlap suppression; code and manuscript have period-stratified gaps and the half-shorter gate. CLAUDE.md:336 calls refinement Smith-Waterman; code uses semi-global prefix edit-distance alignment, now accurately named in Methods. The ≤2% summary at :354 omits the additional autocorrelation heuristics.
- **Check:** `nl -ba CLAUDE.md | sed -n '318,355p'; nl -ba bwtandem/tier1.py | sed -n '194,203p;325,357p'; nl -ba bwtandem/tier3.py | sed -n '23,69p'; nl -ba bwtandem/finder.py | sed -n '329,420p'`.
- **Fix applied:** manuscript disagreements fixed under earlier findings; **CLAUDE.md not edited**, outside authorized scope. **TODO.MD ENTRY:** update these architecture summaries against the code; the environment-name test passes because it does not test semantic prose. Do not change the code to implement the stale architecture descriptions.

### P2-19 — REJECTED — Discussion 4.3 still confines index use to Tier 2/3

- **Claim tested:** whether the earlier correction of quarantine §6.24 / R3-9 is wrong.
- **Evidence:** manuscript.md:327 explicitly says direct Tier-1 scanner plus additive FM motif enumeration; :323 explicitly identifies both supplementary passes as autocorrelation scans. tier1.py:331–333 invokes enumeration when mode=1, and S2 sets it. bwt_seed.py:212,226 provides the Tier-2/3 indexed lookup. No FM query occurs in either supplementary detector.
- **Check:** `sed -n '323,327p' manuscript.md; sed -n '325,335p' bwtandem/tier1.py; sed -n '197,238p' bwtandem/bwt_seed.py; sed -n '480,756p' bwtandem/finder.py`.
- **Fix applied:** none to Discussion, which is outside edit scope and is correct on this point. Its causal restraint is warranted: the code and limited occurrence-provider ablation do not establish whole-pipeline index causation.

### P2-20 — REJECTED — Tier 3 range wiring and 24 Mb saturation are wrong

- **Claim tested:** the previously withdrawn stride findings, and whether current search bounds match release behavior.
- **Evidence:** finder.py:130–138 passes max(100,min_period)..min(100000,max_period). tier3.py:30–67 reduces stride before final clamp; the maximum reduction is ×0.5, so n≥24 Mb guarantees stride 300 under balanced. The existing sentence is a guarantee, not the earliest possible saturation point. k shifts for fast/sensitive and the larger-chromosome occurrence discontinuity also match code. The Col-CEN organellar values remain separately disclosed.
- **Check:** `nl -ba bwtandem/finder.py | sed -n '130,139p'; nl -ba bwtandem/tier3.py | sed -n '23,69p'`; adaptive check below evaluates n=24 Mb at coverage 0,0.5,0.9,1 and returns 300 throughout.
- **Fix applied:** none to these numbers. Quarantine §6.6/§6.16 remains withdrawn; §6.17's release-build correction is retained.

### P2-21 — REJECTED — Headline Methods cost cells lack deposited support

- **Claim tested:** whether the §2.2.1 whole-genome times/memory are still the unresolved old §6.20 problem.
- **Evidence:** results/sacct_provenance.txt:91–98 now contains the job and batch records: Col-CEN 00:40:11/2268896K, human 12:38:42/29447952K, maize 15:51:03/29831980K. Dividing KiB by 1024² rounds to 2.16/28.08/28.45 GiB. Original human competitor GNU-time logs support the quoted 29:46:49 and 33:43:46 and respective RSS. The wait4 JSON memory is a different statistic, not a contradictory cgroup observation.
- **Check:** cost audit below; `rg -n 'Elapsed|Maximum resident' results/competitor_logs/{ultra,trf}__GCA_000001405.15_GRCh38_genomic_run.log`.
- **Fix applied:** no numerical change. The previous missing-sacct issue has been resolved; it is not reopened.

### P2-22 — BLOCKED-ON-MISSING-ARTIFACT — Complete inherited environments and binary identities

- **Claim:** manuscript.md:474 states exact interpreter versions and active compiled accelerators for the benchmark runs; :488 describes reproduction from environment settings.
- **Evidence:** the JSONs have version strings and commands, but no environment or compiled-binary fields. run_with_provenance.sh:53,102–103 probes `python3` on PATH rather than the explicit detector executable. External later-panel launchers explicitly put the detector directory on PATH, providing positive support for their version attribution. The earlier whole-genome launcher does not itself enforce that binding. Its surviving logs print the tuning-prefix subset, not a complete runtime environment or native-library identities. This is **not** evidence that the printed versions or active-native claims are wrong, and does not reverse the adjudication of R2-8.
- **Check:** `sed -n '53,105p' scripts/benchmark/run_with_provenance.sh`; JSON audit below; `tail -12 /data/gpfs/assoc/pgl/devel/exp1_human/regen/maize_rescore/run_human_p100_0363.sbatch`; `sed -n '75,91p' scripts/benchmark/regen_345.sbatch`.
- **Fix applied:** no speculative version substitution. **TODO.MD ENTRY:** deposit surviving main-run environment headers and later launchers, and preserve detector-interpreter/native-library identities in future provenance. Full historical identity cannot be reconstructed merely by checking today's environment. This includes OPENMP/BLAS runtime settings: none is established as a secret detection knob by available records.

### P2-23 — BLOCKED-ON-MISSING-ARTIFACT — Orphan thread-scaling configuration row

- **Claim:** manuscript.md:486 lists a thread-scaling pair for Sections 2.2.1 and 4.4, but those sections no longer report a pair of scaling measurements. The row labels these as outside the manifest.
- **Evidence:** the current manuscript has no numerical thread-scaling comparison; the row itself does not identify inputs/build/job records beyond saying “as the human main run”. This does not prove the historical pair never ran.
- **Check:** `rg -n 'thread.scal|single.thread|speedup|threads' manuscript.md`; compare `sed -n '80,82p;330,336p;486p' manuscript.md`.
- **Fix applied:** removed the misleading “quoted below” cross-reference at :80, but retained the S2 row pending identification of the intended evidence. **TODO.MD ENTRY:** supply and cite the side-measurement artifact, or remove the orphan row and its cross-references. No replacement timing or worker-scaling claim was invented.

### P2-24 — BLOCKED-ON-MISSING-ARTIFACT — Historic competitor versions/container build not independently reconstructible

- **Claim:** manuscript.md:76,490–502 names original versions and a single preserved writable competitor sandbox.
- **Evidence:** deposited original logs positively show `singularity exec ./bwtbench.sif` and the flags, but that command does not prove package versions or whether the path was an image or sandbox at execution. The current Dockerfile installs the detector core, not this old suite; environment.yml does not pin competitor versions. The 2026 additions have explicit version/provenance rows, and the ULTRA attempt is correctly described as a separate self-reported-version-matched binary, not the same binary. The old full sandbox package inventory or contemporaneous immutable image snapshot is not deposited.
- **Check:** `rg -n 'Command being timed' results/competitor_logs/{trf,ultra,tantan}*`; `cat Dockerfile environment.yml`; `sed -n '7,12p' results/comparators2026/README.md`; `cat results/range_cost_attempts/ultra_p2000/run_ultra_human_p2000.sbatch`.
- **Fix applied:** no invented version corrections or claim that the sandbox is absent. **TODO.MD ENTRY:** archive the historical competitor package/binary inventory and container provenance; distinguish author-attested versions from independently preserved execution evidence. Current release metadata's v1.0 Docker label versus 0.9.0 package version can be reconciled separately; it is not evidence against an unrelated competitor version.

### Re-runnable checks used in this pass

Environment names and JSON versions (no imports of the detector):

```bash
python3 - <<'PY'
import runpy, pathlib, json
m = runpy.run_path('tests/test_env_var_docs.py')
read = m['_knobs_read_by_code']()
doc = set(m['_DOC'].findall(pathlib.Path('manuscript.md').read_text()))
print('phantom:', sorted(doc - read))
print('read but not named:', sorted(read - doc))
assert not doc - read
for p in sorted(pathlib.Path('results/regen').glob('*.provenance.json')):
    d = json.loads(p.read_text())
    if 'python' in d:
        print(p.name, d['python'], d['numpy'], d['command'])
PY
```

Small executable mechanism checks, extracting actual function bodies to avoid native-loader compilation or real-genome work:

```bash
/data/gpfs/assoc/pgl/bin/conda/conda_envs/bwtandem/bin/python - <<'PY'
import ast, math, numpy as np, runpy
from pathlib import Path
def method(path, name, extra):
    tree = ast.parse(Path(path).read_text())
    f = next(n for n in ast.walk(tree)
             if isinstance(n, ast.FunctionDef) and n.name == name)
    f.decorator_list = []
    ns = dict(extra)
    exec(compile(ast.Module(body=[f], type_ignores=[]), path, 'exec'), ns)
    return ns[name]
ac = runpy.run_path('bwtandem/autocorr.py')
x = np.frombuffer(b'AAAAAAAAAAN', dtype=np.uint8)
assert ac['autocorr_identity'](x, 1) == 1.0
assert float(ac['windowed_match_counts'](x, 1, 10)[0])/10 == .9
runs = method('bwtandem/accelerators.py', '_find_periodic_runs_py',
              {'np': np, 'List': list, 'Tuple': tuple})
assert runs(np.array([0,10,21], dtype=np.int64), 10, 50, 3, .03) == [(0,21,10)]
f = method('bwtandem/tier1.py', '_base_freqs', {})
class Counter:
    count = 0
    def __getitem__(self, i):
        self.count += 1
        return 'A'
c = Counter()
f(c, 3_000_000)
assert c.count == 3_000_000
adaptive = method('bwtandem/tier3.py', 'compute_adaptive_params', {'math': math})
assert [adaptive(24_000_000, .4, c, 100, 2000)['stride']
        for c in (0, .5, .9, 1)] == [300]*4
assert [max(2, 6//p + 2) for p in range(1,10)] == [8,5,4,3,3,3,2,2,2]
print('mechanism checks passed')
PY
```

Headline cost check, from the deposited artifact (values retained, not edits):

```bash
python3 - <<'PY'
from pathlib import Path
for line in Path('results/sacct_provenance.txt').read_text().splitlines():
    f = line.split('|')
    if f[0] in ('6110900.batch','6110901.batch','6124640.batch'):
        print(f[0], f[2], f'{int(f[3][:-1])/1024**2:.2f} GiB')
PY
```

Validation: `tests/test_env_var_docs.py` **3 passed**; the mechanism checks above passed; `git diff --check` passed. The full suite was not needed for prose-only changes and no native-path flake diagnosis was repeated. A before/after section comparison verified that Abstract/Introduction and Results/Discussion/References were unchanged by this pass.

## REHASH REQUIRED

## Not fixed, and why

- **No results/ files touched by this pass.** Dirty results/ files belong to the explicitly parallel results audit. No rehash command was run.
- **TODO.MD ENTRIES (not written to todo.md):** P2-18 (CLAUDE architecture drift), P2-22 (runtime/environment evidence), P2-23 (orphan scaling row), P2-24 (historic competitor inventory). Also align environment-file/Docker comments with the earlier/later split in P2-13; archive the external p100, identity-sweep and seeding-ablation launchers before presenting the evidence as repository-self-contained. Their surviving source settings were checked here, not presumed lost.
- **QUARANTINE.MD ENTRIES (not written to quarantine.md):** retire the unqualified Methods seeding-linear-cost/no-sequence-scan formulation (P2-01), megabase-array-quadratic-DP explanation (P2-06), raw-equality autocorrelation definition and shared endpoint description (P2-08), and “wrappers add scheduling directives only” (P2-12). Record P2-03 as an explicit evidence-backed reopening/correction of the R3-14 rejection, retaining its historical disposition rather than rewriting it. Mark the already-retired §3.7 efficacy explanation removed from Methods.
- The implementation's speculative masking, retained long-merge statistics and differing supplementary mismatch summaries were documented, not changed. Changing them could change published outputs and is outside this pass's authorized code scope.
- The central causal framing/title was not reopened as a title decision; the actual mechanisms and computational limitations were checked. No genome-scale ablation or rebenchmark was run to manufacture an attribution.
- Missing records were not turned into wrong version/cost claims. Existing unfavourable accuracy results and the revised range-cost result were retained.
