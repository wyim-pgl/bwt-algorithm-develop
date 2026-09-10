# Application Note conversion: author-draft fidelity check

Read the entire new `manuscript.md`, checked its numeric/scientific claims against targeted passages in `manuscript_full.md`, and inspected both main figures and their supplementary mappings. This is a source-fidelity check, not a peer-review panel or raw-result audit. Five local wording/caveat issues follow.

## 1. Identify the audit's actual comparator population

**Exact quotes:** Abstract: “calls absent from both the catalog and other callers.” Results: “400 stratified BWTandem calls absent from both adotto and the other callers”.

**Source evidence:** `manuscript_full.md`, Section 2.2.3, line 86, defines the sampled population as “809,886 regenerated full-range calls overlapping neither the catalog nor any of TRF, ULTRA, tantan or TRASH”. Section 2.2.4, line 99, separately introduces longdust and AniAnn's. They are not part of this audit exclusion rule.

**Issue:** The shortened Introduction prominently includes the two 2026 tools, so “the other callers” can now imply absence from those tools too. The numbers themselves are preserved correctly.

**Minimal replacement:** In the Results, use “400 stratified BWTandem calls overlapping neither adotto nor TRF, ULTRA, tantan or TRASH”. In the Abstract, replace “other callers” with “four original comparators”.

## 2. Restore the in-sample selection qualification

**Exact quote:** “BWTandem's permissive native-period-100 setting reached 81.60% recall at 48.44% precision, versus ULTRA's 53.66% precision.”

**Source evidence:** `manuscript_full.md`, Section 2.2.3, line 94: “Every operating point reported here is therefore a post-selection, in-sample choice rather than a prospectively defined sweep”. The same paragraph states that competitors did not receive an equivalent search. Supplementary Table S3, line 533, says the identity threshold was selected against the same adotto catalog. Supplementary Methods S2, line 504, likewise identifies the Arabidopsis catch-all choice as in-sample selection on the CEN180 evaluation truth.

**Issue:** Neither the main text nor its figure caption currently identifies selection on the evaluation data. “Does not ... establish broad generalization” is a different, weaker qualification; readers could still interpret these operating points as prospectively fixed tests.

**Minimal addition** in Implementation and evaluation: “Human operating points and the Arabidopsis catch-all choice were selected using their evaluation truth sets; these are in-sample comparisons (Supplementary Section 2.2.3 and Methods S2).”

## 3. Make the CEN180 recovery criterion explicit

**Exact quote:** “On Col-CEN, BWTandem recovered 99.72% of conserved CEN180 monomers without a call-period filter, falling to 94.68% within 150–400 bp”.

**Source evidence:** `manuscript_full.md`, Table 2 caption, line 201: “Monomer recall counts a monomer as recovered on a single base pair of overlap with the tool's merged intervals”. Section 2.2.3, line 90, defines the conserved BLAST-derived truth subset and excludes monomers below 80% identity to the consensus.

**Issue:** The new Methods explicitly assigns one-base overlap to *human* recovery only. Thus the plant sentence can be read as recovery of complete monomers, rather than intersection with their coordinates. “Conserved” correctly preserves the population limitation but not the recovery rule.

**Minimal replacement:** “On Col-CEN, BWTandem overlapped 99.72% of conserved CEN180 reference monomers by at least one base without a call-period filter, falling to 94.68% when calls were restricted to 150–400 bp”.

## 4. Retain the condition specific to tantan's observed cost

**Exact quote:** “Widened-window tantan recovered 99.24% with lower observed cost and higher base-pair precision.”

**Source evidence:** `manuscript_full.md`, Section 3.2, line 188: “The tantan runtime was measured on a shared node under a different period ceiling”. Table 2's caption, line 201, identifies the 500 bp window and explicitly cautions against treating its runtime/memory cells as comparable with the other rows. BWTandem searched 1–2,000 bp.

**Issue:** “Observed” avoids a universal speed claim, but omits the specific unmatched-range/shared-node conditions attached to this direct comparison. The main Methods' human scope and mixed-memory caveats do not identify these conditions.

**Minimal replacement:** “tantan's 500 bp-window rerun recovered 99.24% with higher base-pair precision and lower observed cost, although its shared-node timing and narrower search range were not matched to BWTandem.”

## 5. Do not imply a missing independent reader

**Exact quote:** “Images, rendering settings and an independent reader attestation are missing from the deposit”.

**Source evidence:** `manuscript_full.md`, Data and Code Availability, line 356: “The source population BED and a separate reader attestation are also not deposited”. Section 2.2.3, line 86, identifies the completed reading as one author's single-reader audit, not an independently completed second reading.

**Minimal replacement:** Replace “an independent reader attestation” with “a separate reader attestation”.

## No issue found in the remaining checked conversion claims

The quoted numerical results match their source populations/configurations once the above wording is clarified. The historical 5.56% substitution, superseded range-cost estimate, current four-worker paired runs and separate two-worker whole-genome cost are not conflated. No new causal speed or accuracy-leadership claim was found. Retained author–year citations agree with the long-version references, including English's online/publication-year distinction. Figure mapping is correct: main Fig. 1 = old/supplementary Figure 2 (range cost); main Fig. 2 = old/supplementary Figure 1 (accuracy). This check does not establish submission readiness; DOI availability and author funding/COI declarations remain unresolved as specified.

## Parent disposition (2026-09-10)

All five suggestions were applied to the short manuscript, without changing
any numerical result or the frozen long source. The final short text names
the four original audit comparators, discloses in-sample selection and unequal
tuning, states the one-base CEN180 criterion and tantan's unmatched/shared-node
conditions, and uses “separate reader attestation”. String checks confirmed
these changes before rebuilding the proofs. This is an implementation record,
not a claim that the reviewer reread the final version. Final counts are in
`document-checks.json`: 1,136 whitespace-delimited words, 141 abstract words,
three main PDF pages and 45 supplementary pages.
