#!/usr/bin/env python3
"""Export the unchanged accuracy plot without its overlapping legacy caption.

Use the bwtandem environment. Only presentation files in the supplied directory
are written. CSVs and the deposited plotting script remain unchanged.
"""
import hashlib
import json
import os
from pathlib import Path
import runpy
import sys

root = Path.cwd()
source = root / 'results/figures/paper_figs'
out = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else root / 'submission/figures'
out.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(source))
import figstyle

inputs = [source / 'plot_fig1_accuracy_tradeoff.py', source / 'figstyle.py',
          source / 'data/fig1ab_pr_points.csv', source / 'data/fig1c_overlap_rules.csv']
record = {'inputs': {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
          'operation': 'Remove only the legacy Figure 1 figtext caption; unchanged script and CSVs; no scoring.'}

def save(fig, stem):
    assert stem == 'fig1_accuracy_tradeoff'
    captions = [t for t in fig.texts if 'Figure' in t.get_text()]
    assert len(captions) == 1
    captions[0].remove()
    for ext in ('pdf', 'png'):
        fig.savefig(out / (stem + '.' + ext), bbox_inches='tight')

figstyle.save = save
os.chdir(source)
runpy.run_path(str(inputs[0]), run_name='__main__')
record['outputs'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in out.glob('fig1_accuracy_tradeoff.*')}
(out / 'accuracy-export-receipt.json').write_text(json.dumps(record, indent=2) + '\n')
print('Exported unchanged accuracy plot with all axis labels and without its legacy caption.')
