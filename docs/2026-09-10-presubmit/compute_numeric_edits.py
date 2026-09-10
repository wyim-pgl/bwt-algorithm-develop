"""Targeted manuscript revision; run from repository root. No benchmark reruns.
Produces a candidate and an auditable edit list; does not overwrite the manuscript.
"""
import argparse, csv, json, re, subprocess
from collections import Counter
from decimal import Decimal as D, ROUND_HALF_UP
from pathlib import Path
ROOT = Path.cwd()
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, required=True, help='output directory for candidate and numeric edit ledger')
OUT = parser.parse_args().output
OUT.mkdir(parents=True, exist_ok=True)
def load(name):
    return json.loads((ROOT / name).read_text(), parse_float=D)
def fmt(x):
    return str(D(str(x)).quantize(D('.01'), rounding=ROUND_HALF_UP))
base = subprocess.check_output(['git', 'show', '139e361:manuscript.md']).decode()
lines = base.splitlines(keepends=True)
edits = []
def change(line, old, new, source):
    assert lines[line-1].count(old) == 1, (line, old, lines[line-1])
    lines[line-1] = lines[line-1].replace(old, new)
    edits.append(dict(line=line, old=old, new=new, source=source))
def num(line, old, value, source):
    pattern = r'(?<![\d.])' + re.escape(old) + r'(?![\d.])'
    matches = list(re.finditer(pattern, lines[line-1]))
    assert len(matches) == 1, (line, old, len(matches))
    m = matches[0]
    lines[line-1] = lines[line-1][:m.start()] + fmt(value) + lines[line-1][m.end():]
    edits.append(dict(line=line, old=old, new=fmt(value), source=source + '; decimal ROUND_HALF_UP to .01'))
human=load('docs/2026-09-05-astra-review/pass3-human.json')
colcen=load('docs/2026-09-05-astra-review/pass3-colcen.json')
maize=load('docs/2026-09-05-astra-review/pass3-maize.json')
extra=load('results/regen/maize_extra_evidence.json')
for tool,old in [('BWTandem','3.4'),('TRF','2.0')]:
    v=human[tool]['scores']['101-2000']; num(21,old,D(v['truth_hits'])*100/1784804,f'pass3-human.json {tool} 101-2000 truth_hits / 1784804 *100; source BED identified in JSON')
for tool,old in [('BWTandem','99.7'),('tantan (500bp re-run)','99.2')]:
    num(21,old,colcen[tool]['recall'],f'pass3-colcen.json {tool}.recall; underlying BED identified in JSON')
# Cancelled TRF job allocation elapsed, not the batch step (one second longer).
days=D(6)+D(13*3600+57*60+48)/86400
for line in [38,78,107,543]: num(line,'6.6',days,'results/sacct_provenance.txt JobID=6076847 Elapsed=6-13:57:48 /86400')
num(510,'6.6',days,'results/sacct_provenance.txt JobID=6076847 Elapsed=6-13:57:48 /86400')
num(78,'124.8',D(124785432)/1000000,'results/range_cost_attempts/README.md last COMPLETE emitted End=124785432; not processing progress')
for line in [84,103]:
    # Each line has one occurrence of the standalone rounded genome size.
    change(line,'3.1 Gb','3.09 Gb','quarantine.md §6.5 exact primary FASTA length 3088269832 / 1e9; 3.09 is rounded')
num(86,'2.6',D(human['BWTandem']['scores']['101-2000']['calls'])*100/human['BWTandem']['scores']['full']['calls'],'pass3-human.json BWTandem counts 102926/4014108*100')
monomers=[r.split() for r in (ROOT/'results/ground_truth/colcen_cen180.bed').read_text().splitlines() if r and not r.startswith('#')]
n=sum(175<=int(r[2])-int(r[1])<=179 for r in monomers)
for line in [90,201]: num(line,'94.6',D(n)*100/len(monomers),f'results/ground_truth/colcen_cen180.bed count length 175..179: {n}/{len(monomers)}*100')
num(94,'2.7',D(48344)*100/1784804,'results/regen/heldout_select_chr21_22.txt GT regions 48344 / full truth 1784804 *100')
# Wilson interval uses the definitive-verdict denominator, NOT 400.
z=D('1.959963984540054'); n=D(350); p=D(4)/n
center=(p+z*z/(2*n))/(1+z*z/n)
half=z*(p*(1-p)/n+z*z/(4*n*n)).sqrt()/(1+z*z/n)
for line in [119,121,350]:
    num(line,'1.0',D(4)/400*100,'results/audit11/verdicts_reviewer2.tsv: 4 supported /400')
    if line!=350: num(line,'1.1',D(4)/350*100,'results/audit11/verdicts_reviewer2.tsv: 4 supported /350 definitive')
    num(line,'0.4',(center-half)*100,'Wilson score interval, 4/350, z=1.959963984540054; verdicts_reviewer2.tsv')
    num(line,'2.9',(center+half)*100,'Wilson score interval, 4/350, z=1.959963984540054; verdicts_reviewer2.tsv')
num(150,'19.2',D(19*3600+13*60+30)/3600,'results/sacct_provenance.txt 6085144.batch Elapsed=19:13:30')
num(188,'10.1',D(10*3600+7*60+11)/3600,'results/sacct_provenance.txt 5981977.batch Elapsed=10:07:11')
for old,key in [('22.6',"3B/AniAnn's (2026)/knob180"),('83.7',"3B/AniAnn's (2026)/TR-1"),('10.6','3B/TRASH-de-novo/TR-1')]:
    num(248,old,maize[key]['unfiltered']['offset']/1000,f'pass3-maize.json {key}.unfiltered.offset /1000 (bp to kb)')
# Coordinate-merge summaries preserve offsets in whole bp. Convert units,
# but do NOT widen one-decimal calls_per_array without raw counts.
for old,family,gap in [('2.3','knob180','500'),('6.2','knob180','2000'),('130.4','knob180','5000'),('3.4','CentC','2000'),('19.8','TR-1','2000')]:
    num(250,old,D(extra['coordinate_postmerge'][family]['BWTandem'][gap]['mean_offset_bp'])/1000,f'results/regen/maize_extra_evidence.json postmerge/{family}/BWTandem/{gap}/mean_offset_bp /1000')
change(250,'and 4.3 to','and 4.28 to','maize_extra_evidence.json TR-1 gap0 mean_offset_bp=4282 /1000')
for old,family in [('4.1','CentC'),('17.0','TR-1')]:
    num(250,old,D(extra['coordinate_postmerge'][family]['BWTandem']['10000']['mean_offset_bp'])/1000000,f'maize_extra_evidence.json postmerge/{family}/BWTandem/10000/mean_offset_bp /1e6')
num(294,'14.9',maize["3C/AniAnn\'s (2026)/CentC"]['unfiltered']['offset']/1000,"pass3-maize.json 3C/AniAnn's (2026)/CentC.unfiltered.offset /1000")
for line in [294,346]: num(line,'5.3',maize['3C/TRASH-template/CentC']['unfiltered']['offset']/1000,'pass3-maize.json 3C/TRASH-template/CentC.unfiltered.offset /1000')
for old,tool in [('47.3','BWTandem'),('46.5','ULTRA'),('41.2','TRF'),('34.2','tantan-w200')]:
    num(300,old,D(extra['period_100_200_merged_bp'][tool])/1000000,f'results/regen/maize_extra_evidence.json period_100_200_merged_bp/{tool} /1e6')
for old,file in [('12.6','mo17_centc_arrays.bed'),('29.7','mo17_knob180_arrays.bed')]:
    rows=[l.split() for l in (ROOT/'results/ground_truth'/file).read_text().splitlines() if l and not l.startswith('#')]
    bp=sum(int(r[2])-int(r[1]) for r in rows)
    num(300,old,D(bp)/1000000,f'results/ground_truth/{file} sum(end-start)={bp} /1e6')
costs=load('docs/2026-09-05-astra-review/pass3-costs.json')
def runtime(tool,tag):
    pairs=[(k,v) for k,v in costs.items() if k.startswith('results/competitor_logs/'+tool+'__') and tag in k]
    assert len(pairs)==1,pairs
    return pairs[0][0],D(pairs[0][1]['seconds'])/3600
for line,old,tag in [(335,'5.2','exp3A'),(335,'5.5','exp3B'),(344,'131.9','Col-CEN'),(344,'5.5','exp3C')]:
    src,value=runtime('trf',tag);num(line,old,value,src+' elapsed seconds /3600 (pass3-costs.json cross-check)')
for old,supported,total in [('58.5',1162197,1987130),('53.5',797270,1490784),('59.7',839049,1405572),('59.2',1177244,1987130),('71.5',1065430,1490784),('71.6',1006546,1405572)]:
    num(341,old,D(supported)/total*100,f'results/regen/score_table1_regen_v2.txt supported/outGT = {supported}/{total}*100; published then all-other-tools block')
# S2 F/P have enough integer counts to avoid the coarse common 91.3 claim.
change(520,'The outside-catalog fractions of the two configurations both round to 91.3%: this also holds for the P run\'s unique calls.',
       f"The outside-catalog fractions of unique calls are {fmt(D(875084-76251)/875084*100)}% for F and {fmt(D(517791-44827)/517791*100)}% for P.",
       'results/regen/s2_F_p100.txt: (875084-76251)/875084*100; s2_P_p100.txt: (517791-44827)/517791*100')
change(294,'span approximately 0.18 points','span 0.18 points','P3-16 E26 author-approved; pass3-maize.json 58.68451580604715 -58.504213696130364 ->0.18')
# Author-requested representation rule, including explicit source precision exception.
change(86,'For the human genome (Experiment 1),',
       'Measured quantities and derived comparisons are reported to two decimal places using decimal half-up rounding, calculated from deposited values before rounding; counts remain integers and parameters, thresholds and version strings retain their native notation. Where the surviving source provides only coarser precision or an unlogged engineering observation, that precision is retained and the limitation is stated. For the human genome (Experiment 1),',
       'Author instruction; CLAUDE.md Numeric presentation; no new scientific claim')
# Source-limited call means are retained explicitly, not padded with zero.
change(250,'A user who needs contiguity should therefore stop well before that point.',
       'Calls-per-array means retain one decimal because the deposited summary stores only that precision; offsets converted from its integer-bp summaries do not recover sub-base precision. A user who needs contiguity should therefore stop well before that point.',
       'results/regen/maize_extra_evidence.json; score_maize_regen_evidence.py rounds calls_per_array to one decimal')
change(520,'This table describes what the unique calls look like,',
       'The six entropy-threshold and period-composition cells retain the one-decimal precision of the deposited summary. This table describes what the unique calls look like,',
       'results/regen/s2_F_p100.txt; prior L-09 reversion must not be undone')
(OUT/'manuscript.candidate.md').write_text(''.join(lines))
(OUT/'numeric-edits.json').write_text(json.dumps(edits,ensure_ascii=False,indent=2)+'\n')
print(f'{len(edits)} targeted numerical/representation edits written')
