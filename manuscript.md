# BWTandem: FM-index seeding for wide-period-range tandem repeat detection in assembled genomes

Filip Ramazan and Won C. Yim

::: {custom-style="Affiliation"}
Department of Biochemistry and Molecular Biology\
University of Nevada, Reno\
Reno, NV 89557, USA
:::

Correspondence: wyim@unr.edu

## Abstract

**Summary:** BWTandem combines FM-index seeding, candidate refinement and supplementary periodicity scans to report motifs, periods, copy counts and purity across 1-2,000 bp in assembled genomes; in three paired human runs, widening the maximum period from 100 to 2,000 bp increased runtime 1.77-1.82 times (mean 1.79). Its contribution is wide-range structured output with non-leading shared-range accuracy: shared-output-band region recall was 78.87% against ULTRA's 81.62%, and a stratified single-reader audit supported only 4 of 400 calls absent from both the catalog and four original comparators; a causal speed advantage of the index was not demonstrated.

**Availability and Implementation:** MIT-licensed source and scoring scripts: https://github.com/wyim-pgl/bwt-algorithm. Benchmark configurations differ from defaults (Supplementary Methods S2).

**Contact:** wyim@unr.edu

**Supplementary Information:** Supplementary information accompanies this manuscript.

## 1 Introduction

Tandem repeats span short motifs and satellite monomers. Detectors such as TRF (Benson, 1999) and ULTRA (Olson and Wheeler, 2024) require period ceilings whose computational cost depends on the genome and implementation. BWTandem targets one broad pass over assembled genomes, with structured repeat records rather than accuracy leadership. longdust (Li and Li, 2026) reports low-complexity intervals without repeat units; AniAnn's (Sweeten et al., 2026) reports satellite boundaries and monomer lengths but not motif sequences, copy counts or purity. Both are included in our comparison, and their advantages remain explicit.

## 2 Implementation and evaluation

A chromosome-level FM-index supports short-motif enumeration and sampled-k-mer occurrence queries. Three overlapping detection tiers combine short-repeat scanning, longest-common-prefix analysis and sparse seeding with candidate refinement. Satellite gap filling and an optional catch-all pass use autocorrelation, not index queries. Reported performance reflects this complete pipeline; human and maize benchmarks enable the catch-all pass, whereas Arabidopsis does not. Supplementary Sections 2.1-2.2 and Methods S1-S2 specify gates, configurations and scoring.

Human evaluation uses the primary chromosomes of GRCh38, GenBank assembly GCA_000001405.15 (Genome Reference Consortium, 2013), and release v1.2.1 of the adotto variable-repeat catalog (English et al., 2024; dataset English, 2024a). Plant evaluation uses Col-CEN v1.2 (Naish et al., 2021; dataset Schatzlab, n.d.) and maize Mo17, GenBank assembly GCA_022117705.1 (Chen et al., 2023; dataset China Agriculture University, n.d.). Human region recovery requires one-base overlap. Reciprocal-overlap and one-to-one sensitivity analyses are provided in the supplement. Catalog precision is not precision against all genomic repeats. Output-period filtering matches the human comparison band, not execution ranges. Historical competitors processed additional sequences; memory measurements mix sampled cgroup peaks and GNU-time maxima. These observations do not establish matched cross-tool speedups. Human operating points and the Arabidopsis catch-all choice were selected using their evaluation truth sets; these are in-sample comparisons, and competitors did not receive an equivalent tuning search. All tables, original identifiers, detailed caveats and source links are retained in the supplement.

Parameter limits, execution configurations and competitor versions are specified for reproducing the benchmark settings (Supplementary Tables S13-S15).

## 3 Results and limitations

Three paired four-worker human runs at execution commit `0363d8b` changed only the maximum period, from 100 to 2,000 bp. Runtime ratios were 1.77-1.82, with a mean of 1.79 (Fig. 1; Supplementary Fig. S1). Two replicates shared a node. This is a sublinear response over two measured ceilings, not an asymptotic bound. The earlier 1.30-1.41 estimate is superseded: its narrow arm still searched and discarded long-period candidates. A historical Tier-2/3 lookup substitution changed Arabidopsis runtime by 5.56% without changing output, but retained the index; it was not an index-free pipeline ablation.

At the shared ≤100 bp output band, ULTRA had 81.62% region recall and BWTandem 78.87%; ULTRA remained ahead under both reciprocal-overlap rules (Fig. 2; Supplementary Fig. S4; Supplementary Table S2). BWTandem's permissive native-period-100 setting reached 81.60% recall at 48.44% precision, versus ULTRA's 53.66% precision. BWTandem's full-range two-worker run required 12.65 h and 28.08 GiB, distinct from the four-worker paired measurements. No claim of superior shared-range accuracy follows.

A blinded, single-reader audit of 400 stratified BWTandem calls overlapping neither adotto nor TRF, ULTRA, tantan or TRASH returned 4 supported, 346 unsupported and 50 unsure. Equal sampling by period stratum is not a population-weighted estimate. Unmatched-call counts therefore do not demonstrate additional true repeats. Images, rendering settings and a separate reader attestation are missing from the deposit; the verdict records survive.

On Col-CEN, BWTandem overlapped 99.72% of conserved CEN180 reference monomers by at least one base without a call-period filter, falling to 94.68% when calls were restricted to 150-400 bp (Supplementary Table S6 and Section 3.2). tantan's 500 bp-window rerun recovered 99.24% with higher base-pair precision and lower observed cost, although its shared-node timing and narrower search range were not matched to BWTandem. On maize CentC, AniAnn's covered 81.42%, versus BWTandem's 58.55%, with coarser boundaries. BWTandem's period-filtered coverage losses were 15.59, 33.01 and 17.84 percentage points for knob180, TR-1 and CentC. Detection and correct period assignment are different tasks.

Fragmentation, over-calling, missing historical provenance and a still-unresolved layout-dependent native regression test limit deployment claims. The benchmark does not validate all reported motif structures or establish broad generalization to unseen genomes. BWTandem offers wide-range candidate records for downstream validation, not a replacement for that validation.

Full-range human results, the shared ≤100 bp comparison and the 101-2,000 bp stratum describe different output ranges (Supplementary Tables S1-S3). Native-period-100 operating points show the recall-precision trade-off, while cross-caller support rates depend on the corroboration rule (Supplementary Tables S4 and S5). The ULTRA, BWTandem and tantan recall ordering persists across chromosome-subset checks of post-filtered full-range output (Supplementary Fig. S2). Unmatched and shared calls differ in length and motif entropy; these properties do not validate unmatched calls (Supplementary Table S16). Strict one-to-one scores depend on whether matching uses padded regions or annotation coordinates (Supplementary Tables S17 and S18).

The single-reader audit supported few calls absent from both the catalog and the original comparators (Supplementary Fig. S3). Maize microsatellite counts depend on whether the same period rule is applied to every tool (Supplementary Tables S7 and S8). Satellite coverage, boundary offsets and filtering losses differ across knob180, TR-1 and CentC (Supplementary Tables S9-S12; Supplementary Fig. S5). Coordinate-only merging provides a separate boundary and fragmentation diagnostic (Supplementary Fig. S6). Selected k-mer self-similarity and dot-plot examples illustrate repeat structure without independently validating the reported motifs (Supplementary Fig. S7).

In the full-range identity sweep, region recall/precision were 62.59%/54.72% with the catch-all pass disabled, 71.36%/53.42% at identity 0.80, 71.53%/53.35% at 0.76, 80.53%/50.50% at 0.72 and 81.46%/48.92% at 0.68. These in-sample results informed the operating-point selection (Supplementary Section S2).

## Data and code availability

Source code, scorers, regenerated BWTandem BEDs and hashed evidence are in the repository linked above. Execution commit `0363d8b` identifies regenerated benchmark code; the later submission release does not constitute a benchmark rerun. Competitor BEDs and several external inputs are not deposited. The supplement preserves the full evidence/provenance limitations and corrected strict one-to-one panels.

## Acknowledgments

The authors acknowledge Research & Innovation and the Cyberinfrastructure Team in the Office of Information Technology at the University of Nevada, Reno for access to computing resources.

## References

Benson G. (1999) Tandem repeats finder: a program to analyze DNA sequences. *Nucleic Acids Res.*, 27, 573-580.

Chen J. et al. (2023) A complete telomere-to-telomere assembly of the maize genome. *Nat. Genet.*, 55, 1221-1231.

China Agriculture University (n.d.) Zm-Mo17-REFERENCE-CAU-T2T-assembly assembly for *Zea mays* (dataset). GenBank/ENA assembly accession GCA_022117705.1. https://www.ebi.ac.uk/ena/browser/view/GCA_022117705.1

English A.C. et al. (2024) Analysis and benchmarking of small and large genomic variants across tandem repeats. *Nat. Biotechnol.*, published online 26 April 2024; 43, 431-442 (2025).

English A. (2024a) Project Adotto Tandem-Repeat Regions and Annotations, v1.2.1 (dataset). Zenodo. https://doi.org/10.5281/zenodo.13987414

Genome Reference Consortium (2013) GRCh38 human reference genome assembly (dataset). GenBank assembly accession GCA_000001405.15. https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_000001405.15/

Li H. and Li B. (2026) Finding low-complexity DNA sequences with longdust. *Bioinformatics*, 42, btag112.

Naish M. et al. (2021) The genetic and epigenetic landscape of the Arabidopsis centromeres. *Science*, 374, eabi7489.

Schatzlab (n.d.) Col-CEN v1.2 genome assembly (dataset), Col-CEN_v1.2.fasta.gz. GitHub. https://github.com/schatzlab/Col-CEN/tree/main/v1.2

Olson D.R. and Wheeler T.J. (2024) ULTRA-effective labeling of tandem repeats in genomic sequence. *Bioinform. Adv.*, 4, vbae149.

Sweeten A. et al. (2026) AniAnn's: alignment-free annotation of tandem repeat arrays using fast average nucleotide identity estimates. *Bioinformatics*, btag581, advance access.

## Figure legends

![Paired range cost and separate cross-tool observations](submission/figures/fig2_range_cost.png)

**Fig. 1.** Paired human range cost (A); separate maize runtime (B) and human core-hour/memory observations (C). Cross-tool ranges, FASTA scopes and memory accounting differ. The full caption is retained (Supplementary Fig. S1).

**Alt text:** Three-panel chart. Panel A is a slope chart of three paired human runs: runtime rises from about 4 hours at a 100 bp maximum period to 7.1-7.3 hours at 2,000 bp, with the per-replicate ratios 1.77-1.82 labelled beside the endpoints. Panel B shows observed ULTRA and TRF maize runtimes rising with the maximum period on log-log axes. Panel C shows dot plots of per-tool human core-hours and peak memory, each point labelled with its period cap; ranges and inputs are not matched across tools.

![Accuracy trade-offs and overlap-rule sensitivity](submission/figures/fig1_accuracy_tradeoff.png)

**Fig. 2.** Native-period-100 operating points (A-B) and reciprocal-overlap sensitivity of post-filtered full-range output (C). The 2026 points in A-B are full-range, not band-matched. The full caption is retained (Supplementary Fig. S4).

**Alt text:** Three-panel chart. Panels A and B plot region-level and base-pair precision against recall on GRCh38: BWTandem's four operating points P, B, F and H form a connected line whose precision falls as recall rises, and each competing tool is a single labelled point. Panel C plots region recall at periods of 100 bp or less under the one-base, reciprocal-0.25 and reciprocal-0.50 overlap rules; every tool's recall falls under the stricter rules, with ULTRA highest and BWTandem second throughout.
