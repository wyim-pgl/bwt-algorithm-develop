# Final-check F1–F5 corrections (2026-09-10, author-instructed)

Author instruction (2026-09-10): implement the five outstanding items from
`docs/2026-09-10-final-check/` (F1 abstract structure, F2 alt text, F3 dataset
citations, F4 supplement rendering, F5 figure readability). Zenodo/DOI/abstract
archive URL, author declarations and the cover letter remain last-stage and were
not touched. `results/`, `manuscript_full.md`, the public `v0.9.0` tag and the
draft release were not modified.

## What changed

- **F1** `manuscript.md` abstract now has exactly the four prescribed headings
  (Summary; Availability and Implementation; Contact; Supplementary Information)
  with a two-sentence Summary (abstract 120 words). The Summary reuses the
  author-approved C-8 abstract sentences nearly verbatim (measured values,
  bounded-claim wording and all eight adverse-claim needles preserved;
  `check_conversion.py` now asserts the heading structure and sentence bound).
  The unresolved OUP/ISCB LLM-use policy gate is **not** resolved by this edit;
  final author confirmation of the exact wording remains open.
- **F2** An `**Alt text:**` description follows each main figure legend in
  `manuscript.md` and is printed below the caption in the PDF (`build.py`).
- **F3** Four dataset references with identifiers added (GRCh38
  GCA_000001405.15; adotto v1.2.1 Zenodo record 13987414; Col-CEN v1.2 with
  E-MTAB-10272/PRJEB46164; Mo17 GCA_022117705.1) and cited inline in §2. All
  identifiers were taken from the deposited supplement; none invented.
- **F4** 27 blank lines inserted before ATX headings in `supplementary.md`
  (mirrored in `check_conversion.py`'s `supplement_body`, which still replays
  the full body byte-for-byte from `manuscript_full.md`); supplement Pandoc
  call now uses `-f markdown-implicit_figures`. Result: 0 literal `##` (was 22),
  0 automatic "Figure N:" captions (was 7), 6/7 legends on the same page as
  their image; Supplementary Figure 5 is a full-page image with its legend at
  the top of the next page (was 3 pages apart). All 19 table blocks preserved.
- **F5** New `submission/render_main_figures.py` re-renders both main figures
  from the deposited scripts and CSVs (presentation only): seaborn font_scale
  2.0 (dense point labels 0.72 of that), the three range-ratio labels
  vertically separated (0 overlapping text spans measured in both PDFs, was a
  3.3 pt collision), TRF/TRASH lines/legend at alpha 0.55/1.0 with dark marker
  edges. `render-receipt.json` records input/output hashes and supersedes
  `accuracy-export-receipt.json` (removed) and the fig2 crop entry
  (`crop-receipt.json` regenerated with 5 entries). No data value, point or
  measured label text changed.

## Build environment (Pronghorn)

TeX Live 2019 + user-texmf `oup-authoring-template` v1.5 (2026/07/14) from CTAN
(`~/texmf/tex/latex/`; the class dropped `\authormark`, shimmed with
`\providecommand` in `build.py`); TeX Gyre fonts exposed via `~/.fonts` symlink;
pandoc 2.19.2 (`RNASeq_postanalysis` env); Python 3.11.15 `bwtandem` env with
seaborn 0.13.2 and user-site PyMuPDF 1.24.14. Proofs are therefore rebuilt with
class v1.5 rather than the earlier machine's class version; main PDF is still
3 pages. Journal-template column geometry (W1) remains a later, revision-stage
item; initial submission is format-free.

## Verification (2026-09-10)

- `check_conversion.py`: pass (19 table blocks, full prose replay, 2+7 figures,
  new abstract-structure and alt-text assertions).
- Guards: `pytest tests/test_deposit_hashes.py tests/test_env_var_docs.py
  tests/test_one_to_one_scoring.py -q` → **43 passed, 1 skipped**.
- `sha256sum -c submission/SHA256SUMS` → 18/18 OK (regenerated after adopting
  the rebuilt proofs).
- `git status/diff -- results/` → empty; `results/` untouched, no rehash needed.
- `git rev-parse 'v0.9.0^{}'` → `ef98c03…` unchanged.
- Figure measurements (PyMuPDF): 0 significantly overlapping text spans in both
  main-figure PDFs; ratio labels disjoint; effective axis/tick type ≥ ~5–7 pt
  at 171.7 mm print width (was 3.0–4.3 pt).

## Not done here

Zenodo integration, DOI, abstract archive URL, author declarations, cover
letter, LLM-policy resolution, journal-template geometry, and publishing the
draft release. The rebuilt proofs and the Summary wording await final author
approval; the draft GitHub release still carries the previous proof assets and
must not be updated under the frozen tag (a corrected release needs a new tag).


## Continuation corrections (author asked to continue)

- Figure 5 is now explicitly grouped with its unchanged full legend in a
  minipage with a 140 mm image-height cap; all seven complete legends are on
  their respective image pages. The earlier "was 3 pages apart" was inaccurate
  for Figure 5: that earlier gap concerned Figure S2.
- DOCX export also disables implicit figure numbering. ZIP/table validation
  does not establish Word pagination or tagged-PDF accessibility.
- Dataset metadata checked against retained official responses:
  `adotto-record.json` (https://zenodo.org/api/records/13987414),
  `mo17.xml` and `grch38.xml` (ENA browser API /xml/<accession>),
  `colcen-tree.json` and `colcen-v1.2.md` (Schatzlab GitHub repository).
  Adotto uses its sole registered creator Adam English, exact title and DOI.
  Mo17 uses its registered institutional depositor; Col-CEN identifies the
  distributing repository and exact version/file. Unknown dataset publication
  dates are n.d., not borrowed from associated papers. The provisional
  Chen/Naish dataset author-year entries above have therefore been replaced.
- `check_proofs.py` checks complete legend text on image pages (ignoring
  typographic punctuation for placement matching), literal headings and
  duplicate numbering, main page limit, alt text, DOCX CRC and table counts.
  Source replay independently checks exact preservation.
- Bounding-box overlap screening is a heuristic, not proof of complete figure
  readability. Smaller notes remain; accessibility compliance and author
  approval are not certified. Figure 5 was scaled down for grouping; measured
  data were not changed.
