#!/usr/bin/env python3
"""Read-only, cheap evidence checks. Run from the repository root; no rehashing.

Usage: python3 docs/2026-09-05-astra-review/pass1-checks.py SECTION
Sections: inventory, manifest, cen180, sacct, range, s4, ledger, logs, audit,
          sample, beds, ultra, figures
The sample section checks the fixed 20-file pre-edit sample (edits now mismatch).
"""
import collections
import csv
import hashlib
import gzip
import json
from pathlib import Path
import re
import subprocess
import sys


def sha(path):
    return subprocess.check_output(['sha256sum', str(path)], text=True).split()[0]


def rows(path, delimiter='\t'):
    with open(path) as fh:
        return list(csv.DictReader((s for s in fh if not s.startswith('#')), delimiter=delimiter))


def seconds(value):
    days, value = value.split('-') if '-' in value else ('0', value)
    return int(days)*86400 + sum(float(x)*60**i for i, x in enumerate(reversed(value.split(':'))))


section = sys.argv[1]
manifest = rows('results/manifest.tsv')
out = {}
if section == 'inventory':
    tracked = set(subprocess.check_output(['git', 'ls-files', 'results'], text=True).splitlines())
    for fn in ['results/manifest.sha256', 'results/external_evidence.sha256']:
        pairs = [s.split(None, 1) for s in Path(fn).read_text().splitlines()]
        paths = {p for h, p in pairs}
        out[fn] = dict(entries=len(pairs), missing=sorted(p for p in paths if not Path(p).is_file()))
        if 'external' not in fn:
            out[fn]['tracked_unlisted'] = sorted(tracked-paths-{'results/manifest.sha256', 'results/external_evidence.sha256'})
        else:
            out[fn]['manifest_external_unlisted'] = sorted({r['source_bed'] for r in manifest if r['source_bed'].startswith('/')}-paths)
elif section == 'manifest':
    out = []
    cache = {}
    for line, r in enumerate(manifest, 2):
        p = Path(r['source_bed'])
        d = dict(line=line, table=r['table'], row=r['row'], source_present=p.is_file(), commit=r['repo_commit'])
        d['commit_resolves'] = subprocess.run(['git', 'rev-parse', '--verify', r['repo_commit']+'^{commit}'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
        if p.is_file():
            with p.open('rb') as f:
                prefix = hashlib.sha256(f.read(1024**2)).hexdigest()[:16]
            d['source_prefix_ok'] = prefix == r['sha256_1MB'] if len(r['sha256_1MB']) == 16 else None
            d['bytes_ok'] = p.stat().st_size == int(r['bytes']) if r['bytes'].isdigit() else None
        sp = Path('scripts/scoring')/r['scorer'] if r['scorer'].endswith('.py') else p if r['scorer']=='self' else None
        if sp and sp.is_file():
            if str(sp) not in cache:
                versions = {}
                for c in subprocess.check_output(['git', 'log', '--all', '--format=%H', '--', str(sp)], text=True).split():
                    data = subprocess.run(['git', 'show', c+':'+str(sp)], capture_output=True)
                    if data.returncode == 0:
                        versions[c] = hashlib.sha256(data.stdout).hexdigest()
                cache[str(sp)] = (sha(sp), versions)
            h, versions = cache[str(sp)]
            d.update(scorer=str(sp), scorer_present=True, recorded_sha=r['scorer_sha'], current_sha=h,
                     current_match=h.startswith(r['scorer_sha']),
                     history_matches=[c for c, h in versions.items() if h.startswith(r['scorer_sha'])])
        out.append(d)
elif section == 'cen180':
    sets = [collections.Counter(tuple(l.split('\t')[:3]) for l in Path('results/ground_truth/'+p).read_text().splitlines())
            for p in ['colcen_cen180.bed', 'colcen_cen180_raw_blast_hits.bed']]
    f, r = sets
    out = dict(filtered=sum(f.values()), raw=sum(r.values()), filtered_unique=len(f), raw_unique=len(r),
               strict_subset=f < r, missing_from_raw=sum((f-r).values()), dropped=sum((r-f).values()))
elif section == 'sacct':
    records = rows('results/sacct_provenance.txt', '|')
    byid = {r['JobID']: r for r in records}
    out = dict(records=len(records), job_tasks=sum('.' not in k for k in byid),
               allocations=len({k.split('.')[0].split('_')[0] for k in byid}))
    out['headlines'] = {j: dict(elapsed=byid[j]['Elapsed'], hours=seconds(byid[j]['Elapsed'])/3600,
                               GiB=int(byid[j+'.batch']['MaxRSS'][:-1])/1024**2)
                        for j in ['6110900', '6110901', '6124640']}
    out['manifest_producer_jobs_without_record'] = sorted({r['producer_job'] for r in manifest
        if r['producer_job'][:1].isdigit() and r['producer_job'] not in byid
        and not any(k.startswith(r['producer_job']+'_') for k in byid)})
elif section == 'range':
    pairs = []
    for p in sorted(Path('results/range_cost_0363d8b').glob('*.log')):
        t = p.read_text()
        times = re.findall(r'time \(h:mm:ss or m:ss\): (\S+)', t)
        rss = [int(v)/1024**2 for v in re.findall(r'set size \(kbytes\): (\d+)', t)]
        pairs.append(dict(path=str(p), elapsed=times, seconds=[seconds(v) for v in times],
                          ratio=seconds(times[1])/seconds(times[0]), GiB=rss,
                          exit_calls=re.findall(r'exit=(\d+) calls=(\d+)', t)))
    out = dict(pairs=pairs, mean_ratio=sum(p['ratio'] for p in pairs)/len(pairs))
elif section == 's4':
    out = {}
    for p in sorted(Path('results/one_to_one').glob('*.json')):
        d = json.loads(p.read_text())
        out[p.name] = dict(matched=d['matched'], sensitivity=100*d['matched']/d['truth_records'],
                           precision=100*d['matched']/d['pred_records'], period=d['period'], strata=d['strata'])
        assert abs(out[p.name]['sensitivity']-d['sensitivity_1to1_maxcard']) < 1e-8
        assert abs(out[p.name]['precision']-d['precision_1to1_maxcard']) < 1e-8
    fn = 'results/one_to_one/one_to_one_trf_annot_r50.json'
    old = json.loads(subprocess.check_output(['git', 'show', '903245c:'+fn]))
    new = json.loads(Path(fn).read_text())
    out['TRF_changes_since_903245c'] = {k: dict(before=old.get(k), after=new.get(k))
                                      for k in old.keys() | new.keys() if old.get(k) != new.get(k)}
elif section == 'ledger':
    ledger = rows('results/tuning_ledger/ledger.tsv')
    out = dict(scored_rows=len(ledger), kinds=dict(collections.Counter(r['kind'] for r in ledger)),
               decisions=dict(collections.Counter(r['accepted'] for r in ledger)),
               cp3=[r for r in ledger if r['tag']=='f_cp3'],
               best=json.loads(Path('results/tuning_ledger/best.json').read_text()))
elif section == 'logs':
    out = []
    fields = ['Command being timed:', 'Elapsed (wall clock)', 'Maximum resident set size', 'Exit status:']
    for p in sorted(Path('results/competitor_logs').glob('*.log')):
        t = p.read_text()
        out.append(dict(path=str(p), bytes=p.stat().st_size, missing_fields=[f for f in fields if f not in t],
                        timing=[l.strip() for l in t.splitlines() if any(f in l for f in fields[1:])]))
elif section == 'audit':
    sheet = rows('results/audit11/reviewer_sheet.tsv')
    verdicts = rows('results/audit11/verdicts_reviewer2.tsv')
    key = rows('results/audit11/answer_key.tsv')
    assert {r['sample_id'] for r in sheet} == {r['sample_id'] for r in verdicts} == {r['sample_id'] for r in key}
    out = dict(sheet=len(sheet), verdicts=len(verdicts), key=len(key),
               totals=dict(collections.Counter(r['verdict'].strip().upper().replace('SUUPORTED', 'SUPPORTED') for r in verdicts)))
elif section == 'sample':
    saved = json.loads(Path('docs/2026-09-05-astra-review/pass1-checksum-sample.json').read_text())
    out = [dict(path=r['path'], before_matched=r['match'], now_matches=sha(r['path'])==r['recorded']) for r in saved]
elif section == 'beds':
    out = {}
    for species in ['colcen', 'human', 'maize']:
        h, n, size = hashlib.sha256(), 0, 0
        with gzip.open('results/beds/bwtandem_'+species+'.bed.gz', 'rb') as f:
            for line in f:
                h.update(line)
                n += 1
                size += len(line)
        recorded = json.loads(Path('results/regen/regen_'+species+'.provenance.json').read_text())['outputs'][0]
        out[species] = dict(calls=n, bytes=size, sha256=h.hexdigest(),
                            provenance_matches=h.hexdigest()==recorded['sha256'] and size==recorded['bytes'])
elif section == 'ultra':
    p = Path(next(r['source_bed'] for r in manifest if r['row']=='ULTRA-p2000-attempt'))
    b = p.read_bytes()
    lines = b.splitlines()
    out = dict(bytes=len(b), newlines=b.count(b'\n'), final_newline=b.endswith(b'\n'),
               data_field_counts=dict(collections.Counter(len(l.split(b'\t')) for l in lines[1:])),
               last_complete_endpoint=lines[-2].split(b'\t')[2].decode(),
               fragment_endpoint=lines[-1].split(b'\t')[2].decode())
elif section == 'figures':
    base = Path('results/figures/paper_figs')
    out = dict(rendered_pngs=len(list((base/'rendered').glob('*.png'))),
               rendered_pdfs=len(list((base/'rendered').glob('*.pdf'))),
               curve_rows=rows('results/figures/figure_curve_data.csv', ','),
               pairs=rows(base/'data/fig2a_paired_runs.csv', ','),
               fig2_root_equals_rendered={ext: (base/('fig2_range_cost.'+ext)).read_bytes()==
                                         (base/'rendered'/('fig2_range_cost.'+ext)).read_bytes()
                                         for ext in ['png', 'pdf']})
else:
    raise SystemExit('unknown section: '+section)
print(json.dumps(out, indent=2))
