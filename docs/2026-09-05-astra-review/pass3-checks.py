#!/usr/bin/env python3
"""Read-only pass-3 artifact checks. Run from repository root; outputs go to stdout."""
import ast, bisect, csv, gzip, importlib.util, json, re, sys
from pathlib import Path
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[2]
MAN=list(csv.DictReader((ROOT/'results/manifest.tsv').open(),delimiter='\t'))
def module(path):
    spec=importlib.util.spec_from_file_location(Path(path).stem,ROOT/path)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
def path_for(table,row):
    return next(r['source_bed'] for r in reversed(MAN) if r['table']==table and r['row']==row)
def lines(path):
    with (gzip.open(path,'rt') if str(path).endswith('.gz') else open(path)) as f:
        yield from f
def bed(path, chroms=None):
    out=defaultdict(list)
    for line in lines(path):
        p=line.rstrip('\n').split('\t')
        if len(p)<3 or (chroms and p[0] not in chroms):continue
        try:s,e=int(p[1]),int(p[2])
        except ValueError:continue
        out[p[0]].append((s,e,p))
    return out
def recalls(calls, truth, merge):
    merged={c:merge(v) for c,v in calls.items()}
    ends={c:[e for s,e in v] for c,v in merged.items()}
    hit=[]
    for c,s,e,p in truth:
        i=bisect.bisect_right(ends.get(c,[]),s)
        hit.append(i<len(merged.get(c,[])) and merged[c][i][0]<e)
    return hit

def colcen():
    sc=module('scripts/scoring/score_colcen.py')
    truth=sc.load_flat('results/ground_truth/colcen_cen180.bed')
    cens=[(c,s,e) for c,s,e,p in sc.load_flat('results/ground_truth/colcen_centromeres.bed')]
    out={}
    cases=[(r['row'],r['source_bed']) for r in MAN if r['table']=='2']
    cases += [(r['row'],r['source_bed']) for r in MAN if r['table']=='ablation' and r['row'].startswith('gapfill')]
    for name,path in cases:
        calls=bed(path,sc.CHROMS)
        allc={c:[(s,e) for s,e,p in v] for c,v in calls.items()}
        hit=recalls(allc,truth,sc.merge)
        bands={}
        for lo,hi in [(150,200),(150,400)]:
            b=sc.band_calls(calls,lo,hi)
            bands[f'{lo}-{hi}']=100*sum(recalls(b,truth,sc.merge))/len(truth)
        strata=[]
        for lo,hi in [(80,85),(85,90),(90,95),(95,99),(99,101)]:
            ix=[i for i,(_,_,_,p) in enumerate(truth) if lo<=float(p[4])<hi]
            strata.append({'band':[lo,hi],'n':len(ix),'hit':sum(hit[i] for i in ix),'recall':100*sum(hit[i] for i in ix)/len(ix)})
        out[name]={'source':path,'regions':sum(map(len,calls.values())),
          'coverage':sc.centromere_coverage(calls,cens),'count':sc.count_in_centromeres(sc.band_calls(calls,150,200),cens),
          'bp_precision':sc.cen180_bp_precision(calls,truth),'recall':100*sum(hit)/len(truth),'band_recall':bands,'strata':strata}
    lens=[e-s for c,s,e,p in truth]
    out['truth']={'count':len(truth),'min_length':min(lens),'max_length':max(lens),'175-179':100*sum(175<=n<=179 for n in lens)/len(lens)}
    print(json.dumps(out,indent=2))

def maize():
    sc=module('scripts/scoring/rescore_tables_3bc.py')
    out={}
    for table,clslist in [('3B',['knob180','TR-1']),('3C',['CentC'])]:
        entries=[('BWTandem',path_for(table,'BWTandem')),('TRF',path_for(table,'TRF')),('ULTRA',path_for(table,'ULTRA')),
          ('tantan',path_for(table,'tantan (500bp re-run)' if table=='3B' else 'tantan (200bp re-run)')),
          ('TRASH-template',path_for(table,'TRASH-tpl' if table=='3B' else 'TRASH')),
          ("AniAnn's (2026)",path_for(table,"AniAnn's (2026)"))]
        if table=='3B': entries.append(('TRASH-de-novo',path_for(table,'TRASH')))
        for name,path in entries:
            rows=defaultdict(list)
            # Only raw calls intersecting a scored array can affect these metrics.
            # Filtering first avoids repeatedly sorting millions of irrelevant calls.
            targets=defaultdict(list)
            for cls in clslist:
                gtfile={'knob180':'knob180','TR-1':'tr1','CentC':'centc'}[cls]
                for c,s,e in sc.sx.load_gt(f'results/ground_truth/mo17_{gtfile}_arrays.bed'):targets[c].append((s,e))
            for line in lines(path):
                p=line.rstrip('\n').split('\t');c=p[0]
                if c not in targets:continue
                s,e=int(p[1]),int(p[2])
                if not any(s<ge and e>gs for gs,ge in targets[c]):continue
                try:period=int(p[4])
                except (ValueError,IndexError):period=len(p[3]) if len(p)>3 else 0
                rows[c].append((s,e,period))
            for cls in clslist:
                gtfile={'knob180':'knob180','TR-1':'tr1','CentC':'centc'}[cls]
                truth=sc.sx.load_gt(f'results/ground_truth/mo17_{gtfile}_arrays.bed')
                u=sc.metrics(rows,truth)
                # Do not manufacture the missing 2026 banded scoring deposit in this pass.
                b=sc.metrics(rows,truth,(100,500 if table=='3B' else 200)) if '2026' not in name else None
                out[f'{table}/{name}/{cls}']={'source':path,'unfiltered':u,'banded':b,'loss':b['coverage']-u['coverage'] if b else None}
    print(json.dumps(out,indent=2))

def costs():
    out={}
    for p in sorted(Path('results/competitor_logs').glob('*.log')):
        s=p.read_text(errors='replace')
        elapsed=re.search(r'Elapsed \(wall clock\) time \(h:mm:ss or m:ss\):\s*(\S+)',s)
        rss=re.search(r'Maximum resident set size \(kbytes\):\s*(\d+)',s)
        if elapsed and rss:
            sec=0
            for n in elapsed[1].split(':'):sec=sec*60+float(n)
            out[str(p)]={'seconds':sec,'hours':sec/3600,'rss_kib':int(rss[1]),'gib':int(rss[1])/1024**2}
    for r in csv.DictReader((l for l in open('results/sacct_provenance.txt') if not l.startswith('#')),delimiter='|'):
        if r['MaxRSS'].endswith('K') and r['JobID'].endswith('.batch'):
            elapsed=r['Elapsed'];days=0
            if '-' in elapsed:days,elapsed=elapsed.split('-');days=int(days)
            sec=days*86400
            h,m,s=map(int,elapsed.split(':'));sec+=h*3600+m*60+s
            out['sacct:'+r['JobID']]={'seconds':sec,'hours':sec/3600,'rss_kib':int(r['MaxRSS'][:-1]),'gib':int(r['MaxRSS'][:-1])/1024**2}
    for p in sorted(Path('/data/gpfs/assoc/pgl/devel/exp1_human/tools2026/runs').glob('*.time')):
        s=p.read_text(errors='replace');elapsed=re.search(r'Elapsed \(wall clock\) time \(h:mm:ss or m:ss\):\s*(\S+)',s);rss=re.search(r'Maximum resident set size \(kbytes\):\s*(\d+)',s)
        if elapsed and rss:
            sec=0
            for n in elapsed[1].split(':'):sec=sec*60+float(n)
            out[str(p)]={'seconds':sec,'hours':sec/3600,'rss_kib':int(rss[1]),'gib':int(rss[1])/1024**2}
    print(json.dumps(out,indent=2))

def fig5():
    p=Path('results/figures/paper_figs/plot_fig5_array_structure.py')
    tree=ast.parse(p.read_text())
    regions=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='REGIONS' for t in n.targets))
    for (label,fa,chrom,start,end,period),table in zip(regions,['1a','2','3C']):
        matches=[]
        for line in lines(path_for(table,'BWTandem')):
            fields=line.split('\t')
            if fields[0]==chrom and int(fields[1])<end and int(fields[2])>start:
                matches.append([int(fields[1]),int(fields[2]),len(fields[3])])
        print(json.dumps({'label':label,'fasta_exists':Path(fa).exists(),'region':[chrom,start,end,period],'overlapping_deposited_calls':matches}))

def human():
    import numpy as np
    from array import array
    def load(path):
        d=defaultdict(lambda:array('q'))
        for l in lines(path):
            p=l.rstrip('\n').split('\t')
            if len(p)<3:continue
            try:s,e=int(p[1]),int(p[2])
            except ValueError:continue
            try:per=int(p[4])
            except (ValueError,IndexError):per=len(p[3]) if len(p)>3 else 0
            d[p[0]].extend((s,e,per))
        return {c:np.frombuffer(v,dtype=np.int64).reshape(-1,3).copy() for c,v in d.items()}
    def index(d):
        out={}
        for c,v in d.items():
            v=v[np.argsort(v[:,0],kind='stable')]
            out[c]=(v[:,0],np.maximum.accumulate(v[:,1]))
        return out
    def hit(v,idx,c):
        if c not in idx or len(idx[c][0])==0:return np.zeros(len(v),dtype=bool)
        starts,ends=idx[c];i=np.searchsorted(starts,v[:,1],side='left')-1
        return (i>=0)&(ends[np.maximum(i,0)]>v[:,0])
    truth=load('/data/gpfs/assoc/pgl/devel/exp1_human/data/adotto_primary.bed')
    gtidx=index(truth);ntruth=sum(map(len,truth.values()))
    names=['BWTandem','TRF','ULTRA','tantan','TRASH']
    data={n:load(path_for('1a',n)) for n in names}
    indexes={n:index(v) for n,v in data.items()}
    result={}
    for name,d in data.items():
        unique=outside=0
        for c,v in d.items():
            supported=np.zeros(len(v),dtype=bool)
            for n,idx in indexes.items():
                if n!=name:supported|=hit(v,idx,c)
            unique+=int((~supported).sum())
            outside+=int(((~supported)&(~hit(v,gtidx,c))).sum())
        result[name]={'source':path_for('1a',name),'unique_unfiltered':unique,'unique_outside_catalog':outside,'scores':{}}
        for band,lo,hi in [('full',0,10**9),('le100',1,100),('101-2000',101,2000)]:
            part={c:v[(v[:,2]>=lo)&(v[:,2]<=hi)] for c,v in d.items() if c in truth}
            idx=index(part);ng=sum(int(hit(v,idx,c).sum()) for c,v in truth.items())
            npred=sum(map(len,part.values()));nt=sum(int(hit(v,gtidx,c).sum()) for c,v in part.items())
            result[name]['scores'][band]={'calls':npred,'truth_hits':ng,'pred_hits':nt,'recall':100*ng/ntruth,'precision':100*nt/npred if npred else 0}
    # The permissive native point is needed to check the 0.02/5.22-point claims.
    d=load(path_for('1d','BWTandem-H'));idx=index(d)
    ng=sum(int(hit(v,idx,c).sum()) for c,v in truth.items());npred=sum(map(len,d.values()));nt=sum(int(hit(v,gtidx,c).sum()) for c,v in d.items())
    result['native-H']={'calls':npred,'truth_hits':ng,'pred_hits':nt,'recall':100*ng/ntruth,'precision':100*nt/npred}
    print(json.dumps(result,indent=2))

if __name__=='__main__':globals()[sys.argv[1]]()
