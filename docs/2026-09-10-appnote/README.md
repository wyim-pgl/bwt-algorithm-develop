# P4 → C-8 → Application Note → release candidate (2026-09-10)

## Scope and status

Author authorized this sequence after pushing numerical/provenance corrections
in `64964e1`. No benchmark, scorer, genome job or evidence rehash was run.
`results/` payloads and both deposited checksum manifests remain unchanged.
This package is an **author-review submission candidate**, not a submitted or
accepted article, and not a DOI-bearing archive.

1. **P4 review:** `../2026-09-05-astra-review/pass4-manuscript-consistency.md`:
   8 confirmed, 3 rejected. Seven prose findings were fixed in `7df3e6a`
   (15 targeted replacements; table rows unchanged). The eighth, embedded
   figure-caption staleness, is handled by presentation copies outside results/.
2. **C-8:** `94df01e` reconstructs the abstract around bounded capability rather
   than an accuracy or causal speed claim. The initial new abstract is 140
   whitespace-delimited words. Archive availability remains blocked, not invented.
3. **Conversion:** `manuscript_full.md` freezes `94df01e:manuscript.md` exactly.
   Its five pre-existing trailing-whitespace lines are retained; `.gitattributes`
   disables only end-of-line whitespace warnings and newline normalization for
   this immutable archive, not normal checks on the live manuscript.
   `manuscript.md` is the short main article; `supplementary.md` retains all
   substantive long-source sections, including historical corrections and
   unfavorable results. All **19 table blocks** retain every cell and their
   original order. Existing table IDs remain stable; no evidence-manifest
   renumbering is needed. Main Fig. 1 = former Fig. 2; main Fig. 2 = former
   Fig. 1. All seven former figures appear in the supplement, including Fig. 5.
4. **Release preparation:** retain package/CITATION version **0.9.0** and align
   the Docker label; intended tag `v0.9.0`. A GitHub release may be created as a
   **draft** after CI passes on the exact tagged commit. Publication, DOI and
   final journal-submission approval are distinct gates; see `submission/README.md`.

## Verification boundaries

`check_conversion.py` compares ordered complete table blocks, replays the full
supplemental body from the frozen long source, checks image paths and counts,
checks the word budget and asserts the presence of selected adverse claims.
It is **not** a semantic scientific-claim checker or a journal-policy validator.
It also verifies presentation-figure input/output hashes and the three version fields.
`conversion-review.md` is a separate bounded check of the shortened draft.
All five local caveat/wording suggestions were applied before the final proof:
**1,136 words, 141 abstract words, 3 main pages, 45 supplementary pages**
(`document-checks.json`). All PDF text blocks fit inside their pages; both DOCX
ZIP structures passed integrity checks, but Word pagination was not inspected.
README's duplicated benchmark summary was aligned with the already-verified
long-source figures, units and scope; README/MANUAL now link Methods S2 to the
supplement. No new measurements were made.

Run from the repository root:

```sh
python docs/2026-09-10-appnote/check_conversion.py
sha256sum -c results/manifest.sha256 --quiet
python -m pytest tests/test_deposit_hashes.py tests/test_env_var_docs.py tests/test_one_to_one_scoring.py -q
```

The prior `docs/2026-09-10-presubmit/check_patch.py` is a historical checkpoint
for `64964e1`, not the new manuscript layout. Re-run it in that commit's clean
checkout (and with its ignored resume snapshot if available), not against the
converted manuscript. Its historical hashes were not rewritten to manufacture
a pass. The numerical source audits and precision exceptions remain archived.

### Presentation-only figure handling

Six existing PDFs are cropped below their plots to remove embedded legacy
captions; current long-manuscript captions accompany them in the supplement.
The old accuracy caption overlaps its x-axis labels, so cropping it was rejected.
That figure alone was exported with the **unchanged** plotting script and two
**unchanged** CSVs in the remote `bwtandem` environment, suppressing only the
legacy `figtext` caption. This also removes its stale claim that both 2026 tools
lack period bounds. It does not recompute data or change plot points.

Source/output hashes and crop coordinates are recorded in
`submission/figures/crop-receipt.json` (six figures) and
`accuracy-export-receipt.json` (one figure). The discarded crop that clipped
accuracy-axis labels is not part of the final package. Original evidence images
are untouched. Source-limited numerical figure labels remain as deposited.

## Format policy limitation

The retained 2026-09-01 conversion/venue documents cite an approximately
2,600-word Application Note budget. The working target here is ≤2,600 words
including a conservative 500-word allowance per display, ≤200 abstract words
and ≤4 main pages. The initial proof has 1,081 whitespace-delimited words,
140 abstract words, two figures and three pages in the installed OUP authoring
class. These are measured document properties, **not live policy certification**.

Direct retrieval of both OUP `instructions_for_authors` and `general_instructions`
returned HTTP 403; the public text-extraction service returned the CAPTCHA page,
not the policy. No verification challenge was bypassed. The current journal
instructions, display legibility, declarations and archive requirement require
an author check before actual submission. No source was invented to fill this gap.
