# General lab DOCX style and BWTandem display migration

Author-approved scope: apply the supplied citation/display/Word house style to
BWTandem (Opuntia was an example), allow information-preserving restructuring,
install blader/humanizer, use all applicable installed humanizers, save a
general lab workflow in the wiki, THEN generate Word files.

## Order and reusable implementation

The general rules and formatter were saved and pushed to the lab wiki before
project Word generation: initial wiki commit `a7141d4`; subsequent tested fixes
`9bbfcef` (caption-body citation colours) and `b2dbac6` (image/caption grouping)
were likewise saved before their Word regenerations. The exact final wiki
commit is in `wiki-commit.txt`. The vendored formatter is byte-identical to
`paper-format/lab-docx/` at that commit; `wiki-files.sha256` pins the copies.

Canonical rules: https://github.com/wyim-pgl/wiki/blob/main/paper-format/LAB_DOCX_STYLE.md
Toolkit: https://github.com/wyim-pgl/wiki/tree/main/paper-format/lab-docx

This is a lab style, not a journal compliance certificate. Formatting touches
OOXML properties and splits only simple text runs while preserving non-text
content; it does not rewrite scientific prose, invent taxon names, renumber
items, or choose which data to omit. Source migration is project-specific.

## Humanizers

Pi's actual loader detected three entries (`humanizer-discovery.json`):
- `humanizer`: blader v3.0.0, pinned to
  `9862685f575c65a8247f90369951df1b3416e3d6`; installed locally and on Pronghorn.
- `humanizer_eng`: existing Claude English skill, exposed to Pi by symlink.
- `humanize-writing`: existing `humanizer_kor` directory's English-capable
  general checklist, exposed by symlink. Korean-specific rules were not applied
  to the English manuscript. The directory/frontmatter name is retained.

The underscore in `humanizer_eng` causes a naming warning but the loader returns
the skill. Files were explicitly read in this running session; a future normal
startup discovers them. No bundled upstream script was executed. Both original
Claude installations were retained rather than overwritten.

All three checklists were used sequentially, with complete manuscript and
supplement reads. `prose-proposals.json` records scope, passes and deferred
items; `accepted-prose.json` includes parent-reviewed edits. Main Summary stays
two sentences with its adverse accuracy and audit findings. Parent review
removed a proposed long Summary parenthesis rather than accepting it blindly.
This is not three independent scientific reviews, detector testing, or a claim
that publisher LLM-policy/final-author-approval gates are resolved.

## Display migration and information preservation

`display-map.json` binds 19 original physical table blocks by SHA256:
- Original human/plant panels -> Tables S1-S12.
- Two previously unnumbered parameter/configuration matrices -> S13/S14.
- Original versions/commands and unique-call characterization -> S15/S16.
- Small identity-sweep table -> full numerical prose, in Methods S2 and main
  Results; every condition and recall/precision value retained.
- Two former S4 blocks -> distinct region-truth S17 and annotation-truth S18.
- Seven supplementary figures -> S1-S7 in supplementary display order. Main
  Figures 1 and 2 remain unchanged in identity, and correspond to S1 and S4.

All 18 tables and seven supplementary figures are called out in main narrative,
in addition to the two main figures. Finding-first wording replaces display-
as-subject signposting; administrative setting lists are allowed exceptions.
Main-callout order follows the scientific discussion; supplementary numbering
follows physical display order, not necessarily first main-text mention.

Long parameter values, configuration names/environments, and complete command
strings move to keyed P/C/K descriptions beside the relevant Methods tables.
No command character or measurement is removed to make no-wrap fit. Headers
are shortened with explicit abbreviation definitions (`header-aliases.json`).
Positional prose was corrected after relocation (notably 'rightmost column'),
and a historical 'Table 1' reference to original tantan output was disambiguated
rather than silently assigning it to the widened rerun.

`manuscript-before.md` and `supplementary-before.md` are immutable snapshots of
`b02c643`; their hashes are pinned. The old supplement is independently replayed
from frozen `manuscript_full.md`. `main-replay.json` and `supplement-replay.json`
then account for every source edit. `check_migration.py` separately checks cells,
row counts, moved commands, the prose-converted values, unique labels and main
callout coverage. The legacy conversion guard was extended, not removed.

## Word style and scope

TNR prose; bold black headings and caption titles; first prose paragraph flush,
subsequent prose 18 pt first-line indent. Explicit Affiliation style carries the
requested line breaks. Display callouts are red FF0000, literature citations
blue 3399FF (including explanatory legend text). Scientific binomials are native
italics. Tables use Arial 9 pt, no-wrap fitted columns, repeating bold headers,
three horizontal rules and no shading. Long rows are not split; a logical table
may continue across pages with repeated headers. Annotations have no inserted
blank spacer paragraphs. Code/URLs and mathematical minus signs are preserved.

C3/C4 subscript is supported/tested only via the photosynthesis profile; it is
not applied to BWT's unrelated C3/C4 configuration IDs. No geological-age Ma
occurrence required Mya conversion here. Embedded plot artwork is unchanged;
editable source range dashes use hyphens. Font names in DOCX are the requested
names; LibreOffice/fontconfig may use metrically compatible substitutes.

## Verification and limits

- Generic formatter: 13 synthetic tests, including preservation, cross-run
  colours, institution/n.d. citations, captions, species, optional subscripts,
  no-wrap rules, unsupported-input failure and idempotence.
- Migration guards: 7 tests (valid baseline plus changed cell/command/minus,
  deleted caveat, duplicated row/caption). Every deliberate corruption fails.
- Source replay, figure receipts and independent table accounting pass.
- `check_outputs.py`: Word paragraph text, media, relationships, fields and
  bookmarks preserved from plain Pandoc output; table and text formatting
  verified; idempotent. Exactly 18 Word table elements.
- `check_render.py`: all-page LibreOffice geometry, complete 7/7 figure legends
  on image pages; 20 table-bearing pages identified. All those table pages were
  visually inspected via contact sheets during proofing. The final small prose
  cleanups were rebuilt with geometry and complete-caption checks rerun.
- XeLaTeX proofs: main 3 pages, supplement 45 pages. LibreOffice 5.3.6.1 Word
  previews: main 5 pages, supplement 52 pages. Word layout and journal-template
  PDF layout are distinct; Microsoft Word was not run.

`results/`, `manuscript_full.md`, existing public `v0.9.0`, draft release assets
and DOI/declarations were not changed. Final author approval, publisher policy
judgment, missing supporting-data access and release/archive steps remain open.
