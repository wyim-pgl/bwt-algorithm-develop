# Provenance for the reported figures

`manifest.tsv` maps each table row in the manuscript to the interval file it was
scored from, the scoring script and its hash, the scoring rule, and the
repository commit. `figures/` holds the active Figure 1 (`figure_curve.*`,
rendered from the regenerated native period-100 P/B/F/H runs); the earlier-build figure, its
data and its renderer are retained under `superseded` names for audit only.
`regen/` holds the provenance, scoring output and deposited evidence for the
regenerated whole-genome runs. `one_to_one/` holds the strict one-to-one,
boundary-aware scoring results (Supplementary Table S4; see its README for
the metric definitions). `ground_truth/` holds the curated plant coordinate
sets used for accuracy scoring; human truth is external as described below. `range_cost_attempts/` holds the
evidence for the two competitor runs attempted at BWTandem's 2,000 bp ceiling
on human (TRF, ULTRA), neither of which completed. `range_cost_0363d8b/`
holds the three release-build BWTandem range-cost jobs and their authoritative
measurement summary.

## ground_truth/

| File | What it is |
|---|---|
| `colcen_cen180.bed` | 66,683 CEN180 monomers on Col-CEN v1.2, columns 5–6 are percent identity and strand |
| `CEN178_consensus.fa` | the 177 bp query used to produce them |
| `colcen_centromeres.bed` | the five Arabidopsis centromere intervals |
| `mo17_knob180_arrays.bed`, `mo17_tr1_arrays.bed`, `mo17_centc_arrays.bed` | the 25, 17 and 17 curated maize arrays from Chen et al. (2023) |

The CEN180 coordinates are blastn hits of `CEN178_consensus.fa` against the
assembly, filtered from 68,840 raw hits to the 66,683 deposited here. The raw hit set was recovered and is
deposited as `ground_truth/colcen_cen180_raw_blast_hits.bed`; the filtered (chromosome, start, end) coordinates are a strict
subset of its coordinates, so the 2,157 dropped hits are enumerable. The identity values that drove the filter
appear only in the filtered file, so the threshold is attested rather than recomputable. **The blastn
version and command line were not retained.** The deposited coordinates are
therefore the reproducible artefact, not the procedure that made them — every tool
in Table 2 is scored against this one file, so no comparison in the paper depends
on the lost invocation, but regenerating the set from scratch requires choosing
parameters afresh.

The human ground truth is not deposited here: it is adotto v1.2.1, obtainable
unmodified from https://zenodo.org/records/13987414 and used restricted to
chr1–22, X and Y.

## What the manifest does and does not cover

**Accuracy provenance — table-row index, with historical versions and external inputs.**
Rows identify source files and scoring rules; this is not a self-contained executable
manifest. Scorer basenames refer to `scripts/scoring/`, except where the scoring-rule
notes identify a historical external version. Historical hashes can differ from the
current script: recover the matching version from git rather than silently using the
current one. Some diagnostic rows have no recorded scorer hash; these remain explicitly
unpinned. The Table 3BC original producer is external and differs from the
later repository copy, as its scoring-rule notes explain. Competitor
BEDs and human truth still require external inputs. Figure and diagnostic summaries
also have evidence under the subdirectories; not every panel has its own manifest row.

**BWTandem cost figures.** The three regenerated whole-genome rows have
independently deposited SLURM accounting. Other rows include historical or per-arm
measurements; nine native-period-100/identity-sweep tasks have provenance JSONs
but no raw sacct record in this deposit. The `producer_job`,
`elapsed`, `peak_rss_gb_sacct` and `node` columns identify it. Peak memory is the
cgroup maximum from `sacct MaxRSS`, not GNU time, because BWTandem distributes
chromosomes across worker processes and GNU time reports the maximum over
children rather than their sum. For release-build `range-rep` rows, each job ran its 100 bp and 2,000 bp arms
sequentially. The memory column repeats the job-level cgroup maximum over both
arms (41.09, 42.67 or 44.62 GiB); the scoring-rule notes separately give each
arm's GNU-time MaxRSS. The seeding ablation also uses per-arm GNU-time elapsed
values. `sacct` cannot separate arms within one job. The historical column name
`peak_rss_gb_sacct` is retained for compatibility: values use GiB, and the 2026
competitor rows use GNU-time MaxRSS, explicitly not cgroup peaks.

### What the `threads` column means (2026-09-03)

`threads` is the **SLURM allocation** (`--cpus-per-task`), not a measurement of how
many threads the tool actually used. The two differ in one place we know of: the
widened tantan runs were allocated 2 CPUs and ran at 99% CPU, i.e. one active
thread. Splitting the column into `allocated_cpus` and `tool_threads` would be a
schema migration touching every row, `results/README.md`, every consumer and the
external `wp0/make_manifest.py` that regenerates the file, so the column keeps its
meaning and the exceptions are named here instead.

Corrected 2026-09-03: the four AniAnn's rows (123, 126, 129, 132) said `1`. The
sbatch and every run log show `-j 2` under `--cpus-per-task=2`, so both readings
are 2.

**Competitor cost figures — surviving GNU-time logs and some later SLURM accounting.**
The 40 inherited log files deposited under `competitor_logs/` include 37 with
complete GNU-time fields, two empty mreps maize logs and one unfinished TRASH
maize log without a timing footer. All five historical human cost rows recompute
from their logs. This does not establish every competitor cost cell. Later
reruns and 2026 tools have some accounting in `sacct_provenance.txt`; the 2026
per-arm GNU-time logs remain external. Rows whose
`producer_job` is the literal string `published` come from an earlier
benchmarking round. The output files and the command lines survive; the job
accounting records do not. Those rows generally have missing or placeholder `threads`, `elapsed`,
`peak_rss_gb_sacct` and `node` fields, and the runtime and memory printed in
Tables 1a, 1d, 2, 3A, 3B and 3C for those tools are the GNU time values recorded at
the time. They are reported because they are the best record available, and they
should be read as approximate. The accuracy figures computed from the same files
do reproduce.

For scale on how approximate: two BWTandem executions of identical settings on
the same genome at the same thread count differ by 29% in wall clock
(9 h 21 m against 12 h 06 m, both 4,009,261 calls, on the historical build).
The regenerated human run at the campaign pin took 12 h 38 m for 4,014,108
calls, inside that spread. Cost differences below this magnitude between any
two rows here are not interpretable.

## The `repo_commit` column

The column now carries more than one value, and the distinction matters.

Rows for the **regenerated whole-genome runs** (the deposited Col-CEN, human and
maize BEDs, and the scoring output under `regen/`) read **`0363d8b`**, the
campaign pin. Those runs were executed by `run_with_provenance.sh` from a clean
tree. `regen/*.provenance.json` records the commit, command, process-accounting
elapsed time and wait4 peak RSS, and a full SHA-256 for each output. The raw SLURM
accounting is in `sacct_provenance.txt`, not those JSONs. The JSONs do not record
the controlling environment overrides; configuration reconstruction also needs
the launch environment described in Supplementary Methods S2. `0363d8b` is
the detection-code pin, not necessarily the scorer commit: several wrappers
were deposited later. S4 rows instead name scoring commits. Historical values
`0e17d1a+outputfixes` describe an execution state, not a resolvable git object;
they must not be treated as checkout instructions.

**Historical rows**, which the manuscript still cites where a regenerated
replacement does not exist, read `0e17d1a` — the repository HEAD when those runs
were executed — or **`294f8ac`**, which is where the uncommitted `src/`
modifications present in that working tree now live. Rows superseded by the
regeneration are labelled as such in `manifest.tsv` rather than deleted.
The superseded range-cost rows instead read `07ad6fa`, the only commit where
`--max-period` did not bound the Tier 3 search.

The two behavioural differences below separate `294f8ac` from the tree that ran
the historical rows; they do not apply to the `0363d8b` rows, whose outputs are
byte-verified against their recorded hashes.

First, it carries the fix that stops the satellite gap-filling pass from emitting
motifs containing characters other than A, C, G and T; re-running the released code
on the human genome therefore yields 198 fewer calls (4.57 Mb) than
`remeas_human.bed` contains. Second, the released code renders the column recording
each call's originating pass numerically, where the deposited outputs carry a text
label on satellite calls — a byte-level formatting change that alters no coordinate,
motif or statistic. Every other historical output should reproduce.

## Known issue: a memory-layout-dependent flaky test

`tests/test_ground_truth.py::TestAdjacentGroundTruth::test_sensitivity` fails in
roughly 60% of full-suite runs on a small synthetic fixture. It is memory-layout
dependent rather than a logic defect, and it does **not** reach chromosome-scale
output: an 18.8 Mb chromosome produces byte-identical results under three different
process memory layouts. No figure in this manifest depends on it. See CLAUDE.md for
the full evidence table.

## Row classes

| `table` value | What it is |
|---|---|
| `1a`, `1b`, `1c`, `1d`, `1e` | human GRCh38 against adotto v1.2.1 |
| `S3` | the active single-parameter catch-all identity sweep, full range |
| `sweep-superseded` | historical identity sweep; superseded by `S3` |
| `range-rep` | the three active four-thread release-build pairs at 100 and 2,000 bp; both arms ran sequentially in one job and share a node; see `range_cost_0363d8b/` |
| `range-cost` | the two competitor matched-ceiling attempts (`TRF-p2000-attempt`, `ULTRA-p2000-attempt`), both terminated incomplete; see `range_cost_attempts/` |
| `range-cost-superseded`, `range-rep-superseded` | the original pair and three replicate pairs at `07ad6fa`; retained for audit but superseded because the narrow arm performed and discarded the long-period Tier 3 search |
| `2` | Arabidopsis Col-CEN v1.2 |
| `ablation` | Col-CEN satellite gap-fill ablation, three arms from one job |
| `3A`, `3B`, `3C`, `3B-b/3C-b` | Zea mays Mo17 |

Rows whose `source_bed` reads `(same source BEDs as …)` are alternative scorings
of files already listed, not new outputs.

## Deposited interval files

The three whole-genome BWTandem outputs are deposited in `beds/` (gzipped, with
`SHA256SUMS`), and the manifest's `source_bed` column points at them by
repository-relative path. Competitor outputs are not deposited: they are the
inherited files of an earlier benchmarking round and remain on the cluster paths
recorded in the manifest.
