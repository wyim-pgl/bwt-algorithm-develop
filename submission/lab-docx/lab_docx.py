#!/usr/bin/env python3
"""Apply lab style to a Pandoc DOCX without rebuilding paragraphs (requires lxml)."""
import argparse
from copy import deepcopy
import io
from pathlib import Path
from functools import lru_cache
import subprocess
import re
import sys
import tempfile
from zipfile import BadZipFile, ZipFile
from lxml import etree as E

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
XML_SPACE = '{http://www.w3.org/XML/1998/namespace}space'
USABLE = 16838 - 2 * 850  # landscape A4, 15 mm (rounded to twips)
REF = re.compile(r'\b(?:Supplementary\s+)?(?:Tables?|Figures?|Figs?\.)\s+S?\d+[A-Z]?(?!\w)(?:\s*(?:[-–,]|and)\s*(?:and\s+)?S?\d+[A-Z]?(?!\w))*')
CITE = re.compile(r'\([^()]*?\b[A-Z][A-Za-zÀ-ſ’\x27-]+(?:\s+et\s+al\.)?(?:\s+(?:&|and)\s+[A-Z][A-Za-zÀ-ſ’\x27-]+)*,?\s+(?:\d{4}[a-z]?|n\.d\.|in\s+(?:review|press|preparation))[^()]*\)')
CAPTION = re.compile(r'^(?:Supplementary\s+)?(?:Tables?|Figures?|Figs?\.)\s+S?\d+[A-Z]?(?!\w)')
PHOTO = re.compile(r'(?<!\w)C([34])(?!\w)')
# OOXML child order for properties we insert. Existing unrelated children stay.
ORDER = {
    'rPr': 'rStyle rFonts b bCs i iCs caps smallCaps strike dstrike outline shadow emboss imprint noProof snapToGrid vanish webHidden color spacing w kern position sz szCs highlight u effect bdr shd fitText vertAlign rtl cs em lang eastAsianLayout specVanish oMath rPrChange',
    'pPr': 'pStyle keepNext keepLines pageBreakBefore framePr widowControl numPr suppressLineNumbers pBdr shd tabs suppressAutoHyphens kinsoku wordWrap overflowPunct topLinePunct autoSpaceDE autoSpaceDN bidi adjustRightInd snapToGrid spacing ind contextualSpacing mirrorIndents suppressOverlap jc textDirection textAlignment textboxTightWrap outlineLvl divId cnfStyle rPr sectPr pPrChange',
    'tblPr': 'tblStyle tblpPr tblOverlap bidiVisual tblStyleRowBandSize tblStyleColBandSize tblW jc tblCellSpacing tblInd tblBorders shd tblLayout tblCellMar tblLook tblCaption tblDescription tblPrChange',
    'tcPr': 'cnfStyle tcW gridSpan hMerge vMerge tcBorders shd noWrap tcMar textDirection tcFitText vAlign hideMark headers cellIns cellDel cellMerge tcPrChange',
    'trPr': 'cnfStyle divId gridBefore gridAfter wBefore wAfter cantSplit trHeight tblHeader tblCellSpacing jc hidden ins del trPrChange',
    'sectPr': 'headerReference footerReference footnotePr endnotePr type pgSz pgMar paperSrc pgBorders lnNumType pgNumType cols formProt vAlign noEndnote titlePg textDirection bidi rtlGutter docGrid printerSettings sectPrChange',
    'style': 'name aliases basedOn next link autoRedefine hidden uiPriority semiHidden unhideWhenUsed qFormat locked personal personalCompose personalReply rsid pPr rPr tblPr trPr tcPr tblStylePr',
    'docDefaults': 'rPrDefault pPrDefault',
}


class FormatError(ValueError):
    """Unsupported input or unsafe formatting; no output should be written."""


def tag(name):
    return '{' + NS['w'] + '}' + name


def local(node):
    return E.QName(node).localname


def ensure(parent, name):
    nodes = parent.findall('w:' + name, NS)
    if nodes:
        for duplicate in nodes[1:]:
            parent.remove(duplicate)
        return nodes[0]
    node = E.Element(tag(name))
    order = ORDER.get(local(parent), '').split()
    if name in ('rPr', 'pPr', 'tcPr', 'trPr', 'tblPr') and local(parent) in ('r', 'p', 'tc', 'tr', 'tbl'):
        parent.insert(0, node)
    elif name in order:
        index = order.index(name)
        for i, child in enumerate(parent):
            if local(child) in order and order.index(local(child)) > index:
                parent.insert(i, node)
                break
        else:
            parent.append(node)
    else:
        parent.append(node)
    return node


def prop(parent, name, **attrs):
    node = ensure(parent, name)
    node.attrib.clear()
    for key, value in attrs.items():
        node.set(tag(key), str(value))
    return node


def font(rp, family, bold=False, table=False, color='000000', italic=False, sub=False):
    prop(rp, 'rFonts', ascii=family, hAnsi=family, eastAsia=family, cs=family)
    prop(rp, 'color', val=color)
    if bold:
        prop(rp, 'b', val=1)
        prop(rp, 'bCs', val=1)
    if table:
        prop(rp, 'sz', val=18)
        prop(rp, 'szCs', val=18)
    if italic:
        prop(rp, 'i', val=1)
        prop(rp, 'iCs', val=1)
    if sub:
        prop(rp, 'vertAlign', val='subscript')


def indent(pp, value):
    node = ensure(pp, 'ind')
    for name in ('hanging', 'hangingChars', 'firstLineChars'):
        node.attrib.pop(tag(name), None)
    node.set(tag('firstLine'), str(value))


def visible(node):
    return ''.join(node.xpath('.//w:t/text()', namespaces=NS))


def style_labels(styles, style_id):
    labels, seen = [], set()
    while style_id:
        if style_id in seen:
            raise FormatError('Cyclic style inheritance')
        seen.add(style_id)
        labels.append(style_id.lower().replace(' ', ''))
        style = styles.get(style_id)
        if style is None:
            break
        name = style.find('w:name', NS)
        if name is not None:
            labels.append(name.get(tag('val'), '').lower().replace(' ', ''))
        if style.find('w:pPr/w:numPr', NS) is not None:
            labels.append('listparagraph')
        base = style.find('w:basedOn', NS)
        style_id = base.get(tag('val')) if base is not None else None
    return labels


def kind(paragraph, styles):
    ps = paragraph.find('w:pPr/w:pStyle', NS)
    labels = style_labels(styles, ps.get(tag('val')) if ps is not None else 'Normal')
    outline = paragraph.find('w:pPr/w:outlineLvl', NS)
    if any(s.startswith('heading') for s in labels) or (outline is not None and outline.get(tag('val')) in tuple(map(str, range(9)))):
        return 'heading'
    if CAPTION.match(visible(paragraph)) or any('caption' in s for s in labels):
        return 'caption'
    if any('code' in s or 'verbatim' in s for s in labels):
        return 'code'
    if any(s in ('title', 'subtitle', 'author', 'date', 'affiliation', 'correspondence') for s in labels):
        return 'title'
    if paragraph.find('w:pPr/w:numPr', NS) is not None or any('list' in s for s in labels):
        return 'list'
    if any('tablenote' in s for s in labels) or visible(paragraph).startswith(('Abbreviations:', 'Alt text:')):
        return 'note'
    if any('bibliograph' in s or s in ('references', 'reference') for s in labels):
        return 'reference'
    return 'prose'


def caption_title_length(paragraph):
    """Honor Markdown strong title; plain captions fall back to first sentence."""
    text = visible(paragraph)
    length = 0
    for run in paragraph.iter(tag('r')):
        b = run.find('w:rPr/w:b', NS)
        if b is None or b.get(tag('val'), '1') in ('0', 'false', 'off'):
            break
        length += len(visible(run))
    label = CAPTION.match(text)
    if length and (label is None or length > label.end() + 1):
        return length
    start = label.end() if label else 0
    if text[start:start+1] == '.':
        start += 1
    ending = re.search(r'[.!?](?=\s|$)', text[start:])
    return start + ending.end() if ending else len(text)


def lanes(paragraph):
    """Hyperlinks/bookmarks are transparent; non-text content is a barrier."""
    lane = []
    def walk(parent):
        for child in parent:
            name = local(child)
            if child.tag != tag(name):
                raise FormatError('Foreign-namespace paragraph content is unsupported')
            if name in ('pPr', 'bookmarkStart', 'bookmarkEnd', 'proofErr'):
                continue
            if name == 'hyperlink':
                yield from walk(child)
            elif name == 'fldSimple':
                yield None
                yield from walk(child)
                yield None
            elif name == 'r':
                yield child
            else:
                raise FormatError('Unsupported paragraph wrapper: ' + name)
    for run in walk(paragraph):
        simple = run is not None and len(run.findall('w:t', NS)) == 1 and all(local(c) in ('rPr', 't') for c in run)
        if simple:
            lane.append(run)
        else:
            if lane:
                yield lane
                lane = []
            if run is not None and run.findall('w:t', NS):
                yield [run]
    if lane:
        yield lane


def restyle(paragraph, *, family, bold, table, annotate, species, photosynthesis, bold_prefix=0):
    paragraph_offset = 0
    for lane in lanes(paragraph):
        text = ''.join(visible(r) for r in lane)
        marks = [('000000', False, False, paragraph_offset + i < bold_prefix) for i in range(len(text))]
        paragraph_offset += len(text)
        if annotate:
            for regex, color in ((CITE, '3399FF'), (REF, 'FF0000')):
                for match in regex.finditer(text):
                    for i in range(*match.span()):
                        # Titles stay black; explanatory legend text follows
                        # the same citation/callout colours as other prose.
                        if not marks[i][3]:
                            marks[i] = (color, marks[i][1], marks[i][2], marks[i][3])
        for name in species:
            for match in re.finditer(r'(?<!\w)' + re.escape(name) + r'(?!\w)', text):
                for i in range(*match.span()):
                    marks[i] = (marks[i][0], True, marks[i][2], marks[i][3])
        if photosynthesis:
            for match in PHOTO.finditer(text):
                i = match.start(1)
                marks[i] = (marks[i][0], marks[i][1], True, marks[i][3])
        offset = 0
        for run in lane:
            value = visible(run)
            own = marks[offset:offset + len(value)]
            offset += len(value)
            cuts = [0] + [i for i in range(1, len(own)) if own[i] != own[i-1]] + [len(value)]
            if len(cuts) > 2:
                if len(run.findall('w:t', NS)) != 1 or any(local(c) not in ('rPr', 't') for c in run):
                    raise FormatError('Selective formatting would split a non-simple run')
                parent, position = run.getparent(), run.getparent().index(run)
                for a, b in zip(cuts, cuts[1:]):
                    piece = deepcopy(run)
                    t = piece.find('w:t', NS)
                    t.text = value[a:b]
                    t.set(XML_SPACE, 'preserve')
                    color, italic, sub, title = own[a]
                    font(ensure(piece, 'rPr'), family, bold or title, table, color, italic, sub)
                    parent.insert(position, piece)
                    position += 1
                parent.remove(run)
            else:
                color, italic, sub, title = own[0] if own else ('000000', False, False, False)
                font(ensure(run, 'rPr'), family, bold or title, table, color, italic, sub)


def borders(parent, top=False, bottom=False):
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV', 'start', 'end', 'tl2br', 'tr2bl'):
        on = edge == 'top' and top or edge == 'bottom' and bottom
        # Diagonal borders are cell-only.
        if edge in ('tl2br', 'tr2bl') and local(parent) != 'tcBorders':
            continue
        prop(parent, edge, val='single' if on else 'nil', sz=8 if on else 0, color='000000', space=0)


@lru_cache(maxsize=1)
def metric_fonts():
    """Use installed Arial or its fontconfig substitute; PDF Helvetica fallback.

    The DOCX still requests Arial. Record the actual metric font; rendering in
    Word remains necessary if it resolves Arial differently.
    """
    import fitz
    fonts = []
    for query, fallback in (('Arial', 'helv'), ('Arial:style=Bold', 'hebo')):
        try:
            found = subprocess.check_output(['fc-match', '-f', '%{file}', query], text=True).strip()
            fonts.append(fitz.Font(fontfile=found))
        except (OSError, subprocess.SubprocessError, RuntimeError):
            fonts.append(fitz.Font(fontname=fallback))
    return fonts


def table_widths(table):
    if table.findall('.//w:tbl', NS):
        raise FormatError('Nested tables are unsupported')
    forbidden = 'gridSpan hMerge vMerge tblpPr gridBefore gridAfter trHeight textDirection tblPrEx drawing pict object tab br cr fldChar instrText fldSimple sym oMath tcFitText'.split()
    if any(table.findall('.//w:' + name, NS) for name in forbidden) or table.xpath('.//*[namespace-uri() != $w]', w=NS['w']):
        raise FormatError('Table has merged, floating, complex, or unknown-width content')
    if any(c.tag not in {tag(n) for n in ('tblPr', 'tblGrid', 'tr')} for c in table):
        raise FormatError('Unsupported table child structure')
    rows = table.findall('w:tr', NS)
    cells = [r.findall('w:tc', NS) for r in rows]
    if any(any(c.tag not in (tag('trPr'), tag('tc')) for c in row) for row in rows):
        raise FormatError('Unsupported row child structure')
    if any(any(c.tag not in (tag('tcPr'), tag('p')) for c in cell) for row in cells for cell in row):
        raise FormatError('Unsupported cell child structure')
    if not cells or not cells[0] or any(len(r) != len(cells[0]) for r in cells):
        raise FormatError('Table must be rectangular and nonempty')
    minima = []
    for col in zip(*cells):
        # Full text advances, with 6% allowance for renderer/font differences.
        points = max((max(f.text_length(visible(p), fontsize=9) for f in metric_fonts()) * 1.06
                      for cell in col for p in cell.findall('w:p', NS)), default=0)
        minima.append(max(180, int(points * 20 + 0.999) + 120))
    if sum(minima) > USABLE:
        required = ', '.join('column %d: %.1f pt' % (i, n / 20) for i, n in enumerate(minima, 1))
        raise FormatError('Table cannot fit fixed Arial 9 pt/noWrap: conservative minimum %.1f pt exceeds %.1f pt (%s); shorten/move long cells to prose' % (sum(minima) / 20, USABLE / 20, required))
    extra, remainder = divmod(USABLE - sum(minima), len(minima))
    return cells, [n + extra + (i < remainder) for i, n in enumerate(minima)]


def format_table(table, cells, widths, species):
    tp = ensure(table, 'tblPr')
    for name in ('tblStyle', 'tblLook'):
        for node in tp.findall('w:' + name, NS):
            tp.remove(node)
    prop(tp, 'tblW', w=USABLE, type='dxa')
    prop(tp, 'tblInd', w=0, type='dxa')
    prop(tp, 'tblCellSpacing', w=0, type='dxa')
    prop(tp, 'tblLayout', type='fixed')
    prop(tp, 'shd', val='clear', color='auto', fill='auto')
    borders(ensure(tp, 'tblBorders'))
    grid = table.find('w:tblGrid', NS)
    if grid is None:
        grid = E.Element(tag('tblGrid'))
        table.insert(table.index(tp) + 1, grid)
    grid.clear()
    for width in widths:
        prop_col = E.SubElement(grid, tag('gridCol'))
        prop_col.set(tag('w'), str(width))
    for ri, rowcells in enumerate(cells):
        rp = ensure(rowcells[0].getparent(), 'trPr')
        prop(rp, 'cantSplit', val=1)
        prop(rp, 'tblCellSpacing', w=0, type='dxa')
        prop(rp, 'tblHeader', val=1 if ri == 0 else 0)
        for ci, cell in enumerate(rowcells):
            cp = ensure(cell, 'tcPr')
            prop(cp, 'tcW', w=widths[ci], type='dxa')
            prop(cp, 'vAlign', val='top')
            prop(cp, 'noWrap', val=1)
            prop(cp, 'shd', val='clear', color='auto', fill='auto')
            borders(ensure(cp, 'tcBorders'), ri == 0, ri in (0, len(cells)-1))
            margins = ensure(cp, 'tcMar')
            for side in ('top', 'left', 'bottom', 'right', 'start', 'end'):
                prop(margins, side, w=60, type='dxa')
            for p in cell.findall('w:p', NS):
                pp = ensure(p, 'pPr')
                prop(pp, 'jc', val='center' if ri == 0 else 'left')
                prop(pp, 'ind', left=0, right=0, firstLine=0)
                prop(pp, 'spacing', before=0, after=0, line=240, lineRule='auto')
                for shd in p.findall('.//w:shd', NS):
                    shd.attrib.clear()
                    shd.set(tag('val'), 'clear')
                    shd.set(tag('fill'), 'auto')
                restyle(p, family='Arial', bold=ri == 0, table=True, annotate=ri != 0, species=species, photosynthesis=False)
                prop(pp, 'shd', val='clear', color='auto', fill='auto')
                for run in p.iter(tag('r')):
                    rp2 = ensure(run, 'rPr')
                    prop(rp2, 'shd', val='clear', color='auto', fill='auto')
                    prop(rp2, 'highlight', val='none')


def parse(data):
    try:
        root = E.fromstring(data, E.XMLParser(resolve_entities=False, no_network=True, remove_blank_text=False))
    except E.XMLSyntaxError as exc:
        raise FormatError('Invalid XML: ' + str(exc)) from exc
    if root.getroottree().docinfo.doctype:
        raise FormatError('DTD declarations are unsupported')
    return root


def format_bytes(data, *, species=(), photosynthesis=False):
    """Return (ZIP bytes, width warnings); mutate only document.xml/styles.xml."""
    if any(not name or name != name.strip() for name in species):
        raise FormatError('Species entries must be nonempty exact names without outer whitespace')
    with ZipFile(io.BytesIO(data)) as archive:
        infos, comment = archive.infolist(), archive.comment
        if len({i.filename for i in infos}) != len(infos):
            raise FormatError('Duplicate ZIP member names')
        parts = {i.filename: archive.read(i) for i in infos}
    if any(name.startswith('_xmlsignatures/') for name in parts):
        raise FormatError('Signed packages are unsupported')
    if not {'word/document.xml', 'word/styles.xml'} <= parts.keys():
        raise FormatError('Pandoc document.xml and styles.xml required')
    doc, styles_root = parse(parts['word/document.xml']), parse(parts['word/styles.xml'])
    if doc.tag != tag('document') or styles_root.tag != tag('styles'):
        raise FormatError('Only transitional WordprocessingML is supported')
    forbidden = 'ins del moveFrom moveTo sdt altChunk txbxContent customXml'.split()
    if any(doc.findall('.//w:' + n, NS) for n in forbidden) or doc.xpath('.//*[local-name()="AlternateContent"]'):
        raise FormatError('Tracked changes, content controls, text boxes or alternate content are unsupported')
    body = doc.find('w:body', NS)
    if body is None or any(c.tag not in {tag(n) for n in ('p', 'tbl', 'sectPr', 'bookmarkStart', 'bookmarkEnd')} for c in body):
        raise FormatError('Unsupported document body structure')
    tables = body.findall('w:tbl', NS)
    plans = [(table, *table_widths(table)) for table in tables]
    if tables:
        sections = doc.findall('.//w:sectPr', NS)
        if len(sections) != 1 or sections[0].getparent() is not body:
            raise FormatError('Table supplements require one terminal section')
        prop(sections[0], 'pgSz', w=16838, h=11906, orient='landscape')
        margins = ensure(sections[0], 'pgMar')
        for side in ('top', 'bottom', 'left', 'right'):
            margins.set(tag(side), '850')
        margins.set(tag('gutter'), '0')
        cols = sections[0].find('w:cols', NS)
        if cols is not None and (cols.get(tag('num'), '1') != '1' or cols.findall('w:col', NS)):
            raise FormatError('Multi-column table sections are unsupported')
    styles = {s.get(tag('styleId')): s for s in styles_root.findall('w:style', NS)}
    for table in tables:
        if any(kind(p, styles) in ('list', 'code') for p in table.findall('.//w:p', NS)):
            raise FormatError('List/code table cells have unsupported width semantics; move to prose')
    defaults = styles_root.find('w:docDefaults', NS)
    if defaults is None:
        defaults = E.Element(tag('docDefaults'))
        styles_root.insert(0, defaults)
    ensure(ensure(defaults, 'rPrDefault'), 'rPr')
    for style_id, style in styles.items():
        heading = any(s.startswith('heading') for s in style_labels(styles, style_id))
        font(ensure(style, 'rPr'), 'Times New Roman', bold=heading)
        if heading:
            indent(ensure(style, 'pPr'), 0)
    for rp in styles_root.findall('.//w:rPr', NS):
        font(rp, 'Times New Roman')
    first, references = True, False
    for p in body.findall('w:p', NS):
        category = kind(p, styles)
        if p.findall('.//w:drawing', NS) and not visible(p).strip():
            prop(ensure(p, 'pPr'), 'keepNext', val=1)
        if category == 'caption':
            prop(ensure(p, 'pPr'), 'keepLines', val=1)
            prop(ensure(p, 'pPr'), 'keepNext', val=1)
        heading = category == 'heading'
        if heading:
            first = True
            references = visible(p).strip().lower() in ('references', 'bibliography', 'literature cited')
        if category in ('heading', 'caption', 'title', 'note'):
            indent(ensure(p, 'pPr'), 0)
            if category == 'note':
                prop(ensure(p, 'pPr'), 'spacing', before=0, after=0)
        elif category == 'prose' and visible(p).strip():
            pp = ensure(p, 'pPr')
            indent(pp, 0 if first else 360)
            prop(pp, 'jc', val='left')
            first = False
        eligible = category not in ('code', 'reference') and not references
        restyle(p, family='Times New Roman', bold=heading, table=False,
                annotate=eligible and category not in ('heading', 'title'),
                species=species if eligible else (), photosynthesis=photosynthesis and eligible and category == 'prose',
                bold_prefix=caption_title_length(p) if category == 'caption' else 0)
        for rp in p.findall('w:pPr/w:rPr', NS):
            font(rp, 'Times New Roman', bold=heading)
    for table, cells, widths in plans:
        format_table(table, cells, widths, species)
    for name, tree in (('word/document.xml', doc), ('word/styles.xml', styles_root)):
        parts[name] = E.tostring(tree, encoding='UTF-8', xml_declaration=True, standalone=True)
    output = io.BytesIO()
    with ZipFile(output, 'w') as archive:
        archive.comment = comment
        for info in infos:
            archive.writestr(info, parts[info.filename])
    warnings = ['Table %d: widths use fontconfig Arial/substitute metrics with a 6%% allowance; visually verify noWrap fit and row pagination in Word/LibreOffice before submission.' % i for i in range(1, len(tables)+1)]
    return output.getvalue(), warnings


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('docx', type=Path)
    ap.add_argument('--out', type=Path, help='Output path; default: atomically replace input')
    ap.add_argument('--species', action='append', default=[], metavar='EXACT NAME')
    ap.add_argument('--photosynthesis', action='store_true', help='Digit-only C3/C4 subscript in prose')
    args = ap.parse_args(argv)
    try:
        data, warnings = format_bytes(args.docx.read_bytes(), species=args.species, photosynthesis=args.photosynthesis)
        target = args.out or args.docx
        temp = None
        try:
            with tempfile.NamedTemporaryFile(dir=target.parent, prefix='.' + target.name + '.', suffix='.tmp', delete=False) as handle:
                temp = Path(handle.name)
                handle.write(data)
            temp.replace(target)
        finally:
            if temp is not None and temp.exists():
                temp.unlink()
        for warning in warnings:
            print('WARNING: ' + warning, file=sys.stderr)
        print('Formatted ' + str(target))
    except (FormatError, OSError, BadZipFile) as exc:
        ap.exit(2, 'Not formatted: ' + str(exc) + '\n')


if __name__ == '__main__':
    main()
