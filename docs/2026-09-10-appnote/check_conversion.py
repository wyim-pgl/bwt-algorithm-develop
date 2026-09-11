#!/usr/bin/env python3
"""Check the bounded, lossless parts of the Application Note conversion.

Run from the repository root. This is not a scientific-claim validator or a
certification of current journal policy, DOI publication, or author approval.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

root = Path.cwd()
full = (root / 'manuscript_full.md').read_text()
supp = (root / 'supplementary.md').read_text()
main = (root / 'manuscript.md').read_text()
receipt = json.loads((root / 'docs/2026-09-10-appnote/conversion.json').read_text())
assert hashlib.sha256(full.encode()).hexdigest() == receipt['full_manuscript_sha256']

# Compare ordered blocks and complete cell text, not sets of rounded numbers.
def tables(text):
    return re.findall(r'(?:^\|[^\n]*\n)+', text, re.M)
migration = root / 'docs/2026-09-10-lab-docx'
if migration.is_dir():
    before = (migration / 'supplementary-before.md').read_text()
    assert tables(full) == tables(before), 'Pre-migration baseline lost original table content'
    subprocess.run([sys.executable, str(migration / 'check_migration.py')], check=True)
else:
    assert tables(full) == tables(supp), 'Table cells/order changed or a table was lost'
assert not tables(main), 'All tables belong in the supplement'
assert len(tables(full)) == receipt['table_blocks']

# Reconstruct the supplement from the immutable long source, independently of
# the checked-in supplemental file; changes must be explained in the receipt.
def supplement_body(text):
    lines = text.splitlines()
    start = next(i for i, line in enumerate(lines) if line.strip() == '1. Introduction')
    out = []
    for line in lines[start:]:
        line = line.lstrip()
        if line.startswith('|'):
            out.append(line)  # preserve every cell, including headings/references
            continue
        if line.startswith('!['):
            continue  # the sole old image is inserted uniformly below
        line = re.sub(r'(?<!Supplementary )\b(Figures?|Tables?)\b', r'Supplementary \1', line)
        if re.match(r'^\d(?:\.\d+)*\.? ', line) or re.match(r'^S\d(?:\.\d+)*\.? ', line):
            line = '## ' + line
        elif line in ('Data and Code Availability', 'References', 'Supplementary Methods'):
            line = '## ' + line
        if line.startswith('## ') and (not out or out[-1] != ''):
            out.append('')  # Pandoc needs a blank line before ATX headings (F4).
        m = re.match(r'^Supplementary Figure (\d|S\d)\. ', line)
        if m:
            image = receipt['figure_files'][m[1]]
            out += [f'![Supplementary Figure {m[1]}](submission/figures/{image}.png)', '']
        out.append(line)
    return '\n'.join(out) + '\n'

expected = supplement_body(full)
if migration.is_dir():
    assert before.split('<!-- preserved-body -->\n', 1)[1] == expected
    lines = expected.splitlines(keepends=True)
    changes = json.loads((migration / 'supplement-replay.json').read_text())
    previous_end = 0
    for op in changes:
        assert previous_end <= op['start'] <= op['end'] <= len(lines)
        assert ''.join(lines[op['start']:op['end']]) == op['old']
        previous_end = op['end']
    for op in reversed(changes):
        lines[op['start']:op['end']] = op['new'].splitlines(keepends=True)
    expected = ''.join(lines)
assert supp.split('<!-- preserved-body -->\n', 1)[1] == expected, 'Unexplained supplemental change outside approved replay'
for text in (main, supp):
    for image in re.findall(r'!\[[^\]]*\]\(([^)]+)\)', text):
        assert (root / image).is_file(), image
assert len(re.findall(r'!\[', main)) == 2
assert len(re.findall(r'!\[', supp)) == 7
crops = json.loads((root / 'submission/figures/crop-receipt.json').read_text())
assert len(crops) == 5  # both main figures moved to render_main_figures.py (F5)
for item in crops:
    for key in ('source', 'pdf', 'png'):
        assert hashlib.sha256((root / item[key]).read_bytes()).hexdigest() == item[key + '_sha256'], item[key]
render = json.loads((root / 'submission/figures/render-receipt.json').read_text())
assert hashlib.sha256((root / 'submission/render_main_figures.py').read_bytes()).hexdigest() == render['renderer_sha256']
assert set(render['outputs']) == {stem + ext for stem in
    ('fig1_accuracy_tradeoff', 'fig2_range_cost') for ext in ('.pdf', '.png')}
for path, expected in render['inputs'].items():
    assert hashlib.sha256((root / path).read_bytes()).hexdigest() == expected, path
for name, expected in render['outputs'].items():
    assert hashlib.sha256((root / 'submission/figures' / name).read_bytes()).hexdigest() == expected, name
assert not (root / 'submission/figures/accuracy-export-receipt.json').exists()  # superseded
versions = [re.search(r'^version = "([^"]+)"', (root / 'pyproject.toml').read_text(), re.M).group(1),
            re.search(r'^version: "([^"]+)"', (root / 'CITATION.cff').read_text(), re.M).group(1),
            re.search(r'^LABEL version="([^"]+)"', (root / 'Dockerfile').read_text(), re.M).group(1)]
assert versions == ['0.9.0'] * 3, versions
abstract = main.split('## Abstract\n', 1)[1].split('## 1 Introduction', 1)[0]
assert len(abstract.split()) <= 200
# Application Note abstract structure (final-check F1): exactly these four
# headings in order, and a Summary of at most two sentences.
labels = re.findall(r'\*\*([^*]+):\*\*', abstract)
assert labels == ['Summary', 'Availability and Implementation', 'Contact',
                  'Supplementary Information'], labels
summary = abstract.split('**Summary:**', 1)[1].split('**Availability', 1)[0].strip()
assert len(re.findall(r'\.\s+[A-Z]', summary)) + 1 <= 2, 'Summary exceeds two sentences'
# Both main legends carry the journal-requested accessibility description (F2).
assert len(re.findall(r'\*\*Alt text:\*\* \S', main)) == 2
# Editorial working ceiling only. The earlier 500-words-per-figure heuristic
# was not a verified journal rule. The separate rendered-PDF gate enforces
# the actual four-page limit after adding the author-requested full callouts.
assert len(main.split()) <= 2000
for needle in ('78.87%', '81.62%', '1.79', '28.08 GiB', '4 of 400',
               'non-leading shared-range accuracy', 'defaults', 'single-reader'):
    assert needle in main, needle
print(json.dumps({'original_table_blocks_accounted_for': len(tables(full)),
                  'current_supplement_tables': len(tables(supp)),
                  'all_supplemental_prose_replayed': True,
                  'main_words_whitespace': len(main.split()),
                  'abstract_words_whitespace': len(abstract.split()),
                  'main_figures': 2, 'supplement_figures': 7}, indent=2))
