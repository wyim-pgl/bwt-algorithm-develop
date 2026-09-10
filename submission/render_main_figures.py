#!/usr/bin/env python3
"""Presentation-only re-render of the two main figures (final-check F5).

Runs the deposited plotting scripts unchanged from results/figures/paper_figs,
reading only the deposited CSVs, then applies presentation fixes before saving
into submission/figures: larger type for the journal column scale, separated
range-ratio labels, and higher-contrast competitor markers. No data value,
point, line, panel or measured label text is added, removed or changed.
Deposited scripts, CSVs and rendered evidence figures remain untouched.

Supersedes submission/figures/accuracy-export-receipt.json (fig1) and the
former crop-receipt.json entry for fig2_range_cost (see render-receipt.json).
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
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# The deposited layouts are 16-18 in wide but print at 171.7 mm (scale ~0.35),
# leaving 3-4 pt effective type (final-check W2). font_scale 2.0 gives ~6-7 pt
# axis/tick/legend type at print; dense point labels are kept smaller (0.72 of
# that) so the crowded precision-recall panels do not collide.
FONT_SCALE = 2.0
LABEL_SHRINK = 0.72

def setup():
    sns.set_theme(style='ticks', context='paper', font_scale=FONT_SCALE)
    plt.rcParams.update({
        'figure.dpi': 300, 'savefig.dpi': 300,
        'axes.spines.top': False, 'axes.spines.right': False,
        'pdf.fonttype': 42,
        'mathtext.fontset': 'custom', 'mathtext.bf': 'sans:bold',
    })

inputs = [source / 'plot_fig1_accuracy_tradeoff.py', source / 'plot_fig2_range_cost.py',
          source / 'figstyle.py',
          source / 'data/fig1ab_pr_points.csv', source / 'data/fig1c_overlap_rules.csv',
          source / 'data/fig2a_paired_runs.csv', source / 'data/fig2b_maize_scaling.csv',
          source / 'data/fig2c_human_cost.csv']
record = {
    'operation': ('Re-render both main figures from the deposited scripts and CSVs with '
                  'font_scale 2.0 (dense point labels 0.72 of that), removal of the '
                  'embedded legacy caption text, vertical separation of the three '
                  'range-ratio labels (fig2 panel A), legend/note de-collision, and '
                  'alpha 0.55 plus dark marker edges for the TRF/TRASH series and legend '
                  '(fig1 panel C). No data value or measured label text changed.'),
    'font_scale': FONT_SCALE,
    'supersedes': ['accuracy-export-receipt.json',
                   'crop-receipt.json entry for fig2_range_cost'],
    'renderer_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'inputs': {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
               for p in inputs},
}

def save(fig, stem):
    captions = [t for t in fig.texts if 'Figure' in t.get_text()]
    assert len(captions) == 1, stem  # the legacy embedded caption only
    captions[0].remove()
    for t in fig.texts:  # headline text placed at an explicit 14 pt
        if round(t.get_fontsize()) == 14:
            t.set_fontsize(24)
    if fig._suptitle is not None:
        fig._suptitle.set_fontsize(24)
    if stem == 'fig2_range_cost':
        ax_a, ax_b, ax_c1, ax_c2 = fig.axes[:4]
        ratio = sorted((t for t in ax_a.texts if '×' in t.get_text()),
                       key=lambda t: t.xy[1], reverse=True)
        assert len(ratio) == 3, [t.get_text() for t in ratio]
        # Same anchors and label text; only the offsets change so the enlarged
        # labels cannot overlap (W2 measured a 3.3 pt collision), and headroom
        # is added so the top label stays inside the axes.
        ax_a.set_ylim(top=ax_a.get_ylim()[1] + 0.45)
        for t, offset in zip(ratio, ((8, 18), (8, -4), (8, -26))):
            t.set_verticalalignment('center')
            t.xyann = offset
        # Panel B: keep the disclaimer note readable but subordinate, and move
        # the legend clear of it.
        for t in ax_b.texts:
            t.set_fontsize(11)
        ax_b.legend(loc='lower right')
        # Panel C: shorter titles were not authored, so shrink the two long
        # titles instead, drop the redundant seaborn 'tool' axis label and keep
        # the period-cap labels subordinate.
        for ax in (ax_c1, ax_c2):
            ax.title.set_fontsize(ax.title.get_fontsize() * 0.72)
            for t in ax.texts:
                t.set_fontsize(12)
        ax_c1.set_ylabel('')
    if stem == 'fig1_accuracy_tradeoff':
        ax_a, ax_b, ax_c = fig.axes[:3]
        # Dense point labels: smaller than axis type, still ~2x the deposited
        # effective size.
        for ax in (ax_a, ax_b):
            for t in ax.texts:
                t.set_fontsize(t.get_fontsize() * LABEL_SHRINK)
        for ax in (ax_a, ax_b):
            for t in ax.texts:
                if t.get_text().startswith('longdust -k8'):
                    x, y = t.xyann
                    t.xyann = (x, y + 10)  # clear the enlarged neighbours
        # Panel A: the enlarged tantan/ULTRA labels collide in the F/H cluster
        # and ULTRA runs off the panel edge; flip tantan to the left of its
        # point and tuck ULTRA lower right.
        for t in ax_a.texts:
            if t.get_text() == 'tantan':
                t.set_horizontalalignment('right')
                t.xyann = (-6, 8)
            elif t.get_text() == 'ULTRA':
                t.xyann = (2, 10)  # above its point, inside the panel edge
                t.set_fontsize(12)
        # Panel C tick labels are three long rule names; smaller horizontal
        # labels fit the category spacing, and the title gets clearance.
        for lbl in ax_c.get_xticklabels():
            lbl.set_fontsize(13)
        ax_c.set_title(ax_c.get_title(), fontweight='bold', fontsize=ax_c.title.get_fontsize() * 0.85, y=1.03)
        for line in ax_c.get_lines():
            if line.get_alpha() is not None and abs(line.get_alpha() - 0.3) < 1e-6:
                line.set_alpha(0.55)
                line.set_markeredgecolor('#333333')
                line.set_markeredgewidth(0.8)
        legend = ax_c.get_legend()
        for handle in getattr(legend, 'legend_handles', None) or legend.legendHandles:
            if handle.get_alpha() is not None and abs(handle.get_alpha() - 0.3) < 1e-6:
                handle.set_alpha(1.0)
                handle.set_markeredgecolor('#333333')
                handle.set_markeredgewidth(0.8)
    for ext in ('pdf', 'png'):
        fig.savefig(out / (stem + '.' + ext), bbox_inches='tight')
    print('rendered', stem)

figstyle.setup = setup
figstyle.save = save
os.chdir(source)
for script in inputs[:2]:
    plt.close('all')
    runpy.run_path(str(script), run_name='__main__')
record['outputs'] = {name: hashlib.sha256((out / name).read_bytes()).hexdigest()
                     for name in sorted(p.name for p in out.glob('fig1_accuracy_tradeoff.*'))
                     + sorted(p.name for p in out.glob('fig2_range_cost.*'))}
assert len(record['outputs']) == 4
(out / 'render-receipt.json').write_text(json.dumps(record, indent=2) + '\n')
print('Re-rendered both main figures for presentation; results/ is untouched.')
