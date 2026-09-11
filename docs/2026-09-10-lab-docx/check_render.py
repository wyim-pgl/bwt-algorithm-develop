"""All-page LibreOffice proof geometry and complete figure-caption checks."""
from pathlib import Path
import fitz,re,unicodedata,collections,json,sys
from PIL import Image,ImageDraw
out=Path(sys.argv[1]);report={}
normalize=lambda t:''.join(c for c in unicodedata.normalize('NFKC',t) if c.isalnum())
s=Path('supplementary.md').read_text()
pat=r'!\[Supplementary Fig\. (S\d+)\]\(([^)]+)\)\s+(\*\*Supplementary Fig\. S\d+\.[^\n]+(?:\n(?!\n)[^\n]+)*)'
for name in ('manuscript','supplementary'):
    d=fitz.open(out/(name+'.pdf'));off=[];table_pages=[];cards=[]
    for i,p in enumerate(d):
        for b in p.get_text('dict')['blocks']:
            if b['type']==0:
                for line in b['lines']:
                    for span in line['spans']:
                        if not p.rect.contains(fitz.Rect(span['bbox'])):off.append((i+1,span['text']))
        ys=collections.defaultdict(float)
        for draw in p.get_drawings():
            r=draw['rect']
            if r.height<3 and r.width>10:ys[round(r.y0)]+=r.width
        bands=[y for y,w in ys.items() if w>p.rect.width*.7]
        if name=='supplementary' and len(bands)>=2:
            table_pages.append(i+1)
            pix=p.get_pixmap(matrix=fitz.Matrix(1.1,1.1))
            im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
            im.thumbnail((850,600));card=Image.new('RGB',(870,630),'white');card.paste(im,(10,25))
            ImageDraw.Draw(card).text((10,5),f'DOCX-render table-bearing page {i+1}',fill='black');cards.append(card)
    assert not off,(name,off)
    report[name]={'pages':len(d),'off_page_text_spans':len(off),'table_bearing_pages':table_pages}
    if name=='supplementary':
        placements=[]
        for ident,image,caption in re.findall(pat,s):
            found=[i+1 for i,p in enumerate(d) if normalize(caption) in normalize(p.get_text())]
            assert len(found)==1,(ident,found)
            assert d[found[0]-1].get_images(),(ident,'caption detached')
            placements.append({'figure':ident,'page':found[0]})
        report[name]['complete_legends_with_images']=placements
        for k in range(0,len(cards),4):
            sheet=Image.new('RGB',(1740,1260),'#dddddd')
            for j,card in enumerate(cards[k:k+4]):sheet.paste(card,((j%2)*870,(j//2)*630))
            sheet.save(out/f'table-contact-{k//4+1}.png')
print(json.dumps(report,indent=2))
