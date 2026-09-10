# P3-16 — 근거 미복구 편집 5건의 저자 결정 (2026-09-10)

결정: **5건 전부 채택.** 판단 근거는 로그가 아니라 아래 대조에서 온다.

| 편집 | 위치 | 판단 근거 |
|---|---|---|
| E19 | manuscript.md:188 | 옛 문장의 "no plausible correction reverses the direction" 은 검증 불가 단정. 새 문장은 공유 노드·다른 주기 상한이라는 사실만 진술. tantan 0.20 h 대 BWTandem 0.67 h 수치는 그대로 남아 BWTandem 에 유리해지지 않음 |
| E26 | manuscript.md:294 | `pass3-maize.json` /3C: TRASH-template 58.68451580 − TRF 58.50421370 = 0.1803 → 두 자리 0.18 정확. "approximately" 는 불필요 — 후속 삭제 (todo §0-4) |
| E35 | manuscript.md:188 | TRF 200 bp / ULTRA 500 bp / BWTandem 1–2,000 bp 범위 차이는 §2.2 와 quarantine §3.5 의 기록. 비용 비교 자리에 그 사실을 명시한 것 |
| E39 | manuscript.md:543 | 같은 캡션 앞 문장이 ">500 bp regime 은 이 카탈로그로 판정 불가" 라고 함. 위성 실험은 coverage 를 재지 period 배정을 검증하지 않음. 새 문장이 더 정확하고 BWTandem 에 불리한 방향 |
| E47 | manuscript.md:496 | 해당 행은 최대 주기 100 의 네이티브 F 실행. Table 1b 캡션(L139)은 본행이 2,000 bp 전장 실행의 사후 필터라 하고, C-2 결정(2026-09-03)이 네이티브 재실행을 민감도 분석으로 강등. 설정표를 그 결정에 맞춘 것 |

재검사: `git show 3e728cc:manuscript.md | sed -n '182p;284p;527p'` (옛 문장), `python3 -c "import json;j=json.load(open('docs/2026-09-05-astra-review/pass3-maize.json'));print(j['3C']['TRASH-template']['CentC']['unfiltered']['coverage']-j['3C']['TRF']['CentC']['unfiltered']['coverage'])"`.
