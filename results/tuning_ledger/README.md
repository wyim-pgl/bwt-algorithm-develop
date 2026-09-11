# Tuning ledger

Deposited 2026-09-03 as the second half of the author's decision on
`quarantine.md` §3.9: disclose the configuration search rather than re-run it.

`ledger.tsv` is the append-only record of the coordinate-descent campaign that
chose BWTandem's configuration — 44 scored evaluations on adotto chromosomes
21 and 22: 22 labelled `config` and 22 labelled `code`. The decision column
contains 7 `accept`, 14 `reject`, 3 `near/reject`, 3 `near` and 17 `pending`
entries. The scores were observed before decisions were recorded; this is
a partial decision record, not a completed acceptance ledger. `best.json` holds the selection state, including the objective in the
authors' own words: reaching ULTRA's recall at approximately ULTRA's precision.

Methods 2.2.3 states what this implies and the manuscript does not soften it:
every reported operating point is a post-selection, in-sample choice, and the
chromosome 22 result is post-selection validation rather than an independent test.

The catalog scored against is the same adotto v1.2.1 set the paper reports
against. Competitors received no equivalent search.

The two files satisfy the C-3 deposit of the surviving ledger and selection
state; both are byte-identical to `exp1_human/loop/{ledger.tsv,best.json}`.
They do not establish a fully specified final selection/stopping rule. In
particular, `f_cp3` remains `pending`, and `best.json` records the earlier cAB
selection and subsequent catch-all frontiers, not a final copies≥3 selection.
The original acceptance and stopping rules are in
`docs/superpowers/plans/2026-06-23-exp1-recall-loop.md`; the revised
ULTRA-referenced target is `NEW_TARGET` in `best.json`. Code-labelled rows
have environment strings and notes but no per-row code commits or diffs.

These are historical tuning measurements. Many predate the 2026-07-09 native
alignment fix and are retired as benchmark values (`quarantine.md` §1.2).
Retain them as evidence of selection history, not as current accuracy estimates;
use the regenerated evidence elsewhere in `results/` for current measurements.
