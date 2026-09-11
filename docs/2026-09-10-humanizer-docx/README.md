# Repeated English copyediting and lab-style DOCX tables

## Scope and skill installation

User requested repeated humanizer passes in Pi, Claude skill installation, and
DOCX table formatting using the PGL lab wiki. Both local and Pronghorn Claude
skill directories already existed, including references. No installation was
needed and no existing skill was overwritten. No Pi-registered humanizer was
found: Pi read the existing Claude skill files directly, rather than claiming
an unavailable Pi skill had run.

- `~/.claude/skills/humanizer_eng/SKILL.md` SHA256:
  `f6f2dc3bf40554311dd59cbbb6db7d9d7753ce97cc01f9986e2de60a042b1f72`
- `~/.claude/skills/humanizer_kor/SKILL.md` SHA256:
  `0fdfeb38d47c3fecc9adc1540394c1bde249ab3f7be025995ab13630030571ec`

Hashes match local and remote installations. Korean frontmatter is named
`humanize-writing`; preserved as installed. English manuscript uses only the
English rules. This is file/install verification, not a separate Claude runtime
invocation or proof of slash-command discovery.

## Humanizer execution

Three sequential inline reviews in Pi, same model, not independent reviewers:
1. Light surface/grammar copyediting: two replacements.
2. Terminology and reader navigation: two replacements.
3. Over-correction/meaning check: no further changes warranted.

`humanizer-passes.json` records exact replacements and per-pass hashes. Numbers,
URLs, abstract, references, legends and alt text remain unchanged. The locked
supplement and all table cells are unchanged. No blanket rewriting, scientific
claim strengthening, new facts, forced contractions, or detector-evasion
measurement. Earlier publisher LLM-policy/final-author-approval gates remain
open; this work does not certify journal compliance.

## DOCX style

Source: `/data/gpfs/assoc/pgl/wiki/paper-format/README.md`,
https://github.com/wyim-pgl/wiki/tree/main/paper-format . The wiki's three-line
rules were originally specified for XLSX; this is their requested DOCX
adaptation, not a claim that the wiki already supplies a DOCX table formatter.
The supplied `format_docx.py` operates on body paragraphs and reconstructs runs;
we did not apply it blindly to image/link-bearing paragraphs.

`submission/format_docx_tables.py` edits table formatting in document.xml only:
- Arial 9 pt, black; bold centred repeating header; left/top-aligned body.
- Header top and bottom plus final-row bottom rules; no vertical/interior
  rules, shading or conditional table styles.
- Wrapped cells, fixed column grid fitted proportionally to content length
  (weights clamped 10..60), total equal to writable width.
- Landscape A4/15 mm margins for the single-section supplement; no split rows.
- No run rebuilding, text replacement, or changes to media/relationships.
Main DOCX has no tables and is unchanged by this postprocessor. It remains
portrait. Body-font/reference-colour changes were not requested/applied.
The formatter rejects merged/nested/multiple-section table documents rather
than silently misformatting them. Very tall rows require manual layout review.

Build retains `submission/build/*-pandoc.docx` for independent pre/post tests.
Dependencies added to remote user site, not the evidence environment lock:
python-docx 1.1.2 and lxml 5.3.2 (the formatter itself uses lxml only).

## Checks and limits

`check_docx_tables.py` verifies all 19 tables: text/order/content preservation,
all other ZIP parts byte-identical (including images and relationships),
fields/bookmarks/hyperlinks preserved, borders/widths/fonts/header rules, and
idempotence. The formatter was corrected after a first idempotence failure
caused by header-property ordering; the regression now passes.

LibreOffice 5.3.6.1 rendered the DOCX into a separate review PDF (49 pages).
All-page text bounding boxes stayed inside page bounds; sample pages 20 and 48
were visually inspected for three-line rules and wrapping. This is not a full
visual inspection of all 19 tables or a Microsoft Word pagination check.
The regular submission PDFs remain the XeLaTeX proofs, not the LibreOffice
review export. No evidence, scientific numbers, frozen source, release assets,
public tag or DOI operation changed.
