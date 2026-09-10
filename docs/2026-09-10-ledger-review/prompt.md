You are reviewing the four session-handoff ledgers of a scientific software repository (BWTandem, a tandem-repeat detector; manuscript for Bioinformatics). This directory is a READ-ONLY mirror of the repository on an HPC cluster (large data files excluded, .git excluded). Do not edit anything; produce a review only.

The four files under review, and the contract each claims for itself (read the header of each):
- resume.md   — living state + next actions; snapshots stack downward; old snapshots must carry markers (❌ SUPERSEDED / ⚠️ CAUTION / ✏️ PARTIAL / 🧊 ARCHIVED BELOW) with a date and a pointer to the current truth.
- intend.md   — intent and ordered plan for the next session (Phase 0..3), completion criteria, don'ts, start procedure. New file, created 2026-09-10.
- todo.md     — the sole ledger of unresolved work. Marks: [ ] unstarted, [~] in progress, [x] done (must carry ✅ date + evidence: commit hash / job id / file path), [!] blocked, [?] awaiting author decision.
- quarantine.md — the sole ledger of retired numbers, claims, names, job ids and methodological traps. Entries must be 무엇/왜/언제/대체물/근거. It must NOT hold unresolved work (that belongs in todo.md).

Context files you should read to check the ledgers' claims against:
- CLAUDE.md (operating rules; note the new "Numeric presentation" section)
- docs/2026-09-05-astra-review/BRIEF.md, pass1-evidence.md, pass2-methods-vs-code.md (completed review passes), pass3-edits.json, pass3-table-cells.tsv (an interrupted third pass; a report is being reconstructed separately — it may or may not exist yet as pass3-results-tables.md)
- docs/2026-09-10-precision/precision-report.md and precision-edits.json (a two-decimal normalisation applied to manuscript.md on 2026-09-10; rounding convention later switched to decimal half-up)
- docs/2026-09-03-finding-dispositions.md
- manuscript.md (only to spot-check that numbers quoted by the ledgers exist there)
- resume-archive-to-20260904.md (older snapshots, for provenance of claims)

Situation the ledgers describe: on 2026-09-05 a four-pass adversarial review ran; passes 1 and 2 completed, pass 3 was cut off mid-command and the host job later died of OOM, pass 4 never ran. The working tree is dirty (manuscript + 15 results/ files), checksums not regenerated, nothing committed. On 2026-09-10 the ledgers were rewritten for a clean handoff, and two author decisions were recorded (rounding = decimal half-up; pass 3 = reconstruct from artifacts).

Review the four files for a reader who will start a fresh session, read only these files (plus CLAUDE.md), and must resume correctly. Check specifically:

1. Internal contradictions between the four files (dates, commit hashes, counts, verdict tallies, file paths, job ids, which decisions are open vs closed, what is dirty vs committed).
2. Claims that are now stale but carry no marker, or markers that lack a date or a pointer to the current truth. Check the "Where things stand" table and section 5/6 of resume.md especially.
3. todo.md hygiene: [x] items without evidence; [ ] items that are actually done per other files; duplicated items (e.g. Fig 5 placement appears in more than one section); items that belong in quarantine.md instead, and vice versa.
4. quarantine.md hygiene: entries missing 무엇/왜/언제/대체물/근거; unresolved work that should be in todo.md; numbers that contradict CLAUDE.md, the pass reports, or precision-report.md; whether §2's 2026-09-10 table and §8.9 agree with the half-up decision; whether §1.4 and §8.8 state the OOM cause as an inference rather than a fact.
5. intend.md: does its Phase order agree with todo.md §0 and resume.md "다음 작업"? Are completion criteria checkable? Are there instructions a fresh session cannot follow (missing paths, commands that would not work)?
6. File references: for every path mentioned in the four files, check whether it exists in this mirror (note: large data files, .git and some directories are excluded from the mirror; distinguish "excluded from mirror" from "genuinely missing" by the exclusion list: *.gz, *.bed, *.dat, build/, *.egg-info, arabadopsis_chrs/, benchmarking/, files over 5 MB).
7. Anything that would mislead a fresh session into repeating a known mistake (see quarantine §8 traps) or into treating an absence of an artifact as an error.

Output, in Korean with quoted originals in their own language, as Markdown:

# Ledger review — <date>
## Summary            (counts by severity; the single most dangerous inconsistency for a fresh session)
## Findings           (one block each: id L-NN; severity CRITICAL/HIGH/MEDIUM/LOW; file:line; the quoted text; what is wrong and the evidence file:line; a re-runnable check (grep/python one-liner); proposed replacement text)
## Cross-file consistency table   (for each fact that appears in ≥2 files — tip commit, dirty-file counts, pass verdict tallies, precision edit counts, decisions — list the value each file gives)
## Broken or unverifiable references
## Not a problem, checked   (things that looked wrong but are fine, so nobody re-raises them)

Rules: absence of an artifact is not evidence of an error; do not invent numbers; anchor every finding to file:line; do not propose restructuring the files, only targeted edits.
