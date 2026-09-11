# BWTandem — development repository

De novo tandem repeat detection in assembled genomes (FASTA), with BED,
VCF, TRF `.dat` and STRfinder `.csv` output. The pipeline combines FM-index
seeding, candidate refinement and supplementary periodicity scans.

**Repository:** https://github.com/wyim-pgl/bwt-algorithm-develop

This repository was renamed from `bwt-algorithm`; the software/package/CLI name
remains **BWTandem / `bwtandem`**. `main` contains the development code,
manuscript sources, benchmark evidence and author-review documents. It is not
an accepted paper or a DOI-archived final submission. The existing `v0.9.0`
tag remains fixed at `ef98c03`; it is not the current manuscript snapshot.

BWTandem does **not** establish superior shared-range accuracy over ULTRA.
Its wide-range output is intended for downstream validation; period assignment,
fragmentation, over-calling and memory use remain limitations. See
[benchmarks](#benchmarks) and the [reproduction guide](#benchmark-reproduction).

![How BWT finds tandem repeats](figures/Video%20Project.gif)

- **One wide-range pass** — periods 1–2,000 bp by default. Larger ceilings
  are configurable, but the manuscript does not validate accuracy across the
  full configurable range or every reported motif structure.
- **Three-tier pipeline** — exact FM-index enumeration for short perfect
  repeats, LCP/k-mer seeding with mismatch tolerance for medium imperfect
  repeats, sparse seeding with anchor verification for long arrays.
- **Four output formats** — BED (default), VCF, TRF-compatible `.dat`,
  STRfinder CSV.
- **Benchmark evidence and limits** — deposited results include checksums,
  commands and execution records, but some external inputs and historical
  provenance are missing ([below](#benchmarks)).

## Installation

BWTandem is a standard Python package: `pip install .` compiles the Cython
accelerator into the wheel and installs a `bwtandem` command. Requirements:
Python ≥ 3.11 and a C compiler (`gcc`).

### Route A — micromamba / conda (recommended; brings its own compiler)

```bash
git clone https://github.com/wyim-pgl/bwt-algorithm-develop.git
cd bwt-algorithm-develop

# Pins the later development/regeneration core, not every historical run.
# Earlier whole-genome and panel environments differ; see Methods S2.
micromamba create -n bwtandem -f environment.core.lock.yml
micromamba run -n bwtandem pip install .

# verify (~30 s smoke test on bundled data)
micromamba run -n bwtandem bwtandem --help
micromamba run -n bwtandem bash examples/quickstart.sh
```

With conda instead of micromamba, the same file works:
`conda env create -f environment.core.lock.yml && conda activate bwtandem && pip install .`

### Route B — plain pip (any Linux/macOS with Python ≥ 3.11 and gcc)

```bash
git clone https://github.com/wyim-pgl/bwt-algorithm-develop.git
cd bwt-algorithm-develop
pip install .
bwtandem --help
```

`pip install .` pulls numpy and pydivsufsort automatically. On very old
systems (glibc < 2.24) the pydivsufsort binary wheel is not installable —
use Route A, which compiles it locally.

### What needs a compiler, exactly

- **At install time**: the Cython accelerator is compiled into the wheel, so
  `pip install .` requires `gcc`. This is the part that makes real runs fast.
- **At first run**: four small C libraries (`bwtandem/c_extensions/*.c`,
  shipped in the wheel) compile themselves on first import and need `gcc` on
  `PATH` at runtime — the Route A environment provides it. Native/fallback
  parity has regression coverage, but not every C-library path is covered by
  the same disable switch. Check build warnings before benchmarking; do not
  silently compare a fallback run with a native run.

### Editable developer install

```bash
micromamba run -n bwtandem pip install -e .[dev]
micromamba run -n bwtandem python3 -m pytest tests/ -q
```

Before the rename/documentation update, the merged `main` at `3653947`
passed three consecutive full-suite runs on Pronghorn: 219 passed, 1 skipped
per run. These checks do not resolve the known layout-dependent native
regression (see [CLAUDE.md](CLAUDE.md)); test counts depend on the environment.
See [CONTRIBUTING.md](CONTRIBUTING.md) for the development workflow.

### Docker

```bash
docker build -t bwtandem .
docker run --rm -v "$PWD:/data" bwtandem /data/input.fa --format bed -o /data/out
```

The image installs the pinned environment and pre-compiles every native
extension, so it also converts cleanly to a read-only Singularity/Apptainer
image (`singularity build bwtandem.sif docker-daemon://bwtandem:latest`).

## First run

From a repository checkout, on the bundled test data:

```bash
# 35 bp toy sequence: five copies of TCATCGG (runs in <1 s)
bwtandem arabadopsis_chrs/test_seq1.fa --format bed -o /tmp/quick
cat /tmp/quick.bed
# repeatTCATCGG_5    0    35    TCATCGG    5.0    1    0.000    +

# a real 367 kb sequence (Arabidopsis mitochondrial genome, ~2 s, 45 calls)
bwtandem arabadopsis_chrs/ChrM.fa --format bed -o /tmp/chrm -v

# or the packaged smoke test
bash examples/quickstart.sh
```

On your own data (any context):

```bash
# defaults: all tiers, periods 1-2,000 bp, BED written next to the input
bwtandem input.fa
```

`python3 -m bwtandem.main` is the module-form equivalent of the `bwtandem`
command (useful from an uninstalled checkout).

## What the output looks like

```
chr1    100    145    AT       22.5    1    0.022    +
chr1    500    620    AATGG    24.0    2    0.083    +
```

BED columns: `chrom start end motif copies tier mismatch_rate strand`
(0-based; the motif is the canonical rotation reduced to the primitive
period). Complete schemas for all four formats, with real examples, are in
[MANUAL.md §5](MANUAL.md#5-output-formats).

## Common options

| Option | Default | Meaning |
|---|---|---|
| `--min-period` / `--max-period` | 1 / 2000 | period range to search and report; a configurable ceiling is not a validated accuracy range |
| `--tiers tier1,tier2,tier3` | all | run a subset, e.g. `--tiers tier1` for STRs only |
| `--format bed\|vcf\|trf\|strfinder` | bed | output format |
| `-t, --threads N` | 1 | one worker per sequence (helps multi-sequence FASTA only) |
| `--mask soft\|hard\|both` | none | skip soft-masked (lowercase) and/or `N` regions |
| `-o PREFIX` | input name | output prefix |

The full CLI reference, masking semantics, Tier 3 presets, and the
environment-variable sensitivity levers are in [MANUAL.md](MANUAL.md).

## How it works

One FM-index is built per sequence, then three tiers run in order, each
skipping regions the previous tiers already claimed:

1. **Tier 1** (short motifs): sliding-window scanning by default;
   `TIER1_FMSCAN=1` selects FM-index enumeration in the benchmark settings.
   Mode selection is explicit, not a fixed 10 Mb sequence-length switch.
2. **Tier 2** (motifs ≥ 10 bp): LCP-array candidates plus BWT k-mer seeding,
   extended with mismatch/indel tolerance for imperfect repeats.
3. **Tier 3** (periods 100 bp–100 kb): sparse k-mer seeding with adaptive
   parameters; ultra-long arrays use anchor-based boundary verification
   instead of full alignment.

Details, including the post-processing and the optional sensitivity passes,
are in [MANUAL.md §4](MANUAL.md#4-the-three-tier-pipeline).

## Benchmarks

The regenerated whole-genome BWTandem results use execution commit `0363d8b`.
Competitor baselines and historical ablations have distinct provenance; some
raw accounting, visual-audit artifacts and external inputs remain unavailable.
**The full tables and limitations live in [`supplementary.md`](supplementary.md)
and [`results/manifest.tsv`](results/manifest.tsv)**; the short Application Note
is [`manuscript.md`](manuscript.md). Manifest links do not imply every external
artifact is deposited. Deposited evidence:
[`results/regen/`](results/regen/) (score reports, per-run provenance),
[`results/beds/`](results/beds/) (the three whole-genome BWTandem BEDs),
[`results/audit11/`](results/audit11/) (blinded specificity audit),
[`results/one_to_one/`](results/one_to_one/) (strict one-to-one scoring),
[`results/range_cost_0363d8b/`](results/range_cost_0363d8b/) (release-build
range-cost pairs and job logs),
[`results/figures/`](results/figures/) (operating-point figure and data).

Headline results (human GRCh38 vs the GIAB adotto catalog, Arabidopsis
Col-CEN, maize Mo17; see the manuscript for every caveat):

| Claim | Measurement |
|---|---|
| One wide-range pass | periods 1–2,000 bp in 12.65 h / 25.29 core-hours on GRCh38 (ULTRA: 29.78 h / 59.56 core-hours capped at 100 bp; execution ranges and FASTA scopes differ) |
| Sublinear range cost | widening the maximum period 100→2,000 bp costs 1.77–1.82× (mean 1.79) in release-build paired runs; the superseded 1.30–1.41× estimate was too favourable because its narrow arm performed and discarded the long-period Tier 3 search; the TRF and ULTRA 2,000 bp attempts on human were terminated incomplete after 6.58 d and 1 d 22 h |
| Shared-range accuracy | non-leading: ULTRA ranks first in region recall (81.62%); BWTandem 78.87% at the whole-genome configuration, restricted the same way its competitors are, 81.60% at a permissive setting with lower precision |
| Long-period stratum | calls reporting periods 101–2,000 bp overlap 3.43% of the whole catalog; this is not truth-period-stratified recall (original ULTRA ceiling: 100 bp) |
| Plant satellites | Col-CEN unfiltered CEN180 monomer recall 99.72% in 0.67 h; maize CentC unfiltered coverage 58.55%, below AniAnn's 81.42% |
| Specificity audit | Of 400 stratified calls absent from both the catalog and four original comparators, 4 supported, 346 unsupported, 50 unsure (single reader); not a population-weighted estimate |
| Cost of the design | 28.08 GiB sampled cgroup peak on human (ULTRA: 1.68 GiB GNU-time maximum; different accounting) and fragmented satellite calls |

Reproducing any number requires the environment overrides in Supplementary
Methods S2 in [`supplementary.md`](supplementary.md) — the benchmarked operating points differ from
the built-in defaults ([MANUAL.md §9](MANUAL.md#9-reproducing-the-manuscript-numbers-checkout-only)).

## Benchmark reproduction

This section covers the retained benchmark experiment families, their settings,
conversion and scoring commands. **It is not a one-command reproduction of the
paper.** Assemblies, human truth, competitor BEDs, TRASH template CSVs and some
historical build/accounting records are external. A missing record is not
replaced with a guessed command. No benchmark was rerun for this README update.

- [Inputs and preparation](#inputs-and-preparation)
- [Environment and common settings](#environment-and-common-settings)
- [Whole-genome BWTandem runs](#whole-genome-bwtandem-runs)
- [Native-p100 operating points](#native-p100-operating-points)
- [Identity sweep](#identity-sweep)
- [Paired range cost and SLURM](#paired-range-cost-and-slurm)
- [Competitor detection commands](#competitor-detection-commands)
- [Conversion and human scoring](#conversion-and-human-scoring)
- [Plant and 2026-tool scoring](#plant-and-2026-tool-scoring)
- [Other analyses and integrity checks](#other-analyses-and-integrity-checks)

**Two kinds of commands:** fenced shell examples below are **adapted templates
for the current checkout**, with explicit path placeholders. Historical argv,
versions, output hashes and execution commits remain in
[regeneration JSON records](results/regen/),
[competitor logs](results/competitor_logs/),
[the manifest](results/manifest.tsv), and the
[recovered launcher records](docs/2026-09-10-benchmark-launchers/).
Current `bwtandem.main` replaces historical `src.main`; running current `main`
is a new experiment, not execution of the original `0363d8b` binary. Use a
separate pinned checkout and matching native build for historical reproduction.
Do not overwrite the deposited evidence or its checksums with new output.

### Inputs and preparation

| Input | Required identity and scope | Source / expected local name |
|---|---|---|
| Human BWTandem / 2026 tools | hg38 primary chromosomes chr1–22, chrX, chrY only | [UCSC hg38](https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/), `hg38_primary.fa` |
| Human original competitors | GenBank GRCh38 `GCA_000001405.15`, also includes additional sequences | [NCBI assembly](https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_000001405.15/); not the same FASTA scope as the primary-only detector input |
| Human truth | adotto v1.2.1; primary-chromosome region truth has 1,784,804 intervals | [Zenodo record 13987414](https://zenodo.org/records/13987414), `adotto_TRregions_v1.2.1.bed.gz` → `adotto_primary.bed` |
| Arabidopsis | Col-CEN v1.2, preserve `Chr1`–`Chr5` headers for nuclear scoring | [Col-CEN v1.2](https://github.com/schatzlab/Col-CEN/tree/main/v1.2), name local copy `colcen.fa` |
| Maize | Mo17 T2T `GCA_022117705.1` | [NCBI assembly](https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_022117705.1/), name local copy `zmays.fna` |
| Plant truth | CEN180 monomers/centromeres; knob180, TR-1, CentC curated arrays | [Deposited BEDs and consensus](results/ground_truth/) |
| Comparator output | Tool-specific converted BEDs and widened-period reruns | External paths and scoring contracts in [manifest](results/manifest.tsv); **not bundled** |
| Template-guided tools | Exact NCRF consensus strings / TRASH template CSVs | NCRF strings are in [logs](results/competitor_logs/); TRASH CSV contents remain external |

Obtain the named versions from their source records; do not substitute a later
assembly or truth release. The exact historical download/filter launcher was
not recovered, so the links above are acquisition sources, not a claim of
byte-identical download reproduction. Bundled `arabadopsis_chrs/` examples are
not the Col-CEN benchmark. Deposited CEN180 coordinates can be rescored, but the
full original BLAST generation command is not reconstructed here.

Activate the installed environment, then set **absolute paths**. `$OUT` must be
a new writable campaign directory outside tracked evidence. `$CB` and `$WP0`
represent external comparator roots, not directories created by cloning.

```bash
cd /path/to/bwt-algorithm-develop
REPO=$PWD
PY=$(command -v python)
DATA=/path/to/benchmark-data
OUT=/path/to/new-benchmark-output
CB=/path/to/competitor-beds
WP0=/path/to/external-wp0
export BEDTOOLS=/path/to/bedtools
mkdir -p "$OUT"
```

After obtaining `hg38.fa.gz` and `adotto_TRregions_v1.2.1.bed.gz`, this is an
**adapted primary-chromosome preparation example**, not the recovered producer.
Keep the full annotation-bearing truth for the later annotation-coordinate test.

```bash
"$PY" - "$DATA" <<'PY'
import gzip, pathlib, sys
p = pathlib.Path(sys.argv[1])
keep = {f'chr{i}' for i in range(1, 23)} | {'chrX', 'chrY'}
with gzip.open(p/'hg38.fa.gz', 'rt') as src, (p/'hg38_primary.fa').open('w') as dst:
    selected = False
    for line in src:
        if line.startswith('>'):
            selected = line[1:].split()[0] in keep
        if selected:
            dst.write(line)
with gzip.open(p/'adotto_TRregions_v1.2.1.bed.gz', 'rt') as src, \
     (p/'adotto_TRregions_v1.2.1.bed').open('w') as full, \
     (p/'adotto_primary.unsorted.bed').open('w') as dst:
    for line in src:
        full.write(line)
        fields = line.rstrip('\n').split('\t')
        if len(fields) >= 3 and fields[0] in keep:
            dst.write('\t'.join(fields[:3])+'\n')
PY
LC_ALL=C sort -k1,1 -k2,2n "$DATA/adotto_primary.unsorted.bed" > "$DATA/adotto_primary.bed"
grep -c '^>' "$DATA/hg38_primary.fa"  # expected: 24
wc -l "$DATA/adotto_primary.bed"     # expected: 1784804
```

Check input hashes against the relevant retained records where available; a
matching accession alone does not verify exact file bytes or contig filtering.
Original whole-genome environments report Python 3.11.14/numpy 2.3.1; later
native-p100/sweep records report 3.11.15/2.4.6. The lock file describes the later
core, not all historical environments. The original comparator container cannot
be reconstructed from the current Dockerfile alone.

### Environment and common settings

Run from the repository root with Cython/native helpers built and gcc available.
On Pronghorn, the recorded interpreter is
`/data/gpfs/assoc/pgl/bin/conda/conda_envs/bwtandem/bin/python`; put its directory
on `PATH` too when using the provenance wrapper. Use the installed environment's
interpreter elsewhere. Benchmarks differ from built-in defaults.

The following Bash helper clears inherited detector tuning variables **in a
subshell for each arm**, then applies that arm's settings. This prevents a
previous F run from silently enabling catch-all in a P or Col-CEN run. It does
not reconstruct the missing historical BLAS/OpenMP or binary environment.

```bash
bwt_run() (
  while IFS= read -r name; do
    case "$name" in
      TIER1_*|TIER2_*|TIER3_*|CATCHALL_*|SAT_*|BWT_*) unset "$name" ;;
    esac
  done < <(compgen -e)
  env "$@"
)
base=(TIER1_FMSCAN=1 TIER1_FMSCAN_MIN_DENSITY=0.45 TIER1_FMSCAN_MIN_LLR=6.0
      TIER1_MIN_ARRAY_LEN=20 TIER1_MIN_SCORE=20 TIER1_MIN_COPIES=2
      TIER1_COPYBASE=6 TIER1_COPYADD=2 TIER1_EXT_COPIES=2
      TIER2_MISMATCH=0.30 TIER2_SHORT_REQ_COPIES=2)
gate=(TIER1_SHORT_PERIOD_MAX=9 TIER1_SHORT_MIN_ARRAY_LEN=17 TIER1_SHORT_MIN_SCORE=17)
catchF=(CATCHALL_SCAN=1 CATCHALL_MIN_IDENTITY=0.72 CATCHALL_MIN_COPIES=3)
```

Source: [whole-genome launcher](scripts/benchmark/regen_345.sbatch),
[Methods S2](supplementary.md), and
[recovered P/B/F/H and sweep launchers](docs/2026-09-10-benchmark-launchers/).
Default all tiers, balanced Tier 3 and no masking are used. Main arms do not
enable index cache, k-tuple ablation, rolling extension or approximate Tier-2
seeding. Cache timing and native-versus-fallback timing must not be mixed.

### Whole-genome BWTandem runs

Human and maize use F; Col-CEN uses the same relaxed short-period gate but
catch-all is **off**. Each command writes `PREFIX.bed`.

```bash
bwt_run "${base[@]}" "${gate[@]}" "${catchF[@]}" \
  "$PY" -m bwtandem.main "$DATA/hg38_primary.fa" --min-period 1 --max-period 2000 \
  --threads 2 --format bed -o "$OUT/regen_human" -v
bwt_run "${base[@]}" "${gate[@]}" "${catchF[@]}" \
  "$PY" -m bwtandem.main "$DATA/zmays.fna" --min-period 1 --max-period 2000 \
  --threads 2 --format bed -o "$OUT/regen_maize" -v
bwt_run "${base[@]}" "${gate[@]}" \
  "$PY" -m bwtandem.main "$DATA/colcen.fa" --min-period 1 --max-period 2000 \
  --threads 2 --format bed -o "$OUT/regen_colcen" -v
```

To **rescore deposited output without rerunning detection**, use a separate
output directory and the committed compressed BEDs instead:

```bash
mkdir -p "$OUT/deposited"
for genome in human colcen maize; do
  gzip -dc "results/beds/bwtandem_${genome}.bed.gz" > "$OUT/deposited/regen_${genome}.bed"
done
# In scoring commands below, substitute these paths for newly generated BEDs.
```

### Native-p100 operating points

All four arms actually execute at period ceiling 100 with four workers. P
omits the relaxed gate; B uses identity 0.76 and max catch-all period 50; F
requires three catch-all copies; H leaves the default two-copy requirement.
This is not post-filtering a full-range output.

```bash
bwt_run "${base[@]}" "$PY" -m bwtandem.main "$DATA/hg38_primary.fa" \
  --min-period 1 --max-period 100 --threads 4 --format bed -o "$OUT/bwt_human_P_p100" -v
bwt_run "${base[@]}" "${gate[@]}" CATCHALL_SCAN=1 CATCHALL_MIN_IDENTITY=0.76 CATCHALL_MAX_P=50 \
  "$PY" -m bwtandem.main "$DATA/hg38_primary.fa" \
  --min-period 1 --max-period 100 --threads 4 --format bed -o "$OUT/bwt_human_B_p100" -v
bwt_run "${base[@]}" "${gate[@]}" "${catchF[@]}" \
  "$PY" -m bwtandem.main "$DATA/hg38_primary.fa" \
  --min-period 1 --max-period 100 --threads 4 --format bed -o "$OUT/bwt_human_F_p100" -v
bwt_run "${base[@]}" "${gate[@]}" CATCHALL_SCAN=1 CATCHALL_MIN_IDENTITY=0.72 \
  "$PY" -m bwtandem.main "$DATA/hg38_primary.fa" \
  --min-period 1 --max-period 100 --threads 4 --format bed -o "$OUT/bwt_human_H_p100" -v
```

Historical launcher array order is P/B/F/H; its `.txt` copy records the original
paths and full execution pin. Recovering that launcher does not recover the
missing raw scheduler accounting for the nine panel/sweep tasks.

### Identity sweep

This is a **full-range** sweep, with three-copy catch-all setting held constant
and catch-all disabled for `off`. These are in-sample operating-point experiments,
not independent validation of parameter selection.

```bash
for arm in off 0.80 0.76 0.72 0.68; do
  settings=(CATCHALL_MIN_COPIES=3)
  if [ "$arm" != off ]; then
    settings+=(CATCHALL_SCAN=1 CATCHALL_MIN_IDENTITY="$arm")
  fi
  bwt_run "${base[@]}" "${gate[@]}" "${settings[@]}" \
    "$PY" -m bwtandem.main "$DATA/hg38_primary.fa" --min-period 1 --max-period 2000 \
    --threads 4 --format bed -o "$OUT/bwt_human_idsweep_${arm}_p2000" -v
done
```

### Paired range cost and SLURM

Each range-cost replicate runs F at 100 then 2,000 inside one job with four
workers. Repeat with distinct output prefixes and record node placement.
Source: [original launcher and three job logs](results/range_cost_0363d8b/).
Two published replicates shared a node; they are not three independent machines.

```bash
REP=1  # use 1, 2, 3 in separate replicate jobs
for maxp in 100 2000; do
  prefix="$OUT/rep${REP}_p${maxp}"
  bwt_run "${base[@]}" "${gate[@]}" "${catchF[@]}" \
    /usr/bin/time -v "$PY" -m bwtandem.main "$DATA/hg38_primary.fa" \
    --min-period 1 --max-period "$maxp" --threads 4 --format bed -o "$prefix" -v \
    > "$prefix.stdout" 2> "$prefix.time"
done
```

| Campaign | Recorded resource request | Launcher / parameters |
|---|---|---|
| Whole genomes | 2 CPUs, 120G, 36h | [regen_345.sbatch](scripts/benchmark/regen_345.sbatch), `GENOME=human`, `maize`, `colcen` |
| Native-p100 | 4 CPUs, 64G, 12h, array 0–3 | [Recovered launcher](docs/2026-09-10-benchmark-launchers/run_human_p100_0363.sbatch.txt) |
| Identity sweep | 4 CPUs, 64G, 12h, array 0–4 | [Recovered launcher](docs/2026-09-10-benchmark-launchers/run_human_idsweep_0363.sbatch.txt) |
| Range pairs | 4 CPUs, 44G, 24h | [run_rangerep0363.sbatch](results/range_cost_0363d8b/run_rangerep0363.sbatch), `REP=1`, `2`, `3` |

These requests are not measured consumption. Original launchers contain hard-coded
cluster paths and commit guards; **adapt a copy**, pre-create its log/output
directories, and choose account/partition/time for your cluster. Do not edit a
commit guard to mislabel a new build as the historical pin. The original range
launcher still invokes `src.main` and cannot simply be run against current main.
Clear inherited `SBATCH_*` settings that override your request:

```bash
# Define PARTITION, ACCOUNT, and LAUNCHER for your own cluster/adapted script.
env -u SBATCH_PARTITION -u SBATCH_ACCOUNT -u SBATCH_TIMELIMIT \
  sbatch --partition="$PARTITION" --account="$ACCOUNT" --time=36:00:00 \
  --export=ALL,GENOME=human "$LAUNCHER"
# After completion; JOBID is the actual returned scheduler job ID.
sacct -j "$JOBID" --format=JobID,Elapsed,MaxRSS,State -P
```

[run_with_provenance.sh](scripts/benchmark/run_with_provenance.sh) can wrap a
detector command as `--tag NAME --out PREFIX -- COMMAND ...` on a clean tracked
tree. Use a unique prefix. It records Git/command/output information and rusage,
but **not** the complete tuning environment, input FASTA hash or native binary
identity: save those separately. Scheduler cgroup memory and GNU-time
max-over-children memory are different metrics; a single job's sacct peak cannot
separate the two range-pair arms. The superseded `07ad6fa` range-cost series is
not an alternative estimate to average into the corrected series.

### Competitor detection commands

The following matrix retains the recorded flags while replacing private paths.
Original runs generally used `singularity exec ./bwtbench.sif`; widened reruns
and 2026 additions may use local installations. Tool versions in old logs are
not a complete binary/environment reconstruction. Run each arm in a fresh output
directory and preserve its command, output, stderr, exit status and resource log.

| Tool (reported version) | Argument pattern | Experiment settings |
|---|---|---|
| TRF (4.10.0rc2) | `trf FASTA 2 7 7 80 10 50 MAXP -ngs -h` | human 500; Col-CEN 200; maize SSR/knob+TR-1/CentC 6/500/200; no extra `-l 6` |
| tantan (51) | `tantan -f4 FASTA`; widened `tantan -f4 -w MAXW FASTA` | original window 100; reruns human 2000, Col-CEN 500, maize 500 and 200 |
| ULTRA (1.2.1), original human/Col-CEN | `ultra -t 2 -o OUT.tsv FASTA` | default period ceiling 100 |
| ULTRA, maize | `ultra --read_all -p MAXP -t 2 -i 3 -d 3 --bed -o OUT FASTA` | SSR/knob+TR-1/CentC ceilings 6/500/200 |
| ULTRA, Col-CEN p500 | `ultra -t 2 -p 500 -o OUT.tsv FASTA` | successful job 5981977; command confirmed in [recovered execution log](docs/2026-09-10-benchmark-launchers/ultra_colcen_p500_5981977.out.txt) |
| mreps (original report 2.6.01) | `mreps -fasta -res 5 -allowsmall RECORD.fa` | human per-record attempt; incomplete, not a complete scored human baseline |
| mreps, Col-CEN | `mreps -fasta -maxperiod 6 -res 10 RECORD.fa`; rerun `mreps -fasta -minperiod 150 -maxperiod 400 -res 10 RECORD.fa` | split FASTA per record; original container wide attempt failed, later local rerun succeeded |
| NCRF (1.01.02) | `NCRF NAME:MOTIF ... < FASTA` | Col-CEN CEN159+CEN178; maize TAG adds `--minlength=200`, knob180+TR1 and CentC use `--minlength=500` |
| TRASH (v1), de novo | `TRASH_run.sh FASTA --o OUTDIR --par 2` | maize additionally uses `--def`; maize CentC de novo did not finish |
| TRASH, template | de novo command plus `--seqt TEMPLATE.csv --horclass CLASS` | CEN159, CEN178, TAG, knob180, TR1, CentC; requires actual external CSV |
| longdust (1.4, g9491215) | `longdust FASTA`; `longdust -k8 -w20000 FASTA` | both on all three genomes; emits intervals, not periods |
| AniAnn's (0.7.1, 0d79851) | `anianns annotate -f FASTA -d OUTDIR -j 2 -q` | all three genomes; no classification database; output per-sequence BED files |

**Known command-description discrepancy:** Supplementary Table S15 / K5 also
attributes the maize-style ULTRA flags to the Col-CEN rerun. Job 5981977's
successful log instead records the simpler p500 TSV command above. That source
conflict is documented in the [recovery record](docs/2026-09-10-benchmark-launchers/);
no benchmark value was changed to resolve a command-description error.

Example stream capture, with `FASTA` set to the selected experiment's input,
`MAXP`/`MAXW` from the matrix, and `RAW` a fresh per-genome/per-arm directory:

```bash
RAW="$OUT/raw-selected-arm"
mkdir -p "$RAW"
RUNNER=()  # locally installed tool; use (singularity exec /path/to/image) only if available
/usr/bin/time -v "${RUNNER[@]}" trf "$FASTA" 2 7 7 80 10 50 "$MAXP" -ngs -h \
  > "$RAW/trf.dat" 2> "$RAW/trf.time"
/usr/bin/time -v "${RUNNER[@]}" tantan -f4 -w "$MAXW" "$FASTA" \
  > "$RAW/tantan.out" 2> "$RAW/tantan.time"
/usr/bin/time -v "${RUNNER[@]}" ultra -t 2 -o "$RAW/ultra.tsv" "$FASTA" \
  > "$RAW/ultra.stdout" 2> "$RAW/ultra.time"
# NCRF motif strings must be the exact consensus, not just the family name.
"${RUNNER[@]}" NCRF TAG:TAG --minlength=200 < "$FASTA" > "$RAW/tag.ncrf"
longdust "$FASTA" > "$RAW/longdust.bed"
longdust -k8 -w20000 "$FASTA" > "$RAW/longdust_k8w20000.bed"
anianns annotate -f "$FASTA" -d "$RAW/anianns" -j 2 -q
```

For all original commands, including NCRF's full consensus strings, follow the
individual [GNU-time logs](results/competitor_logs/). Their command blocks are
argv renderings; multiline `bash -c` quoting and outer stream redirection may
not survive, so do not blindly paste them as executable shell. Some records
show failed/incomplete runs. Human TRF p2000 and
[ULTRA p2000](results/range_cost_attempts/ultra_p2000/) were stopped incomplete;
the latter used `ultra -t 2 -p 2000 -o OUT.tsv FASTA`. Treat their elapsed time
as a lower bound, not completion cost or percentage processed. No source-grounded
TideHunter command was recovered and no completed arm is claimed here.

### Conversion and human scoring

Source interfaces: [conversion](scripts/scoring/convert_to_bed.py),
[2026 conversion](scripts/scoring/convert_2026_tools.py), and
[human regeneration wrapper](scripts/scoring/score_table1_regen.py).
BWTandem native BED column 5 is copies; converted competitors usually store a
period there. TRF's converted motif field can contain the full array sequence.
Check schema/coordinates rather than renaming raw files to `.bed`.

```bash
"$PY" scripts/scoring/convert_to_bed.py --tool trf \
  --input "$RAW/trf.dat" --output "$OUT/trf.bed"
# Same interface: --tool tantan, ncrf, mreps, trash, ultra (correct raw schema required).
"$PY" scripts/scoring/convert_2026_tools.py longdust "$RAW/longdust.bed" "$OUT/longdust.bed"
"$PY" scripts/scoring/convert_2026_tools.py anianns "$RAW/anianns" "$OUT/anianns.bed"
```

**Destructive batch behavior:** `convert_to_bed.py --batch --results-dir RAW
--output-dir DEST` recursively deletes an existing DEST before reconstruction.
Only use a new disposable destination. Its directory-layout and union rules
are not a generic single-file conversion contract; never aim it at `results/`
or retained data. Human mreps correction is separately available as
`reconvert_mreps_human.py INPUT OUTPUT --primary-only`; it does not complete
an incomplete detector run.

Human wrappers require these files under `$CB`:
`trf/GCA_000001405.15_GRCh38_genomic_output.bed`,
`tantan/GCA_000001405.15_GRCh38_genomic_output.bed`, and
`trash/GCA_000001405.15_GRCh38_genomic_trash.bed`, plus the separate ULTRA BED
passed below. These external inputs are mandatory, not downloaded by a scorer.

```bash
human_args=(--bwt-bed "$OUT/regen_human.bed" --gt "$DATA/adotto_primary.bed"
            --competitor-root "$CB" --ultra-bed "$WP0/beds/ultra_human_GCA.bed"
            --adj published,loo)
"$PY" scripts/scoring/score_table1_regen.py "${human_args[@]}" \
  --workdir "$OUT/score_human_work" > "$OUT/score_table1.txt"
# Native panel is appended as diagnostics to the full-range baseline.
"$PY" scripts/scoring/score_table1_regen.py "${human_args[@]}" \
  --extra "tantan-w2000:$WP0/fixcampaign/tantan/tantan_human_w2000.bed" \
  --extra "BWT-P-p100:$OUT/bwt_human_P_p100.bed" \
  --extra "BWT-B-p100:$OUT/bwt_human_B_p100.bed" \
  --extra "BWT-F-p100:$OUT/bwt_human_F_p100.bed" \
  --extra "BWT-H-p100:$OUT/bwt_human_H_p100.bed" \
  --workdir "$OUT/score_p100_work" > "$OUT/score_table1_p100.txt"
extras=(--extra "tantan-w2000:$WP0/fixcampaign/tantan/tantan_human_w2000.bed")
for arm in off 0.80 0.76 0.72 0.68; do
  extras+=(--extra "idsweep-${arm}:$OUT/bwt_human_idsweep_${arm}_p2000.bed")
done
"$PY" scripts/scoring/score_table1_regen.py "${human_args[@]}" "${extras[@]}" \
  --workdir "$OUT/score_idsweep_work" > "$OUT/score_table1_idsweep.txt"
for frac in 0.25 0.50; do
  RECIP_F="$frac" "$PY" scripts/scoring/score_table1_reciprocal_regen.py \
    "${human_args[@]}" --workdir "$OUT/recip_$frac" > "$OUT/recip_$frac.txt"
done
```

Reciprocal threshold is environment variable `RECIP_F`, not a CLI flag. Leave
it unset for one-base scoring. `--chroms chr21,chr22` or its complement gives
chromosome-subset rescoring; this is not independent training/validation after
those data have already been used for parameter selection. Native p100 and
post-filtered full-range results must remain separately labelled.

For strict one-to-one matching, compare annotation-coordinate and padded-region
truth separately ([method and retained outputs](results/one_to_one/)):

```bash
"$PY" scripts/scoring/derive_adotto_annotated_truth.py "$DATA/adotto_TRregions_v1.2.1.bed" \
  --restrict-to "$DATA/adotto_primary.bed" > "$OUT/adotto_annotated.bed"
"$PY" scripts/scoring/score_one_to_one.py "$OUT/adotto_annotated.bed" "$OUT/regen_human.bed" \
  --min-overlap 0.5 --truth-chroms-only --json "$OUT/one_to_one_bwt_annot.json"
"$PY" scripts/scoring/score_one_to_one.py "$DATA/adotto_primary.bed" "$OUT/regen_human.bed" \
  --min-overlap 0.5 --truth-chroms-only --json "$OUT/one_to_one_bwt_region.json"
# Converted competitors: add --pred-col5 period.
# Converted TRF also needs --pred-motif-is-sequence.
# Split truth-period bands: --strata 1-6,7-20,21-100,101-500,501-2000
```

The retained human annotation truth has no primitive-period records above 500 bp;
these commands do not validate the entire advertised search ceiling. Period
length agreement is not motif-sequence identity.

### Plant and 2026-tool scoring

Col-CEN uses deposited truth and explicitly supplied regenerated/widened outputs:

```bash
COLCEN_GT="$REPO/results/ground_truth" COLCEN_BEDS="$CB" \
  "$PY" scripts/scoring/score_colcen.py "regen:$OUT/regen_colcen.bed" \
  "tantan-w500:$WP0/fixcampaign/tantan/tantan_colcen_w500.bed" \
  "ULTRA-p500:$WP0/beds/ultra_colcen_p500.bed" \
  "mreps-150-400:$WP0/beds/mreps_colcen_150_400.bed" > "$OUT/score_colcen.txt"
```

Legacy default rows can print `(missing)`; that is not a scored zero. This
scorer's `--validate` option checks an older BWTandem row, not the regenerated
output. CEN180 period-filtered and unfiltered metrics use different call sets.
The [template-only TRASH union](results/regen/colcen_trash_template_union.bed)
is deposited; its producer template CSVs remain external.

For maize 3B/3C's original scoring rule, override roots explicitly:

```bash
BWT_MAIZE_GT_ROOT="$REPO/results/ground_truth" BWT_COMPETITOR_BEDS="$CB" \
BWT_WP0="$WP0" BWT_REGEN_MAIZE_BED="$OUT/regen_maize.bed" \
BWT_SCORE_EXP3="$REPO/scripts/scoring/score_exp3.py" \
  "$PY" scripts/scoring/rescore_tables_3bc.py
```

**Output-side effect:** this script writes `table3bc_results.json`,
`table3bc_replacement.md`, and `table3bc_provenance.json` beside itself in
`scripts/scoring/`. Run in a disposable full checkout if preserving a clean
tree. It needs historical and regenerated BWT BEDs plus comparator files;
setting only the regenerated path is insufficient. The exact source layout is
in [the script](scripts/scoring/rescore_tables_3bc.py) and the
[deposited provenance](results/regen/table3bc_provenance.json).

Coordinate-only post-merging is a **separate diagnostic**, not a replacement
for the original table's raw-call boundaries/fragmentation rule:

```bash
"$PY" scripts/scoring/score_maize_postmerge_regen.py --bwt-bed "$OUT/regen_maize.bed" \
  --gt-root "$REPO/results/ground_truth" --competitor-root "$CB" --wp0-root "$WP0" \
  --score-exp3 "$REPO/scripts/scoring/score_exp3.py" 0 100 1000 10000 \
  > "$OUT/score_maize_postmerge.txt"
```

The explicit-input supplementary maize producer covers SSR/TAG counts, period
filtering and related evidence. Set each `TRF_*`, `ULTRA_*`, `TANTAN_*` variable
to the corresponding **converted BED** in the manifest; do not substitute a
p500 arm for the p200 CentC arm.

```bash
"$PY" scripts/scoring/score_maize_regen_evidence.py \
  --bwt "$OUT/regen_maize.bed" \
  --trf-3a "$TRF_3A" --ultra-3a "$ULTRA_3A" --tantan-3a "$TANTAN_3A" \
  --trf-3b "$TRF_3B" --ultra-3b "$ULTRA_3B" --tantan-500 "$TANTAN_500" \
  --trf-3c "$TRF_3C" --ultra-3c "$ULTRA_3C" --tantan-200 "$TANTAN_200" \
  --knob-gt "$REPO/results/ground_truth/mo17_knob180_arrays.bed" \
  --tr1-gt "$REPO/results/ground_truth/mo17_tr1_arrays.bed" \
  --centc-gt "$REPO/results/ground_truth/mo17_centc_arrays.bed" \
  --score-exp3 "$REPO/scripts/scoring/score_exp3.py" --output "$OUT/maize_extra_evidence.json"
```

2026-tool examples (use species-specific converted outputs; include a separate
`longdust-k8w20000:PATH` row for the second setting):

**Human scoring writes outside `$OUT`:** the 2026 wrapper does not expose a
work-directory option; its underlying scorer uses `scripts/scoring/work/`,
overwrites matching prepared filenames and deletes its prepared inputs afterward.
Run it in a disposable full checkout without retained files in that directory.
Redirecting stdout to `$OUT` does not relocate these intermediate writes.

```bash
BWT_TABLE1_GT="$DATA/adotto_primary.bed" \
  "$PY" scripts/scoring/score_2026_tools.py human \
  "longdust:$OUT/longdust.bed" "AniAnns:$OUT/anianns.bed" > "$OUT/score_2026_human.txt"
COLCEN_GT="$REPO/results/ground_truth" COLCEN_BEDS="$CB" \
  "$PY" scripts/scoring/score_colcen.py "longdust:$OUT/longdust_colcen.bed" \
  "AniAnns:$OUT/anianns_colcen.bed" > "$OUT/score_2026_colcen.txt"
BWT_MAIZE_GT_ROOT="$REPO/results/ground_truth" BWT_SCORE_EXP3="$REPO/scripts/scoring/score_exp3.py" \
  "$PY" scripts/scoring/score_2026_tools.py maize \
  "longdust:$OUT/longdust_maize.bed" "AniAnns:$OUT/anianns_maize.bed" > "$OUT/score_2026_maize.txt"
```

Human 2026-only scoring disables cross-caller corroboration; it cannot compute
that quantity without the required comparator set. longdust supplies no period,
so a period-filtered row is undefined, not an accuracy failure. For maize, read
the labelled gap/merge rule in output before comparing with original tables.
The earlier crashed human 2026 score file is not the authoritative completed run.

### Other analyses and integrity checks

These are additional retained interfaces, **not interchangeable scoring rules**.
Inspect their linked sources for legacy absolute paths before running.

| Analysis | Command / source | Limits |
|---|---|---|
| Generic overlap | [score_overlap.py](scripts/scoring/score_overlap.py) `GT.bed TOOL.bed[:LABEL] ... --chroms chr21,chr22` | path precedes label, unlike `--extra LABEL:PATH` |
| Out-of-catalog base decomposition | [fp_check_regen.py](scripts/scoring/fp_check_regen.py) `TOOL ADOTTO ULTRA TANTAN` | all four plain BED inputs required |
| Specificity sample | [sample_specificity_audit.py](scripts/scoring/sample_specificity_audit.py) `BWT_ONLY.bed FASTA OUTDIR --per-stratum 100 --seed 20260827` | needs the unmatched population first; creates sheet/key, not the missing historical plots |
| Unique-call properties | [analyze_unique_regions.py](scripts/scoring/analyze_unique_regions.py) `--tool BED --label NAME --workdir DIR` | external truth/comparator defaults; not biological validation |
| CEN180 identity strata | [score_cen180_identity_strata.py](scripts/scoring/score_cen180_identity_strata.py) `[LABEL:PATH ...]` | inspect external truth defaults |
| Family grouping | [catalog_blind_families.py](scripts/scoring/catalog_blind_families.py) `[BED] [TOPN]` | previous analysis used superseded output; no new family-discovery claim |
| Maize flanks | [analyze_maize_flanks.py](scripts/scoring/analyze_maize_flanks.py) `--min-flank 500 --max-flank 20000 --seed 20260804` | external inputs and detector imports |
| Legacy maize tables | [score_maize_3a.py](scripts/scoring/score_maize_3a.py), [score_maize_consistent.py](scripts/scoring/score_maize_consistent.py), [score_trash_maize.py](scripts/scoring/score_trash_maize.py), [score_exp3.py](scripts/scoring/score_exp3.py) | read hard-coded input/producer contracts; prefer explicit-input wrappers above where available |
| Figure inputs | [make_figure_inputs.py](scripts/scoring/make_figure_inputs.py) `--genome all --tracks-only` | writes under scripts; legacy inputs, not the final figure renderer |
| Presentation | [figure sources](results/figures/paper_figs/), [proof build instructions](submission/README.md) | rebuilding changes outputs; not part of read-only evidence verification |
| Pipeline triage | [triage_regen.py](scripts/benchmark/triage_regen.py) `NEW_BED OLD_BED FASTA --provenance JSON` | comparison/diagnosis, not a detector benchmark |
| Historical seeding ablation | `BWT_SEED_KTUPLE=0` versus `1`, Col-CEN, 4 workers, 1–2000 | set before Python import; historical `294f8ac`, not index-free pipeline or regenerated causal speed proof |
| Historical gap-fill ablation | normal setting versus `SAT_FILL_MIN_IDENTITY=1.01`, or `SAT_FILL_MIN_PERIOD=400 SAT_FILL_MAX_PERIOD=1000` | historical Col-CEN base omitted the relaxed short gate; see Methods S2; not a CLI disable option |

Read-only checksum checks (no detection or rescoring):

```bash
sha256sum -c results/manifest.sha256
(cd results/beds && sha256sum -c SHA256SUMS)
sha256sum -c submission/SHA256SUMS
```

Development tests execute code and may create caches, bytecode and native build
artifacts; they are separate from read-only checksum verification:

```bash
"$PY" -m pytest tests/ -q
```

`scripts/benchmark/hash_deposited_beds.sh` **rewrites** checksums; it is not a
read-only verifier. Original scheduler/environment/binary gaps, absent comparator
BEDs, missing audit images and unresolved native regression remain limitations.
No historical one/two-thread scaling command is presented as a matched regenerated
experiment where its input/build/job link could not be established.

## Documentation

- [MANUAL.md](MANUAL.md) — the reference: CLI, masking, tiers, output
  schemas, environment variables, testing, reproduction, troubleshooting
- [CONTRIBUTING.md](CONTRIBUTING.md) — development setup, CI expectations,
  repository artifact policy
- [CLAUDE.md](CLAUDE.md) — architecture notes and the complete sensitivity
  env-var list (kept in sync with the code by `tests/test_env_var_docs.py`)
- [manuscript.md](manuscript.md) — the short Application Note
- [supplementary.md](supplementary.md) — all tables, detailed methods and limitations;
  Methods S2 gives benchmark configurations and their provenance limits
- [manuscript_full.md](manuscript_full.md) — frozen long source after P4 and C-8
- [submission/](submission/) — author-review PDF/DOCX proofs and release/DOI gates
- [CHANGELOG.md](CHANGELOG.md) — release history
- [Repository rename record](docs/2026-09-10-repository-rename.md) — active URL changes,
  preserved historical evidence, and the distinction between current sources and frozen proofs

## Citation

If you use BWTandem, please cite the repository (see
[CITATION.cff](CITATION.cff)) until the paper is published; the citation
will be updated on acceptance.

## License

MIT — see [LICENSE](LICENSE).
