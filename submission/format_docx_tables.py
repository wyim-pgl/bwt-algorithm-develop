#!/usr/bin/env python3
"""Table-only DOCX adaptation of PGL wiki paper-format three-line XLSX rules.

Arial 9 pt; bold centred repeating header; left/top-aligned wrapped body;
three horizontal rules, no vertical/interior rules or shading. One-section
supplements with simple, unmerged tables use landscape A4 with 15 mm margins.
Only word/document.xml changes; runs, links, drawings and other ZIP parts stay.
Requires lxml. Usage: python submission/format_docx_tables.py file.docx
"""
import sys
from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
def tag(name):
    return '{' + NS['w'] + '}' + name

def prop(parent, name, **attrs):
    node = parent.find('w:' + name, NS)
    if node is None:
        node = E.SubElement(parent, tag(name))
    node.attrib.clear()
    for key, value in attrs.items():
        node.set(tag(key), str(value))
    return node

def rule(parent, edge, on=False):
    prop(parent, edge, val='single' if on else 'nil', sz=8 if on else 0,
         color='000000', space=0)

def format_tables(path):
    path = Path(path)
    with ZipFile(path) as z:
        infos = z.infolist()
        parts = {i.filename: z.read(i.filename) for i in infos}
    root = E.fromstring(parts['word/document.xml'])
    tables = root.findall('.//w:tbl', NS)
    if not tables:
        return 0
    sections = root.findall('.//w:sectPr', NS)
    assert len(sections) == 1, 'Multiple-section documents need explicit layout mapping'
    for table in tables:
        assert not table.findall('.//w:gridSpan', NS) and not table.findall('.//w:vMerge', NS)
        assert not table.findall('.//w:tbl', NS), 'Nested tables are unsupported'
    sec = sections[0]
    prop(sec, 'pgSz', w=16838, h=11906, orient='landscape')
    # Preserve existing header/footer distances; change only page margins.
    margins = sec.find('w:pgMar', NS)
    if margins is None:
        margins = E.SubElement(sec, tag('pgMar'))
    for side in ('top', 'bottom', 'left', 'right'):
        margins.set(tag(side), '850')
    margins.set(tag('gutter'), '0')
    usable = 16838 - 1700
    for table in tables:
        tp = table.find('w:tblPr', NS)
        if tp is None:
            tp = E.Element(tag('tblPr')); table.insert(0, tp)
        # Remove conditional table style so theme borders/shading cannot return.
        for name in ('tblStyle', 'tblLook'):
            for node in tp.findall('w:' + name, NS):
                tp.remove(node)
        for node in table.findall('.//w:shd', NS) + table.findall('.//w:noWrap', NS):
            node.getparent().remove(node)
        prop(tp, 'tblW', w=usable, type='dxa')
        prop(tp, 'tblInd', w=0, type='dxa')
        prop(tp, 'tblLayout', type='fixed')
        borders = prop(tp, 'tblBorders'); borders.clear()
        for edge in ('top', 'bottom', 'left', 'right', 'insideH', 'insideV', 'start', 'end'):
            rule(borders, edge, edge in ('top', 'bottom'))
        rows = table.findall('w:tr', NS)
        cells = [r.findall('w:tc', NS) for r in rows]
        n = len(cells[0]); assert all(len(r) == n for r in cells)
        weights = [max(10, min(60, max(len(''.join(c.itertext(tag('t')))) for c in col)))
                   for col in zip(*cells)]
        widths = [int(usable * w / sum(weights)) for w in weights]
        widths[-1] += usable - sum(widths)
        grid = table.find('w:tblGrid', NS); assert grid is not None
        grid.clear()
        for width in widths:
            E.SubElement(grid, tag('gridCol')).set(tag('w'), str(width))
        for ri, (row, rowcells) in enumerate(zip(rows, cells)):
            rp = row.find('w:trPr', NS)
            if rp is None:
                rp = E.Element(tag('trPr')); row.insert(0, rp)
            for old in rp.findall('w:tblHeader', NS) + rp.findall('w:cantSplit', NS):
                rp.remove(old)
            prop(rp, 'cantSplit', val=1)
            if ri == 0:
                prop(rp, 'tblHeader', val=1)
            for ci, cell in enumerate(rowcells):
                cp = cell.find('w:tcPr', NS)
                if cp is None:
                    cp = E.Element(tag('tcPr')); cell.insert(0, cp)
                prop(cp, 'tcW', w=widths[ci], type='dxa')
                prop(cp, 'vAlign', val='top')
                cb = prop(cp, 'tcBorders'); cb.clear()
                for edge in ('top', 'bottom', 'left', 'right', 'insideH', 'insideV', 'start', 'end'):
                    rule(cb, edge, edge == 'top' and ri == 0 or edge == 'bottom' and ri in (0, len(rows)-1))
                cm = prop(cp, 'tcMar')
                for side in ('top', 'bottom', 'left', 'right'):
                    prop(cm, side, w=60, type='dxa')
                for paragraph in cell.findall('.//w:p', NS):
                    pp = paragraph.find('w:pPr', NS)
                    if pp is None:
                        pp = E.Element(tag('pPr')); paragraph.insert(0, pp)
                    prop(pp, 'jc', val='center' if ri == 0 else 'left')
                    prop(pp, 'ind', left=0, right=0, firstLine=0)
                    prop(pp, 'spacing', before=0, after=0, line=240, lineRule='auto')
                for run in cell.findall('.//w:r', NS):
                    rp2 = run.find('w:rPr', NS)
                    if rp2 is None:
                        rp2 = E.Element(tag('rPr')); run.insert(0, rp2)
                    prop(rp2, 'rFonts', ascii='Arial', hAnsi='Arial', eastAsia='Arial', cs='Arial')
                    prop(rp2, 'sz', val=18); prop(rp2, 'szCs', val=18)
                    prop(rp2, 'color', val='000000')
                    if ri == 0:
                        prop(rp2, 'b', val=1)
    parts['word/document.xml'] = E.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
    temp = path.with_suffix('.formatted.tmp')
    with ZipFile(temp, 'w') as z:
        for info in infos:
            z.writestr(info, parts[info.filename])
    temp.replace(path)
    return len(tables)

if __name__ == '__main__':
    print(f'Formatted {format_tables(sys.argv[1])} tables: {sys.argv[1]}')
