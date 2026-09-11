# Pre-submission provenance disclosures — 2026-09-10

Scope authorized by the author: remaining numeric presentation, TR-1 statistic definitions, and priority-2 provenance disclosure. This is not ASTRA P4, an Abstract rewrite, a benchmark rerun, or submission-readiness certification.

Baseline: remote `pronghorn:~/scratch/devel/bwt-algorithm`, branch `perf/exp1-human-sensitivity`, clean commit `139e361`. Baseline guard suite: 43 passed, 1 skipped. `resume.md`'s older tip `7556727` was a stale snapshot, not the working tip.

## Dispositions

| Item | Action | Evidence and remaining limit |
|---|---|---|
| P3-14 / P1-08 | Disclose, values unchanged | `pass1-checks.py sacct` confirms nine producer tasks without deposited raw rows: `6141841_0`, `6143150_1–3`, `6143151_0–4`. Table 1d's four runtimes remain manifest transcriptions. Wrapper JSON process accounting is not substituted for scheduler cgroup accounting. No scheduler recovery or new execution was attempted. |
| P1-11 | Align S4 provenance; append C-10 completion | P3 already added the `903245c` TRF exception and restricted split-run equivalence to matching/strata. Clarify that the correction is not attributed to the original `43543da` execution. Corrected JSON changes five numerical period fields and adds `strata_spec`; split TRF period statistics remain superseded. JSON is not modified. |
| P1-13 | Disclose incomplete final-selection trace | Re-executed `pass1-checks.py ledger`: 44 rows, 22 config / 22 code, 17 pending including `f_cp3`. Earlier `best.json` final configuration is not a complete final decision history. No accept/reject outcomes are invented; ledger bytes remain unchanged. |
| P1-15 | Align attempt wording and observed-cost scope | Cancelled TRF and ULTRA elapsed ratios remain lower bounds for their attempt environments. Emitted output coordinate is not percentage processed. ULTRA files only self-report the same version; binary/environment identity is not claimed. Remove the unjustified shared-node-to-isolated-node upper-bound inference for the widened tantan timing; no timing value is replaced on that ground. |
| P1-19 | Disclose visual and reader/population provenance limits | `results/audit11/` lacks original 400 images, renderer/settings, source population BED and separate reader attestation. Sampler makes sheet/key, not images. New visualizations would not establish the original presentation. Manuscript and README both say so. Recorded verdicts are not invalidated or edited. |
| P2-22 | Qualify environment reconstruction | Preserve the existing reported 3.11.14/2.3.1 whole-genome and 3.11.15/2.4.6 later-panel versions. Describe PATH probe versus detector interpreter, partial tuning headers, absent complete inherited environments and native-binary identities. Today's environment cannot fill those historical gaps. |
| P2-23 | Qualify orphan settings row | Keep the thread-scaling row as unverified historical settings, not a currently reported pair or regenerated scaling result. No inferred inputs/build/job identity or invented timing. |
| P2-24 | Qualify original competitor versions/container | Original logs preserve `singularity exec ./bwtbench.sif` and flags, not immutable snapshot, version inventory or container format at execution. Retain original versions as author-reported; qualify S1 and competitor-log README. |
| P2-13 follow-up | Comment-only correction | `environment.yml`, `environment.core.lock.yml`, `Dockerfile`: later environment pins only, not all published executions. Dependencies and commands unchanged. Docker version reconciliation remains the separate release task. |
| External launchers | Choose authorized weaker-claim alternative | Native-p100, identity-sweep and historical seeding launchers remain external; S2 explicitly says this is not a self-contained reproduction package for those executions. Existing whole-genome and paired-range launchers are still linked. No launcher archive was manufactured. |

Raw BEDs, scorer outputs, run provenance JSONs, tuning ledger, verdicts, and table timing/cgroup transcriptions remain unchanged. Only two evidence READMEs are edited; rehash them with the full established script after all edits, never concurrently with another `results/` change.

## Checks

- `python docs/2026-09-05-astra-review/pass1-checks.py sacct`
- `python docs/2026-09-05-astra-review/pass1-checks.py ledger`
- `python docs/2026-09-05-astra-review/pass1-checks.py audit`
- `python docs/2026-09-05-astra-review/pass1-checks.py s4`
- `bash scripts/benchmark/hash_deposited_beds.sh` (after all results edits)
- `python -m pytest tests/test_deposit_hashes.py tests/test_env_var_docs.py tests/test_one_to_one_scoring.py -q`

Final command results are recorded separately; the list above is not a claim that every command has already run.
