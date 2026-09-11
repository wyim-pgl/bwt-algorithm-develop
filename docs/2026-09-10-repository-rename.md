# Repository rename and benchmark README (2026-09-10)

## Scope

At the author's request, GitHub repository `wyim-pgl/bwt-algorithm` was renamed
to `wyim-pgl/bwt-algorithm-develop`. The canonical working directory remains
Pronghorn `~/scratch/devel/bwt-algorithm/`. Its `origin` now points to
`https://github.com/wyim-pgl/bwt-algorithm-develop.git`; the `framazan` remote
was not changed. Package, executable and project name remain BWTandem / `bwtandem`.

Starting commit: `3653947c1875d0c406170dd3411a84cd2ba19325` on `main` (clean).
This was the merge of `perf/exp1-human-sensitivity`; earlier handoff ledgers
refer to pre-merge snapshots and do not change the current branch.

## Active changes

- README: new clone URL, development status, corrected provenance/architecture
  statements, benchmark commands and explicit reproduction prerequisites/limits.
- `CITATION.cff`: repository URL only; authors, version and date unchanged.
- `pyproject.toml`: repository/issues/documentation URLs; no dependency, version,
  executable or implementation change.
- `manuscript.md` and `supplementary.md`: repository URL replacement only.
- `submission/README.md`: current repository and source/proof distinction.
- GitHub repository description: development code, commands, evidence and sources.

## Preservation contract

New read-only documentation copies in `docs/2026-09-10-benchmark-launchers/`
preserve two recovered external detector launchers and the successful ULTRA
Col-CEN p500 log. Their README records source paths, byte-matched SHA-256 hashes
and a follow-up correction needed for Supplementary Table S15 / K5. These files
were not previously tracked by the starting commit and do not retroactively
complete the historical accounting or binary provenance.

No benchmark was rerun and no numerical result was edited. `results/`, frozen
`manuscript_full.md`, historical audit/replay documents, proof PDF/DOCX files,
presentation figures and payload checksums are unchanged. Old URLs in those
artifacts remain historical records. The current source URL consequently
postdates the frozen proof outputs; the proofs were not regenerated during this
rename. Historical replay scripts may expect the old source URL and need a new
approved proof workflow before being used to certify a future rendering.

Annotated `v0.9.0` tag object remains
`90309451970efb3cd7ad0f7c775688f20ca2619d`, targeting
`ef98c03c8710dfb529d2cab0cbe7231080ab07f6`.
Release ID `386640503` was rechecked as draft, not published. Its assets were not
replaced. No DOI was created, no Zenodo integration was configured, and no
PyPI/container release was published.

## Verification

- GitHub preflight: administrator permission, `main` default branch, no Pages
  site, no configured repository webhooks, unprotected `main`, target name absent.
- Rename verified via GitHub API; requesting the old repository endpoint resolves
  to `wyim-pgl/bwt-algorithm-develop`. New URL works with `git ls-remote`/fetch.
  This does not certify redirects for every third-party service or an archive.
- After active metadata/source edits, three full-suite runs on Pronghorn each
  returned **219 passed, 1 skipped**. This does not resolve the known native
  layout-dependent regression or establish benchmark accuracy.
- Frozen tracked evidence/proofs had no diff against `3653947`; all 18
  submission payload checksum checks passed.
- After the README expansion, focused deposit-hash, environment-documentation
  and one-to-one-scoring guards returned **43 passed, 1 skipped**.
- A final three-run full-suite check after the README expansion also returned
  **219 passed, 1 skipped** per run. Read-only command review then identified two
  documentation cautions: the 2026 human scorer's implicit working-directory
  writes and pytest's cache/build side effects. Both warnings are now explicit;
  no implementation or test was changed.
- Static documentation checks: 26 shell blocks passed `bash -n`; the embedded
  Python preparation example compiled; the tuning-reset helper removed injected
  catch-all/cache settings while retaining explicitly selected overrides.
  README relative file links and 13 internal anchor references resolved; TOML
  parsed and retained package/version identity. Manuscript diffs were URL-only.
- README examples are source-linked historical invocations or explicitly adapted
  templates. They require the documented external data/tools; syntax validation
  alone does not establish that a complete benchmark can run from a clean clone.
