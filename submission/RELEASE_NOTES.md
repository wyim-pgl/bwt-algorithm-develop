# BWTandem v0.9.0 — manuscript-preparation snapshot

**Draft release. DOI pending Zenodo enablement. This is not the final journal
submission record.**

- Python package, CITATION.cff and Docker label use 0.9.0.
- Numerical/provenance corrections are preserved from `64964e1`.
- P4 consistency corrections (`7df3e6a`) and C-8 reconstruction (`94df01e`)
  precede the Application Note conversion.
- Short manuscript, full long source, complete supplement, PDF/DOCX proofs,
  and presentation-only figure copies are included; all 19 table blocks remain
  unchanged. Attachment integrity is recorded in `SHA256SUMS`.
- No benchmark reruns, scorer changes, evidence payload changes, Docker image
  publication or PyPI publication were performed. Benchmark execution commit
  `0363d8b` remains distinct from this later documentation/software snapshot.

## Limitations retained

Shared-range accuracy is non-leading; over-calling, memory, fragmentation and
period-assignment limitations remain explicit. The audit is single-reader and
not population-weighted. Some historical accounting, competitor outputs, image
provenance and external inputs remain unavailable. A layout-dependent native
regression issue remains unresolved; passing tests do not establish its absence.
Built-in defaults differ from the deposited benchmark configurations.

MIT license. Source and existing citation metadata are in the tagged tree.
A DOI, author declarations and final submission approval remain pending.
