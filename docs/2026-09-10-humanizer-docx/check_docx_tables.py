"""Compare pre/post table formatting without trusting the formatter's receipt."""
import sys
from zipfile import ZipFile
from lxml import etree as E
from pathlib import Path
import importlib.util
import tempfile
import shutil
N={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W='{'+N['w']+'}'
def parts(path):
    with ZipFile(path) as z:
        assert z.testzip() is None
        return {k:z.read(k) for k in z.namelist()}
before,after=map(parts,sys.argv[1:3])
assert before.keys()==after.keys()
assert all(before[k]==after[k] for k in before if k!='word/document.xml'), 'Non-document part changed'
a,b=[E.fromstring(d['word/document.xml']) for d in (before,after)]
assert a.xpath('//w:t/text()',namespaces=N)==b.xpath('//w:t/text()',namespaces=N)
for name in ('drawing','hyperlink','bookmarkStart','bookmarkEnd','fldChar','instrText','footnoteReference','endnoteReference','commentReference'):
    assert [E.tostring(n) for n in a.findall('.//w:'+name,N)]==[E.tostring(n) for n in b.findall('.//w:'+name,N)], name
# Strip only permitted format properties then compare the complete XML trees.
for doc in (a,b):
    for t in doc.findall('.//w:tbl',N):
        for kind in ('tblPr','trPr','tcPr','pPr','rPr','tblGrid'):
            for n in t.findall('.//w:'+kind,N): n.getparent().remove(n)
    for n in doc.findall('.//w:sectPr/w:pgSz',N)+doc.findall('.//w:sectPr/w:pgMar',N):
        n.getparent().remove(n)
assert E.tostring(a)==E.tostring(b), 'Content/order changed outside allowed formatting'
b=E.fromstring(after['word/document.xml'])
tables=b.findall('.//w:tbl',N); assert len(tables)==19
for t in tables:
    assert not t.findall('.//w:shd',N)
    assert not t.findall('.//w:noWrap',N)
    assert t.find('w:tblPr/w:tblStyle',N) is None
    rows=t.findall('w:tr',N)
    widths=[int(x.get(W+'w')) for x in t.findall('w:tblGrid/w:gridCol',N)]
    assert sum(widths)==15138
    for i,row in enumerate(rows):
        assert (row.find('w:trPr/w:tblHeader',N) is not None)==(i==0)
        assert row.find('w:trPr/w:cantSplit',N) is not None
        for j,cell in enumerate(row.findall('w:tc',N)):
            assert int(cell.find('w:tcPr/w:tcW',N).get(W+'w'))==widths[j]
            for edge in ('left','right','insideH','insideV','start','end'):
                assert cell.find('w:tcPr/w:tcBorders/w:'+edge,N).get(W+'val')=='nil'
            assert cell.find('w:tcPr/w:tcBorders/w:top',N).get(W+'val')==('single' if i==0 else 'nil')
            assert cell.find('w:tcPr/w:tcBorders/w:bottom',N).get(W+'val')==('single' if i in (0,len(rows)-1) else 'nil')
            for run in cell.findall('.//w:r',N):
                assert run.find('w:rPr/w:rFonts',N).get(W+'ascii')=='Arial'
                assert run.find('w:rPr/w:sz',N).get(W+'val')=='18'
script=Path(sys.argv[3])
spec=importlib.util.spec_from_file_location('formatter',script);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
with tempfile.TemporaryDirectory() as tmp:
    p=Path(tmp)/'again.docx';shutil.copyfile(sys.argv[2],p);mod.format_tables(p)
    assert parts(p)==after, 'Formatter is not idempotent'
print('PASS: 19 tables; exact text/content, media, links and other ZIP parts preserved; three-line rules/widths/fonts checked; idempotent.')
