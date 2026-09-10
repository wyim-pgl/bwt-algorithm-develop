"""Recalculate registered derived claims; no benchmark reruns or intersections.
Run from the repository root; accepts an optional report path.
This verifies registered arithmetic and JSON/cost operands, not semantic completeness.
"""
import ast, csv, json, operator, re, sys
from collections import Counter
from decimal import Decimal as D, ROUND_HALF_UP
from pathlib import Path
report=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('derived-claims.json')
rows=json.loads(report.read_text())['claims']
cache={}
def get(path):
    if path not in cache: cache[path]=json.loads(Path(path).read_text(),parse_float=D)
    return cache[path]
def calc(node,a):
    if isinstance(node,ast.Expression): return calc(node.body,a)
    if isinstance(node,ast.Index): return calc(node.value,a)  # Python 3.8 compatibility
    if isinstance(node,ast.Constant) and isinstance(node.value,(int,float)): return D(str(node.value))
    if isinstance(node,ast.List): return [calc(n,a) for n in node.elts]
    if isinstance(node,ast.Subscript) and isinstance(node.value,ast.Name) and node.value.id=='a':
        return a[int(calc(node.slice,a))]
    if isinstance(node,ast.BinOp):
        fn={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv}[type(node.op)]
        return fn(calc(node.left,a),calc(node.right,a))
    if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id in ('min','max') and not node.keywords:
        return {'min':min,'max':max}[node.func.id](*[calc(n,a) for n in node.args])
    raise ValueError(ast.dump(node))
assert str(D('12.645').quantize(D('.01'),rounding=ROUND_HALF_UP))=='12.65'
verified=Counter()
costs=get('docs/2026-09-05-astra-review/pass3-costs.json')
for c in rows:
    if c.get('rounded_half_up') is None:continue
    operands=[]
    for op in c['operands']:
        v=D(op['value']);operands.append(v);path=op['path'];key=op.get('key')
        if isinstance(key,list) and path.endswith('.json'):
            actual=get(path)
            for k in key:actual=actual[k]
            assert D(str(actual))==v,(c['claim_id'],op,actual)
            verified['JSON operands']+=1
        elif isinstance(key,str) and '/' in key and key.rsplit('/',1)[0] in costs:
            costkey,field=key.rsplit('/',1)
            assert D(str(costs[costkey][field]))==v,(c['claim_id'],op)
            verified['cost-cache operands']+=1
        else:verified['other cited operands (not source-replayed here)']+=1
    result=calc(ast.parse(c['formula'],mode='eval'),operands)
    assert result.quantize(D('.01'),rounding=ROUND_HALF_UP)==D(c['rounded_half_up']),(c['claim_id'],result)
    verified['formula results']+=1
remaining=json.loads(report.with_name('remaining-sources.json').read_text())
accounting={r['JobID']:r for r in csv.DictReader((l for l in Path('results/sacct_provenance.txt').read_text().splitlines() if not l.startswith('#')),delimiter='|')}
def seconds(text):
    days, clock=(text.split('-',1) if '-' in text else ('0',text))
    value=D(0)
    for part in clock.split(':'):value=value*60+D(part)
    return value+D(days)*86400
for name,series in remaining['runtime_series'].items():
    for value,source in zip(series['seconds'],series['sources']):
        if source['path']=='results/sacct_provenance.txt':
            actual=seconds(accounting[source['key'].split('/')[0]]['Elapsed'])
        else:
            arm='100' if name.endswith('p100') else '2000'
            text=Path(source['path']).read_text().split('--- ARM MAXP='+arm+' start ',1)[1]
            elapsed=re.search(r'Elapsed \(wall clock\) time \(h:mm:ss or m:ss\):\s*(\S+)',text).group(1)
            actual=seconds(elapsed)
        assert actual==value,(name,source,actual,value)
    mean=D(sum(series['seconds']))/(len(series['seconds'])*3600)
    assert mean.quantize(D('.01'),rounding=ROUND_HALF_UP)==D(series['half_up_mean_hours']),name
    verified['runtime means from raw elapsed records']+=1
print(json.dumps(dict(verified),indent=2))
print('PASS: registered arithmetic; other cited operands require their recorded source checks')
