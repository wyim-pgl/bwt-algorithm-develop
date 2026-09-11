"""Synthetic OOXML/ZIP fixtures only; no manuscript or Word file is generated."""
import io
import unittest
from zipfile import ZipFile
from lxml import etree as E
import lab_docx as lab

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NS = {'w': W, 'r': R}


def run(text, props=''):
    return f'<w:r><w:rPr>{props}</w:rPr><w:t xml:space="preserve">{text}</w:t></w:r>'


def para(text='', style='', xml=None):
    pp = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ''
    return '<w:p>' + pp + (run(text) if xml is None else xml) + '</w:p>'


def table(values):
    return '<w:tbl><w:tblPr><w:tblStyle w:val="Fancy"/></w:tblPr><w:tblGrid/>' + ''.join(
        '<w:tr>' + ''.join('<w:tc><w:tcPr><w:shd w:fill="FFFF00"/></w:tcPr>' + para(v) + '</w:tc>' for v in row) + '</w:tr>' for row in values) + '</w:tbl>'


def package(body, styles='', section='<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:header="400"/></w:sectPr>'):
    out = io.BytesIO()
    with ZipFile(out, 'w') as z:
        z.comment = b'archive metadata'
        z.writestr('word/document.xml', f'<w:document xmlns:w="{W}" xmlns:r="{R}"><w:body>{body}{section}</w:body></w:document>')
        z.writestr('word/styles.xml', f'<w:styles xmlns:w="{W}">{styles}</w:styles>')
        z.writestr('word/_rels/document.xml.rels', b'opaque relationships')
        z.writestr('word/media/image1.png', b'\x89PNG synthetic')
        z.writestr('[Content_Types].xml', b'opaque types')
    return out.getvalue()


def parts(data):
    with ZipFile(io.BytesIO(data)) as z:
        return {n: z.read(n) for n in z.namelist()}


def root(data, part='word/document.xml'):
    return E.fromstring(parts(data)[part])


def text(node):
    return ''.join(node.xpath('.//w:t/text()', namespaces=NS))


def attr(node, path, name='val'):
    found = node.find(path, NS)
    return None if found is None else found.get(f'{{{W}}}{name}')


class Formatting(unittest.TestCase):
    def apply(self, source, **options):
        output, warnings = lab.format_bytes(source, **options)
        self.assertEqual(text(root(source)), text(root(output)))
        return output

    def test_cross_run_and_payload_preservation(self):
        drawing = '<w:r><w:drawing><x:opaque xmlns:x="urn:test" keep="yes"/></w:drawing></w:r>'
        field = '<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText> REF mark </w:instrText></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r>'
        p = para(xml=run('See Supplementary ') + '<w:bookmarkStart w:id="2" w:name="mark"/>' + run('Fig.', '<w:i/>') + '<w:hyperlink r:id="rId7" w:history="1">' + run(' S1') + '</w:hyperlink><w:bookmarkEnd w:id="2"/>' + drawing + run(' (Smith ') + run('et al.', '<w:i/>') + run(', 2020).') + field)
        before = package(p)
        after = self.apply(before)
        tree = root(after)
        reds = tree.xpath('.//w:r[w:rPr/w:color/@w:val="FF0000"]', namespaces=NS)
        self.assertEqual(''.join(text(r) for r in reds), 'Supplementary Fig. S1')
        blues = tree.xpath('.//w:r[w:rPr/w:color/@w:val="3399FF"]', namespaces=NS)
        self.assertEqual(''.join(text(r) for r in blues), '(Smith et al., 2020)')
        self.assertEqual(tree.find('.//w:hyperlink', NS).attrib, root(before).find('.//w:hyperlink', NS).attrib)
        for tag in ('drawing', 'bookmarkStart', 'bookmarkEnd', 'instrText', 'fldChar'):
            self.assertEqual([E.tostring(x) for x in root(before).findall('.//w:' + tag, NS)], [E.tostring(x) for x in tree.findall('.//w:' + tag, NS)])
        self.assertTrue(tree.xpath('.//w:r[w:t="Fig."]/w:rPr/w:i', namespaces=NS))
        for name, payload in parts(before).items():
            if name not in ('word/document.xml', 'word/styles.xml'):
                self.assertEqual(parts(after)[name], payload)
        with ZipFile(io.BytesIO(after)) as z:
            self.assertEqual(z.comment, b'archive metadata')

    def test_paragraph_state_and_styles(self):
        styles = '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:rPr><w:rFonts w:asciiTheme="majorHAnsi"/><w:color w:themeColor="accent1"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="MyCode"><w:basedOn w:val="SourceCode"/></w:style>'
        before = package(para('Heading', 'Heading1') + para('Table 1. Caption') + para('title', 'Title') + para('item', 'ListParagraph') + para('C3', 'MyCode') + para('First') + para('Second'), styles)
        after = self.apply(before, photosynthesis=True)
        ps = root(after).findall('.//w:body/w:p', NS)
        self.assertEqual(attr(ps[-2], 'w:pPr/w:ind', 'firstLine'), '0')
        self.assertEqual(attr(ps[-1], 'w:pPr/w:ind', 'firstLine'), '360')
        for p in ps[:2]:
            self.assertEqual(attr(p, 'w:r/w:rPr/w:b'), '1')
            self.assertEqual(attr(p, 'w:r/w:rPr/w:color'), '000000')
        self.assertFalse(ps[4].findall('.//w:vertAlign', NS))
        for fonts in root(after, 'word/styles.xml').findall('.//w:rFonts', NS):
            self.assertEqual(set(fonts.attrib.values()), {'Times New Roman'})
            self.assertEqual(len(fonts.attrib), 4)
        heading = root(after, 'word/styles.xml').find('w:style', NS)
        self.assertEqual(attr(heading, 'w:rPr/w:bCs'), '1')
        self.assertEqual(E.tostring(root(before).find('.//w:sectPr', NS)), E.tostring(root(after).find('.//w:sectPr', NS)))

    def test_species_and_photosynthesis_are_opt_in_exact_and_prose_only(self):
        body = para(xml=run('Opuntia ') + run('ficus-indica and C3/C4; AC3 C34.')) + para('C3 Opuntia ficus-indica', 'SourceCode') + para('References', 'Heading1') + para('C4 reference')
        source = package(body)
        plain = self.apply(source)
        self.assertFalse(root(plain).findall('.//w:i', NS))
        self.assertFalse(root(plain).findall('.//w:vertAlign', NS))
        after = self.apply(source, species=['Opuntia ficus-indica'], photosynthesis=True)
        italic = root(after).xpath('.//w:r[w:rPr/w:i/@w:val="1"]', namespaces=NS)
        self.assertEqual(''.join(text(x) for x in italic), 'Opuntia ficus-indica')
        subs = root(after).xpath('.//w:r[w:rPr/w:vertAlign/@w:val="subscript"]', namespaces=NS)
        self.assertEqual([text(x) for x in subs], ['3', '4'])

    def test_table_geometry_borders_emphasis_and_widths(self):
        source = package(table([['Name', 'Count'], ['A', '12'], ['B', '4']]).replace('<w:rPr></w:rPr><w:t xml:space="preserve">A</w:t>', '<w:rPr><w:i/><w:b/></w:rPr><w:t xml:space="preserve">A</w:t>'))
        output, warnings = lab.format_bytes(source)
        self.assertTrue(warnings)
        tree = root(output)
        self.assertEqual(attr(tree, './/w:pgSz', 'orient'), 'landscape')
        self.assertEqual(attr(tree, './/w:pgMar', 'header'), '400')
        self.assertEqual(attr(tree, './/w:pgMar', 'left'), '850')
        widths = [int(x.get(f'{{{W}}}w')) for x in tree.findall('.//w:gridCol', NS)]
        self.assertEqual(sum(widths), 15138)
        self.assertFalse(tree.findall('.//w:tblStyle', NS))
        emphasized = tree.xpath('.//w:r[w:t="A"]', namespaces=NS)[0]
        self.assertIsNotNone(emphasized.find('w:rPr/w:i', NS))
        self.assertIsNotNone(emphasized.find('w:rPr/w:b', NS))
        self.assertTrue(all(x.get(f'{{{W}}}fill') == 'auto' for x in tree.findall('.//w:shd', NS)))
        for ri, row in enumerate(tree.findall('.//w:tr', NS)):
            for ci, cell in enumerate(row.findall('w:tc', NS)):
                self.assertEqual(attr(cell, 'w:tcPr/w:tcW', 'w'), str(widths[ci]))
                self.assertEqual(attr(cell, 'w:tcPr/w:noWrap'), '1')
                self.assertEqual(attr(cell, 'w:tcPr/w:vAlign'), 'top')
                self.assertEqual(attr(cell, 'w:p/w:pPr/w:jc'), 'center' if ri == 0 else 'left')
                self.assertEqual(attr(cell, './/w:sz'), '18')
                self.assertEqual(attr(cell, './/w:rFonts', 'ascii'), 'Arial')
                for edge in ('top', 'bottom', 'left', 'right', 'insideH', 'insideV'):
                    on = edge == 'top' and ri == 0 or edge == 'bottom' and ri in (0, 2)
                    self.assertEqual(attr(cell, 'w:tcPr/w:tcBorders/w:' + edge), 'single' if on else 'nil')

    def test_caption_bolds_only_source_title_span(self):
        caption = para(xml=run('Supplementary Table S1. Short title.', '<w:b/>') + run(' Explanation with Table S2 and (Lee, 2020).'))
        after = self.apply(package(caption))
        runs = root(after).findall('.//w:p/w:r', NS)
        self.assertEqual(attr(runs[0], 'w:rPr/w:b'), '1')
        self.assertIsNone(attr(runs[1], 'w:rPr/w:b'))
        self.assertEqual(attr(runs[0], 'w:rPr/w:color'), '000000')
        red = root(after).xpath('.//w:r[w:rPr/w:color/@w:val="FF0000"]', namespaces=NS)
        blue = root(after).xpath('.//w:r[w:rPr/w:color/@w:val="3399FF"]', namespaces=NS)
        self.assertEqual(''.join(text(r) for r in red), 'Table S2')
        self.assertEqual(''.join(text(r) for r in blue), '(Lee, 2020)')
        plain = self.apply(package(para('Table 2. Short title. Explanation.')))
        bold = root(plain).xpath('.//w:r[w:rPr/w:b/@w:val="1"]', namespaces=NS)
        self.assertEqual(''.join(text(r) for r in bold), 'Table 2. Short title.')

    def test_table_species_emphasis_and_inherited_shading(self):
        before = package(table([['Species'], ['Arabidopsis thaliana']]))
        after = self.apply(before, species=['Arabidopsis thaliana'])
        body = root(after).findall('.//w:tr', NS)[1]
        self.assertEqual(attr(body, './/w:rPr/w:i'), '1')
        self.assertEqual(attr(body, './/w:pPr/w:shd', 'fill'), 'auto')
        self.assertEqual(attr(body, './/w:rPr/w:shd', 'fill'), 'auto')

    def test_unknown_wrapper_rejected_and_simple_field_preserved(self):
        for content in ('<x:r xmlns:x="urn:foreign"><x:t>text</x:t></x:r>', '<w:unknown>' + run('text') + '</w:unknown>'):
            with self.assertRaises(lab.FormatError):
                lab.format_bytes(package(para(xml=content)))
        source = package(para(xml='<w:fldSimple w:instr="REF bookmark">' + run('1', '<w:color w:val="ABCDEF"/>') + '</w:fldSimple>'))
        after = self.apply(source)
        self.assertEqual(root(source).find('.//w:fldSimple', NS).attrib, root(after).find('.//w:fldSimple', NS).attrib)
        self.assertEqual(attr(root(after), './/w:fldSimple/w:r/w:rPr/w:color'), '000000')

    def test_caption_normalized_idempotence_and_boundaries(self):
        source = package(para('Supplementary Table S1. Short title. Plain legend.') + para('Zea mays; Zea maysX; zea mays; AC3; C34; C3.'))
        one = self.apply(source, species=['Zea mays'], photosynthesis=True)
        two = self.apply(one, species=['Zea mays'], photosynthesis=True)
        self.assertEqual(parts(one), parts(two))
        italics = root(one).xpath('.//w:r[w:rPr/w:i/@w:val="1"]', namespaces=NS)
        self.assertEqual(''.join(text(x) for x in italics), 'Zea mays')
        subs = root(one).xpath('.//w:r[w:rPr/w:vertAlign/@w:val="subscript"]', namespaces=NS)
        self.assertEqual(''.join(text(x) for x in subs), '3')

    def test_width_diagnostic_and_duplicate_package_rejection(self):
        with self.assertRaisesRegex(lab.FormatError, r'column 1: .*pt'):
            lab.format_bytes(package(table([['W' * 200, 'small']])))
        out = io.BytesIO(package(para('text')))
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', UserWarning)
            with ZipFile(out, 'a') as z:
                z.writestr('word/document.xml', b'duplicate')
        with self.assertRaisesRegex(lab.FormatError, 'Duplicate'):
            lab.format_bytes(out.getvalue())

    def test_institutional_citation_affiliation_and_notes(self):
        source = package(para('Title', 'Title') + para('Authors', 'Author') +
                         para('Department; institution; location', 'Affiliation') +
                         para('Introduction', 'Heading1') + para('First.') + para('Second.') +
                         para('Abbreviations: R = recall; P = precision.') +
                         para('Versioned sources (Schatzlab, n.d.; English, 2024a).'))
        output = self.apply(source)
        ps = root(output).findall('.//w:body/w:p', NS)
        self.assertEqual(attr(ps[2], 'w:pPr/w:ind', 'firstLine'), '0')
        self.assertEqual(attr(ps[4], 'w:pPr/w:ind', 'firstLine'), '0')
        self.assertEqual(attr(ps[5], 'w:pPr/w:ind', 'firstLine'), '360')
        self.assertEqual(attr(ps[6], 'w:pPr/w:spacing', 'after'), '0')
        blue = root(output).xpath('.//w:r[w:rPr/w:color/@w:val="3399FF"]', namespaces=NS)
        self.assertEqual(''.join(text(r) for r in blue), '(Schatzlab, n.d.; English, 2024a)')
        self.assertEqual(parts(output), parts(self.apply(output)))

    def test_image_and_caption_stay_together(self):
        image = para(xml='<w:r><w:drawing><x:opaque xmlns:x="urn:test"/></w:drawing></w:r>')
        source = package(image + para('Supplementary Fig. S5. Title. Full explanatory legend.'))
        output = self.apply(source)
        ps = root(output).findall('.//w:body/w:p', NS)
        self.assertEqual(attr(ps[0], 'w:pPr/w:keepNext'), '1')
        self.assertEqual(attr(ps[1], 'w:pPr/w:keepLines'), '1')
        self.assertEqual(parts(output), parts(self.apply(output)))

    def test_idempotence(self):
        source = package(para('H', 'Heading1') + para('See Table 1 (Lee, 2021), Opuntia ficus-indica C3.') + table([['Key', 'Value'], ['A', '2']]))
        one = self.apply(source, species=['Opuntia ficus-indica'], photosynthesis=True)
        two = self.apply(one, species=['Opuntia ficus-indica'], photosynthesis=True)
        self.assertEqual(parts(one), parts(two))

    def test_fail_closed(self):
        simple = table([['A'], ['B']])
        bad = [simple.replace('<w:tcPr>', '<w:tcPr><w:gridSpan w:val="1"/>', 1), simple.replace('<w:tcPr>', '<w:tcPr><w:vMerge/>', 1), simple.replace('<w:tcPr>', '<w:tcPr><w:hMerge/>', 1), simple.replace('</w:tc>', simple + '</w:tc>', 1), simple.replace('<w:tblPr>', '<w:tblPr><w:tblpPr/>', 1), table([['A', 'B'], ['C']]), table([['W' * 200]]), simple.replace('</w:p>', '<w:r><w:drawing/></w:r></w:p>', 1), simple + '<w:p><w:pPr><w:sectPr/></w:pPr></w:p>', '<w:ins>' + para('tracked') + '</w:ins>', para(xml='<w:r><w:t>See Table 1.</w:t><w:drawing/></w:r>')]
        for xml in bad:
            with self.subTest(xml=xml[:120]):
                with self.assertRaises(lab.FormatError):
                    lab.format_bytes(package(xml))


if __name__ == '__main__':
    unittest.main()
