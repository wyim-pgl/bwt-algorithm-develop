# Final Bioinformatics preflight — policy verified; submission not cleared

Checked 2026-09-10 against `ef98c03c8710dfb529d2cab0cbe7231080ab07f6` (`v0.9.0`). This is an internal technical/compliance check of the authors' own submission candidate, not journal peer review or an editorial decision. No manuscript, evidence, proof, tag, release or declaration was changed by this check.

## Official policy now accessible

The canonical [Bioinformatics author guidelines](https://academic.oup.com/bioinformatics/pages/author-guidelines) were obtained through ordinary Chrome access; the former URL redirects there. The earlier HTTP 403/CAPTCHA obstacle is therefore resolved for this check. See `policy-sources.json` for URLs and capture hashes. Full publisher pages are retained only in local research scratch, not reproduced here.

An Application Note may occupy **up to 4 pages**, with approximate examples of 2,600 words or 2,000 words plus one figure. These examples are not an explicit one-figure maximum. Initial submission is format-free; that does not dispense with article-type structure, accessibility, supporting-data or ethical requirements. The previous 200-word abstract / 500-words-per-figure working heuristics were **not verified journal rules** and must not be used to certify compliance.

## Verified preservation and bounded technical passes

- Main PDF: **3 pages**, 1,136 whitespace-delimited source words, 141-word abstract and 2 figures. Supplement: 45 PDF pages, 19 table blocks and 7 figures. Word counts are mechanical counts, not a journal certification.
- Current conversion validator passed: all 19 table blocks and the supplemental prose replay are preserved; figure receipts/input hashes passed.
- `submission/SHA256SUMS` and `results/manifest.sha256` passed. Focused guards: **43 passed, 1 skipped**. These were checks, not benchmark/scorer reruns.
- Existing CI [34532733719](https://github.com/wyim-pgl/bwt-algorithm/actions/runs/34532733719) remains successful for exactly `ef98c03`: native 220 tests, fallback parity 49 tests, plus wheel/CLI checks. It does not establish Docker-image validity or absence of the documented layout-dependent native regression.
- No off-page text/image geometry or broken image paths was found. Main figures/captions are visibly unclipped. DOCX CRC, media relationships and 19 supplemental tables passed inspection; **Word pagination was not inspected**.
- The public tag still points to `ef98c03`; release `386640503` remains a draft. No publication, DOI operation or archive-link edit occurred.

## Corrections identified, not applied

| ID | Priority | Location and evidence | Required/recommended action |
|---|---|---|---|
| F1 | Required structure | `manuscript.md:11–19`: five headings, Motivation and Results followed by three other headings. | [Application Note abstract instructions](https://academic.oup.com/bioinformatics/pages/author-guidelines#section-17-5) prescribe four headings: Summary; Availability and Implementation; Contact; Supplementary Information. Summary is 1–2 sentences. The current 141-word count does not cure this mismatch. Obtain author-written wording; no replacement abstract was drafted in this audit. |
| F2 | Required accessibility | `manuscript.md:71,75`: neither main legend is followed by an `Alt text:` description. Short Markdown image labels are not the requested submission text. | Add descriptions directly below both main legends, as required by the [figure-accessibility section](https://academic.oup.com/bioinformatics/pages/author-guidelines#section-17-10). The explicit mandate here concerns the **main article**; supplemental alt text is also advisable, but was not promoted into an unsupported all-nine mandatory rule. |
| F3 | Required data citation | `manuscript.md:51–65` has seven article references but no full dataset entries/identifiers; dataset identifiers/URLs appear only elsewhere in the supplement. | [Data Citation](https://academic.oup.com/bioinformatics/pages/author-guidelines#section-10-2) requires public underlying datasets to be fully referenced with accession numbers or unique identifiers. Add references for the actual assembly/catalog datasets and relevant deposited supporting data/software. A reference to an associated paper is not a substitute for identifying the dataset release. The project's future archive citation remains deferred with its DOI. |
| F4 | Proof correction | `supplementary.md:79,81` and elsewhere; PDF p8 visibly includes literal `##` in prose. There are **22 occurrences on 14 pages**. All seven images have an additional automatic Figure 1–7 numbering layer; five full legends are detached from their images, in one case pp26/29. | Correct heading parsing and figure/legend grouping; suppress the redundant automatic numbering while retaining intended Supplementary identifiers. Preserve all prose and every table cell. The existing preservation validator does not validate heading rendering or float placement. See `layout-report.md`, W3–W4. |
| F5 | Reviewer readability | Main PDF p3 / Supplementary Fig. 2: small annotations near **3.02 pt**, axis titles approximately **3.81–4.29 pt**, and two `1.77×` labels physically overlap. Figure 2C also has pale legend markers. | Improve typography and separate labels without moving/changing measured data; add clearer redundant visual cues. The linked accessibility guide recommends larger text and adequate contrast but acknowledges constraints. These are genuine readability concerns, **not a fabricated mandatory 8 pt rule or automatic rejection criterion**. See W2/W5. |

Main PDF columns are **82.68 mm**, whereas the LaTeX-specific instructions call for 86 mm. Its **171.69 mm** figures fit within the 178 mm double-column format; being narrower than 178 mm is not itself a figure violation. Format-free initial submission does not establish compliance with the requested LaTeX settings. Adjust column geometry before claiming journal-template/revision readiness and recheck pagination after all changes.

## Supporting-data access remains an open compliance question

The main manuscript contains a data/code availability statement (`manuscript.md:43–45`), satisfying statement presence. It also explicitly says that competitor BEDs and external inputs are not deposited. `supplementary.md:365` says that inherited competitor outputs are on manifest paths rather than in this repository and that original audit images, renderer/settings and the source-population BED are not deposited.

The journal's [Supporting Data](https://academic.oup.com/bioinformatics/pages/author-guidelines#section-6-4) and Software requirements call for publicly accessible supporting data/software. Local cluster paths and checksum declarations do not demonstrate a reader-accessible download route. Therefore **complete public supporting-data availability cannot be certified from this deposit**. Identify any existing public access routes, or resolve the deposit/claim boundary with the authors and, where necessary, the editor. Do not assume that disclosure alone waives the policy.

This is not a finding that the numbers are false. Verdict records and aggregate evidence survive; the missing artifacts and historical accounting limits were already disclosed. No unavailable data, reconstructed historical image, reader identity or numerical precision should be invented. No rerun or deposit was undertaken here.

## Author/editor decisions deliberately left until the final stage

These are recorded now, **not drafted, approved or acted on**:

1. **LLM-process compliance needs explicit resolution.** The OUP page permits correction, translation and consistency evaluation, but restricts drafting from prompts. Its linked [ISCB policy](https://transition.iscb.org/iscb-policy-statements/iscb-policy-for-acceptable-use-of-large-language-models), updated 3 April 2025, more broadly restricts drafting paper sections. Previous assistant work substantially condensed/reworded the supplied long manuscript and reconstructed the Abstract; it cannot honestly be characterized as only spelling correction. The precise classification of this source-based transformation requires author/editor judgment; this audit does not label misconduct or certify acceptability. Seek editorial clarification or author-led writing as appropriate. A disclosure does not automatically make a prohibited use permissible. No further paper prose was generated in this audit.
2. Confirm Funding, COI, CRediT, ORCID/submitting-author requirements, appropriate AI-use details and final scientific approval. Applicable AI disclosure locations include the cover letter, Methods/Acknowledgements and supplementary details, but no declaration was composed here.
3. A **cover letter is mandatory**; no cover-letter-like tracked file was found in this package. An author may have one elsewhere. Prepare/confirm it at the final author stage rather than representing the existing release notes as a cover letter.
4. Confirm the software maintenance undertaking, archive creator/license metadata, and final figure/manuscript approval.
5. Perform the separately authorized Zenodo integration/publication/DOI and archive-URL work last. Preserve the public `v0.9.0` target; later DOI/manuscript edits require their own snapshot.

## Production and coverage limits

Initial inline review figures are allowed. Current main PDFs mix vectors with raster components; raster components measure approximately **794 / 704 ppi**, not simply their original export metadata. Do not impose raster DPI on vector text/paths. This is not certification of final TIFF/line-art production delivery. Two supplemental PNG components are approximately 339 ppi at their large landscape placement; confirm final delivery format/resolution when required.

Clipped legacy caption text remains extractable from some PDF content streams even though it is not visibly printed. Do not mistake it for visible overprinting; nevertheless, clean the final accessible/searchable presentation assets rather than treating a visual crop as removal of the underlying text. Preserve original evidence figures separately.

All three main pages were visually checked. Supplement coverage was all-page geometry/text/image inspection plus visual checks on selected pages (8, 13, 19, 29), not a visual reading of every page. All 19 table blocks were mechanically compared; no new independent re-scoring or complete scientific peer review was performed. Existing source-limited operands, missing evidence and the unresolved native-layout issue remain open exactly as disclosed.

**Disposition:** policy lookup completed; preservation checks passed; F1–F5 and the stated access/author gates mean that the candidate is **not yet cleared for submission**. The manuscript and release remain frozen pending separately approved corrections.
