# todo.md — BWTandem 남은 작업

> 📌 **정본**: 이 파일이 "앞으로 할 일"의 유일한 정본이다 — **미해결은 전부 여기 있다.**
> 이미 틀렸거나 시도해서 안 됐거나 배제된 것은 [`quarantine.md`](quarantine.md),
> 살아 있는 상태는 `resume.md`, 운영 규칙은 `CLAUDE.md`.
> 최종 갱신 **2026-09-10**. 다음 세션의 순서·완료 기준은 [`intend.md`](intend.md).

## 표기 규약

| 마크 | 뜻 |
|---|---|
| `- [ ]` | 미착수 |
| `- [~]` | 진행 중 |
| `- [x]` | **완료** — 뒤에 `✅ (YYYY-MM-DD, 근거)` 를 붙인다 |
| `- [!]` | 차단됨 — 뒤에 `⛔ 무엇에 막혔는지` 를 붙인다 |
| `- [?]` | 저자 결정 대기 — 내가 임의로 정할 수 없는 것 |

**완료 표시 규칙**: 체크만 바꾸지 말고 **근거**(커밋 해시, 잡 ID, 파일 경로)를 같은 줄에 남긴다.
근거 없는 완료는 다음 세션이 다시 조사한다.

```bash
grep -n '^- \[ \]' todo.md    # 미착수
grep -n '^- \[!\]' todo.md    # 차단
grep -n '^- \[?\]' todo.md    # 저자 결정 대기
```

## 우선순위 등급 (2026-09-10, 저자 지시)

미착수 37건은 세 등급으로 나뉜다. 항목은 원래 절에 그대로 두고(절 번호를 `resume.md`·`intend.md`·`quarantine.md` 가
참조한다) 각 줄 머리에 등급 태그를 붙였다. **전부 다 할 필요는 없다** — 3등급은 제출 뒤로 미루거나 버린다.

| 등급 | 뜻 | 건수 | 묶음 |
|---|---|---:|---|
| **[1·제출 전]** | 제출에 반드시 필요 | 15 | Phase 0 트리 정리(§0-1 4건) · 소수점 잔여(§0-4 L79·80·81·84) · §6.12 · P4 · Abstract · App Note 전환 · 릴리스(#14 포함) |
| **[2·공개 문장]** | 값은 안 바꾸고 "예치 근거 없음/한계" 를 한 문장씩 적는 정직성 공개. **한 번에 몰아 재해시 1회** | 11 | P3-14+P1-08 · P1-11 · P1-13 · P1-15 · P1-19 · P2-22/23/24(S2 한계 문장) · P2-13 후속 · 외부 런처 예치(또는 자기완결 주장 약화) |
| **[3·제출 후]** | 내부 위생·선택. 제출과 무관 | 11 | bedtools 교차검증 · sacct 세대 마커 · CLAUDE.md 아키텍처 · 장부 위생 3건 · S2 재생성 · 그림 라벨 · 스코어러 출력 · 처분표 재대조 · Kimi 잔여 |

실제로 해야 할 덩어리는 여덟 개다: **Phase 0 → 소수점 잔여 → §6.12 → 공개 문장 일괄(2등급 전부) → P4 → Abstract → App Note 전환 → 릴리스.**

```bash
grep -n '^- \[ \] \*\*\[1' todo.md    # 제출 전
grep -n '^- \[ \] \*\*\[2' todo.md    # 공개 문장 일괄
grep -n '^- \[ \] \*\*\[3' todo.md    # 제출 후
```

---

## 0. ASTRA 리뷰 수습 — 2026-09-10 추가, **먼저 할 것**

> 배경: 2026-09-05 ASTRA 4패스 중 P1·P2 완료, **P3 중단(보고서 없음), P4 미착수**, 호스트 세션 OOM.
> 상세는 `resume.md` 상단, 순서·완료 기준은 `intend.md`, 사고 기록은 `quarantine.md` §1.4·§8.8.

### 0-1. 트리 정리 (Phase 0)

- [ ] **[1·제출 전]** `git diff manuscript.md` 출처 대조 — 순서: P2 보고서 → `pass3-edits.json`(46 순차 치환, 21→22 연쇄) → `pass3.log:8123` 의 JSON 밖 수정(`manuscript.md:496`) → `precision-edits.json`(88). **잔여를 자동으로 P2 에 귀속하지 않는다**; 출처 미복구 편집은 `APPLIED-RATIONALE-NOT-RECOVERED` 로 표시해 저자 판단 (Codex 장부 리뷰 L-01·L-02)
- [ ] **[1·제출 전]** `results/` 15개 diff 를 `pass1-evidence.md` 의 REHASH REQUIRED 목록·각 finding 과 대조
- [ ] **[1·제출 전]** `quarantine.md` §8.2 순서로 **재해시 → 체크섬 포함 `git add` → `git diff --cached` → 가드 테스트 → 커밋**
- [ ] **[1·제출 전]** 커밋 2개 후 origin 푸시 — (a) 채택 원고·results 편집 + 체크섬 / (b) `intend.md`·`todo.md`·`quarantine.md`·`CLAUDE.md` + `docs/2026-09-05-astra-review/`·`docs/2026-09-10-precision/`·`docs/2026-09-10-ledger-review/`. `resume.md` 는 비추적(`.gitignore:24`) (L-13)
- [x] **P3 복구 방식 — 저자 결정: (a) 산출물로 보고서 재구성** ✅ (2026-09-10) 재실행 없음
- [x] P3 보고서 재구성 ✅ (2026-09-10, `docs/2026-09-05-astra-review/pass3-results-tables.md` 36 KB + `pass3-reconstruct.py`) — 13 CONFIRMED / 1 REJECTED(586 셀 일치) / 1 BLOCKED / 1 APPLIED-RATIONALE-NOT-RECOVERED(5 편집). 표 셀 8개가 예치물과 달랐고 전부 경쟁 도구 값이 BWTandem 에 불리한 쪽으로 정정됨. `results/` 는 P3 가 건드리지 않았다(15개는 전부 P1 몫)
- [x] **P3-16** 근거 미복구 편집 5건 — **저자 결정: 5건 전부 채택** ✅ (2026-09-10) E19(L188 tantan 비용: 검증 불가 단정 제거, 사실만), E26(L294: 예치값 58.6845−58.5042=0.1803 → 0.18 정확), E35(L188: 범위 차이는 §2.2·quarantine §3.5 기록), E39(L543: 위성 실험은 period 배정을 검증하지 않음), E47(L496: C-2 결정과 정합 — 네이티브 p100 F 실행은 1b 민감도 분석). 근거: `pass3-results-tables.md` P3-16 + 2026-09-10 세션 대조(`docs/2026-09-10-ledger-review/p3-16-decision.md`)
- [ ] **[2·공개 문장]** **P3-14** Table 1d 런타임 셀 4개(잡 6141841_0, 6143150_1–3) — 원시 sacct 부재로 BLOCKED. P1-08 과 같은 묶음으로 처리
- [ ] **[3·제출 후]** **P3 미완 교차검증** — Table 1a 의 새 unique 카운트 3개(TRF 18,904 / ULTRA 518,440 / tantan 518,488)는 `pass3-checks.py human` 한 방법에만 의존. 독립 `bedtools intersect -v` 검증은 OOM 으로 미완 — 원하면 별도 sbatch(≥16 GB, §8.8)로
- [ ] **[1·제출 전]** P4(원고 일관성) 실행 — BRIEF.md 계약 그대로
- [ ] **[1·제출 전]** `resume.md` 스냅샷 갱신 (Phase 0·1 끝날 때마다)

### 0-2. P1 이 넘긴 통합 항목 (`pass1-evidence.md` "Not fixed, and why")

- [ ] **[3·제출 후]** **P1-07** sacct 예치 두 세대 구분 — 9월 3일 예치(34 할당) vs 9월 4일 재수집(37 할당 / 40 잡-태스크). `todo.md` D 절·요약문의 "34" 에 마커
- [ ] **[2·공개 문장]** **P1-08** 네이티브 p100·identity-sweep 9개 태스크의 cgroup 셀(`manifest.tsv:89–98`) — 원시 sacct 를 복구·예치하거나 "예치 원시 근거 없음" 을 명시. 값은 바꾸지 않는다
- [ ] **[2·공개 문장]** **P1-11** S4 TRF 보정 팔 출처 — 원고 S4 의 `43543da`/6146229 "metric-identical" 출처 문장에 TRF-only 예외를 달고, C-10 JSON 교체 완료를 `todo.md`·`quarantine.md` 에 append
- [ ] **[2·공개 문장]** **P1-13** 튜닝 원장(`results/tuning_ledger/`) — 예치 완료와 "최종 선택 규칙 추적 가능" 을 구분. pending 17건은 남은 기록으로만 설명, 사후 accept/reject 발명 금지
- [ ] **[2·공개 문장]** **P1-15** 원고 전수 검색 — "처리 비율(percentage processed)", "버전 일치", "취소된 실행 비용 비율" 문장을 `results/range_cost_attempts/README.md`·`comparator_baselines.md` 정정과 맞춘다 (취소 실행은 **하한**으로 유지)
- [ ] **[2·공개 문장]** **P1-19** `results/audit11/` 원본 이미지·렌더러 설정·판독자/모집단 출처 — 복구하거나 "정확한 시각 재현 불가" 를 README 와 원고에 명시 (R2-6/R3-2 의 산출물 한계와 동일; 오류로 승격 금지)
- [x] **P1-14** Figure README 정정은 P1 완료; Fig 5 는 P3 가 삽입 완료(D 절 참조) ✅ (2026-09-10, L-03)

### 0-3. P2 가 넘긴 통합 항목 (`pass2-methods-vs-code.md` "Not fixed, and why")

- [ ] **[3·제출 후]** **P2-18** `CLAUDE.md:318–355` 아키텍처 요약을 코드에 맞춘다 — 10 Mb 임계값(실제는 mode 0/1/2), Tier 3 고정 k=20/stride=100(실제 적응형), gap 규칙, "Smith-Waterman"(실제 semi-global prefix edit distance), ≤2% 요약. **코드를 옛 서술에 맞추지 말 것**
- [ ] **[2·공개 문장]** **P2-22** 상속 환경·바이너리 신원 — 전체 게놈(3.11.14/2.3.1) vs 패널(3.11.15/2.4.6) 환경의 완전한 기록이 없다. 복구하거나 S2 에 한계 명시 (BLOCKED)
- [ ] **[2·공개 문장]** **P2-23** 고아 thread-scaling 설정 행 — **Supplementary Methods S2 설정표**(`manuscript.md:502` "Thread-scaling pair"; P3 셀 파서가 3C-b 로 잘못 분류했던 행) — 예치 근거를 찾거나 행을 한정 (BLOCKED) (위치 정정 L-20)
- [ ] **[2·공개 문장]** **P2-24** 옛 경쟁 도구 버전·컨테이너 빌드 재구성 불가 — 원고 S2 와 `results/competitor_logs/README.md` 에 명시 (BLOCKED)
- [ ] **[2·공개 문장]** **P2-13 후속** `environment.yml:6`·`environment.core.lock.yml:1`·`Dockerfile:16` 주석을 "후기 환경만 동결" 로 한정
- [ ] **[2·공개 문장]** 외부 런처 예치 — p100·identity-sweep·seeding-ablation 의 sbatch/래퍼를 `results/` 아래로 (저장소 자기완결 주장 전에). `results/` 편집이므로 0-2 의 P1-08·P1-13 과 **한 번에** 재해시
- [x] P2 의 quarantine 항목(P2-01·06·08·12 폐기 문구, P2-03 의 R3-14 재개, §3.7 Methods 제거) ✅ (2026-09-10, `quarantine.md` §3.7 마커·§3.11–3.15)

### 0-5. 장부 위생 — Codex 장부 리뷰 (2026-09-10, `docs/2026-09-10-ledger-review/`) 잔여분

- [x] 21건 중 즉시 반영분: L-01·02·03·04·05·06·07·08·09·10·11·12·13·14·15·19·20·21 ✅ (2026-09-10, 이 파일·`resume.md`·`intend.md`·`quarantine.md`·`CLAUDE.md`·`manuscript.md:528–530` 되돌림; 처분은 `docs/2026-09-10-ledger-review/dispositions.md`)
- [ ] **[3·제출 후]** **L-16** `todo.md` 완료행 날짜·근거 보강 — `✅ (날짜, 커밋/경로)` 없는 `[x]` 행(A-1 의 09-03 적용분 등)에 근거를 붙인다. 커밋 해시는 `git log -S` 로 복구; 복구 안 되면 "확인 대기" 표시
- [ ] **[3·제출 후]** **L-18** `quarantine.md` 항목 형식 공백 — §3.2·3.3·3.5·3.6·4.1·4.2·8.7·9.2 에 언제/근거 경로 보강. 확인 안 되는 날짜는 "미확인" 으로 두고 추정 금지
- [ ] **[3·제출 후]** **L-20 후속** `quarantine.md` 의 옛 코드 경로(`c_extensions/align_accel.c`, `scripts/score_overlap.py`)에 "당시 경로" 표시 + 현행 경로 병기; `run_fullgenome.sbatch` 의 전체 외부 경로 확인

### 0-4. 수치 표기 — 소수점 두 자리 통일 (2026-09-10 저자 지시, 규칙은 `CLAUDE.md` "Numeric presentation")

- [x] 표 셀 1자리 → 2자리 **59건**(65 적용 − S2 6셀 되돌림) + 본문 인용 24곳 + 문맥 지정 5곳(TRF 5.22/5.51/5.48 h, core-hours 25.29/59.56/33.73) ✅ (2026-09-10, `docs/2026-09-10-precision/precision-edits.json` 88건 유효, `reverted` 6건 표시)
- [ ] **[3·제출 후]** **S2 여섯 셀 재생성** — `results/regen/s2_F_p100.txt` 가 1자리(38.9/46.4, 13.2/24.8, 21.9/6.1)라 되돌렸다(L-09). `scripts/scoring/analyze_unique_regions.py` 의 `:.1f` 를 `:.2f` 로 바꿔 요약을 재생성·예치(재해시)한 뒤 다시 넓힌다
- [ ] **[1·제출 전]** **본문 1자리 후보 토큰 118개 — 먼저 분류** — `docs/2026-09-10-precision/precision-report.md` "Remaining 1-dp tokens" 가 목록. 절 번호(2.1, 2.2, 3.x)·버전(longdust 1.4)·파라미터·정의 상수는 **제외**하고(L-11), 남는 측정값만 예치물에서 재계산(자릿수 덧붙이기 금지). 큰 묶음: %(L21·L78·L86·L94·L119·L121), kb 오프셋(L70·L248·L250·L294), calls-per-array(L250), range-cost "6.6 h→4.0 h / 8.6→7.3"(L105, `quarantine.md` §2 의 4.02/4.11/4.02 · 7.31/7.28/7.13 로), "6.6 days"(L38·L78·L107 — **TRF** p2000 취소 실행 잡 `6076847`, 6-13:57:48, `results/sacct_provenance.txt:40–42`; 취소 실행은 완료비용 **하한** 한정 유지, L-12), Wilson CI(L119·L121). 분류 후 실제 측정값 건수를 여기 기록
- [ ] **[1·제출 전]** **파생값 전수 재계산** — "points", "percentage points", "×"/"times", "factor of" 가 붙은 문장을 grep 해 예치 전정밀도 값에서 다시 계산(반올림 셀끼리 뺀 값 금지). §6.8 과 R2-9 가 이 계열
- [ ] **[1·제출 전]** E26 후속 — L294 "span approximately 0.18 points" 의 **"approximately" 삭제** (예치값 차이 0.1803, 두 자리 0.18 정확; 저자 채택 2026-09-10)
- [ ] **[3·제출 후]** 그림 주석 — `plot_fig4_plant_satellites.py`·`plot_figS2_postmerge.py` 의 `:.1f` 라벨을 `:.2f` 로, 재렌더는 `bwtandem` env 로(재렌더 자체는 별도 결정)
- [ ] **[3·제출 후]** 스코어러 콘솔 출력 `:.1f`/`:.3f` (`fp_check*.py`, `analyze_unique_regions.py`, `score_cen180_identity_strata.py`, `score_maize_3a.py`) → `:.2f`. 예치 JSON 은 전정밀도라 결과값은 안 바뀐다; 출력을 다시 예치할 때만 재해시
- [ ] **[1·제출 전]** 원고 Methods 에 표기 규칙 한 문장(측정값 2자리, 예치물에서 계산, 파라미터는 원형)
- [x] **반올림 규약 — 저자 결정: decimal half-up** ✅ (2026-09-10, `docs/2026-09-10-precision/reapply_halfup.py`) 94건 재적용, `:.2f` 와 달라진 값 6곳(12.645 h → **12.65** ×5, 58.845 → **58.85**). 기존 2자리 셀 345개(유니코드 음수 포함 349)는 half-up 과 전부 일치(감사 결과 `precision-report.md` 부록; "586" 은 P3 셀 판정 REJECTED 수였다, L-10). `normalize_precision.py`·`CLAUDE.md` 규칙 갱신


---

## A. 원고 결함 수정 — 내가 고칠 수 있는 것

`quarantine.md` §6 의 확정 결함 중 값·문구 교체로 끝나는 것. §6.17/C-1은
`0363d8b` 재측정값으로 2026-09-04에 적용했다.

### A-1. 원고만 수정 (재해시 불필요, CI 위험 없음)

- [x] **§6.7** Table 3C-b 캡션: "smallest banded loss" → TRF 0.87 이 최소. 차이값 14.36 → **14.88** ✅ (2026-09-03, `2901ff3`; tantan 손실은 뒤의 R2-9 로 0.92 → **0.91** 재정정, L-08)
- [x] **§6.8** "at most 1.5 / 2.8 points" → 실제 최대 **1.54 / 2.81** ✅ (2026-09-03, `2901ff3`) → ❌ 2.81 은 뒤의 R2-9 로 **2.82** 재정정(예치본 뺄셈; 원고 현행 2.82). 이 행의 2.81 을 복사하지 말 것 (L-08)
- [x] ~~**§6.9** Table 1c: 캡션은 네 도구, 표는 세 행~~ — **오탐으로 철회** ✅ (2026-09-03, `quarantine.md` §6.9; 수정한 것이 아니다, L-16)
- [x] **§6.10** 본문 107행에 TRF 의 precision 두 값 추가 (97.18% vs 64.60%, 31.19 vs 29.25)
- [x] **§6.11** Table 2 캡션에 BWTandem 의 CEN180 bp precision 최저(57.08%) 사실 한 문장
- [x] **§6.13** S4 캡션 "lowest of the five tools" → **second-lowest** (tantan 3.42% < 8.68%)
- [x] **§6.14** "All competitor runs ... inside one Singularity container" → 예외 2건 명시
- [x] **§6.21** "at least 70%" → **80%**, catch-all 에도 적용됨을 공개
- [x] ~~§6.6 stride 공식~~ · ~~§6.16 stride 축소 모순~~ — **오탐으로 철회** ✅ (2026-09-03, `quarantine.md` §6.6·§6.16)
- [x] **§6.5** "roughly 5% more sequence" → 두 값을 같은 단위(염기)로 재계산 후 교체
- [x] **§6.4** 2026 도구 메모리 셀 2개: AniAnn's Col-CEN 0.50 → **0.48**, longdust 0.07 → **0.06**
- [ ] **[1·제출 전]** **§6.12** TR-1 경계 오차 네 값(771 bp / 4.3 kb / 4,265 / 7,973)의 통계 정의 후 일치
- [x] **§6.24** Discussion 4.3 — Tier 1 도 FM-index 열거를 돌린다(`TIER1_FMSCAN=1`). 메커니즘 서술 정정
- [x] **§6.25** Abstract 의 "per-figure provenance manifest" 약속 삭제 (매핑 0건, 그림 프로그램 6/6 스텁)
- [x] **§6.26** S1.3 파라미터 범위를 "핵 염색체 5개"로 한정하거나 ChrC/ChrM 값 추가
- [x] **Codex R3-10** Discussion 4.2 에 게놈×패스 행렬 명시 — 어블레이션이 있는 것과 없는 것을 구분
- [x] **Codex R3-12** Limitations 에 native-path flake 명시 ✅ (2026-09-03) §4.4 에 네 번째 한계로 추가 — 소진된 진단과 재현 불가 사유까지
- [x] **Codex R2-9** 밴드 손실 반올림 ✅ (2026-09-03) 예치본 기준 전수 정정 — 3C-b 표 −0.92→−0.91, 캡션 0.92→0.91, 3B-b 캡션 0.50→0.51, ULTRA 상계 2.81→**2.82**(내 앞선 수정도 뺄셈이라 틀렸다), §4.4 의 같은 주장도
- [x] **Codex R2-8(정정)** 전체 게놈 실행은 3.11.14/2.3.1 이 맞다 — 다른 것은 p100 패널·식별도 스윕이며,
      S2 에 그 별도 환경을 공개했다. 매니페스트 스코어러 해시 2건은 `results/` 라 A-2 로 이월
- [x] 원고 전체 **GiB/GB 라벨 37곳 교체** ✅ (2026-09-03, 숫자 불변)

### A-2. `results/` 수정 — ⚠️ 재해시 필수

**순서 엄수** (`quarantine.md` §8.2 — 2026-09-03 정정): 모든 편집 완료 → **재해시(포그라운드, 또는 wait 로 완료 확인)** →
그 다음 체크섬 2개 포함 `git add` → `git diff --cached` 확인 + 미스테이징 results 변경 없음 → 테스트 → 커밋.
**옛 순서(`git add` 를 먼저)는 위험하다** — 스테이징엔 옛 해시, 워킹트리엔 새 해시인 커밋이 나온다.
재해시 중 `results/` 를 건드리지 않는다. 아래 넷을 **한 번에** 처리해 재해시를 1회로 끝낸다.

- [x] **§6.1** Table 2 TRASH 비용 셀 ✅ (2026-09-03, `e232bcf`) template 행을 **CEN159+CEN178 397행 합집합**으로 재정의·재채점 — 비용 **31:41:09 = 31.69 h / 2.63 GiB**, de novo 는 별도 5:47:30 = 5.79 h (`results/regen/colcen_trash_template_scored.txt:9–13`, 원고 Table 2). ❌ 37:28:39 는 de novo 를 포함한 폐기 계약의 합계 — 인용 금지 (L-07)
- [x] **§6.2** `results/manifest.tsv:67` — 정정 전 문장 4개를 원고 현행 문구로 교체 ✅ (2026-09-04, `da9e484` 이후) 네 주장 전부 교체 — 다른 바이너리·자기보고 버전·하한 표시·마지막 출력 위치
- [x] **§6.3** AniAnn's 스레드 `1` → `2` (매니페스트 행 123·126·129·132) ✅ (2026-09-03, `e232bcf`)
- [x] **Codex 발견 11** tantan 스레드/명령: 실제 활성 스레드 1, 확장 명령(`-w 500/2000/200`) 명시. ✅ (2026-09-04) 할당 2 CPU / 활성 1 스레드를 네 행에 명시
- [x] **Codex 발견 14** 매니페스트의 `PENDING` 행 5개(8, 16–19)를 superseded 로 표시하거나 분리 ✅ (2026-09-04) `1b-superseded`/`1d-superseded` + 기동 실패 사유
- [x] ~~재해시 후 pytest~~ — **항목 아님**: A-2 절차의 마지막 단계이지 독립 항목이 아니다
- [x] **Codex 라운드 2** — Results ↔ 예치 산출물, 9건 ✅ (2026-09-03, `docs/2026-09-03-codex-review-round2.md`)
- [x] **Codex 라운드 3** — Discussion 메커니즘 ↔ 코드, 14건 ✅ (2026-09-03, `docs/2026-09-03-codex-review-round3.md`)
- [x] R2·R3 의 최중대 6건 실물 검증 후 §6 에 추가 ✅ (2026-09-03, §6.22–6.26 · §3.10)
- [ ] **[3·제출 후]** ~~R2·R3 의 나머지 17건 검증 또는 명시적 기각~~ / ~~Codex 첫 리뷰의 미검증 14건~~ → ✏️ **재정의 (2026-09-10, L-04)**: `docs/2026-09-03-finding-dispositions.md:95–99` 에 따르면 Codex R1–R3 43건은 **전부 판정 완료**(CONFIRMED 17 / RESOLVED 14 / PARTIAL 10 / DUPLICATE 1 / REJECTED 1). 남은 작업은 처분표의 **CONFIRMED 17 + PARTIAL 10** 을 P1/P2/P3 후속 증거와 대조해 아직 열린 것만 갱신하는 일이다. R3-14 는 `quarantine.md` §3.15 로 재개됨
- [ ] **[3·제출 후]** Kimi 라운드 1–3 의 MEDIUM/LOW 중 미검증분 선별 검증
- [x] ~~`TIER2_APPROX_SEED` at identity ≥ 0.88~~ — **제외** (2026-09-03): 미시험 연구 방향이지
      논문 작업이 아니다. `quarantine.md` §9.3 으로 이관
- [x] **C-1. Tier 3 탐색 창 — (b) `0363d8b` 재실행 적용** ✅ (2026-09-04)
      SLURM `6147698`·`6147699`·`6147700` 세 쌍의 비율은 **1.82 / 1.77 / 1.77
      (평균 1.79, 범위 1.77–1.82)**. p100은 6.6 h→4.0 h, p2000은 8.6 h→7.3 h로
      줄었다. `07ad6fa`에서 p100 arm이 장주기 탐색을 수행하고 결과를 버려 기존
      1.30–1.41(평균 1.34)이 너무 유리하게 낮았다. 원고·manifest·Figure 2 소스·격리 대장에 반영.
- [x] **C-2. matched-range — (a) 사후필터로 통일** ✅ (2026-09-03) Table 1b 행·캡션·본문 교체, 네이티브 재실행(79.88/50.62)은 민감도 분석으로 강등
- [x] **C-3. 튜닝 캠페인 — (a) 최소 공개 채택** ✅ 본문 반영 (2026-09-03, `d580840`) · ⏳ 원장 예치는 A-2 재해시와 함께 ✅ 본문 반영 (`d580840`) + 원장 예치 (`e4ae632`, `results/tuning_ledger/`)
- [x] **C-4. catch-all 0.72 — (a) 최소 공개 채택** ✅ (2026-09-03, `d580840`) S3 에 in-sample 명시
- [x] **C-9. AniAnn's 밴드 셀 — (a) 사전등록 준수** ✅ (2026-09-03) 예치돼 있던 셀을 Table 1b·1c·§3.2 에 반영, 캡션의 거짓 배제 사유 정정
- [x] **C-10. TRF period 열 복구 + S4 재채점 — 저자 지시대로 수행** ✅ (2026-09-03) 스코어러 2곳 수정, 테스트 교체(39 passed), TRF period-exact **63.53%**, 원고 S4 반영. ⏳ 예치 JSON 교체는 A-2 재해시와 함께
- [x] **C-11. Arabidopsis catch-all off — (a) 최소 공개 채택** ✅ (2026-09-03, `d580840`) S2 에 65.54 vs 60.72 와 보류셋 부재 명시
- [x] **C-5. TRASH = de novo** ✅ (2026-09-03, 저자 결정: TRASH 에 de novo 모드가 있다) — 326행을 human 한정으로 좁히고 TRASH 를 de novo 로 재분류. §6.15
- [x] **C-6. 투고처 — Bioinformatics Application Note** ✅ (2026-09-03, 저자 결정)
- [x] **C-7. 제목 — 현행 유지** ✅ (2026-09-03) `BWTandem: FM-index seeding for wide-period-range tandem repeat detection in assembled genomes` — 저자가 지정한 문구가 원고 현행과 동일. **#27(FM-index 인과 프레이밍 지적)은 저자 유지 결정으로 종결**
- [ ] **[1·제출 전]** **C-8. Abstract 재구성 — 전체 이슈 정리 후로 연기** (저자 결정 2026-09-03)
---

## D. 재실행·재측정이 필요한 것

- [ ] **[1·제출 전]** **App Note 전환 실행** — 계획서는 있고 전환된 원고는 없다. 본문 약 24,500 단어,
      표가 전부 본문에 있다. 표는 삭제가 아니라 **보충자료로 이동**한다
- [ ] **[1·제출 전]** **릴리스** — LICENSE·CITATION.cff·pyproject·CI 는 이미 있다. 없는 것은 **태그·DOI·제출본 스냅샷**.
      Bioinformatics 는 초록에 안정 아카이브 URL 을 요구한다
- [x] **Fig 5 본문 참조·이미지·캡션 삽입** ✅ (2026-09-05, P3 — `manuscript.md:327–331`; `pass3-edits.json` 마지막 항목). 미커밋 편집의 채택 검토는 §0-1 에서 (L-03)

- [x] **§6.20** `sacct -j ... --format=JobID,Elapsed,MaxRSS,State -P` 원문을 체크섬과 함께 예치. ✅ (2026-09-03, `e4ae632`) 34개 잡 sacct 예치, 헤드라인 3개 정확히 일치
- [x] **§6.27** Col-CEN 밴드 recall 을 재생성 BED 로 재채점 — 원고의 91.31/94.68 은 예치 출처가 없다 ✅ (2026-09-03, `e4ae632`) **오탐이었다** — 재생성본이 91.31/94.68 을 그대로 준다. 산출물만 없었고 이제 예치됨
- [x] **TRF S4 JSON 교체** — `results/one_to_one/one_to_one_trf_annot_r50.json` 을 재채점본으로. ✅ (2026-09-03, `e4ae632`)
- [x] **원장 예치** — `exp1_human/loop/{ledger.tsv,best.json}` 를 `results/` 에 예치 (C-3 (a) 의 나머지 절반). ✅ (2026-09-03, `e4ae632`) `results/tuning_ledger/` + README
- [x] **§6.19** 누락 스코어러 3개 커밋 — `rescore_tables_3bc.py`, `score_exp3.py`, `score_overlap.py`. ✅ (2026-09-03, `e4ae632`) 3개 커밋 + 클러스터 경로를 env 오버라이드로
- [x] **Codex 발견 9** CEN180 identity 층화를 재생성 BED 로 재채점, 다섯째 층(99–100%, 100 monomers) 포함 ✅ (2026-09-03, `e4ae632`) 재생성본으로 재채점, 다섯째 층 추가
- [x] **Codex 발견 8** §2.2.4 채점 경로 정확화 ✅ (2026-09-03) "no second scoring implementation exists" 는 거짓 — human 은 EXTRA·argv 도 덮고, maize 는 `score_maize_postmerge.py`(좌표 전용 진단)를 쓰지 정본 `rescore_tables_3bc.py` 가 아니다
- [x] **#30** 경쟁 도구 GNU-time 로그 예치 + 해시 (현재 저장소 밖) ✅ (2026-09-03, `e4ae632`) 40개 예치, 5개 도구 전부 재현 확인
- [x] **Codex 발견 10** CEN180 진실셋 생성 과정(BLAST 버전·명령·원시 68,840 hit) 복구 또는 ✅ (2026-09-03, `e4ae632`) **원시 hit 68,840개가 살아 있었다** — 예치하고 원고 정정
- [ ] **[1·제출 전]** **#14** [HIGH] 잔여 범위 = 릴리스 태그·버전 정합성(`pyproject` 0.9.0 vs Docker LABEL v1.0)·아카이브(DOI). LICENSE·CITATION.cff·CI 는 **이미 있다** — 생성 작업이 아니다 (L-15)
- [x] **#26** 2026-tool 벤치마크 반영 ✅ (2026-09-03) C-9(a) 로 Table 1b·1c·§3.2 에 진입, 본문 언급 32곳 · **GitHub 닫힘**
- [x] **#27** 제목의 FM-index 인과 프레이밍 — **저자 유지 결정으로 종결** ✅ (2026-09-03, C-7)
- [x] ~~#28~~ — **C-8 에 흡수**: Abstract 재구성 안에서 함께 처리된다
- [x] ~~#29~~ — **C-1 에 흡수**: 재실행 결과가 이 주장의 운명을 정한다
- [x] **#30** — 위 D 절의 #30 완료 기록과 동일 사실; 여기는 GitHub 종료 이력만 · **GitHub 닫힘** (L-21)
- [x] **#31** deposit-hash 워크플로 ✅ 완화됨 — `tests/test_deposit_hashes.py` 가 오늘 두 번 잡아냈고,
      순서는 `quarantine.md` §8.2 에 성문화. 스크립트 자체 재작성은 하지 않는다 · **GitHub 닫힘**
- [x] **#32** 동등성 주장에 검사 첨부 ✅ `24cd12a`·`ccf04dd`·`e8ac50c` 가 두 건 모두 처리.
      재발 방지는 `quarantine.md` 의 "대체물 없으면 없음이라 적는다" 규약이 맡는다 · **GitHub 닫힘**
- [~] **#33** 2차 의견 리뷰 — Kimi 3라운드·Codex 4라운드 **전부 완료**. 남은 것은 미검증분 처리(B절)
      > ✏️ **PARTIAL (2026-09-10):** "B절" 은 없다 — 미검증분은 A-2 의 세 항목(R2·R3 17건 / 첫 리뷰 14건 / Kimi MEDIUM·LOW). ASTRA 4패스(2026-09-05)는 P1·P2 만 완료, P3 중단·P4 미착수 — §0-1.

---

## F. 기타

> ⚠️ **SLURM 제출 함정 (2026-09-03)**: 이 환경은 `SBATCH_PARTITION`·`SBATCH_ACCOUNT`·**`SBATCH_TIMELIMIT`**
> 를 export 해 두고 있어 `--time` 이 무시된다(24h 요청이 13-23:00:00 이 됐다). `resume` 의 회피법
> `SBATCH_X= sbatch` 는 `SBATCH_TIMELIMIT` 에서는 *빈 시간 스펙* 오류를 낸다. **`env -u` 로 지울 것**:
> `env -u SBATCH_PARTITION -u SBATCH_ACCOUNT -u SBATCH_TIMELIMIT sbatch --partition=cpu-s2-core-0 --account=cpu-s2-pgl-0 ...`
> s1 은 자기 6일짜리 annotation 잡으로 늘 막혀 있다 — 이걸로 시작 예정이 9/5 에서 즉시로 바뀌었다.

- [x] **origin 푸시** ✅ (2026-09-03) `67f11b1..f57fcb0`, 21 커밋
- [x] 위키의 "미커밋" ⚠️ 정리 + 개명 반영 ✅ (2026-09-03, wiki `50e863d`)
- [!] **flaky `TestAdjacentGroundTruth::test_sensitivity`** ⛔ 클러스터 ASLR 이 꺼져 있어
      실패 레이아웃에 도달 불가. 관리자에게 노드 1대 ASLR 재활성화 요청 필요 (`quarantine.md` §9.1)
- [x] **Filip 그림 6개 — 전달 완료 (2026-09-03), 통합됨** ✅ (2026-09-03, `340316f`·`bc3aafc`) 6개 통합·재렌더, BWTandem 강조 팔레트
- [x] `quarantine.md` 신설 (§1–§10, 폐기 대장) ✅ (2026-09-03, `0357cbd`)
- [x] resume.md 격리 — 📌 정본 포인터 + ❌ MOVED 배너 4곳, 앵커 0 broken ✅ (2026-09-03, `0357cbd`)
- [x] Codex 2차 의견 리뷰 전사본 예치 ✅ (2026-09-03, `0357cbd` / `docs/2026-09-03-codex-review-findings.md`)
- [x] Kimi 원고 교차검증 라운드 1–3 (11청크, 타임아웃 0) ✅ (2026-09-03, `docs/2026-09-03-kimi-{review,recheck,thirdpass}-*.md`)
- [x] Codex 원고 라운드 1 (코드 ↔ 원고 대조) ✅ (2026-09-03, `docs/2026-09-03-codex-review-findings.md`)
- [x] 확정 결함 21건을 `quarantine.md` §6 에 기록 ✅ (2026-09-03, 전건 실물 파일 재현)
- [x] 랩 위키 반영 ✅ (2026-09-03, wiki `eecf950`)
