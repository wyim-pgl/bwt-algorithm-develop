# Recovered benchmark command records (2026-09-10)

Read-only copies inspected during the repository rename / README update.
These are text evidence, **not portable or newly executed launchers**. Do not
submit them unchanged: they pin old worktrees, external paths and scheduler
settings and inherit the submitting environment. The historical detector uses
`src.main`, whereas current development code uses `bwtandem.main`.

| Copy | Original Pronghorn path | SHA-256 |
|---|---|---|
| [run_human_p100_0363.sbatch.txt](run_human_p100_0363.sbatch.txt) | `/data/gpfs/assoc/pgl/devel/exp1_human/regen/maize_rescore/run_human_p100_0363.sbatch` | `01b13172ee3d84fa34d800555fb3a7c097a01609f4e4de5c5c2d10a4a189e9b5` |
| [run_human_idsweep_0363.sbatch.txt](run_human_idsweep_0363.sbatch.txt) | `/data/gpfs/assoc/pgl/devel/exp1_human/regen/maize_rescore/run_human_idsweep_0363.sbatch` | `c1aa4bbf6d0e79bc0803c2b1813702dd4f20a54bd26a9b74cf24da2415322c3f` |
| [ultra_colcen_p500_5981977.out.txt](ultra_colcen_p500_5981977.out.txt) | `/data/gpfs/assoc/pgl/devel/exp1_human/wp0/logs/ultra_colcen_p500_5981977.out` | `a8b85700ada5fcf8c3956a070060eb33020cada73480abca475ef16d32a52b1a` |

Local copies and remote originals matched the above hashes when read. These
hashes establish the bytes recovered now, not that launcher source was immutable
at the historical execution. Existing `results/regen/` provenance JSON records
provide complementary commands, commit IDs and output hashes. Missing raw sacct
for nine panel/sweep tasks remains missing; recovering launcher files does not
recover accounting or every inherited environment variable.

## ULTRA command discrepancy

The successful job 5981977 log records local ULTRA 1.2.1 with
`-t 2 -p 500 -o OUT.tsv FASTA`, 36,430 seconds and exit 0. It does not record
`--read_all -i 3 -d 3 --bed`. Those extra flags appear for maize in deposited
comparator logs but were also attributed to this Col-CEN rerun in Supplementary
Table S15 / K5. README now separates the commands. The supplementary scientific
text was not silently repaired during this URL/documentation task: **K5's
Col-CEN command description requires a follow-up correction**, together with
any related container/general provenance prose. No accuracy or cost cell was
changed, and the current command record is not a complete historical binary or
container reconstruction.

Earlier handoff snapshots correctly describe what was deposited then; this
small new documentation deposit does not rewrite those historical records or
extend `results/manifest.sha256` retroactively.
