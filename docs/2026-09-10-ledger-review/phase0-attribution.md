# Phase 0 — 원고 diff 출처 대조 · results/ 대조 (2026-09-10)

기준: `3e728cc:manuscript.md`. 방법: 현재 원고에서 precision 편집(유효 88건, 실패 0) → E47(발견 1) → P3 46건(역순, 복원 46건, 미발견 []) 을 되돌린 뒤 기준과 비교. 남는 차이는 P2 보고서가 인용한 기준 줄 번호(P2 는 줄 구조를 보존했다)와 대조.

## 잔여 차이 (P2 후보): 39 블록 · P2 인용 줄과 일치 37 · **미설명 2**

| 종류 | 기준 줄 | 기준 줄수 | 현재 줄수 | P2 finding | 기준 텍스트(앞 90자) |
|---|---|---|---|---|---|
| replace | 46 | 1 | 1 | P2-01 | Given a genomic sequence S of length n, BWTandem constructs a suffix array using divsufsor |
| replace | 48 | 1 | 1 | P2-07 | BWTandem processes each chromosome independently, constructing a single FM-index and then  |
| replace | 50 | 1 | 1 | P2-02 | The first tier detects microsatellites with periods of one to nine base pairs through dire |
| replace | 52 | 1 | 1 | P2-02 | Candidates are bidirectionally extended while the cumulative Hamming mismatch fraction rem |
| replace | 54 | 1 | 1 | P2-03 | An optional FM-index enumeration mode, enabled for every run reported in this paper, runs  |
| replace | 58 | 1 | 1 | P2-05 | In the first phase, the LCP array is scanned to identify adjacent suffixes sharing long co |
| replace | 60 | 1 | 1 | P2-04 | The second phase applies BWT k-mer seeding to regions the previous phases left more than h |
| replace | 62 | 1 | 1 | P2-09 | For highly diverged sequences where exact k-mer recurrence fails, an autocorrelation-based |
| replace | 66 | 1 | 1 | P2-09 | The tier automatically adapts its parameters based on input sequence properties. K-mer siz |
| replace | 68 | 1 | 1 | P2-06 | Boundary refinement uses two strategies depending on array scale. For large arrays (more t |
| replace | 70 | 1 | 1 | P2-07 | Post-processing consolidates raw detections by sorting coordinates, merging adjacent calls |
| replace | 72 | 1 | 1 | P2-08 | Two supplementary passes address gaps in the core pipeline. A satellite gap-fill pass exam |
| replace | 74 | 1 | 1 | P2-08 | An optional catch-all periodicity pass evaluates windowed autocorrelation at periods 1–20  |
| replace | 76 | 1 | 1 | P2-14, P2-24 | BWTandem was benchmarked against seven tools: TRF 4.10.0rc2 (Benson, 1999), mreps 2.6.01 ( |
| replace | 78 | 1 | 1 | P2-16 | Period search ranges were not uniform across tools, and because this affects which metrics |
| replace | 80 | 1 | 1 | P2-15, P2-23 | All benchmarking was performed on the University of Nevada, Reno Pronghorn HPC cluster usi |
| replace | 82 | 1 | 1 | P2-13, P2-15 | The regenerated whole-genome BWTandem results were produced from clean commit `0363d8b` wi |
| replace | 90 | 1 | 1 | P2-17 | For Arabidopsis thaliana (Experiment 2), performance was measured as mean centromere cover |
| replace | 99 | 1 | 1 | P2-15 | Two tools published in 2026, after this benchmark was frozen, were added under a preregist |
| replace | 419 | 1 | 1 | P2-02 (수동 확인: 보고서 'per-period candidate-buffer cap … transcribed from 0363d8b:src/tier1.py'; 삽입 문장 'min(⌊n/p⌋ + 1, 1,000,000) candidates per period') | 		 The length floor L_min and score floor Q_min are 17 for the runs using the relaxed shor |
| replace | 421 | 1 | 1 | P2-03 | 		 In the configuration used throughout this paper the FM-index enumeration runs as a seco |
| replace | 423 | 1 | 1 | P2-05 | 		 In the LCP-driven phase, the detected motif is reduced to its primitive period using ex |
| replace | 425 | 1 | 1 | P2-04 | 		 In the BWT k-mer seeding phase, the k-mer and stride formulas resolve to 9 bp k-mers sa |
| replace | 431 | 1 | 1 | P2-09 (수동 확인: 보고서 'limited the statement about the GC formula not attaining its ceiling to the benchmark chromosomes rather than all real sequence') | 		 The GC term is bounded in practice by genomic composition: ¦GC − 0.5¦ reaches 0.5 only  |
| replace | 435 | 1 | 1 | P2-09 | 		 All adaptive parameters are then clamped to empirically validated ranges. The rightmost |
| replace | 451 | 1 | 1 | P2-06 | 		 The anchor-based boundary verification threshold for large arrays ranges from 70% to 80 |
| replace | 453 | 1 | 1 | P2-08 | 		 The autocorrelation identity at period p over a window W of length w is defined as foll |
| replace | 455 | 1 | 1 | P2-08 | 		 A(W, p) = (1 / (w − p)) · Σᵢ₌₀^{w−p−1} 𝟙[W[i] = W[i + p]] |
| replace | 457 | 1 | 1 | P2-08 | 		 where 𝟙 denotes the indicator function. For the satellite gap-fill pass, the default mi |
| replace | 459 | 1 | 1 | P2-01 | 		 The suffix array is stored as 32-bit integers and the BWT as an 8-bit character array.  |
| replace | 461 | 1 | 1 | P2-10 | 		 BWTandem results in this paper come from the nine configuration rows tabulated below, n |
| replace | 474 | 1 | 1 | P2-13, P2-22 | 		 The configurations then differ as follows. The command line is `python -m src.main FAST |
| replace | 488 | 1 | 1 | P2-10, P2-12, P2-22 | 		 The catch-all periodicity pass is therefore enabled at 0.72 with three copies for the h |
| replace | 490 | 1 | 1 | P2-14, P2-24 | 		 Supplementary Table S1. Competitor tool versions and command lines. All competitor runs |
| replace | 495 | 1 | 1 | P2-24 | ¦ tantan ¦ 51 ¦ `tantan -f4 FASTA` ¦ |
| replace | 498 | 4 | 4 | P2-24 | ¦ ULTRA ¦ 1.2.1 ¦ human and Arabidopsis `ultra -t 2 -o OUT.tsv FASTA` (default maximum per |
| replace | 499 | 4 | 4 | P2-24 | ¦ mreps ¦ 2.6.01 ¦ human, unbounded, one sequence at a time; Arabidopsis re-run over 150–4 |
| replace | 500 | 4 | 4 | P2-24 | ¦ NCRF ¦ 1.01.02 ¦ `NCRF NAME:MOTIF …`, given the exact consensus for each target family ¦ |
| replace | 501 | 4 | 4 | P2-24 | ¦ TRASH ¦ v1 ¦ de novo `TRASH_run.sh FASTA --o OUT --par 2`; template mode adds `--seqt TE |

## 미설명 블록 (저자 판단)

없음 — 1차 실행에서 남았던 기준 L419·L431 은 P2 보고서의 'Fix applied' 서술과 대조해 P2-02·P2-09 로 확정했다(위 표). 결론: **현재 원고의 모든 hunk 는 P2(37 블록) · P3 46건+E47 · precision 88건으로 설명된다.** P2 는 줄 구조를 보존했으므로 기준 줄 번호가 곧 P2 인용 번호다.

## precision 되돌리기 실패 로그

없음

## results/ 15개 대조

- git diff: 15개, P1 REHASH REQUIRED: 15개
- 일치: True
- git 에만: 없음
- P1 에만: 없음
- P3 는 results/ 를 쓰지 않았다 (`pass3-results-tables.md` REHASH REQUIRED: none).
