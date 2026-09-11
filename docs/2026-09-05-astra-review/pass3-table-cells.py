#!/usr/bin/env python3
"""Compare every numerical Results-table cell with a named artifact field.
Read-only; run after pass3-checks.py modes to refresh raw-BED/accounting snapshots.
The generated TSV preserves row/column/line, expected/printed value and source.
"""
import csv,json,re,sys
from pathlib import Path
from decimal import Decimal,ROUND_HALF_UP
D=Path('docs/2026-09-05-astra-review')
read=lambda n:json.loads((D/n).read_text())
human=read('pass3-human.json');colcen=read('pass3-colcen.json');maize=read('pass3-maize.json');costs=read('pass3-costs.json')
extra=json.loads(Path('results/regen/maize_extra_evidence.json').read_text())['table3a']
extra_small=read('pass3-maize3a-extra.json')
manifest=list(csv.DictReader(open('results/manifest.tsv'),delimiter='\t'))
ms=Path(sys.argv[1] if len(sys.argv)>1 else 'manuscript.md').read_text().splitlines()
E={};records=[]
def expect(t,r,values,source,start=1):
    for i,v in enumerate(values,start):E[t,r,i]=(v,source)
def blocks(path):
    out={};head=None
    for line in Path(path).read_text().splitlines():
        if line.startswith('##########'):
            head=line.strip('# ');out[head]={}
        elif head:
            p=line.split()
            if len(p)>2 and p[1].isdigit():out[head][p[0]]=p[1:]
    return out
p100=blocks('results/regen/score_table1_p100.txt');h26=blocks('results/comparators2026/score_2026_human.txt')
def block(d,prefix):return next(v for k,v in d.items() if k.startswith(prefix))
base=block(p100,'BASELINE');matched=block(p100,'MATCHED');stratum=block(p100,'STRATUM')
adjusted=block(p100,'ADJUSTED PRECISION — full range, corroborators ULTRA+tantan')
adjmatch=block(p100,'ADJUSTED PRECISION — period <= 100, corroborators ULTRA+tantan')
leave=block(p100,'ADJUSTED PRECISION — full range, corroborators = all other tools')
for name in ['TRF','ULTRA','BWTandem','tantan','TRASH']:
    v=base[name];expect('1a',name,v[:3]+[adjusted[name][-1]]+v[3:]+[human[name]['unique_unfiltered']],
      'results/regen/score_table1_p100.txt: BASELINE/published support; pass3-checks.py human: unique_unfiltered')
    expect('1b',name,matched[name],'results/regen/score_table1_p100.txt: MATCHED RANGE')
    if name in stratum:expect('1c',name,stratum[name],'results/regen/score_table1_p100.txt: STRATUM')
    expect('1e',name,[adjusted[name][-1],leave[name][-1]],'results/regen/score_table1_p100.txt: full-range support blocks')
for name,alias in [('longdust (2026)','longdust'),('longdust `-k8 -w20000` (2026)','longdust-k8w20000'),("AniAnn's (2026)",'AniAnns')]:
    v=block(h26,'BASELINE')[alias];expect('1a',name,v[:3]+[None]+v[3:]+[None],'results/comparators2026/score_2026_human.txt: BASELINE')
    if alias=='AniAnns':
        expect('1b',name,block(h26,'MATCHED')[alias],'results/comparators2026/score_2026_human.txt: MATCHED')
        expect('1c',name,block(h26,'STRATUM')[alias],'results/comparators2026/score_2026_human.txt: STRATUM')
expect('1c','tantan (2,000 bp re-run)',stratum['tantan-w2000'],'results/regen/score_table1_p100.txt: STRATUM tantan-w2000')
for cfg,label in [('P','catch-all off'),('B','id 0.76'),('F','id 0.72, ≥3 copies'),('H','id 0.72')]:
    name=f'BWTandem-{cfg} ({label})';key=f'BWT-{cfg}-p100'
    expect('1d',name,base[key]+[adjusted[key][-1]],'results/regen/score_table1_p100.txt: native '+key)
for name in ['ULTRA','tantan','TRF','TRASH']:
    expect('1d',name,matched[name]+[adjmatch[name][-1]],'results/regen/score_table1_p100.txt: MATCHED and banded support')
for name,alias in [('TRF','TRF'),('mreps','mreps'),('ULTRA','ULTRA'),('BWTandem','BWTandem'),('tantan','tantan (500bp re-run)'),('NCRF','NCRF'),('TRASH (de novo)','TRASH-dn'),('TRASH (template)','TRASH-tpl'),('longdust (2026)','longdust (2026)'),('longdust `-k8 -w20000` (2026)','longdust -k8 -w20000 (2026)'),("AniAnn's (2026)","AniAnn's (2026)")]:
    v=colcen[alias];expect('2',name,[v[k] for k in ['regions','coverage','count','bp_precision','recall']],v['source']+'; pass3-checks.py colcen')
for name,alias in [('BWTandem','bwt'),('TRF','trf_3a'),('ULTRA','ultra_3a'),('tantan','tantan_3a'),('NCRF','NCRF'),('TRASH (de novo)','TRASH-dn'),('TRASH (template)','TRASH-tpl')]:
    v=extra[alias]['published_rule'] if alias in extra else extra_small[alias]['metrics']
    source='results/regen/maize_extra_evidence.json: table3a/'+alias if alias in extra else extra_small[alias]['source']+'; scan_3a'
    expect('3A',name,[v['bp'],v['regions'],v['tag_substring'],Decimal(v['longest_substring_bp'])/1000],source)
    if alias in extra:
        v=extra[alias]['band_1_6'];expect('3A-b',name,[v['bp'],v['regions'],v['tag_rotation'],Decimal(v['longest_rotation_bp'])/1000],source+'/band_1_6')
for name,alias in [('BWTandem','BWTandem'),('TRF','TRF'),('ULTRA','ULTRA'),('tantan','tantan'),('TRASH (de novo)','TRASH-de-novo'),('TRASH (template)','TRASH-template'),("AniAnn's (2026)","AniAnn's (2026)")]:
    v=maize['3B/'+alias+'/knob180'];k=v['unfiltered'];t=maize['3B/'+alias+'/TR-1']['unfiltered']
    expect('3B',name,[k['detected'],t['detected'],k['frag'],k['offset'],t['offset']],v['source']+'; pass3-checks.py maize raw calls')
    if alias!='TRASH-de-novo':
        v=maize['3C/'+alias+'/CentC'];c=v['unfiltered']
        expect('3C',name,[c['detected'],c['coverage'],c['frag'],c['offset']],v['source']+'; pass3-checks.py maize raw calls')
for cls in ['knob180','TR-1']:
    for name,alias in [('BWTandem','BWTandem'),('TRF','TRF'),('ULTRA','ULTRA'),('tantan','tantan'),('TRASH (de novo)','TRASH-de-novo')]:
        v=maize['3B/'+alias+'/'+cls]
        for rule in ['unfiltered','banded']:
            m=v[rule];expect('3B-b',cls+'/'+name+'/'+rule,[f"{m['detected']}/{m['total']}",m['coverage'],m['offset']],v['source']+'; pass3-checks.py maize '+rule,start=3)
for name in ['BWTandem','TRF','ULTRA','tantan']:
    v=maize['3C/'+name+'/CentC']
    for rule in ['unfiltered','banded']:
        m=v[rule];expect('3C-b',name+'/'+rule,[f"{m['detected']}/{m['total']}",m['coverage'],m['offset'],v['loss'] if rule=='banded' else None],v['source']+'; pass3-checks.py maize '+rule,start=2)
for table in ['3B','3C']:
    for name in ['longdust (2026)','longdust `-k8 -w20000` (2026)']:
        expect(table,name,[0,0,None,None,None] if table=='3B' else [0,0,None,None],'results/comparators2026/score_2026_maize.txt: no calls at gap zero')
# Supplementary data tables.
s2=[('Calls',875084,3118067),('Share of BWTandem output (%)',100*875084/3993151,100*3118067/3993151),('Median call length (bp)',25,24),('Mean motif entropy (bits)',1.241,1.030),('Motif entropy below 1 bit (%)',38.9,46.4),('Period 1–2 bp (%)',13.2,24.8),('Period 21–100 bp (%)',21.9,6.1),('Outside the adotto catalog (%)',100*(1-76251/875084),100*(1-1945232/3118067))]
for name,u,v in s2:expect('S2',name,[u,v],'results/regen/s2_F_p100.txt: '+name)
idbase=block(blocks('results/regen/score_table1_idsweep.txt'),'BASELINE')
for name in ['pass disabled','0.80','0.76','0.72','0.68']:
    expect('S3',name,idbase['BWT-id-'+('off' if name=='pass disabled' else name)][1:3],'results/regen/score_table1_idsweep.txt: BASELINE')
for name,slug in [('ULTRA','ultra'),('BWTandem','bwtandem'),('TRF','trf'),('tantan','tantan'),('TRASH','trash')]:
    for panel,mid in [('a',''),('b','_annot')]:
        path=f'results/one_to_one/one_to_one_{slug}{mid}_r50.json';d=json.loads(Path(path).read_text())
        vals=[d['matched'],100*d['matched']/d['truth_records'],100*d['matched']/d['pred_records']]
        if panel=='b':vals += [d['boundary']['start_offset_median'],d['period']['exact_pct'],d['copies']['rel_error_median_pct'] if name=='BWTandem' else None]+[100*d['strata'][b]['matched']/d['strata'][b]['truth'] for b in ['1-6','7-20','21-100','101-2000']]
        expect('S4'+panel,name,vals,path)
# Cost cells: exact raw log seconds / KiB, not the printed manifest rounding.
def log(prefix,contains):
    hits=[(p,v) for p,v in costs.items() if p.startswith('results/competitor_logs/'+prefix+'__') and contains in p]
    assert len(hits)==1,(prefix,contains,hits)
    return hits[0]
def fromcost(table,name,key,v):
    pos={'1a':8,'1d':7,'2':6,'3A':5,'3B':6,'3C':5}[table]
    expect(table,name,[Decimal(str(v['seconds']))/3600,Decimal(v['rss_kib'])/1024**2] if table!='1d' else [Decimal(str(v['seconds']))/3600],key,start=pos)
for table in ['1a','2','3A','3B','3C']:
    genome='GCA_000001405.15' if table=='1a' else 'Col-CEN_v1.2' if table=='2' else 'exp'+table
    for name in ['TRF','ULTRA','tantan','NCRF','TRASH'] if table=='1a' else []:pass
    for name,tool in [('TRF','trf'),('ULTRA','ultra'),('tantan','tantan')]:
        if (table=='2' and name in ['ULTRA','tantan']) or (table in ['3B','3C'] and name=='tantan'):
            job={('2','ULTRA'):'5981977',('2','tantan'):'6085141',('3B','tantan'):'6085142',('3C','tantan'):'6085143'}[table,name]
            key='sacct:'+job+'.batch';v=costs[key]
        else:key,v=log(tool,genome)
        fromcost(table,name,key,v)
    job={'1a':'6110901','2':'6110900','3A':'6124640','3B':'6124640','3C':'6124640'}[table];key='sacct:'+job+'.batch';fromcost(table,'BWTandem',key,costs[key])
for table,name,tool,contains in [('1a','mreps','mreps','GCA_000001405.15'),('1a','TRASH','trash','GCA_000001405.15'),('2','NCRF','ncrf','Col-CEN'),('2','TRASH (de novo)','trash','Col-CEN_v1.2_denovo'),('3A','NCRF','ncrf','TAG_exp3A'),('3A','TRASH (de novo)','trash','denovo_exp3A'),('3A','TRASH (template)','trash','templates_TAG_exp3A'),('3B','TRASH (de novo)','trash','denovo_exp3B'),('3B','TRASH (template)','trash','templates_knob180_exp3B'),('3C','TRASH (template)','trash','templates_CentC_exp3C')]:
    key,v=log(tool,contains);fromcost(table,name,key,v)
fromcost('2','mreps','sacct:5981987.batch',costs['sacct:5981987.batch'])
a,va=log('trash','Col-CEN_v1.2_CEN159');b,vb=log('trash','Col-CEN_v1.2_CEN178');fromcost('2','TRASH (template)',a+' + '+b,{'seconds':va['seconds']+vb['seconds'],'rss_kib':max(va['rss_kib'],vb['rss_kib'])})
for table,genome in [('1a','human'),('2','colcen'),('3B','maize'),('3C','maize')]:
    for name,tail in [('longdust (2026)',f'longdust_{genome}_default.time'),('longdust `-k8 -w20000` (2026)',f'longdust_{genome}_k8w20000.time'),("AniAnn's (2026)",f'anianns_{genome}.time')]:
        key=next(k for k in costs if k.endswith('/'+tail));fromcost(table,name,key,costs[key])
for name in ['ULTRA','tantan','TRF','TRASH']:
    key,v=log(name.lower(),'GCA_000001405.15');fromcost('1d',name,key,v)
# Scan the manuscript and keep every cell, including unsupported costs and NA cells.
current=None;header=None;cls='';panel='a'
for lineno,line in enumerate(ms,1):
    match=re.match(r'\s*(?:Supplementary )?Table (1[a-e]|2|3[A-C](?:-b)?|S[1-4])\.',line)
    if line.strip()=='4. Discussion':current=None;header=None
    if match:current=match[1];header=None
    if current=='S4' and line.startswith('(b)'):panel='b';header=None
    if not line.startswith('|') or current is None:continue
    cells=[v.strip() for v in line.strip().strip('|').split('|')]
    if all(re.fullmatch(r'[-: ]+',v) for v in cells):continue
    if header is None:header=cells;continue
    table=current+panel if current=='S4' else current
    if table=='S1':continue # Command/version fields are audited against logs by pass 2 and in the report.
    name=re.sub(r' [‡†§¶‖]','',cells[0])
    if table=='3B-b':
        cls=cells[0] or cls;name=cls+'/'+re.sub(r' [‡†§¶‖]','',cells[1])+'/'+cells[2]
    elif table=='3C-b':name+='/'+cells[1]
    for i,printed in enumerate(cells[1:],1):
        if not re.fullmatch(r'[−-]?[\d,.]+(?:/\d+)?',printed):continue
        expected,source=E.get((table,name,i),(None,'NO FIELD MAPPING'))
        if table=='1d' and name.startswith('BWTandem-') and i==7:
            row=next(r for r in manifest if r['table']=='1d' and r['row']==name.split(' ')[0]);expected=row['elapsed'];source='results/manifest.tsv; original sacct absent for '+row['producer_job'];verdict='BLOCKED-ON-MISSING-ARTIFACT'
        elif expected is None:verdict='BLOCKED-ON-MISSING-ARTIFACT'
        elif '/' in printed:verdict='REJECTED' if printed==str(expected) else 'CONFIRMED'
        else:
            cleaned=printed.replace(',','').replace('−','-');places=len(cleaned.split('.')[1]) if '.' in cleaned else 0
            wanted=Decimal(str(expected)).quantize(Decimal(1).scaleb(-places),rounding=ROUND_HALF_UP)
            verdict='REJECTED' if Decimal(cleaned)==wanted else 'CONFIRMED'
        records.append([table,lineno,name,header[i],printed,str(expected),verdict,source])
w=csv.writer(sys.stdout,delimiter='\t',lineterminator='\n');w.writerow(['table','manuscript_line','row','column','printed','artifact_value','verdict','source']);w.writerows(records)
