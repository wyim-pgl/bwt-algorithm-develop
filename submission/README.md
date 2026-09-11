# BWTandem 0.9.0 — author-review submission candidate

**Not submitted, accepted, or DOI-archived.** The software release tag and the
final journal-submission record are distinct. Do not describe a draft GitHub
release or the repository homepage as a minted DOI or permanent archive.

## Files

- `../manuscript.md`: short Application Note source.
- `../manuscript_full.md`: immutable long source at `94df01e` (P4 + C-8).
- `../supplementary.md`: 18 uniquely numbered tables, with the former small identity-sweep table retained as numerical prose. Original payloads and the source migration are accounted for in `docs/2026-09-10-lab-docx/`.
- `manuscript.pdf`, `supplementary.pdf`: compiled author-review proofs.
- `manuscript.docx`, `supplementary.docx`: lab-style editable Word files, also rendered with LibreOffice for geometry, figure-caption and table-layout review. Microsoft Word itself was not run.
- `figures/`: presentation copies; original evidence files remain under results/.
- `SHA256SUMS`: exact PDF/DOCX and presentation-figure payload hashes.
- `RELEASE_NOTES.md`: draft release scope and known limitations.

## Rebuild and check

Use installed Pandoc, XeLaTeX/TeX Live (including `oup-authoring-template`),
TeX Gyre fonts and DejaVu fonts. No detector or evidence-environment changes
are required. The main proof uses OUP's authoring class with its misleading
"Published by OUP" placeholder copyright footer suppressed. The supplement
uses a landscape single-column layout for wide original tables. An empty
publisher-assigned article DOI field in the template is not a software DOI.

From the repository root:

```sh
python submission/build.py
# Inspect all warnings and the PDFs in submission/build/ before adopting outputs.
python docs/2026-09-10-appnote/check_conversion.py
sha256sum -c submission/SHA256SUMS
```

The committed PDFs/DOCX are frozen proof outputs, copied from `build/` after
inspection. Rebuilding changes PDF timestamps; update the payload checksum file
only after adopting a new proof. `build/` is ignored. To reproduce presentation
copies, `prepare_figures.py` needs PyMuPDF; both main figures are re-rendered
for print readability (final-check F5) by `render_main_figures.py`, which must
use the `bwtandem` environment with the existing plotting dependencies:

```sh
python submission/prepare_figures.py
/data/gpfs/assoc/pgl/bin/conda/conda_envs/bwtandem/bin/python submission/render_main_figures.py
```

Neither command edits results/ or reruns a scorer. The renderer runs the
deposited plotting scripts on the deposited CSVs and changes presentation only
(type size, label spacing, marker contrast); `render-receipt.json` records the
input and output hashes and supersedes the former accuracy-export receipt and
the fig2 crop entry.

## Release / DOI gates

The repository is public and GitHub release-write permission was verified.
No Zenodo token was configured locally or on Pronghorn, and no repository
webhook was configured at the pre-release check. Therefore no DOI was reserved,
minted, or added to the abstract. The planned release is a **draft** on the
existing annotated `v0.9.0` tag, after branch CI passes on that exact commit.
No Docker image or PyPI package was built/published as part of this preparation.
Changing the Docker label does not validate the image build.

1. The owner enables `wyim-pgl/bwt-algorithm` in Zenodo's GitHub integration and
   verifies archive metadata (especially software creators and license).
2. Publish the draft release once, then verify the actual Zenodo record and DOI;
   or reserve a DOI in an authorized Zenodo deposit before finalizing an archive.
   Never infer successful DOI creation from a GitHub release alone.
3. Add the verified software archive URL to the abstract's Availability field
   and `doi` to CITATION.cff as appropriate; rebuild and rehash the manuscript
   proofs. A post-archive manuscript-only commit is a new submission snapshot;
   do **not** move or overwrite a public software tag to conceal the difference.
4. Record the final submission snapshot separately, after author approval.

## Author confirmations still needed

- Funding and conflicts of interest: absent from the source; no negative
  declaration or grant number has been invented.
- Author contributions / CRediT: roles have not been assigned by the assistant.
- AI-use disclosure: AI-assisted consistency checking, language editing and
  format conversion occurred. Confirm the venue's required disclosure and the
  authors' final review; do not claim that final author review has already occurred.
- Current Bioinformatics requirements: official guideline retrieval was completed in `docs/2026-09-10-final-check/`; the earlier HTTP 403 obstacle is historical. Final policy/author gates remain separate from these formatting checks.
- Final figures, PDF/DOCX presentation and scientific wording.

These gates block a claim of final submission readiness, not preservation of
the draft or a clearly labelled software/source snapshot.


## Lab-style Word tables (2026-09-10)

`build.py` uses `submission/lab-docx/lab_docx.py`, vendored from the version
recorded in `docs/2026-09-10-lab-docx/wiki-commit.txt` before Word generation.
This supersedes the earlier table-only `format_docx_tables.py` workflow.
Body text is Times New Roman; tables use Arial 9 pt, no-wrap columns, repeated
bold headers and three horizontal rules. Headings and caption titles are bold
black, display callouts red, and literature citations light blue. The
supplement uses landscape A4 with 15 mm margins. Long cells have explicit keyed
Methods destinations; no measurements were discarded. Plain Pandoc exports
remain in build/*-pandoc.docx for preservation/idempotence checks. Dependencies:
lxml 5.3.2 and PyMuPDF 1.24.14, with fontconfig metrics where available.

Run `python docs/2026-09-10-lab-docx/check_outputs.py` after building and
`python docs/2026-09-10-lab-docx/test_migration_guards.py` for negative tests.
The general lab specification is `submission/lab-docx/LAB_DOCX_STYLE.md`.
Evidence, limits and the display map are in `docs/2026-09-10-lab-docx/`.
