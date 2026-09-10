"""Bounded final-proof checks; no scientific or accessibility certification."""
import json
import re
import zipfile
from pathlib import Path
import fitz

root = Path.cwd()
main = fitz.open('submission/build/manuscript.pdf')
supp = fitz.open('submission/build/supplementary.pdf')
text = '\n'.join(p.get_text() for p in supp)
assert '##' not in text
assert not re.search(r'Figure \d+:', text)
source = Path('supplementary.md').read_text()
pairs = re.findall(r'!\[Supplementary Figure ([^\]]+)\]\([^)]+\)\s+(Supplementary Figure [^\n]+)', source)
# Source replay separately pins all punctuation/cells. Here ignore Markdown
# delimiters, typographic quotes and TeX line-break hyphens for page placement.
import unicodedata
def normalize(s):
    return ''.join(c for c in unicodedata.normalize('NFKC', s) if c.isalnum())
placements = []
for ident, caption in pairs:
    # Check whole legend, not a mention of a different figure elsewhere.
    needle = normalize(caption)
    pages = [i + 1 for i, p in enumerate(supp) if needle in normalize(p.get_text())]
    assert len(pages) == 1, (ident, pages)
    p = supp[pages[0]-1]
    assert p.get_images(), ('legend has no on-page image', ident, pages)
    placements.append({'figure': ident, 'page': pages[0]})
assert len(placements) == 7
assert len(main) <= 4
main_text = '\n'.join(p.get_text() for p in main)
assert main_text.count('Alt text:') == 2
for name, expected in [('manuscript', 0), ('supplementary', 19)]:
    with zipfile.ZipFile(f'submission/build/{name}.docx') as z:
        assert z.testzip() is None
        from xml.etree import ElementTree as ET
        xml = ET.fromstring(z.read('word/document.xml'))
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        assert len(xml.findall('.//w:tbl', ns)) == expected
print(json.dumps({'main_pages': len(main), 'supplement_pages': len(supp),
                  'literal_headings': 0, 'automatic_figure_numbers': 0,
                  'complete_legends_with_images': placements,
                  'docx_zip_and_tables': 'pass'}, indent=2))
