# Ledger review — 2026-09-10

## Summary

| 심각도 | 건수 |
|---|---:|
| CRITICAL | 0 |
| HIGH | 9 |
| MEDIUM | 11 |
| LOW | 1 |
| **합계** | **21** |

가장 위험한 불일치는 **원고 diff에서 P3 JSON에 없는 부분을 P2로 귀속하고, 근거가 없으면 되돌리라는 지시**입니다. 9월 10일 precision 편집 94건뿐 아니라 **P3가 JSON 기록 후 추가한 수정**도 있습니다. 현재 절차로는 정당한 편집을 잘못 분류하거나 취소할 수 있습니다.

파일은 수정하지 않았습니다. 아래 줄 번호는 검토한 미러 기준입니다. `.git`과 HPC 접근이 없으므로 현재 HEAD·푸시·SLURM 상태는 직접 검증하지 않았습니다. P3 보고서는 검토 종료 시점에도 없었으며, 이를 오류로 판정하지 않았습니다.

## Findings

### L-01 — HIGH — 편집 출처 판별 절차가 불완전하여 정상 편집을 되돌릴 수 있음

**위치:** `resume.md:38`, `todo.md:36`, `intend.md:23–25`

> “P3 의 45건을 빼고 남는 것이 P2 몫이다.”  
> “둘을 빼고 남는 것이 P2 몫.”  
> “근거가 없는 hunk 는 **되돌린다**”

**문제와 근거:** resume/todo는 precision 편집을 누락합니다. intend는 precision JSON을 포함하지만, 두 JSON도 완전한 편집 원장은 아닙니다. `pass3.log:8123`에는 JSON 작성 이후의 설정표 수정이 있고, 현재 `manuscript.md:496`에 적용되어 있습니다. 이 수정은 P2 잔여분이 아닙니다. 또한 같은 hunk에 여러 단계의 편집이 겹칠 수 있습니다.

**재검사:**

```bash
grep -nF '1b sensitivity analysis, 1d' manuscript.md docs/2026-09-05-astra-review/pass3.log docs/2026-09-05-astra-review/pass3-edits.json
```

**제안 문구:**

> 원고 diff를 P2 보고서, P3 편집 JSON과 후속 로그(`pass3.log:8123` 포함), precision 편집 JSON에 순서대로 대조한다. JSON에 없는 잔여분을 자동으로 P2에 귀속하지 않는다. 출처를 복구하지 못한 편집은 `APPLIED-RATIONALE-NOT-RECOVERED`로 기록하여 채택 판단을 남긴다.

---

### L-02 — MEDIUM — “46건 중 45건 적용”은 실행 건수와 최종 문자열 수를 혼동함

**위치:** `resume.md:13,27`, `todo.md:36`, `quarantine.md:98–106`

> “원고 편집 46건 중 45건을 적용”  
> “46쌍, 45건이 `manuscript.md` 에 존재”

**문제와 근거:** `pass3.log:7925`는 **“Applied 46 targeted replacements”**라고 기록합니다. JSON의 21번째 치환 결과를 22번째가 다시 치환합니다(`pass3-edits.json:83–88`). 따라서 중간 문자열 하나가 남지 않는 것은 미적용 증거가 아닙니다. 후속 precision 편집 때문에 현재 완전일치 문자열 수도 달라집니다.

**재검사:**

```bash
python3 -c 'import json; e=json.load(open("docs/2026-09-05-astra-review/pass3-edits.json")); print(len(e), e[20]["new"]==e[21]["old"])'
```

결과: `46 True`.

**제안 문구:**

> P3 로그는 순차 치환 46건의 성공을 기록한다. 한 치환 결과는 다음 치환으로 즉시 대체되었으므로 최종 문자열 45개와 실행 46건을 구분한다. 이후 JSON 밖 설정표 수정과 precision 편집도 적용되었다.

---

### L-03 — HIGH — Fig 5를 다시 배치하도록 안내함

**위치:** `todo.md:53,151`, `intend.md:57`, `resume.md:46,160–162`

> “Fig 5 를 원고에 배치 — 그려졌지만 아직 참조되지 않는다”

**문제와 근거:** 현재 `manuscript.md:327,329,331`에 본문 참조·이미지·캡션이 모두 있습니다. P3 JSON 마지막 항목(`pass3-edits.json:182–184`)이 그 삽입을 기록합니다. P1 보고서의 미배치 상태는 P3 이전 상태입니다.

**재검사:**

```bash
grep -n 'Figure 5' manuscript.md
```

**제안 문구:**

> `- [x] Fig 5 본문 참조·이미지·캡션 삽입 ✅ (2026-09-05, manuscript.md:327–331; docs/2026-09-05-astra-review/pass3-edits.json 마지막 항목). 미커밋 편집의 채택 검토는 §0-1에서 수행.`

§0-2의 중복 체크행은 이 항목을 가리키는 일반 참조로 바꾸고, intend의 “배치”는 “기존 배치의 채택·최종 위치 확인”으로 한정합니다.

---

### L-04 — HIGH — 이미 판정된 Codex 발견 31건을 미검증으로 되돌림

**위치:** `todo.md:123–124,173`, `resume.md:46,96`

> “R2·R3 의 나머지 17건 검증 또는 명시적 기각”  
> “Codex 첫 리뷰의 **미검증 14건** 처리”

**문제와 근거:** `docs/2026-09-03-finding-dispositions.md:95–99`는 세 Codex 라운드에 미검증 항목이 없다고 명시합니다. 역사적 집계는 CONFIRMED 17 / RESOLVED 14 / PARTIAL 10 / DUPLICATE 1 / REJECTED 1입니다. 이것은 “R2·R3 미검증 17건”과 다른 모집단입니다. P1/P2가 후속 해결한 항목도 있으므로 옛 OPEN 상태를 그대로 재사용해서도 안 됩니다.

**재검사:**

```bash
grep -nE 'Nothing.*unverified|CONFIRMED|RESOLVED|PARTIAL|DUPLICATE|REJECTED' docs/2026-09-03-finding-dispositions.md
```

**제안 문구:**

> Codex R1–R3 43건은 판정 완료. 처분표의 CONFIRMED/PARTIAL 항목을 P1/P2/P3 후속 증거와 대조하여 아직 남은 작업만 갱신한다. R3-14의 재개 근거는 quarantine §3.15. Kimi MEDIUM/LOW 잔여분의 선별 검증은 별도로 유지한다.

---

### L-05 — HIGH — 해결된 산출물 부재를 현재 결함처럼 재선언함

**위치:** `quarantine.md:362–365,602–623,692–699`, `todo.md:98`

> “수정 미적용”  
> “원고·증거 트리에 **아직 그대로 있다**”  
> “스코어러 3개가 저장소에 없다”  
> “원시 `sacct` 출력이 … 남아 있지 않다”  
> “그림 프로그램 **6개 전부**가 … 스텁”

**문제와 근거:**

- 스코어러 예치 완료: `todo.md:157`, 처분표 `:71`.
- 헤드라인 sacct 검증 완료: P1 `:190–202`, P2 `:157–162`.
- 그림 구현·렌더 완료: `results/figures/paper_figs/README.md:3–15`, P1 `:297`.
- §6 머리의 “25건, 철회 2건”도 현재 27개 항목과 철회 4건을 반영하지 않습니다.

**재검사:**

```bash
python3 -c 'from pathlib import Path; print([(p,Path(p).exists()) for p in ["scripts/scoring/rescore_tables_3bc.py","scripts/scoring/score_exp3.py","scripts/scoring/score_overlap.py","results/sacct_provenance.txt"]]); print(len(list(Path("results/figures/paper_figs").glob("plot_*.py"))))'
```

**제안 문구:**

> ⚠️ CAUTION (2026-09-10): §6은 27개 역사적 항목이며 전부 미적용 상태가 아니다. 철회 항목은 §6.6·6.9·6.16·6.27이다. §6.19 스코어러 예치와 §6.20 헤드라인 sacct 예치는 완료되었다(`todo.md` D, P1-09/P2-21). §6.25의 스텁 상태도 해소되었으나 per-panel provenance 범위는 별도로 판단한다. 현재 미해결 작업은 `todo.md`.

각 해당 절에도 같은 날짜의 짧은 상태 마커를 붙이는 것이 필요합니다.

---

### L-06 — HIGH — 이전 실행 세대의 비용과 잡 ID를 “현행 정본”으로 지정함

**위치:** `quarantine.md:119–121,354,803–807`

> “human 비용 … **12.1 h / 21.86 GB**”  
> “5983792/93/94 | **현행 비용 정본**”  
> “경쟁 도구와 비교할 값은 재측정 쪽이다.”

**문제와 근거:** 이 값은 이전 재측정 세대입니다. 현행 원고의 재생성 실행은 P1 `:192–194`에서 확인되는 다음 세대입니다.

| 게놈 | 잡 | 시간 | cgroup 메모리 |
|---|---|---:|---:|
| Col-CEN | 6110900 | 0.67 h | 2.16 GiB |
| human | 6110901 | 12.65 h | 28.08 GiB |
| maize | 6124640 | 15.85 h | 28.45 GiB |

§8.6의 역사적 노드 비교를 현행 비용 선택 규칙으로 읽으면 이 세대를 다시 바꾸게 됩니다. 이전 측정 자체가 틀렸다는 뜻은 아닙니다.

**재검사:**

```bash
grep -nE '^6110900\.batch|^6110901\.batch|^6124640\.batch' results/sacct_provenance.txt
```

**제안 문구:**

> ❌ SUPERSEDED (2026-09-10): §2의 0.51/12.1/15.4 h와 §5의 5983792/93/94는 이전 비용 세대의 대체 기록이다. 현행 원고 헤드라인은 6110900/6110901/6124640의 재생성 실행이며 P1-09를 따른다. §8.6의 노드 비교도 해당 역사적 실행쌍에만 적용한다.

---

### L-07 — HIGH — TRASH template-only 비용에 폐기된 3실행 합계를 유지함

**위치:** `todo.md:114`, `quarantine.md:392–393`

> “template 행은 3실행 합집합임을 반영(합계 **37:28:39** …)”  
> “대체값: 3개 순차 합계 **37:28:39**”

**문제와 근거:** 최종 계약은 **CEN159+CEN178의 397행 합집합**입니다. 비용은 **31:41:09 = 31.69 h**, de novo는 별도 **5:47:30 = 5.79 h**입니다. 같은 quarantine의 적용 배너 `:369–377`, 예치 보고서 `results/regen/colcen_trash_template_scored.txt:8–14`, 원고 `:212`가 일치합니다.

**재검사:**

```bash
grep -nE '31:41:09|37:28:39|397|31.69' todo.md quarantine.md results/regen/colcen_trash_template_scored.txt
```

**제안 문구:**

> template-only 행은 CEN159+CEN178의 397행 합집합이며 비용은 31:41:09 / 2.63 GiB. 37:28:39는 de novo를 포함한 폐기 계약의 합계로 인용 금지. ✅ (2026-09-03, `results/regen/colcen_trash_template_scored.txt`)

---

### L-08 — MEDIUM — 정정의 정정이 앞선 “대체값”에 연결되지 않음

**위치:** `todo.md:86,91`, `quarantine.md:142,469,475–479,539–544`

> “실제 최대 **1.54 / 2.81**”  
> “TRF loses least (0.87); tantan **0.92**”  
> “예외 **2건** 명시”

**문제와 근거:** 같은 todo `:102`는 ULTRA 상계를 **2.82**, tantan 손실을 **0.91**로 정정합니다. 현재 원고 `:296,314`도 그러합니다. P2-14(`pass2-methods-vs-code.md:109–114`)는 컨테이너 예외에 두 2026 도구와 ULTRA 시도를 포함하도록 다시 수정했습니다. 오래된 대체문을 그대로 복사하면 이미 고친 오류가 돌아옵니다.

**재검사:**

```bash
grep -nE '2\.81|2\.82|tantan 0\.92|예외 2건|two noted below' todo.md quarantine.md
```

**제안 문구:**

> ❌ SUPERSEDED (2026-09-10): 1.54/2.81 및 tantan 0.92는 후속 정정 전 기록이다. 현행은 예치값에서 계산한 1.54/2.82 및 0.91(`todo.md` Codex R2-9, 원고 Table 3C-b). 컨테이너 예외 문구는 P2-14의 후속 수정본을 따른다.

---

### L-09 — HIGH — S2 여섯 셀의 자릿수 확장을 “전정밀도 재계산 완료”로 인증함

**위치:** `resume.md:51–52`, `todo.md:67`, `quarantine.md:154`

> “전건 … 예치물 값에서 재계산”  
> “94건, **전건 예치물에서 재계산**”

**문제와 근거:** S2 여섯 셀은 원천 로그에도 한 자리로만 남아 있습니다.

- `38.9 → 38.90`, `46.4 → 46.40`
- `13.2 → 13.20`, `24.8 → 24.80`
- `21.9 → 21.90`, `6.1 → 6.10`

`results/regen/s2_F_p100.txt:10–16`과 precision JSON `:804–880`에서 확인됩니다. 새 두 번째 자릿수를 복구한 계산이 아니라 기존 반올림값의 서식 확장입니다. 이는 `CLAUDE.md:374–376`의 규칙과 충돌합니다. 실제 정밀값이 다른지는 현재 근거로 판정할 수 없습니다.

**재검사:**

```bash
python3 -c 'import json; e=json.load(open("docs/2026-09-10-precision/precision-edits.json")); print([(x["line"],x["old"],x["new"],x.get("artifact_value")) for x in e if x.get("line") in (528,529,530)])'
```

**제안 문구:**

> ✏️ PARTIAL (2026-09-10): precision 편집 94건은 적용되었다. 다만 S2 여섯 셀은 한 자리 예치값을 두 자리로 표시했으며 추가 정밀도를 복구한 것은 아니다. 해당 셀의 원시 집계 복구 또는 기존 정밀도 유지 판단을 `todo.md` §0-4에 남긴다.

---

### L-10 — MEDIUM — half-up 감사 모집단 586개가 잘못됨

**위치:** `resume.md:53`, `todo.md:73`

> “기존 2자리 셀 **586개**는 half-up 과 … 일치”

**문제와 근거:** 586은 P3 TSV의 `REJECTED` 행 수입니다. `reapply_halfup.py:54–59`의 실제 정규식에 해당하는 셀은 **345개**입니다. 유니코드 음수 기호 `−`를 포함하면 기존 두 자리 표기는 **349개**이며 이번 재검산에서도 불일치는 0개였습니다. `CLAUDE.md:366`도 동일한 잘못된 수를 공유합니다.

**재검사:**

```bash
python3 -c 'import csv,re,collections; r=list(csv.DictReader(open("docs/2026-09-05-astra-review/pass3-table-cells.tsv"),delimiter="\t")); print(collections.Counter(x["verdict"] for x in r)); print(sum(bool(re.fullmatch(r"-?[\d,]+\.\d\d",x["printed"])) for x in r),sum(bool(re.fullmatch(r"[-−]?[\d,]+\.\d\d",x["printed"])) for x in r))'
```

**제안 문구:**

> 기존 감사 코드가 검사한 두 자리 셀은 345개, 불일치 0개다. 유니코드 음수 기호를 포함한 349개도 2026-09-10 재검산에서 불일치 0개였다. 586은 P3 셀 판정 `REJECTED` 건수이며 정밀도 감사 건수가 아니다. `CLAUDE.md`의 같은 집계도 정정 대상이다.

---

### L-11 — MEDIUM — 118개 후보 토큰을 모두 측정값으로 취급함

**위치:** `resume.md:54`, `intend.md:46`, `todo.md:68`

> “본문에 남은 **1자리 측정값 118개** … 각각 예치물을 찾아 2자리로 재계산”

**문제와 근거:** precision 보고서는 **“Remaining 1-dp tokens”**라고 부릅니다(`precision-report.md:109`). 목록에는 절 번호 `2.1`, `2.2`, 버전 `longdust 1.4`, 파라미터 `6.0`도 포함됩니다(`:120,125–126,221,226`). 전부 측정값으로 변환하면 Numeric presentation의 예외를 위반합니다.

**재검사:**

```bash
grep -nE 'L44|L75|longdust 1.4|L481|Remaining 1-dp' docs/2026-09-10-precision/precision-report.md
```

**제안 문구:**

> 본문 한 자리 숫자 후보 토큰 118개를 먼저 분류한다. 절 번호·버전·파라미터·정의 상수는 제외하고, 측정값과 파생값만 예치 근거에서 재계산한다. 실제 잔여 측정값 건수는 분류 후 기록한다.

---

### L-12 — HIGH — 6.6일 취소 실행의 도구를 TRF에서 TRASH로 바꿈

**위치:** `todo.md:68`

> “'6.6 days' … **TRASH p2000 취소 실행 sacct**”

**문제와 근거:** 이것은 **TRF** 잡 `6076847`입니다. `quarantine.md:358`, `results/sacct_provenance.txt:40–41`, `manuscript.md:510`이 일치합니다. 이 작업 지시를 따르면 다른 도구의 비용으로 원고를 재계산할 수 있습니다.

**재검사:**

```bash
grep -nE '^6076847|TRASH p2000|TRF p2000' results/sacct_provenance.txt todo.md quarantine.md
```

**제안 문구:**

> “6.6 days”는 TRF p2000 취소 실행 `6076847`의 경과시간을 뜻한다. `results/sacct_provenance.txt`의 job/batch 기록을 구분하여 재계산하며 취소된 실행의 완료비용 하한이라는 한정을 유지한다.

---

### L-13 — HIGH — Phase 0 커밋 범위로는 명시된 완료 기준을 충족할 수 없음

**위치:** `intend.md:29–32`, `todo.md:39`, `resume.md:23,55`

> “(b) **장부 4개** + `docs/2026-09-05-astra-review/`”  
> “완료 기준: `git status` 클린”

**문제와 근거:** `resume.md`는 `.gitignore:24`에서 제외되며 resume 자신도 비추적이라고 명시합니다. 반면 변경된 `CLAUDE.md`와 `docs/2026-09-10-precision/`는 명시된 커밋 목록에서 빠졌습니다(`resume.md:16,50–55`). 상태표도 이 둘을 전체 더티 목록에서 누락합니다.

**재검사:**

```bash
grep -nE '^resume\.md|CLAUDE.md|2026-09-10-precision|장부 4개|git status.*클린' .gitignore resume.md intend.md
```

**제안 문구:**

> 커밋 (a)는 채택한 원고·results 편집과 체크섬, (b)는 추적 대상 장부 `intend.md`·`todo.md`·`quarantine.md`, `CLAUDE.md`, 두 날짜의 review/precision 산출물을 포함한다. `resume.md`는 비추적 메모로 갱신한다. HPC 원본에서 추적·untracked 변경의 처리 여부를 전체 `git status`로 확인한다.

---

### L-14 — MEDIUM — P4 선행 조건과 후속 트리 정리 단계가 모호함

**위치:** `intend.md:34–48,50–58,62`, `todo.md:34–73`, `resume.md:42–45`

> “Phase 1 — P3·P4 마무리”  
> “Phase 1b — 소수점 두 자리 잔여분”  
> “P4 전에 끝내면 …”  
> “더티 트리 위에서 새 리뷰 패스를 돌리지 않는다.”

**문제와 근거:** 번호대로 수행하면 P4가 precision 잔여분보다 먼저입니다. P3 재구성·잔여 편집 후에는 다시 더티해질 수 있는데, P4 전 정리 단계가 없습니다. BRIEF는 패스가 더티 트리를 남기도록 요구합니다(`BRIEF.md:54–65`). Phase 2/3에는 명시적 완료 기준도 없습니다.

**재검사:**

```bash
grep -nE 'Phase|P4|완료 기준|더티|커밋' intend.md
```

**제안 문구:**

> Phase 1 내부 순서는 P3 보고서 재구성 → Phase 1b precision 잔여분 처리 → 통합 담당자의 변경 검토·필요 시 재해시·커밋 → P4이다. P4 후에도 같은 정리 절차를 수행한다. 리뷰 패스 자체는 커밋·재해시·SLURM 제출을 하지 않는다.  
> Phase 2 완료는 §0-2/0-3 각 항목의 완료 근거 또는 구체적 차단 사유 기록으로, Phase 3 완료는 각 저자 결정과 제출 산출물 경로·태그·DOI 기록으로 확인한다.

---

### L-15 — MEDIUM — 닫힌 결정과 대기 중인 결정을 구분하는 표기가 불일치함

**위치:** `resume.md:30–31,43`, `quarantine.md:107`, `todo.md:140–142,147–150,162`

> “재구성하거나 더 큰 메모리로 재실행 (**저자 결정**)”  
> “복구 방식(재구성 vs 재실행)은 … 저자 결정”  
> “저자 대기 … App Note 전환”  
> “C-6. 투고처 — Bioinformatics Application Note ✅”

**문제와 근거:** P3 재구성은 `intend.md:36–38`, `todo.md:40`에서 이미 결정되었습니다. resume가 가리키는 intend의 “결정 지점” 절도 없습니다. App Note의 투고 형식 결정은 완료됐지만 실행 착수 결정은 별도인지 불분명합니다. 저자 대기라고 소개한 작업을 todo에서는 모두 `[ ]`로 표시하며, #14는 이미 존재하는 LICENSE·CI까지 미착수처럼 나열합니다.

**재검사:**

```bash
grep -nE '결정 지점|재구성|재실행|저자 대기|C-6|C-8|#14|App Note' resume.md intend.md todo.md quarantine.md
```

**제안 문구:**

> P3 복구 방식은 2026-09-10 재구성으로 결정 완료(`intend.md` Phase 1). Abstract는 전체 이슈 정리 후 수행한다. App Note 형식 선택은 완료됐으며 변환 실행의 착수 조건을 별도로 명시한다. 실제 저자 결정을 기다리는 작업만 `[?]`로 표시한다. #14의 잔여 범위는 기존 파일의 생성이 아니라 릴리스·버전 정합성·아카이브 작업으로 한정한다.

---

### L-16 — MEDIUM — 완료 표시의 날짜·증거 규칙이 다수 항목에 적용되지 않음

**위치:** `todo.md:40,85–105,117–122,128–141,159–170,195`

> “완료 — 뒤에 `✅ (YYYY-MM-DD, 근거)` 를 붙인다” (`todo.md:14`)

**문제와 근거:** 다음 유형이 남습니다.

- 날짜와 ✅가 없는 완료: `:85–92,94–100,103`.
- 날짜는 있지만 명확한 증거 파일/커밋이 없는 예: `:40,105,137,140,195`.
- 근거가 다음 줄에만 있는 항목: C-1 `:128–132`.
- 날짜 없는 완료·흡수 표시: `:165–170`.
- 실제 완료 대신 철회·흡수를 나타내는 체크행: `:87,119,165–166`.

특히 `:87`은 철회된 §6.9를 실제 결함 수정처럼 남깁니다. quarantine `:482–493`의 철회 기록과 맞춰야 합니다.

**재검사:**

```bash
python3 -c 'import pathlib,re; print("\n".join(f"{n}:{s}" for n,s in enumerate(pathlib.Path("todo.md").read_text().splitlines(),1) if s.startswith("- [x]") and not re.search(r"✅.*\d{4}-\d\d-\d\d",s)))'
```

**제안 문구:**

> 각 완료행에 검증 가능한 날짜와 파일/커밋 근거를 붙인다. 예: `§6.7 … ✅ (2026-09-03, 2901ff3; quarantine.md §6.7)`. §6.9는 “오탐 철회”로 명시한다. 흡수·절차 설명은 완료 작업으로 세지 않고 해당 정본 항목을 가리킨다. 증거가 복구되지 않은 완료는 확인 대기로 표시한다.

---

### L-17 — MEDIUM — quarantine의 완료 마커 아래에 살아 있는 미완 지시가 남음

**위치:** `quarantine.md:189,211,215,225–243,259–260,573,661–677`

> “원장 예치는 미완”  
> “원장과 `best.json` 은 **저장소 밖에 있다**”  
> “예치 JSON 교체는 … A-2 재해시와 함께”  
> “렌더링은 별도로 남았다.”

**문제와 근거:** 원장과 TRF JSON 예치는 `todo.md:155–156`, P1 `:255,279`에서 완료가 확인됩니다. Figure 2 렌더도 P1 `:297` 및 archive `:12–16`에서 완료입니다. §3.7은 바로 위에서 제거 완료라고 하면서 아래에 “미적용 상태”를 유지합니다.

§3.8–3.10의 새 평가 요구와 §6.12의 통계 정리처럼 아직 남은 작업은 quarantine의 금지 기록과 구분되어야 합니다. 특히 보류셋 추가 평가는 이미 채택한 “최소 공개” 결정과 별개입니다.

**재검사:**

```bash
grep -nE '미완|미조치|미적용|미산출|미결정|렌더링은|예치 JSON 교체' quarantine.md
```

**제안 문구:**

> ✏️ PARTIAL 정정 (2026-09-10): 원장·TRF JSON 예치와 Figure 2 렌더는 완료되었다(`todo.md` D, P1-11/13/14). 아래 미완 문장은 당시 기록이다. 현재 잔여 작업은 `todo.md` §0-2의 P1-13 및 해당 명시 항목만 따른다. §6.12의 작업 지시는 `todo.md` A-1을 참조하고, 여기에는 혼용하면 안 되는 통계와 이유만 남긴다.

---

### L-18 — MEDIUM — quarantine의 고정 항목 형식에 실제 공백이 있음

**위치:** `quarantine.md:44–46,170–202,327–344,811–818,869–872`

> “항목 형식은 고정이다: **무엇 / 왜 / 언제 / 대체물 / 근거 경로**.”

**문제와 근거:** 제목·절 날짜·배너를 필드로 인정해도 다음 정보는 부족합니다.

| 항목 | 부족한 정보 |
|---|---|
| §3.2 | 판정 날짜, 로그의 식별 가능한 전체 위치 |
| §3.3·§3.5 | 날짜, 구체적 증거 경로 |
| §3.6 | 재검산 기록을 찾을 증거 경로 |
| §4.1 | 폐기 날짜 |
| §4.2 | 행별 날짜와 증거 연결 |
| §8.7 | 여러 행의 날짜가 `—`, 근거 경로 없음 |
| §9.2 | 날짜, 측정 기록 경로 |

형식상 `무엇`이 제목에 있는 경우까지 모두 정보 누락으로 판정하지는 않았습니다.

**재검사:**

```bash
grep -nE '^### (3\.[2356]|4\.[12]|8\.7|9\.2)|^\|.*—|^\- \*\*(언제|근거|대체물)' quarantine.md
```

**제안 문구:**

> 각 해당 항목에 `무엇/왜/언제/대체물/근거`를 명시한다. 확인할 수 없는 날짜·근거는 “미확인”으로 표시하고 복구 작업을 todo에 남긴다. 기록을 찾기 전 날짜나 측정 근거를 추정하여 채우지 않는다.

---

### L-19 — MEDIUM — 시작 명령이 PATH 실패를 “잡 0개”로 오인시킬 수 있음

**위치:** `intend.md:71–79`, `quarantine.md:780–786`, `resume.md:208–215`

> `squeue -u $USER | grep -i -c bwt   # 0 이어야 정상`  
> “`squeue`/`sacct`/`sbatch`는 PATH에 없다”

**문제와 근거:** 문서 자신이 SLURM 명령이 PATH에 없다고 말하면서 bare `squeue`를 호출합니다. `squeue` 실패 뒤 grep이 `0`을 출력할 수 있습니다. 이름에 `bwt`가 없는 관련 잡도 누락됩니다. bare `pytest` 역시 지정된 Python 환경을 보장하지 않습니다. “이 세션은 2 CPU/4 GB”, s1은 “늘 막힘”, 특정 sandbox가 항상 실패한다는 표현은 이전 세션의 조건입니다.

**재검사:**

```bash
grep -nE 'squeue|PATH|pytest|이 세션|이 Claude 세션|늘 막혀|sandbox' intend.md resume.md quarantine.md
```

**제안 문구:**

> 아래 명령은 HPC 원본 저장소에서 실행한다. 저장소 경로와 명령 존재 여부를 먼저 확인하고, `/cm/shared/apps/slurm/current/bin/squeue -u "$USER"`의 성공 여부 및 전체 결과를 확인한다. 테스트는 지정 Python의 `-m pytest`로 실행한다. 과거 2 CPU/4 GB·파티션 혼잡·sandbox 실패는 역사적 조건이며 새 세션에서 재확인한다.

---

### L-20 — MEDIUM — 완료 근거와 작업 위치에 잘못된 경로·표 번호가 있음

**위치:** `todo.md:59,120–121,193–194`, `quarantine.md:280,494,608`, `resume.md:229`

> “Table **3C-b** 마지막 행 ‘Thread-scaling pair’”  
> “`msreview/codex_out_R2.txt`”  
> “`todo.md` B-0”

**문제와 근거:**

- Thread-scaling 행은 **Supplementary Methods S2 설정표**, 현재 `manuscript.md:502`입니다. P2-23 `:173–176`도 S2라고 명시합니다.
- `msreview/`는 없고 Codex 전사본은 `docs/2026-09-03-codex-review-*.md`에 예치되어 있습니다. R2 문서 `:7–8`은 이 경로 문제 때문에 예치했다고 설명합니다.
- `todo.md` B-0은 없습니다.
- 현재 코드 경로는 `bwtandem/c_extensions/align_accel.c`, `scripts/scoring/score_overlap.py`입니다.
- `run_fullgenome.sbatch`는 미러에 없고 외부 전체 경로도 지정되지 않았습니다.

**재검사:**

```bash
python3 -c 'from pathlib import Path; print([(p,Path(p).exists()) for p in ["msreview/codex_out_R2.txt","docs/2026-09-03-codex-review-round2.md","c_extensions/align_accel.c","bwtandem/c_extensions/align_accel.c","scripts/score_overlap.py","scripts/scoring/score_overlap.py","run_fullgenome.sbatch"]])'
```

**제안 문구:**

> P2-23 위치를 “Supplementary Methods S2 설정표의 Thread-scaling pair 행”으로 고친다. 완료 근거는 저장소에 예치된 전사본 경로로 연결한다. 과거 코드 경로는 “당시 경로”로 표시하고 현행 경로를 병기한다. `run_fullgenome.sbatch`는 외부 런처의 전체 경로를 확인하기 전 재현 진입점으로 사용하지 않는다.

---

### L-21 — LOW — 동일 사실을 독립 항목처럼 중복 유지함

**위치:** `quarantine.md:129–134`, `todo.md:160,167`

> range-cost p100/p2000/비율 행의 반복  
> “#30 경쟁 도구 GNU-time 로그 예치”의 반복

**문제와 근거:** range-cost 세 사실이 두 번씩 적혀 있고 #30 완료도 두 번 기록됩니다. 현재 값은 같지만 이후 한쪽만 갱신될 위험이 있습니다. Fig 5의 실행상 중복은 L-03으로 별도 집계했습니다.

**재검사:**

```bash
grep -nE 'range-cost (p100|p2000|비율)|\*\*#30\*\*' quarantine.md todo.md
```

**제안 문구:**

> 중복 행은 동일 항목의 참조로 표시한다. 예: “위 range-cost 행과 동일; 추가 정보는 실행 커밋 구분뿐.” #30 두 번째 행은 “D의 #30 완료 기록 참조; GitHub 종료 이력”으로 한정한다.

## Cross-file consistency table

`—`는 해당 값을 직접 제시하지 않음을 뜻합니다. 역사적 값은 현재값과 구분했습니다.

| 사실 | resume.md | intend.md | todo.md | quarantine.md | 대조 결과 |
|---|---|---|---|---|---|
| 현행 팁 | `3e728cc` (`:22`); 과거 `da9e484` (`:126`) | — | 여러 완료 커밋 | 여러 실행·완료 커밋 | P1 `:13`이 `3e728cc` 기준 확인. 현재 HEAD/푸시는 검증 불가 |
| 원고·results 더티 | 원고 + results 15개 (`:15,23`) | results 15개 (`:26`) | results 15개 (`:37`) | 재해시 절차 | P1 목록 15개 = README 12 + 기타 3, 모두 존재 |
| 09-10 추가 변경 | 장부 4개·CLAUDE·precision (`:16`) | 커밋 목록에서 CLAUDE·precision 누락 | 동일 범위 불명확 | — | L-13 |
| resume 추적 여부 | 비추적 (`:55`) | 장부 4개 커밋 (`:29`) | 장부 커밋 (`:39`) | — | `.gitignore:24`와 충돌 |
| 체크섬 상태 | 미갱신 (`:24`) | 재해시 선행 | 재해시 선행 | §8.2 동일 | 세 텍스트 파일의 현재 해시 불일치 직접 확인 |
| 체크섬 목록 수 | 역사적 197/80 (`:129`) | — | — | — | 현재 목록 행 수도 197/80 |
| P1 판정 | 14 C / 4 R / 2 B (`:25`) | 커밋 메시지에 기록 지시 | P1 후속 작업 | — | P1 `:5`와 일치 |
| P2 판정 | 17 C / 4 R / 3 B (`:26`) | 커밋 메시지에 기록 지시 | P2 후속 작업 | P2 정정 기록 | P2 `:5`와 일치 |
| P3 적용 건수 | 46 중 45 | 45 | 46쌍·45 적용 | 46 적용 / 45 존재 | 로그는 46 순차 치환 성공; L-02 |
| P3 보고서 | 없음·재구성 중 | 재구성 산출물 | `[~]` | 없음 | 미러에 없음. 예정 산출물이므로 오류 아님 |
| P4 상태 | 미착수 | Phase 1 예정 | `[ ]` | P1/P2만 완료 | 일치 |
| P3 복구 결정 | 재구성 결정 / 재실행 선택지 병존 | 재구성 확정 | 결정 `[x]` | 선택지 문구 잔존 | L-15 |
| 반올림 결정 | half-up | half-up | half-up | §2·§8.9 half-up | **결정 자체와 12.65/58.85는 일치** |
| precision 편집 수 | 65+24+5=94 | 94 | 94 | 65+29=94 | JSON의 종류별 건수와 일치 |
| float→half-up 변경 | 6곳 | — | 6곳 | 12.65 ×5, 58.85 | 보고서 부록·JSON·원고와 일치 |
| 기존 두 자리 감사 수 | 586 | — | 586 | — | 실제 코드 검사 345; `−` 포함 349. L-10 |
| 잔여 한 자리 수 | 측정값 118 | 측정값 118 | 측정값 118 | — | 실제로는 후보 토큰 118. L-11 |
| Fig 5 | 미착수/미참조 | 배치 예정 | 미착수 2곳 | — | 현재 원고에 배치됨. L-03 |
| Codex 미검증 잔여 | 미검증 3묶음 | 통합 예정 | 17+14+Kimi | 옛 미조치 기록 | Codex 43건 판정 완료; Kimi 잔여는 별도 |
| sacct 예치 수 | 과거 34잡 (`:72`) | 원시 9건 후속 | 34 및 37/40 구분 작업 | 헤드라인 원시 증거 없다는 옛 문구 | 34는 09-03 역사값; 현행 37할당/40잡-태스크 |
| C-1 실행 | 3개 완료 | — | 6147698/699/700, 1.79 | 같은 잡·비율 | 원시 초 단위와 일치 |
| 현행 비용 세대 | 현행 원고 참조 | precision 처리 | 현행 원고 참조 | 옛 5983792/93/94를 현행 지정 | L-06 |
| TRASH template 비용 | — | — | 37:28:39 | 31:41:09 / 37:28:39 병존 | 현행 397행·31.69 h. L-07 |
| ULTRA 최대 밴드 손실 | — | 재계산 지시 | 2.81 / 2.82 | §2·§6.8은 2.81, §8.9는 2.82 | 현행 원고 2.82 |
| C-3 원장 예치 | — | P1-13 후속 | 완료 / 옛 대기 문구 | 미완·외부만 존재 | 예치 완료; 최종 선택 기록의 불완전성과 구별 필요 |
| C-10 JSON | — | P1 통합 | 완료 / 옛 대기 문구 | 교체 대기 | JSON 교체 완료, P1-11 확인 |
| 저자 항목 | Abstract·전환·릴리스 대기 | Phase 3 | 형식 선택 완료, 실행 `[ ]` | 일부 미결정 잔존 | L-15 |
| 호스트 OOM | 6147604, 09-06 06:49 | 4 GB 위험 회피 | 호스트 OOM | 같은 잡·시각, 원인 추정 | 서로 일치하나 HPC accounting 직접 검증 불가 |

## Broken or unverifiable references

경로는 백틱·명령 안의 인자까지 확인하고, basename·중괄호 확장·상대 문맥을 구분했습니다. **미러에서 찾을 수 없음**과 **원본 저장소의 실제 누락**은 동일하게 취급하지 않았습니다.

| 경로 또는 참조군 | 상태와 조치 |
|---|---|
| 네 ledger, `CLAUDE.md`, `manuscript.md`, 두 resume archive, `resume.md.autolog-bak`, `.gitignore` | 모두 존재 |
| `docs/2026-09-05-astra-review/BRIEF.md`, P1/P2 보고서 | 존재 |
| `pass1-checks.py`, checksum sample, manifest audit before/after | 해당 review 디렉터리에 모두 존재 |
| `pass3-edits.json`, table-cells before/after TSV·스크립트, checks.py, colcen/costs/human/maize/maize3a-extra JSON, fig5 JSONL, pass3.log | 해당 review 디렉터리에 모두 존재 |
| `pass3-results-tables.md`, `pass3-*.md`, `pass4-*.md` | 검토 시 없음. 재구성/미착수 단계의 예정 산출물 |
| precision 보고서·JSON·`normalize_precision.py`·`reapply_halfup.py` | 모두 존재. **normalizer의 dry run도 보고서·JSON을 덮어씀**(`normalize_precision.py:120–121`); 순수 읽기 검사용으로 실행하면 안 됨 |
| 지정된 finding dispositions, App Note 계획, benchmark protocol, nondeterminism·flaky 진단 문서, recall-loop 계획 | 모두 존재 |
| `results/` 15개 수정 대상, 두 체크섬, tuning ledger/best.json, TRF 1:1 JSON, Col-CEN banded·template scoring 보고서, provenance JSON | 모두 존재 |
| `scripts/scoring/` 아래 열거된 scorer와 precision 대상 스크립트 | 존재. basename은 이 디렉터리 기준으로 해석 가능 |
| `plot_fig4_plant_satellites.py`, `plot_figS2_postmerge.py`, 나머지 `plot_*.py` | `results/figures/paper_figs/`에 존재 |
| `resume.md:240`의 `rendered/` | 루트에는 없으나 바로 앞 문맥의 `results/figures/paper_figs/rendered/`는 존재. 전체 경로 병기 권장 |
| `msreview/codex_out_R1.txt`, `R2.txt`, `R3.txt`, `out_R*.md` | 현재 상대경로로는 없음. Codex는 `docs/2026-09-03-codex-review-findings.md`, `…-round2.md`, `…-round3.md`로 교체 가능. Kimi는 예치된 review/recheck/thirdpass 문서에 개별 연결 필요 |
| `c_extensions/align_accel.c` | 루트 기준으로 틀린 경로. 현행은 `bwtandem/c_extensions/align_accel.c` |
| `scripts/score_overlap.py` | 현행 경로 없음. `scripts/scoring/score_overlap.py` 존재. quarantine에서는 당시 부재 주장임을 표시 |
| `run_fullgenome.sbatch` | 미러에 없고 완전한 외부 경로도 미지정. `.sbatch`는 확장자 제외 대상이 아님. 원본 위치 미확인 |
| `exp1_human/loop/{ledger.tsv,best.json}` | 저장소 상대경로에는 없음. P1 `:285–286`이 원본을 `/data/gpfs/assoc/pgl/devel/exp1_human/loop/`로 식별하며, 복사본은 `results/tuning_ledger/`에 존재 |
| `exp1_human/filip_repro/catchall_experiment_results.md`, `exp1_human/tools2026/runs/run_anianns.sbatch`, `*.time` | 외부 실험 디렉터리의 축약 경로. 전자는 Codex R2 `:37`, 후자는 P1 근거가 외부 위치를 확인함. 미러만으로 원본 존재 재검증 불가 |
| `exp1_human/data/adotto_primary.bed`, `colcen_cen180.bed`, `Col-CEN_v1.2_trash.bed`, template union BED | BED 제외 규칙 또는 외부 입력에 해당. 부재를 오류로 판정하지 않음 |
| `results/regen/colcen_trash_template_union.bed` 뒤의 `_scored.txt` | 축약이 모호함. 실제 보고서는 `results/regen/colcen_trash_template_scored.txt`이며 `_union_scored.txt`가 아님 |
| `/data/gpfs/…` Python·bedtools·Filip benchmark·TRASH 로그, `/cm/shared/apps/slurm/current/bin/` | HPC 외부 경로. 이 미러에서 검증 불가 |
| `~/scratch/devel/bwt-algorithm` | HPC 작업 경로/별칭으로 보이나 이 환경에서는 확인 불가. BRIEF의 원본 경로는 `/data/gpfs/assoc/pgl/devel/bwt-algorithm` |
| `~/.codex/sessions/…rollout-…jsonl` | 호스트 세션 기록. 저장소 산출물이 아니며 미러에 없음 |
| `guide/handoff-hygiene.md`, `ruleout.md` | 전자는 명시된 외부 랩 위키 문서. 후자는 개명 이력에 등장하는 옛 이름. 저장소 누락으로 보지 않음 |
| `slurm_5912536_*.log`, `bwt_hg38.log` | 과거 실행 로그의 basename만 있음. 현재 위치·보존 여부 미확인 |
| `0363d8b:src/tier3.py`, `0363d8b:src/autocorr.py` | 역사적 Git 객체 경로. `.git` 제외로 검증 불가하며 현행 파일 누락이 아님 |
| `todo.md` B-0, intend “결정 지점”, Table 3C-b의 thread-scaling 행 | 실제로 없는 내부 참조. L-15/L-20 참조 |
| `/proc/self/status`, `/proc/<pid>`, `/usr/bin/time` | 시스템 경로 또는 명령 템플릿. 저장소 파일로 분류하지 않음 |

`*.gz`, `*.bed`, `*.dat`, `build/`, `*.egg-info`, `arabadopsis_chrs/`, `benchmarking/`, 5 MB 초과 파일의 제외 규칙을 적용했습니다. 크기를 알 수 없는 부재 파일을 임의로 “5 MB 초과 제외”라고 설명하지 않았습니다.

## Not a problem, checked

- **half-up 결정은 살아 있습니다.** quarantine §2의 2026-09-10 표와 §8.9는 서로 일치합니다. precision 보고서 앞부분의 12.64/58.84는 부록 `:231–242`에서 정정되며, 현재 JSON·원고는 12.65/58.85입니다.
- **94건이라는 편집 수는 맞습니다.** JSON은 table 65 + prose 24 + prose-explicit 5입니다. 다만 모든 편집의 정밀도 근거가 충분하다는 뜻은 아닙니다(L-09).
- **OOM 원인 프로세스는 추정으로 표시되어 있습니다.** quarantine §1.4 `:103`과 §8.8 `:825` 모두 이를 명시합니다. 마지막 BED intersect와 잡 종료 사이에는 시간 간격도 있으므로 그 단서를 삭제하면 안 됩니다.
- **P1/P2 판정 수와 results 수정 파일 수는 맞습니다.** 15개 목록은 README 12개와 TSV·accounting header·comparator prose 3개입니다.
- **과거 34할당과 현행 37할당/40잡-태스크는 모순이 아닙니다.** P1 `:155`가 세대와 집계 단위 차이를 설명합니다.
- **Where things stand의 `da9e484`, 197/80, green tests에는 유효한 역사 마커가 있습니다.** `resume.md:122`는 날짜와 상단 상태표 포인터를 갖습니다. 위의 09-04 스냅샷도 `:57–58`의 전체 archive 배너 범위에 있습니다.
- **체크섬 불일치는 현재 설명과 맞습니다.** 미러에 있는 `manifest.tsv`, `sacct_provenance.txt`, `results/README.md`를 기존 해시와 비교해 불일치를 확인했습니다. 전체 guard는 제외 파일 때문에 원본과 같은 조건으로 실행할 수 없습니다.
- **C-1 비율 1.82/1.77/1.77, 평균 1.79는 맞습니다.** 서로 다른 실행 세대의 비용과 섞지 않는 것이 핵심입니다.
- **R3-14 재개는 정당한 형태로 기록되었습니다.** P2-03은 실제 루프 실행 결과를 근거로 원 기각을 명시적으로 재개합니다. 역사적 처분표의 REJECTED를 지우지 않은 것은 오류가 아닙니다.
- **§9.1의 진단 기록과 todo의 차단 작업은 역할이 다릅니다.** 소진된 진단은 quarantine에, 관리자 ASLR 요청은 todo에 있습니다. §9.3의 ≥0.88 설정도 “시험 실패”가 아니라 “미시험·논문 범위 밖”으로 명확히 구분합니다.
- **P3/P4 보고서, 원시 accounting, audit 이미지의 부재는 측정 오류를 입증하지 않습니다.** 새 세션은 이를 재실행 요구나 수치 폐기로 자동 변환하면 안 됩니다.
