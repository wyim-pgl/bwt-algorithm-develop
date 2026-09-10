# 제출 전 수치·경계 정의·재현성 공개 — 2026-09-10

저자 지시 1–3번만 수행한다. 시작점은 `pronghorn:~/scratch/devel/bwt-algorithm`, 클린 `139e361`이다. **P4·Abstract 재작성·App Note 전환·벤치마크 재실행·릴리스는 수행하지 않았다.** 초록에서는 다른 본문과 같은 수치 표기만 고쳤다. 제출 가능 판정이나 독립 리뷰 인증이 아니다.

## 1. 한 자리 후보 118개

`one-decimal-classification.tsv`는 이전 `precision-report.md`의 118개 후보를 순서대로 전수 분류한다. 원고 전체의 모든 숫자를 추출했다는 뜻은 아니다.

| 분류 | 토큰 수 |
|---|---:|
| 측정/파생 후보 — 재계산 또는 근거에 맞게 재서술 | 81 |
| 측정 후보 — 원천 정밀도 유지 | 10 |
| 절 제목/참조 | 12 |
| 파라미터/정의·설계 예시 | 11 |
| 버전 | 2 |
| 인용 문헌의 원래 정밀도 | 2 |
| 합계 | 118 |

측정 후보는 91개이다. 81개 중 above-100 merged-bp 비율 33.4%/65.7%는 정확한 피연산자가 확인되지 않아 현행 수치 주장에서는 제외하고 한계를 명시했다. 이는 그 값이 틀렸다고 판정한 것이 아니다.

정밀도 예외 10개는 postmerge calls-per-array 8개(예치 JSON이 한 자리만 보존), unlogged cache 0.6 s, 과거 회귀검사 요약의 Chr4 18.8 Mb이다. 원고와 todo에 남겼다. S2의 여섯 한 자리 셀은 이 **본문 118개 목록 밖**이며, 기존 L-09 예외와 제출 후 재생성 작업을 그대로 보존했다. 추가 0을 붙이지 않았다. 두 자리 표기는 불확실성이 줄었다는 주장이 아니다.

`numeric-edits.json`과 `compute_numeric_edits.py`가 원자료/집계값·단위변환·half-up 계산을 기록한다. 실제 적용되는 최종 원고는 수치 후보에 아래의 파생값·정의·공개 문장 수정까지 합친 `patch.json`이다. 계산 스크립트는 중간 수치 후보만 생성하므로 최종 원고를 덮어쓰지 않는다.

## 2. 파생값 및 TR-1

- `derived-claims.json`: 비교/정의 125건의 위치·피연산자·경로·식·판정. 그중 102개 수치 식을 Decimal로 재계산했다. 정의나 자료 부재 행은 수치 검증 성공으로 세지 않았다. 범위 식의 min 결과와 전체 범위/해석의 검토를 혼동하지 않는다.
- `remaining-sources.json`: 과거/현행 range-cost 각 세 반복의 정확한 elapsed 배열, merged-bp 분자·분모 부재, native-F truth-hit 분자 부재.
- 과거/현행 **각 세 반복의 산술평균**은 narrow **6.23→4.05 h**, wide **8.31→7.24 h**이다. 기존 6.6→4.0/8.6→7.3은 첫 반복에 가까운 요약이었으므로 원고에서 평균 모집단을 새로 명시했다. 서로 다른 빌드의 기록을 요약한 것이며 새 matched 실험이 아니다. 1.79 headline은 각 paired ratio의 평균으로, 평균 elapsed의 비율과 혼동하지 않는다.
- 잔여 불확실한 파생 주장은 값/한계를 함께 표시하거나 비교를 피연산자로 대체했다: native-F의 1.01 pp, TRASH empty-window ≤0.20 pp, mreps per-base slowdown, rounded-offset 비율 등. 정확한 지원 부족을 원자료 오류로 승격하지 않는다.
- `tr1-source-report.md`: 770.65 bp(raw TR-1,17배열), 4,282 bp(coordinate-merged TR-1,17배열), 4,265.30 bp(banded **knob180**,25배열), 7,973.15 bp(banded TR-1,17배열)의 코드/출처. 4,282는 정수 bp만 예치되어 있어 4,282.00으로 넓히지 않았다.
- 핵심 정정 예: 세 도구 Col-CEN spread **0.20→0.15 pp**, H–ULTRA gap **0.02→0.03 pp**, 최대 full→matched recall 이동 **1.1→1.66 pp**, TRASH–BWTandem coverage 차이 **1.44/2.83/0.13→1.43/2.84/0.14 pp**.
- AniAnn 삽입절 뒤에 sub-kb 경계의 주어가 모호해진 곳은 **BWTandem**을 명시했다. AniAnn의 높은 coverage나 큰 경계 오차를 숨기지 않는다.

## 3. 공개 문장

`provenance-dispositions.md`가 2등급 11항목의 근거와 한계를 정리한다. raw sacct9태스크·시각감사 원본·튜닝17pending·환경/컨테이너·외부런처 등의 복구를 가장하지 않고 공개 문장 경로를 택했다. 환경 파일은 주석만 변경했다. **원시 BED, 점수 JSON/TSV, 런타임/cgroup 셀, reader verdict, 튜닝 decisions는 불변**이다. `results/`에서는 `audit11/README.md`와 `competitor_logs/README.md` 두 파일만 편집한 뒤 기존 전체 재해시 스크립트를 사용한다.

## 재실행 가능한 검사

저장소 루트에서, 클러스터의 `$PY=/data/gpfs/assoc/pgl/bin/conda/conda_envs/bwtandem/bin/python`:

```bash
$PY docs/2026-09-10-presubmit/check_patch.py
$PY docs/2026-09-10-presubmit/verify_derived.py
$PY docs/2026-09-10-presubmit/compute_numeric_edits.py --output /tmp/bwt-numeric-check
cmp /tmp/bwt-numeric-check/numeric-edits.json docs/2026-09-10-presubmit/numeric-edits.json
sha256sum -c results/manifest.sha256 --quiet
$PY -m pytest tests/test_deposit_hashes.py tests/test_env_var_docs.py tests/test_one_to_one_scoring.py -q
```

`check_patch.py`는 변경 10파일의 최종 SHA 및 git 기준점에서 추적 9파일의 바이트 동일 replay를 검사한다. ignored `resume.md`는 적용 시 원본 해시를 확인하고, 이후에는 최종 해시를 확인한다. 결과 재해시 파일은 기존 스크립트가 생성하므로 patch 대상이 아니다.

`verify_derived.py`는 등록 식102개 및 JSON 피연산자144개·예치 cost-cache 피연산자58개와 range-cost 평균4개/원시 elapsed를 검사한다. 기타 인용 피연산자106개는 이 검사기에서 자동 source-replay하지 않는다. 그 출처는 JSON에 남겨 수동 검토했으며, 이것을 전수 원자료 재실행이나 의미적 완전성 증명이라고 부르지 않는다. Benchmark detector/scorer 재실행은 없었다.

최종 출력은 `verification.txt`, 적용 전 가드 출력은 `baseline-tests.txt`, sacct/ledger/audit와 S4 재검사는 `provenance-checks.txt`·`s4-check.txt`다. **미커밋/스테이징 상태**는 remote git 및 `resume.md`에 명시한다.
