# PGL lab manuscript and DOCX style

Updated from the author's explicit requirements on 2026-09-10. This is a lab
house style, not a certification of any journal's current instructions. A
mandatory journal template overrides conflicting layout choices; record the
exception. Preserve all evidence and identify unresolved author/publisher gates.

## Required order

1. Freeze the input revision and inventory manuscript, physical tables, figures,
   citations, commands, species and abbreviations.
2. Install/review requested humanizer skills from pinned sources. Enumerate what
   the active runtime actually discovers. Read each applicable skill and run
   its review on the prose; log edits and justified no-op passes. Language-
   specific rules apply only to the corresponding language. These are writing
   checklists, not detector-evasion tools or independent scientific reviewers.
3. Approve a display migration map. Give every physical table its own number.
   Convert a genuinely small table to explicit numerical prose if that reads
   better. Move long command/configuration strings into keyed Methods text;
   retain every string, unit, count and caveat. Remove columns only after their
   necessary information is preserved elsewhere and the disposition is logged.
4. Put a finding-first callout for EVERY table and figure, including supplements,
   in the narrative manuscript. Captions alone do not satisfy coverage. Verify
   callouts and destinations in both directions after renumbering.
5. Apply approved source edits and validate content preservation. Save the
   reusable style specification, formatter, tests and version to the lab wiki
   BEFORE generating the manuscript Word files. Keep project-specific data and
   prose migrations in the project, not in the generic formatter.
6. Generate DOCX, apply the pinned toolkit, compare content/media/relationships,
   render in Word or LibreOffice, inspect the full display set, and record
   actual renderer/version and unresolved pagination limits. Hash outputs last.

## Prose and citation rules

- State the finding, followed by the display callout at sentence end:
  `PEPC transcript abundance peaked at dusk (Fig. 4).`
  A figure/table is not the grammatical subject of a finding sentence.
  Direct references are acceptable for administrative material without a
  scientific claim, such as accession lists or primer sequences.
- Use parenthetical, information-prominent literature citations by default.
  Narrative author citation is appropriate for a disputed interpretation,
  explicit method/framework credit, or historical review narrative.
- Combined callouts put displays before literature, separated by a semicolon:
  `(Fig. 3; Smith et al., 2020)`.
- Keep parentheses concise. Place species, sample counts, repository details
  and explanatory narrative in the sentence, not inside a citation bundle.
  Introduce a URL separately rather than attaching counts and several Methods
  locations to it in one parenthesis. Avoid `as shown in` and `data not shown`.
- Use ordinary hyphens for numeric ranges and compounds, and grammatical
  punctuation in place of em/en dashes. Protect command flags, URLs, paths,
  quoted source titles and mathematical minus/inequality semantics.
- `Mya` denotes an age in millions of years; replace `Ma` only in this temporal
  context, not within identifiers, words, quoted titles or other units.
- Write scientific binomials in true italics. Use a confirmed species lexicon;
  format only the names, not accompanying citations. Markdown delimiters must
  not appear literally in the final document.
- In photosynthesis contexts, C3/C4 have subscript digits. Do not silently
  reinterpret unrelated C3/C4 IDs (complement proteins, labels, code).
- Humanizer suggestions to remove contrast or caveats never authorize removing
  supported negative findings, uncertainty, invalidated-result explanations,
  provenance limitations, or disclosure. Preserve scholarly register.

## Word body and captions

- Body: Times New Roman, black. Set all script-specific font variants and styles.
- Headings: bold, black, no first-line indent.
- First eligible prose paragraph after a heading: flush. Later prose paragraphs:
  18 pt first-line indent (not a literal tab character). Titles, affiliations,
  captions, lists, code and tables are excluded from this paragraph rule.
- Author affiliation: separate department, institution, and location onto lines
  without changing the affiliation wording.
- Table/figure callouts: red `FF0000`, including supplementary references.
- Literature citations: light blue `3399FF`. Preserve species italics within
  or beside a reference without merging species and citation into one bundle.
- Table titles: bold. Keep captions distinct from text callouts; titles/headings
  remain black. Footnotes are contiguous with no blank spacer paragraphs; merge
  meaningful extra notes into the annotations and remove only true redundancy.

## Word tables

- Arial 9 pt. Header bold/centred; body left/top aligned. Preserve intentional
  italics and other meaningful emphasis.
- Three rules: top of first header row; bottom of last header row; bottom of
  final data row. No vertical or interior horizontal rules, no shading.
- Repeat header rows at page breaks. Keep ordinary data rows intact.
- No column/cell wrapping. Fit fixed column widths to available page width;
  shorten headings with explicit abbreviation definitions. Relocate long prose,
  commands or configuration strings before rendering rather than hide overflow
  or make fonts illegibly small. `w:noWrap` alone is not proof of visible fit.
- Use landscape pages when needed. Merged, nested or multi-header tables require
  explicit support and tests; fail closed if unsupported. Do not merge two
  unrelated physical tables under a single display number.

## Validation contract

- Every original table row/cell and moved string has a declared destination;
  preserve order, signs, units, meanings, captions, footnotes and caveats.
- Structural edits replay from immutable source plus approved edits. A changed
  validator must retain independent cell/command checks and negative tests.
- Verify figure/table identity, one caption per item, full main-body coverage,
  correct callout order, and no stale or orphaned IDs.
- DOCX tests cover fonts, colours, indentation, real italics/subscripts, borders,
  no-wrap, cell/grid widths, repeated headers, hyperlinks/fields/bookmarks/media,
  ZIP integrity and idempotence. The formatter must not rebuild whole paragraphs
  or discard non-text run content to colour a citation.
- Rendered checks cover clipped text/cells, small type, overflow, detached
  captions, repeated headers and page limits. Distinguish XML tests from visual
  review and Word from LibreOffice. Do not claim a complete check from samples.
- Final author approval, journal policy/AI disclosure, DOI and release publication
  are separate gates. Never move an existing public tag to conceal revisions.
