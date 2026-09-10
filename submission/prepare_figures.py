#!/usr/bin/env python3
"""Crop embedded legacy captions, not plots, from deposited figure PDFs.

Presentation-only copies live outside results/. Requires PyMuPDF; no plotting,
scoring, source-data changes, or modification of the deposited images occurs.
"""
import hashlib
import json
from pathlib import Path
import fitz

source = Path('results/figures/paper_figs/rendered')
target = Path('submission/figures')
target.mkdir(parents=True, exist_ok=True)
records = []
for path in sorted(source.glob('*.pdf')):
    if path.name in ('fig1_accuracy_tradeoff.pdf', 'fig2_range_cost.pdf'):
        continue  # Both main figures are re-rendered by render_main_figures.py (F5).
    doc = fitz.open(path)
    assert len(doc) == 1, path
    page = doc[0]
    boxes = page.search_for('Figure')
    assert len(boxes) == 1 and boxes[0].y0 > 0.70 * page.rect.height, path
    crop = fitz.Rect(0, 0, page.rect.width, boxes[0].y0 - 4)
    page.set_cropbox(crop)
    pdf = target / path.name
    png = pdf.with_suffix('.png')
    doc.save(pdf)
    page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72)).save(png)
    records.append({'source': str(path), 'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                    'crop_box_points': list(crop), 'pdf': str(pdf), 'png': str(png),
                    'pdf_sha256': hashlib.sha256(pdf.read_bytes()).hexdigest(),
                    'png_sha256': hashlib.sha256(png.read_bytes()).hexdigest()})
assert len(records) == 5
(target / 'crop-receipt.json').write_text(json.dumps(records, indent=2) + '\n')
print('Created five plot-only PDF/PNG pairs; results/ is untouched.')
