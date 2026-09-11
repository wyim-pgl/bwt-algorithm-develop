## Finding

**The four numbers are compatible, but describe three scoring conditions and two repeat families.** In particular, **4,265 bp is knob180—not TR-1**. The current manuscript already explains raw-call versus coordinate-merged baselines (`manuscript.md:250`), while `quarantine.md §6.12` still says unresolved.

Read-only inspection completed on `pronghorn`, repository tip `139e361`; working tree remained clean. No scorers, intersections, benchmarks, or jobs were run.

Paths below are relative to `~/scratch/devel/bwt-algorithm` unless absolute.

## Exact mapping

Let **A** = `docs/2026-09-05-astra-review/pass3-maize.json` and **B** = `results/regen/maize_extra_evidence.json`.

| Manuscript value | Deposited value and exact key | Population and treatment |
|---|---|---|
| **771 bp** | A `["3B/BWTandem/TR-1"]["unfiltered"]["offset"]` = **770.65** | All **17 detected TR-1 arrays**; raw output calls directly overlapping each array; no period filter or additional coordinate merge. Coverage = **50.335993757089206%**. |
| **4.3 kb** | B `["coordinate_postmerge"]["TR-1"]["BWTandem"]["0"]["mean_offset_bp"]` = **4282** | Same **17 TR-1 arrays**, but first coordinate-merge all overlapping/touching calls chromosome-wide, then select merged intervals overlapping each array. No period filter. Deposited coverage = **50.34%**. |
| **4,265 bp** | A `["3B/BWTandem/knob180"]["banded"]["offset"]` = **4265.3** | All **25 detected knob180 arrays**; raw overlapping calls restricted to reported periods **100–500 bp inclusive**. Coverage = **64.20234882686118%**. |
| **7,973 bp** | A `["3B/BWTandem/TR-1"]["banded"]["offset"]` = **7973.15** | All **17 detected TR-1 arrays**; raw overlapping calls restricted to reported periods **100–500 bp inclusive**. Coverage = **17.326009710139918%**. |

Thus the supported two-decimal raw/banded values are **770.65, 4,265.30, and 7,973.15 bp**.

## Definition and generating code

### Common boundary statistic

`scripts/scoring/score_exp3.py:61–86`, specifically `array_metrics`, calculates, for each detected truth array \(i=[g_s,g_e)\):

\[
d_i=\frac{|g_s-\min_{(s,e)\in H_i}s|+|g_e-\max_{(s,e)\in H_i}e|}{2}.
\]

Here \(H_i\) contains intervals on the same chromosome with **positive overlap**, `max(gs,s) < min(ge,e)`. The reported statistic is the **equally weighted mean of \(d_i\) across detected arrays**, rounded to two decimals. All arrays are detected in these four cases.

It is **not** a per-call mean, median, signed error, length-weighted mean, or one-to-one interval match. Endpoints are not clipped to truth boundaries; under-extension and over-extension both contribute absolute error.

### Raw and banded results

- Original generator: `scripts/scoring/rescore_tables_3bc.py`
  - period parsing: **65–85**;
  - inclusive band selection: **88–91**;
  - raw offsets versus merged coverage: **121–127**;
  - knob180/TR-1 band specification: **134–151**.
- Period is integer BED column 5 if parseable; otherwise motif length from column 4. The regenerated BWTandem BED uses decimal copy counts in column 5, so the fallback supplies its reported motif length.
- Original surviving JSON:
  `/data/gpfs/assoc/pgl/devel/exp1_human/regen/maize_rescore/table3bc_results.json`
  - `["regen"]["3B"]["BWTandem"]["TR-1"]["unfiltered"]["offset"]`
  - `["regen"]["3B"]["BWTandem"]["knob180"]["banded"]["offset"]`
  - `["regen"]["3B"]["BWTandem"]["TR-1"]["banded"]["offset"]`

  I read these directly; they match A.
- Deposited table/provenance: `results/regen/table3bc_replacement.md` and `table3bc_provenance.json`.
- A’s independent artifact-check generator is `docs/2026-09-05-astra-review/pass3-checks.py:60–92`, which calls the same `metrics` function and reads the deposited gzip BED.

### Coordinate-merge result

`scripts/scoring/score_maize_regen_evidence.py:56–63, 148–168` merges chromosome-wide when `start - previous_end <= gap`, ignoring motifs. At gap zero this joins both overlaps and touching intervals. It then applies the same `array_metrics` function, but stores **`round(offset)`**, losing sub-bp precision.

Corroborating deposits:

- `results/regen/score_maize_regen.txt:43`: **4,282 bp**, 17/17 arrays.
- `results/figures/paper_figs/data/figS2_postmerge.csv:9`: **4282**, gap zero.
- B’s gap-2000 row gives **19,776 bp**, explaining the manuscript’s **19.8 kb** endpoint.

Equal coverage does **not** imply equal boundary offsets: overlap/touch merging preserves covered bases, while chains extending beyond an array can move merged outer endpoints beyond those of the raw calls directly intersecting it.

## Shared input provenance

Both original scoring deposits identify:

`/data/gpfs/assoc/pgl/devel/exp1_human/regen/regen_maize.bed`

SHA-256 recorded in both:
`e9729337017639d10956a53edf655f4fe3217209b6b7aa2eef2d5108faf3a8df`.

`results/regen/regen_maize.provenance.json` associates that output with commit `0363d8b`, native search range **1–2,000 bp**, tag `regen_maize_6124640`. The later check uses `results/beds/bwtandem_maize.bed.gz`.

Truth files are `results/ground_truth/mo17_tr1_arrays.bed` (**17 arrays; 5,899,812 bp**) and `mo17_knob180_arrays.bed` (**25 arrays; 29,655,996 bp**). Recorded truth hashes agree across original raw-call and postmerge provenance.

## Recommended replacement wording

> Across all 17 curated TR-1 arrays, unfiltered raw calls give 50.34% coverage and a mean absolute outer-boundary offset of 770.65 bp. Coordinate-only merging of overlapping or touching calls before scoring preserves coverage but increases the offset to approximately 4.28 kb because merged chains can extend beyond the directly overlapping raw calls. Restricting raw calls to reported periods of 100–500 bp gives offsets of 4,265.30 bp for knob180 (25 arrays) and 7,973.15 bp for TR-1 (17 arrays).

**Remaining limits:** the postmerge deposit preserves only integer-bp offsets; do not manufacture **4,282.00 bp** without recovering a higher-precision artifact or rescoring. No per-array contributions were examined, so specific arrays or chains responsible for the increase remain unidentified. Provenance hashes were read, not recomputed over the large BED.
