# Lab DOCX formatter

**Publication gate:** save/review this toolkit in the lab wiki **before generating any project manuscript Word files**. The formatter does not publish itself or invoke Pandoc. Tests use synthetic XML and in-memory ZIP archives, not manuscript files.

## Files and verification

- `lab_docx.py`: standalone CLI/library; tested on Python 3.11 with `lxml` 5.3.2 and PyMuPDF 1.24.14.
- `test_lab_docx.py`: standard-library `unittest` tests with synthetic fixtures.

```sh
python -m unittest discover -s paper-format/lab-docx -v
```

After the wiki-saving gate is satisfied, format a Pandoc-produced DOCX:

```sh
python lab_docx.py input.docx --out styled.docx \
  --species 'Arabidopsis thaliana' --species 'Zea mays'
```

Omit `--out` for atomic in-place replacement. `--species` is repeatable, case-sensitive, exact-name matching with word boundaries; it never infers binomials. `--photosynthesis` optionally subscripts only the digit in standalone `C3`/`C4` in prose, excluding code and bibliography sections/styles. It is off by default and is not needed for BWT. Original emphasis/subscripts remain intact; omitting an option later does not undo prior intentional formatting.

Library API: `output_bytes, warnings = format_bytes(input_bytes, species=(), photosynthesis=False)`. A `FormatError` means no output should be used. The CLI computes everything before writing an atomic temporary replacement; failure does not replace the target.

## Applied style

- Times New Roman in all four font variants and style/default run definitions; theme-font/color overrides removed. Body point sizes and existing emphasis are preserved. Heading styles and heading runs are bold black.
- First eligible prose paragraph after a heading is flush; later prose gets 18 pt first-line indentation and left alignment. Captions, titles, `Author`/`Affiliation`/`Correspondence` styles, lists, code, and tables do not consume the first-prose position. `Table Note` styles and `Abbreviations:` paragraphs have zero first-line indent and zero before/after spacing. Existing left/right prose indentation is retained.
- Caption titles beginning with Table/Figure/Fig. or Supplementary equivalents are black; explanatory legend text follows the normal red-callout/blue-citation rules. **Only the title is newly bolded**, not the explanation. Prefer Markdown `**Supplementary Table S1. Short title.**` followed by the normal-weight legend on the next source line (same Pandoc paragraph). The existing leading bold span defines the title. Without explicit bold markup, the fallback is the first sentence after the display label; abbreviations can make this ambiguous, so mark titles explicitly. Image-only paragraphs keep with the following caption; captions keep their lines together and stay with the next item. No paragraphs, blank notes, numbering, or display names are inserted or moved. A caption taller than a page still needs explicit source/layout revision.
- Table/figure display callouts, including `Supplementary Fig. S1`, are red `FF0000`; parenthetical author–year citations are light blue `3399FF`. Other text is black. Headings, caption titles and table headers stay black. Matching spans runs, italics, hyperlinks, and bookmarks. Display matches take color precedence if a citation parenthesis includes a display callout. This is a bounded English author–year grammar, not a bibliographic parser or numeric-citation formatter.
- Tables: fixed Arial 9 pt, existing body emphasis retained, bold centered repeating first row, left/top body cells, explicit `noWrap`, 3 pt cell margins on each side, fixed table/grid/cell widths. Only header top/bottom and final-row bottom rules remain; vertical/interior/diagonal rules and table/cell/paragraph/run shading/highlights are disabled.
- Documents containing tables must be single-section supplements: landscape A4, 15 mm margins. Header/footer distances are preserved. Table-free document geometry is untouched, so Pandoc portrait main manuscripts remain portrait.

## Preservation and supported scope

Only `word/document.xml` **and `word/styles.xml`** change (the latter is necessary for the requested style definitions). Every other ZIP member's uncompressed payload, member order/metadata, and archive comment are preserved. ZIP compressed streams are not promised byte-identical. Normalized XML parts are byte-idempotent when options are unchanged.

Paragraphs are never flattened or rebuilt. Simple text-only runs may be split with copied attributes and complete `rPr`; concatenated visible text is unchanged. Hyperlink relationship attributes, bookmarks, drawing nodes, field instructions/control nodes, and unrelated run children are retained. Drawings/tabs/field boundaries prevent matches across them. Simple-field result text can be styled without changing field instructions. A selective match that would require splitting a run containing non-text children fails closed.

Fail-closed scope includes merged/nested/floating/ragged/empty tables, table lists/code, unknown-width table content (drawings, fields, tabs, manual breaks, equations), explicit row heights, multi-column table sections, multiple table sections, tracked changes, content controls, text boxes, unknown paragraph wrappers, alternate content, strict OOXML namespaces, DTDs, signed packages, and duplicate ZIP members. This is a narrow Pandoc formatter, not a general Word-document repair tool. Non-document headers/footers/footnotes, including their direct formatting, are deliberately not rewritten.

## Width preflight is not a render proof

`noWrap` alone does not prevent overflow. Column minima use PyMuPDF text advances from fontconfig's Arial or its installed substitute (regular and bold), plus a 6% allowance and cell margins. When fontconfig is unavailable, PDF Helvetica is the fallback. Remaining page width is distributed deterministically. If summed minima exceed the 756.9 pt landscape text width, formatting fails with total/per-column required widths; it never wraps, shrinks fonts, truncates, or silently accepts that overflow. Long command cells should move to Methods/prose in the source.

These are available-font metrics, **not a guarantee that Word selects that same font**; they may reject text that another renderer could fit. Every table emits a warning to visually verify horizontal fit and row pagination in Word/LibreOffice with the intended fonts. Tall rows, substituted fonts, inherited unusual spacing, and complex scripts require particular care. Synthetic tests establish XML behavior and preservation, not rendered pagination or actual physical fit. Source dash/age edits and content moves belong in Markdown, not this formatter.
