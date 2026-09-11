# Codex 장부 리뷰 처분 — 2026-09-10

리뷰어: Codex CLI 0.153.4, 모델 `gpt-6-astra`, reasoning `high`, `--sandbox read-only`, 로컬 미러(데이터 파일·.git 제외).
프롬프트: `prompt.md`. 원문: `codex-review.md`. 검증: 21건 전부 pronghorn 원본에서 재확인했다(`~/scratch/tmp/verify_codex.py`).

| ID | 심각도 | 처분 | 어디에 반영 |
|---|---|---|---|
| L-01 | HIGH | CONFIRMED · 반영 | resume.md "원고 diff 의 출처", intend.md Phase 0-1, todo.md §0-1 |
| L-02 | MEDIUM | CONFIRMED · 반영 | resume.md 요약·상태표, quarantine.md §1.4 |
| L-03 | HIGH | CONFIRMED · 반영 | todo.md D(Fig 5 → [x] 2026-09-05 P3), §0-2 P1-14, intend.md Phase 3, resume.md 다음 작업 |
| L-04 | HIGH | CONFIRMED · 반영 | todo.md A-2 두 행 재정의(처분표 CONFIRMED 17 + PARTIAL 10 재대조) |
| L-05 | HIGH | CONFIRMED · 반영 | quarantine.md §6 머리 CAUTION 마커 |
| L-06 | HIGH | CONFIRMED · 반영 | quarantine.md §2 SUPERSEDED 행, §5 5983792 행, §8.6 CAUTION |
| L-07 | HIGH | CONFIRMED · 반영 | todo.md A-2 §6.1, quarantine.md §6.1 대체값 마커 |
| L-08 | MEDIUM | CONFIRMED · 반영 | todo.md A-1 §6.7/§6.8, quarantine.md §6.7/§6.8 |
| L-09 | HIGH | CONFIRMED · 반영 | manuscript.md:528–530 여섯 셀 되돌림, precision-edits.json `reverted`, CLAUDE.md, todo.md §0-4 재생성 항목 |
| L-10 | MEDIUM | CONFIRMED · 반영 | CLAUDE.md, resume.md, todo.md (586 → 345/349) |
| L-11 | MEDIUM | CONFIRMED · 반영 | resume.md, intend.md 1b, todo.md §0-4 (측정값 118 → 후보 토큰 118, 분류 선행) |
| L-12 | HIGH | CONFIRMED · 반영 | todo.md §0-4 (TRASH → TRF p2000, 잡 6076847) |
| L-13 | HIGH | CONFIRMED · 반영 | intend.md Phase 0-4·완료 기준, todo.md §0-1, resume.md 상태표 |
| L-14 | MEDIUM | CONFIRMED · 반영 | intend.md Phase 1 내부 순서, Phase 2·3 완료 기준 |
| L-15 | MEDIUM | CONFIRMED · 반영 | resume.md 다음 작업 2, quarantine.md §1.4, todo.md #14 범위 |
| L-16 | MEDIUM | CONFIRMED · 부분 반영 | §6.9 행을 철회로 표시; 나머지 날짜·근거 보강은 todo.md §0-5 |
| L-17 | MEDIUM | CONFIRMED · 반영 | quarantine.md §3.4(189)·§3.7·§3.8·§3.9·§3.10·§6.17(573)·§6.23(661·677) 마커 |
| L-18 | MEDIUM | CONFIRMED · todo 이관 | todo.md §0-5 (추정으로 채우지 않는다) |
| L-19 | MEDIUM | CONFIRMED · 반영 | intend.md 시작 절차(전체 경로 squeue, 실패 감지, `$PY -m pytest`), resume.md §5 CAUTION |
| L-20 | MEDIUM | CONFIRMED · 반영 | todo.md P2-23 위치 정정, msreview 경로 4곳 → docs/2026-09-03-*; 옛 코드 경로 표기는 §0-5 |
| L-21 | LOW | CONFIRMED · 반영 | quarantine.md §2 중복 행 표시, todo.md #30 둘째 행 |
| (부록) | — | CONFIRMED · 반영 | `normalize_precision.py` dry-run 이 `precision-edits.json`·보고서를 덮어쓰던 문제 → `*.dryrun.*` 로 분리; 1자리 예치값은 거부 |

기각한 항목: 없음. "Not a problem, checked" 절의 확인 사항(half-up 결정 일관, 94건 집계, OOM 추정 표기, 34 vs 37/40 세대, C-1 비율, R3-14 재개 형식)은 그대로 유효하다.
