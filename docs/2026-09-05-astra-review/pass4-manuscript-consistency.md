# Pass 4 — Internal manuscript consistency

## Summary

Review date: **2026-09-10**. Explicit baseline: **64964e1** (`64964e14683aa7fa54a50932d202ba60463eff00`), branch `perf/exp1-human-sensitivity`, on `pronghorn:~/scratch/devel/bwt-algorithm`. HEAD and the existing origin tracking ref agreed; the tracked working tree was clean before this report. The older uncommitted-state sentence in ignored `resume.md` is a stale snapshot, not a manuscript defect.

**8 CONFIRMED** scoped corrections; **3 REJECTED** candidate concerns; **0 BLOCKED-ON-MISSING-ARTIFACT** new findings. The most consequential inconsistency is extrapolating the equal-per-stratum audit to a population count despite explicitly disclaiming population weighting. Other corrections concern semantic cross-references, a reversed runtime list, accounting exceptions, historical counts, interpretation of period-band totals, and the strength of the native-path disclaimer.

Read BRIEF, CLAUDE, quarantine, todo and resume in the prescribed order; reviewed the dispositions and latest presubmit README; read all 563 lines of `manuscript.md`, including captions, references and supplement. This is P4 only, not a peer-review panel, code audit, evidence audit, or submission-readiness certification. No manuscript edits were applied. No BED reads, intersections, scorer runs, jobs, rehashes, staging, commits or branch changes were performed.

All line numbers below refer to baseline `manuscript.md`. Proposed replacements retain existing measurements and adverse findings. The 10 source-limited numerical tokens and six Supplementary Table S2 cells are intentionally unchanged.

## Findings

### P4-01 — CONFIRMED / WARNING: maize TRF runtime list reverses its last two ceilings

**Quote:** `manuscript.md:32`: “on the maize genome ULTRA took 0.23 h at a maximum period of 6 bp, 12.86 h at 200 bp, and 34.73 h at 500 bp, while TRF over that same span was flat, at 5.22 h, 5.51 h and 5.48 h.”

**Positive counterevidence:** Table 3B at :260 gives TRF 5.51 h, Table 3C at :308 gives 5.48 h, and S1 at :510 explicitly maps maize 3A/3B/3C to “6/500/200”. The preceding ULTRA sequence instead orders ceilings 6/200/500. This is a prose-to-table pairing error, not a new cost calculation.

**Proposed replacement:** Replace only “while TRF over that same span was flat, at 5.22 h, 5.51 h and 5.48 h” with “while TRF at those respective ceilings took 5.22 h, 5.48 h and 5.51 h”.

**Cheap check:** C1 below verifies the prose and table/command pairings. **Applied:** no.

### P4-02 — CONFIRMED / WARNING: semantic section references point to the wrong material

**Quotes:** Supplementary Table S4, `manuscript.md:543`, cites “Section 2.2.2” for the scoring definition, the many-to-one baseline, the TRF 2,000 bp attempt, and pairing indeterminacy. At :201 and :543, fragmentation is described as “fragmentation in Section 4.5”.

**Positive counterevidence:** :83 labels 2.2.2 “Genome Assemblies”; :85 labels 2.2.3 “Evaluation Metrics”, and :88 contains the one-to-one definition, baseline and matching-indeterminacy discussion. The failed TRF attempt is described at :78 under 2.2. “4.5 Future directions” begins at :351; the fragmentation/post-merge discussion is :248–254 under “3.3.2 Satellite Array Detection (knob180 and TR-1)” (:247).

**Proposed replacements:** In :543, change the first, second and fourth occurrences of “Section 2.2.2” to “Section 2.2.3”; change its third occurrence, attached to the TRF attempt, to “Section 2.2”. At :201 and :543 replace “fragmentation in Section 4.5” with “fragmentation in Section 3.3.2”. Do not globally replace 2.2.2: references to FASTA scope elsewhere are correct.

**Cheap check:** C2 checks the occurrences and destination headings. **Applied:** no. Named table/figure destinations exist in the manuscript; the sole Markdown image link, Figure 5, resolves locally. This finding concerns destination meaning, not missing artifacts.

### P4-03 — CONFIRMED / WARNING: historical band-count contrast reads as a current result

**Quote:** `manuscript.md:194`: “the same pipeline with the relaxed short-period gate omitted reports 25 calls in the band rather than 1,380, at essentially unchanged coverage and unfiltered recall.”

**Positive counterevidence:** Earlier in that same paragraph the BWTandem figures are explicitly “the regenerated ones”. Table 2 at :208 gives the current CEN180-band count as 1,533; :82 explicitly distinguishes its rise “from 1,380 to 1,533”. The old count is not numerically false; the comparison lacks the historical qualifier needed to prevent attribution to the current Table 2 run.

**Proposed replacement:** “In the historical comparison, omitting the relaxed short-period gate reduced the band count from 1,380 to 25 at essentially unchanged coverage and unfiltered recall; this is not a gate ablation of the regenerated Table 2 output, whose band count is 1,533.”

**Cheap check:** C3 verifies all three contexts. **Applied:** no. Do not replace the old comparison denominator with 1,533 or infer a regenerated ablation.

### P4-04 — CONFIRMED / WARNING: blanket cost-source definition drops disclosed exceptions

**Quote:** `manuscript.md:82`: “Runtime for BWTandem rows is SLURM elapsed time and memory is sacct MaxRSS; competitor rows retain GNU-time measurements.”

**Positive counterevidence:** :80 explicitly says “The ULTRA and mreps Arabidopsis re-runs have job records and carry accounting values like the BWTandem rows.” :358 identifies the paired BWTandem range-cost rows as an exception because their two arms use separate GNU-time MaxRSS records. :80 also identifies historical seeding-ablation GNU-time measurements. Those exceptions contradict a definition of all rows by tool identity.

**Proposed replacement:** “The regenerated whole-genome BWTandem rows use SLURM elapsed time and sacct MaxRSS. Original competitor rows retain GNU-time measurements; later re-runs use the per-run sources described above, including accounting values for the ULTRA and mreps Arabidopsis re-runs. The historical seeding ablation and paired BWTandem range-cost arms use their separately recorded per-arm measurements.”

**Cheap check:** C4 verifies the explicit exceptions. **Applied:** no. No cost cell or missing-accounting disclosure should change.

### P4-05 — CONFIRMED / WARNING: audit population is blurred and an unweighted rate is extrapolated

**Quotes:** `manuscript.md:350`: “The regenerated full-range output has 893,480 calls absent from the other four tabulated tools”; later, “the supported fraction, extrapolated to the population, would still amount to on the order of 10^4 candidate loci”. The first sentence leads into the audit without identifying its narrower target population.

**Positive counterevidence:** Methods :86 defines the audit population as “809,886 regenerated full-range calls overlapping neither the catalog nor any of TRF, ULTRA, tantan or TRASH”, with 100 sampled per stratum. Figure 3 caption :121 states: “Equal sampling across strata does not make this a population-weighted estimate.” Table 1a :132 correctly reports 893,480 tool-unique calls, irrespective of catalog overlap. The counts measure different populations; the audit does not support the population projection.

**Proposed replacements:** After the first sentence at :350 insert: “The audit population was the narrower set of 809,886 calls also absent from the catalog.” Replace “the supported fraction, extrapolated to the population, would still amount to on the order of 10^4 candidate loci, but nothing in this comparison identifies which ones without locus-level review” with “the equal-per-stratum sample does not support a population-wide supported-call count, and individual candidate loci require locus-level review”.

**Cheap check:** C5 verifies the population definition, sampling warning and extrapolation. **Applied:** no. Preserve 4 SUPPORTED / 346 UNSUPPORTED / 50 UNSURE, the criterion, single-reader limitation and denominator-qualified Wilson interval; no new interval or population estimate is proposed.

### P4-06 — CONFIRMED / WARNING: band excess is called established over-calling despite a stated alternative

**Quote:** `manuscript.md:300`: “It establishes that over-calling in this band is general to every tool that detects the arrays at all, TRF included despite its otherwise strong boundary precision.” Later: “re-run at 200 bp it over-calls the band like the others”.

**Positive counterevidence:** The same paragraph calls the total a “loose proxy rather than a measurement of CentC content”, notes that the band also admits knob180, and states “we did not classify the called sequence by family”. Called bases exceeding curated CentC bases establish excess relative to that footprint, not false-positive detection or CentC specificity. This does not negate the separate human audit evidence of over-calling.

**Proposed replacements:** Replace the first quoted sentence with “For all four tools, the called total in this period band exceeds the curated CentC footprint; without family classification, this does not distinguish false-positive calls from knob180 or other repeat sequence.” Replace “re-run at 200 bp it over-calls the band like the others, 2.72 times the curated array” with “re-run at 200 bp its banded total is 2.72 times the curated CentC footprint”. Replace “and no tool here is specific to this band” with “and these totals alone do not establish CentC specificity for any tool”.

**Cheap check:** C6 verifies the inference and explicit qualification together. **Applied:** no. Retain all banded totals and the correction of the misleading narrow-window tantan comparison.

### P4-07 — CONFIRMED / WARNING: native-path disclaimer asserts independence stronger than its evidence

**Quote:** `manuscript.md:350`: “No figure here depends on the affected path, but it is unresolved and we do not claim otherwise.”

**Positive counterevidence:** The paragraph identifies a failure “of the native code path” and limits the chromosome evidence to “the one chromosome tested for it”, explicitly “weaker than a general guarantee”. S2 at :490 states that the whole-genome results used “compiled Cython/C accelerators”. The manuscript supplies a limited non-manifestation observation, not an established exclusion of the affected code path from every figure. Calling the fixture alone the affected path would also conflict with the native-code description.

**Proposed replacement:** “The failure has not been observed in the chromosome-scale check described above; that limited check does not establish that all benchmark executions are independent of the unresolved native-code issue.”

**Cheap check:** C7 verifies the limited observation and native execution statement. **Applied:** no. This is a scope correction, not a finding that any benchmark output is corrupted, and does not reopen exhausted diagnostics.

### P4-08 — CONFIRMED / WARNING: embedded Figure 2 caption retains the older input-scope generalisation

**Quote and location:** `results/figures/paper_figs/plot_fig2_range_cost.py:86`: “these runs are not range-matched, and the competitor FASTA carries 3.92% more sequence.” The caption label is embedded at :80 and painted below the panels by `plt.figtext` at :90. The parent reported direct pixel inspection of both `results/figures/paper_figs/fig2_range_cost.png` and `results/figures/paper_figs/rendered/fig2_range_cost.png`, confirming that this caption and the old Figure 2 label are baked into both images. P4 independently checked the source text, rendering placement and existence of both files, not their plot data or pixels.

**Positive counterevidence:** The current manuscript caption at `manuscript.md:109` correctly says: “the original ULTRA/TRF FASTA includes unplaced sequence, while the 2026 inputs match BWTandem’s chromosome-only scope” (the source uses straight apostrophes). Methods :99 likewise specifies chromosome-only FASTAs for both additions. Thus the embedded blanket competitor-input statement is stale even though the external caption is current. This is bounded caption staleness, not a finding about underlying figure values.

**Proposed replacement:** For the conversion copy only, remove the bottom baked-in caption without removing any plot pixels or axis/legend text; retain the original results files unchanged. Supply the full current `manuscript.md:109` caption externally, replacing its opening figure number with the final assigned number. In particular retain its distinction between original ULTRA/TRF input scope and the 2026 chromosome-only inputs. The parent plans a main-Figure-1 remapping; embedded Figure 2 would then also be stale. This is presentation-only cropping outside `results/`, not rerendering or data editing.

**Cheap rerunnable check:** C8 in the Python block checks the exact source string, caption-rendering call, both image paths and the current manuscript counterstatement. For pixel confirmation, open each named PNG and read its bottom caption; verify the conversion crop against the original to ensure every plot pixel is retained. **Applied:** no; parent handles presentation copies. No further figure-data review is requested.

### P4-R1 — REJECTED: different TR-1 offsets imply contradictory results

**Quote:** `manuscript.md:248`: “50.34% at a 770.65 bp mean boundary offset”.

**Positive counterevidence:** :250 separates raw-call 770.65 bp from coordinate-merged 4,282 bp; :256 identifies banded TR-1 as 7,973.15 bp and the 4,265.30 bp value as knob180. Methods :92 defines the populations and equally weighted outer-boundary statistic. **Check:** R1. **Replacement:** retain existing text. This preserves the resolved quarantine §6.12 correction.

### P4-R2 — REJECTED: matched/native counts or coarse precision need harmonising

**Quote:** `manuscript.md:139`: “a native `--max-period 100` rerun ... gives 3,993,151 regions”; the comparison row at :144 contains 3,911,182. The ellipsis separates quoted fragments.

**Positive counterevidence:** :139 distinguishes native rerunning from filtering the full-range execution; :162 scopes Table 1d to native runs. :86 authorises source-limited precision, :250 explains one-decimal calls-per-array, and :520 preserves six one-decimal cells. **Check:** R2. **Replacement:** retain these distinctions and existing precision. No artificial digits or new recall difference.

### P4-R3 — REJECTED: “index-based approach” necessarily asserts a measured causal advantage

**Quote:** `manuscript.md:188`: “Runtime on satellite-dense sequence is where the index-based approach separates”.

**Positive counterevidence:** The same paragraph labels the costs as not range-matched and states the tantan exception. :111 says the paired measurement “does not isolate the index’s contribution”; :344 expressly denies identification of the mechanism behind the cost inversion. “Index-based” can classify the approach without attributing the contrast to the index. **Check:** R3. **Replacement:** no mandatory correction. During later shortening, retain the causal disclaimer rather than strengthening this descriptive label. The retained title is not reopened.

### Rerunnable cheap checks

From the remote repository root, set `PY=/data/gpfs/assoc/pgl/bin/conda/conda_envs/bwtandem/bin/python`. The Python block below can be extracted and executed with that interpreter; it reads manuscript text only and prints identifiers rather than paragraphs. After author edits, obtain the baseline text with `git show 64964e1:manuscript.md` instead of the working-file read. These checks reproduce the positive text comparisons, not raw-data validation.

```python
from pathlib import Path
m = Path("manuscript.md").read_text().splitlines()
checks = {
"C1": [(32,"5.22 h, 5.51 h and 5.48 h"),(228,"5.22"),(260,"5.51"),(308,"5.48"),(510,"6/500/200")],
"C2": [(83,"Genome Assemblies"),(85,"Evaluation Metrics"),(247,"Satellite Array Detection"),(351,"Future directions"),(201,"fragmentation in Section 4.5"),(543,"fragmentation in Section 4.5")],
"C3": [(194,"25 calls in the band rather than 1,380"),(82,"from 1,380 to 1,533"),(208,"1,533")],
"C4": [(82,"competitor rows retain GNU-time"),(80,"carry accounting values like the BWTandem rows"),(358,"exception")],
"C5": [(86,"809,886"),(121,"does not make this a population-weighted estimate"),(350,"extrapolated to the population")],
"C6": [(300,"It establishes that over-calling"),(300,"we did not classify the called sequence by family")],
"C7": [(350,"No figure here depends on the affected path"),(350,"weaker than a general guarantee"),(490,"compiled Cython/C accelerators")],
"R1": [(92,"equally weighted mean across detected arrays"),(250,"4,282 bp"),(256,"7,973.15 bp for TR-1")],
"R2": [(139,"3,993,151 regions"),(144,"3,911,182"),(520,"six entropy-threshold and period-composition cells retain")],
"R3": [(188,"not a range-matched comparison"),(111,"does not isolate"),(344,"does not identify")]
}
for key, pairs in checks.items():
    for line, text in pairs:
        assert text in m[line-1], (key,line,text)
    print(key,"OK",[line for line,_ in pairs])
assert m[542].count("Section 2.2.2") == 4
print("S4 wrong-destination occurrences: 4")
fig = Path("results/figures/paper_figs/plot_fig2_range_cost.py").read_text().splitlines()
assert "the competitor FASTA carries 3.92% more sequence" in fig[85]
assert "plt.figtext" in fig[89]
assert "the 2026 inputs match BWTandem" in m[108]
for name in ("fig2_range_cost.png", "rendered/fig2_range_cost.png"):
    assert (Path("results/figures/paper_figs") / name).is_file()
print("C8 OK: source caption, target caption, image paths")
```

## REHASH REQUIRED

None. No `results/` file was changed.

## Not fixed and why

All confirmed items are proposed changes only: the parent session applies verified author-level fixes. Abstract restructuring, Application Note conversion, figure relabelling, release/tag/DOI work and ledger updates are subsequent tasks. Existing provenance limitations remain disclosures, not invented findings. Historical retractions, adverse banded results, incomplete visual-audit provenance and source-limited precision must survive conversion. Only this report was written.
