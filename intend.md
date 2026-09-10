# intend.md — 다음 세션의 의도와 순서

> 📌 **정본**: "다음에 무엇을, 왜, 어떤 순서로" 는 이 파일. 살아 있는 상태는 `resume.md`,
> 할 일 전수는 `todo.md`, 폐기값은 `quarantine.md`, 운영 규칙은 `CLAUDE.md`.
> 최종 갱신 **2026-09-10**. 세션은 `resume.md` 상단 → 이 파일 → `todo.md` §0 순으로 읽고 시작한다.

## 변하지 않는 목적

BWTandem 을 Bioinformatics **Application Note** 로 제출한다. 증거 저장소(`results/`)가 공개되므로
원고의 셀 하나도 예치물 없이 존재할 수 없다. **Honest science only** — 벤치마크 게이밍·GT 과적합·
불리한 결과 은폐 금지. BWTandem 에 불리한 정정은 그대로 둔다.

## 지금의 의도

끊긴 ASTRA 리뷰(2026-09-05)를 **수습해 트리를 깨끗하게 만든 뒤**, 리뷰가 넘긴 항목을 장부에 통합하고,
그다음에야 저자 결정 항목(Abstract·App Note 전환·릴리스)으로 넘어간다. 순서를 바꾸지 않는다 —
더티 트리 위에서 원고를 더 고치면 어느 편집이 누구 것인지 다시 잃는다.

## 순서

> 미착수 항목의 등급(1 제출 전 / 2 공개 문장 / 3 제출 후)은 `todo.md` 머리 표. 아래 Phase 는 1·2등급만 다룬다; 3등급은 제출 뒤.

### Phase 0 — 트리 정리 (한 세션 안에 끝낸다) — ✅ 완료 2026-09-10 (`744ef3a`, `7556727`, 푸시됨)

1. `git diff manuscript.md` 를 **순서대로** 대조한다 — P2 보고서(`pass2-methods-vs-code.md`, §2·보충 Methods) →
   `pass3-edits.json`(46건 순차 치환; 21→22 는 연쇄) → P3 의 JSON 밖 후속 수정(`pass3.log:8123`, 현재 `manuscript.md:496`) →
   `precision-edits.json`(88건, `reverted` 6건 제외). **JSON 에 없는 잔여를 자동으로 P2 에 귀속하지 않는다.**
   출처를 복구하지 못한 편집은 `APPLIED-RATIONALE-NOT-RECOVERED` 로 기록해 채택 판단을 저자에게 남긴다. 각 hunk 를 P2 보고서의 해당 finding 또는 P3 의 json 근거와 연결한다.
   근거가 없는 hunk 는 **되돌린다**(폐기가 아니라 미채택 — `todo.md` 에 남긴다).
2. `results/` 15개 파일 diff 를 P1 보고서 REHASH REQUIRED 목록·각 finding 과 대조한다.
3. `quarantine.md` §8.2 순서: 편집 완료 → 포그라운드 재해시 → 체크섬 2개 포함 `git add` →
   `git diff --cached` 확인 + 미스테이징 `results/` 없음 → 가드 테스트 → 커밋.
4. 커밋은 둘로: (a) 채택한 원고·`results/` 편집 + 체크섬 2개, (b) 추적 장부 `intend.md`·`todo.md`·`quarantine.md` + `CLAUDE.md` +
   `docs/2026-09-05-astra-review/` + `docs/2026-09-10-precision/` + `docs/2026-09-10-ledger-review/`.
   `resume.md` 는 `.gitignore:24` 로 **비추적**이다 — 갱신은 하되 커밋 목록에 넣지 않는다.
   커밋 메시지에 P1/P2 verdict 수와 "P3 중단·보고서 없음" 을 적는다.

**완료 기준**: `git status --short` 에 추적 파일 변경·untracked 산출물이 없음(`resume.md` 는 ignored 라 원래 안 보인다),
`$PY -m pytest tests/test_deposit_hashes.py tests/test_env_var_docs.py tests/test_one_to_one_scoring.py -q` 녹색, 푸시.

### Phase 1 — P3·P4 마무리

- ✅ **결정됨 (2026-09-10, 저자)**: P3 는 **(a) 산출물로 보고서 재구성**. 재실행하지 않는다. 산출물은
  `pass3-results-tables.md` (재구성 표시 배너, 근거 못 찾은 편집은 `APPLIED-RATIONALE-NOT-RECOVERED`).
  > ❌ SUPERSEDED (2026-09-10): 옛 선택지 (b) 재실행은 채택되지 않았다. 재실행이 다시 필요해지면 `quarantine.md` §8.8.
- ✅ P3 보고서 재구성 완료 (2026-09-10). P3-16 편집 5건은 저자 채택(2026-09-10). 잔여: P3-14 차단 셀 4개 (`todo.md` §0-1).
- **Phase 1 내부 순서**: ~~P3 보고서 재구성~~ → Phase 1b(소수점 잔여) → 변경 검토·필요 시 재해시·커밋(트리 정리) → P4 → 같은 정리 절차.
  리뷰 패스 자체는 커밋·재해시·SLURM 제출을 하지 않으므로(BRIEF), 패스 전후에 사람이 정리한다.
- P4 는 P3 보고서가 있어야 의미가 있다. P3 없이 P4 를 돌리면 P3 편집을 P4 가 다시 의심한다.
- 두 패스 모두 BRIEF.md 계약 그대로: 커밋 금지, sbatch 금지, 재해시 금지, 부재→오류 승격 금지.

**완료 기준**: `pass3-*.md`·`pass4-*.md` 존재, 각각 Summary/Findings/REHASH REQUIRED/Not fixed 4절.

### Phase 1b — 소수점 두 자리 잔여분 (`todo.md` §0-4)

본문 1자리 **후보 토큰 118개를 먼저 분류**한다(절 번호·버전·파라미터·정의 상수는 제외) — 남는 측정값과 파생값(points·×·factor)만 예치 근거에서 재계산.
S2 여섯 셀은 원천 요약이 1자리라 되돌렸다; `analyze_unique_regions.py` 를 `:.2f` 로 재생성한 뒤에만 다시 넓힌다. 규칙은 `CLAUDE.md` "Numeric presentation"
(**decimal half-up**, 저자 결정 2026-09-10).
예치물이 없는 값은 건드리지 않고 목록에 남긴다. P4 전에 끝내면 P4 가 반올림 불일치를 다시 잡지 않아도 된다.

### Phase 2 — 리뷰가 넘긴 항목 통합

**완료 기준**: `todo.md` §0-2·§0-3 의 각 항목에 완료 근거(커밋·파일 경로) 또는 구체적 차단 사유가 적혀 있다.

`todo.md` §0-2(P1) · §0-3(P2). 대부분 `todo.md`·`quarantine.md`·CLAUDE.md 프로즈 편집이다.
`results/` 를 건드리는 항목(P1-08 원시 sacct 9건, P1-13 튜닝 원장)은 **한 번에 모아** 재해시 1회로 끝낸다.

### Phase 3 — 저자 결정 항목

C-8 Abstract → App Note 전환(표는 보충자료로 이동, 삭제 아님) → Fig 5 채택·최종 위치 확인(P3 가 이미 `manuscript.md:327–331` 에 삽입) → 릴리스(태그·Zenodo DOI·
제출본 스냅샷). 릴리스는 원고 확정 뒤. Bioinformatics 는 초록에 안정 아카이브 URL 을 요구한다.

**완료 기준**: 각 저자 결정이 `todo.md` 에 날짜와 함께 기록되고, 제출본 경로·태그·DOI 가 `resume.md` 상태표에 있다.

## 하지 말 것

- 더티 트리 위에서 새 리뷰 패스를 돌리지 않는다.
- `results/` 를 부분 편집 후 재해시하지 않는다 (§8.2).
- 4 GB 세션에서 전장 BED intersect·conda solve·pytest 루프를 돌리지 않는다 (§8.3·§8.8).
- 리뷰가 "BLOCKED-ON-MISSING-ARTIFACT" 로 둔 것을 오류로 승격하지 않는다 (지난 라운드 철회 4건의 실패 모드).
- `quarantine.md` §8.7 의 env 레버를 다시 시도하지 않는다.

## 세션 시작 절차

```bash
cd ~/scratch/devel/bwt-algorithm
grep -n '📌 \*\*정본' resume.md intend.md todo.md quarantine.md
git status --short | head; git log -1 --oneline
grep -n '^- \[ \]\|^- \[!\]\|^- \[?\]\|^- \[~\]' todo.md
SQ=/cm/shared/apps/slurm/current/bin/squeue; $SQ -u "$USER" || echo 'squeue FAILED — 0 으로 오독 금지'   # bwt 잡은 없어야 정상
PY=/data/gpfs/assoc/pgl/bin/conda/conda_envs/bwtandem/bin/python; $PY --version
```

python 은 로그인 셸 PATH 에 없다 — `/data/gpfs/assoc/pgl/bin/conda/conda_envs/bwtandem/bin/python`.
SLURM 명령은 `/cm/shared/apps/slurm/current/bin/`.

## 이 파일의 갱신 규칙

Phase 가 끝나거나 결정 지점이 해소될 때만 고친다. 상태 수치는 여기 적지 않는다(`resume.md`).
옛 의도를 지우지 말고 ❌/✏️ 마커로 표시한다.
