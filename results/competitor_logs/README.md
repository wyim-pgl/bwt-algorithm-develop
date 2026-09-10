# Competitor GNU-time logs

Deposited 2026-09-03 for issue #30 and `quarantine.md` §6.20/§6.13.

These inherited benchmark logs previously lived only on the benchmarking cluster at
`/data/gpfs/assoc/pgl/filip/bwtandem_results/benchmarking_results/<tool>/logs/`.
A reader outside this filesystem had to take the transcription on trust. They are
small, so there was no reason for that.

The 40 files are verbatim copies. Of these, 37 contain `/usr/bin/time -v`
command, wall-clock, maximum-resident-set-size and exit-status fields. The two
mreps maize logs (`*_a_exp_run.log`, `*_b_exp_run.log`) are empty; the TRASH
maize `*_trash_denovo_exp3C_centc_run.log` ends during sequence analysis without
a GNU-time footer. These three files do not establish completed-run costs.
The separate 2026-tool per-arm time logs are not in this directory. Names are
`<tool>__<original filename>`; the original names carry the assembly.

## What they establish

The human GCA_000001405.15 row of `comparator_baselines.md` recomputes from these
exactly: ULTRA 29:46:49 / 1,758,540 KiB, TRF 33:43:46 / 1,518,668 KiB, tantan
51:46.94 / 281,316 KiB, TRASH 107:37:36 / 15,298,244 KiB, mreps 54:41.08 /
6,691,220 KiB. Divide the kibibyte counts by 1024² for the GiB figures printed in
the tables.

## Reconstruction limits

The command lines record `singularity exec ./bwtbench.sif`, not a contemporaneous
package inventory, tool-binary hashes or an immutable container snapshot. They
do not independently establish the original tool-version strings or whether
that path was an image or writable sandbox at execution. The manuscript retains
the original versions as author-reported; current release environment/lock files
and Dockerfile do not reconstruct this historical competitor container.

## Two things they also show

The three Col-CEN TRASH runs are separate executions with separate costs —
CEN159 6:18:29 / 1,389,316 KiB, CEN178 25:22:40 / 2,761,680 KiB, de novo
5:47:30 / 1,357,252 KiB. The former use of the CEN159 cost for both Table 2 rows is superseded
(`quarantine.md` §6.1). The deposited template-only union has 397 records and
costs the sum of the two template runs, 31:41:09 (31.69 h), with peak
max(1,389,316, 2,761,680)/1024² = 2.63 GiB. The de novo row uses its own
5:47:30 (5.79 h) / 1.29 GiB log; see `../regen/colcen_trash_template_scored.txt`.

The human TRASH log ends with exit status 1 after a Circos plotting error. The
failure appears to fall after data export; the manuscript now discloses the
nonzero exit (`quarantine.md`, Codex round-1 finding 12).
