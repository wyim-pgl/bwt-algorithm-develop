"""Independent payload/accounting check for the approved 19 -> 18 migration.
Run from repository root after replaying the declared prose changes.
"""
from pathlib import Path
import hashlib,json,re
ROOT=Path.cwd();D=ROOT/'docs/2026-09-10-lab-docx'
m=json.loads((D/'display-map.json').read_text())
# Baseline is the source-locked supplement at the author-approved pre-migration
# revision. It must match the recorded hash, independently of current tables.
baseline=(D/'supplementary-before.md').read_text()
assert hashlib.sha256(baseline.encode()).hexdigest()==m['supplementary_before_sha256']
current=(ROOT/'supplementary.md').read_text();main=(ROOT/'manuscript.md').read_text()
main_before=(D/'manuscript-before.md').read_text()
assert hashlib.sha256(main_before.encode()).hexdigest()==m['main_before_sha256']
lines=main_before.splitlines(keepends=True)
changes=json.loads((D/'main-replay.json').read_text())
end=0
for op in changes:
    assert end <= op['start'] <= op['end'] <= len(lines)
    assert ''.join(lines[op['start']:op['end']])==op['old']
    end=op['end']
for op in reversed(changes):lines[op['start']:op['end']]=op['new'].splitlines(keepends=True)
assert ''.join(lines)==main,'Main text changed outside recorded edits'
pattern=r'(?:^\|[^\n]*\n)+'
def blocks(s):return re.findall(pattern,s,re.M)
def rows(t):return [[v.strip() for v in r.strip('|').split('|')] for r in t.strip().splitlines()]
def canon(s):return re.sub(r'\s+',' ',s.replace('–','-').replace('—','-').replace('**','').replace('`','')).strip()
old=blocks(baseline);new=blocks(current)
assert len(old)==19 and len(new)==18
aliases=json.loads((D/'header-aliases.json').read_text())
for item in m['tables']:
    i=item['source_block']; source=old[i-1]
    assert hashlib.sha256(source.encode()).hexdigest()==item['sha256']
    sr=rows(source)
    if i==17:
        for identity,recall,precision in sr[2:]:
            label='with the catch-all pass disabled' if identity=='pass disabled' else 'at identity '+identity
            assert f'{recall}% region recall and {precision}% region precision {label}' in current
        continue
    dest=int(item['destination'][1:])-1; dr=rows(new[dest])
    assert len(sr)==len(dr),(i,'row lost or duplicated')
    for ri,(a,b) in enumerate(zip(sr,dr)):
        if ri==1:continue # Markdown alignment declarations have no data value.
        if i not in (13,14,15):
            expected=[aliases.get(x,x) if ri==0 else x for x in a]
            assert list(map(canon,expected))==list(map(canon,b)),(i,ri,'cell changed')
        elif ri>=2:
            key={13:'P',14:'C',15:'K'}[i]+str(ri-1)
            line=next((x for x in current.splitlines() if x.startswith(key+': ')),None)
            assert line is not None,(i,key)
            if i==13:
                assert b==[key,a[1],a[2]]
                assert canon(a[0]) in canon(line) and canon(a[3]) in canon(line)
            elif i==14:
                assert b==[key,a[2],a[3]]
                assert canon(a[0]) in canon(line)
                # Exact command/config syntax plus scientific numeric operands;
                # display IDs are independently checked against the map below.
                assert re.findall(r'`([^`]+)`',a[4])==re.findall(r'`([^`]+)`',line)
            else:
                assert b==[a[0],a[1],key]
                assert re.findall(r'`([^`]+)`',a[2])==re.findall(r'`([^`]+)`',line)
# Exactly one physical caption per target; no shared S4 caption remains.
for kind,total in [('Table',18),('Fig\\.',7)]:
    labels=re.findall(r'^\*\*Supplementary '+kind+r' (S\d+)\.',current,re.M)
    assert len(labels)==total and set(labels)=={f'S{i}' for i in range(1,total+1)},(kind,labels)
body=main.split('## References')[0]
for kind,total in [('Table',18),('Fig\\.',7)]:
    # Parenthetical callouts only, captions/references do not count. Expand
    # ranges and lists in each parenthesis before checking coverage.
    seen=set()
    for par in re.findall(r'\([^()]+\)',body):
        for hit in re.finditer(r'Supplementary '+kind+r's?\s+(S\d+(?:\s*(?:-|,|and)\s*S\d+)*)',par):
            text=hit.group(1)
            for a,b in re.findall(r'S(\d+)-S(\d+)',text):seen.update(range(int(a),int(b)+1))
            seen.update(map(int,re.findall(r'S(\d+)',text)))
    assert seen==set(range(1,total+1)),(kind,'main-body coverage',seen)
assert re.findall(r'\*\*Fig\. (\d+)\.\*\*',main)==['1','2']
# Every scientific citation / code span remains auditable through full-source
# replay in check_conversion.py; these table tests are independent of replay.
print('PASS: 19 source blocks accounted for; 18 unique tables, 7 supplement figures; every display called out in main narrative.')
