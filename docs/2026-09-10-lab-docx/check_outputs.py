"""Verify generated lab-style Word/PDF outputs; source migration has its own guard."""
from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import re,json,sys,importlib.util,unicodedata
import fitz
N={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};W='{'+N['w']+'}'
def partmap(p):
    with ZipFile(p) as z:
        assert z.testzip() is None
        return {n:z.read(n) for n in z.namelist()}
def visible(n):return ''.join(n.xpath('.//w:t/text()',namespaces=N))
def norm(s):return ''.join(c for c in unicodedata.normalize('NFKC',s) if c.isalnum())
spec=importlib.util.spec_from_file_location('lab_docx',Path('submission/lab-docx/lab_docx.py'))
lab=importlib.util.module_from_spec(spec);spec.loader.exec_module(lab)
report={}
for name,count in [('manuscript',0),('supplementary',18)]:
    pre=partmap(f'submission/build/{name}-pandoc.docx');post=partmap(f'submission/build/{name}.docx')
    assert pre.keys()==post.keys()
    assert all(pre[k]==post[k] for k in pre if k not in ('word/document.xml','word/styles.xml'))
    a,b=[E.fromstring(m['word/document.xml']) for m in (pre,post)]
    assert [visible(p) for p in a.findall('.//w:p',N)]==[visible(p) for p in b.findall('.//w:p',N)]
    for tag in ['drawing','bookmarkStart','bookmarkEnd','instrText','fldChar','footnoteReference','endnoteReference']:
        assert [E.tostring(x) for x in a.findall('.//w:'+tag,N)]==[E.tostring(x) for x in b.findall('.//w:'+tag,N)],tag
    assert [x.attrib for x in a.findall('.//w:hyperlink',N)]==[x.attrib for x in b.findall('.//w:hyperlink',N)]
    tables=b.findall('.//w:tbl',N);assert len(tables)==count
    for t in tables:
        widths=[int(x.get(W+'w')) for x in t.findall('w:tblGrid/w:gridCol',N)]
        assert sum(widths)==15138
        rows=t.findall('w:tr',N)
        for ri,row in enumerate(rows):
            assert row.find('w:trPr/w:tblHeader',N).get(W+'val')==('1' if ri==0 else '0')
            for ci,cell in enumerate(row.findall('w:tc',N)):
                assert cell.find('w:tcPr/w:noWrap',N).get(W+'val')=='1'
                assert int(cell.find('w:tcPr/w:tcW',N).get(W+'w'))==widths[ci]
                for edge in ('top','bottom','left','right','insideH','insideV'):
                    on=edge=='top' and ri==0 or edge=='bottom' and ri in (0,len(rows)-1)
                    assert cell.find('w:tcPr/w:tcBorders/w:'+edge,N).get(W+'val')==('single' if on else 'nil')
                for r in cell.findall('.//w:r',N):
                    if not r.findall('w:t',N):continue
                    assert r.find('w:rPr/w:rFonts',N).get(W+'ascii')=='Arial'
                    assert r.find('w:rPr/w:sz',N).get(W+'val')=='18'
    reds=blues=0
    for p in b.findall('w:body/w:p',N):
        for r in p.findall('.//w:r',N):
            if not r.findall('w:t',N):continue
            assert r.find('w:rPr/w:rFonts',N).get(W+'ascii')=='Times New Roman'
            color=r.find('w:rPr/w:color',N).get(W+'val')
            reds+=color=='FF0000';blues+=color=='3399FF'
    assert reds and blues
    again,_=lab.format_bytes(Path(f'submission/build/{name}.docx').read_bytes(),species=['Arabidopsis thaliana','Zea mays'])
    import io
    with ZipFile(io.BytesIO(again)) as z:assert {n:z.read(n) for n in z.namelist()}==post
    report[name]={'tables':count,'text_media_links_preserved':True,'idempotent':True,'red_runs':reds,'blue_runs':blues}
main=fitz.open('submission/build/manuscript.pdf');supp=fitz.open('submission/build/supplementary.pdf')
assert len(main)<=4
source=Path('supplementary.md').read_text()
pat=r'!\[Supplementary Fig\. (S\d+)\]\(([^)]+)\)\s+(\*\*Supplementary Fig\. S\d+\.[^\n]+(?:\n(?!\n)[^\n]+)*)'
placements=[]
for ident,image,caption in re.findall(pat,source):
    found=[i+1 for i,p in enumerate(supp) if norm(caption) in norm(p.get_text())]
    assert len(found)==1,(ident,found)
    assert supp[found[0]-1].get_images(),ident
    placements.append({'figure':ident,'page':found[0]})
assert len(placements)==7
text='\n'.join(p.get_text() for p in supp)
assert '##' not in text
assert not re.search(r'Figure \d+:',text)
report['xelatex']={'main_pages':len(main),'supplement_pages':len(supp),'complete_legends_on_image_pages':placements}
print(json.dumps(report,indent=2))
