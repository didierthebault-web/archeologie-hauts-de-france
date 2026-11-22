import sys,json,urllib.request,concurrent.futures,io,re
from pathlib import Path
ROOT=Path(__file__).parent
sys.path.insert(0,str(ROOT/'.tools'))
import pymupdf as fitz
from PIL import Image,ImageOps,ImageDraw
data=json.loads((ROOT/'sources/inventory.json').read_text(encoding='utf8'))
def work(row):
 n=row['number']; result={'number':n,'attempts':[]}
 for notice in row['notices']:
  for pdf in notice.get('pdfs',[]):
   try:
    path=ROOT/f'sources/pdf/archeologie-{n:03}.pdf'
    if not path.exists():
     with urllib.request.urlopen(urllib.request.Request(pdf['url'],headers={'User-Agent':'Mozilla/5.0'}),timeout=90) as r: b=r.read()
     if not b.startswith(b'%PDF'): raise ValueError('Réponse non PDF')
     path.write_bytes(b)
    doc=fitz.open(path); page=doc[0]; text=page.get_text(); pix=page.get_pixmap(matrix=fitz.Matrix(1.65,1.65),alpha=False)
    im=Image.open(io.BytesIO(pix.tobytes('png'))); im.thumbnail((1400,1800)); im.save(ROOT/f'images/archeologie-{n:03}.webp',quality=88,method=6)
    (ROOT/f'sources/pdf/archeologie-{n:03}-texte.txt').write_text('\n\n'.join(p.get_text() for p in doc),encoding='utf8')
    result.update({'url_pdf':pdf['url'],'url_publication':notice['url'],'titre_officiel':notice['h1'],'first_page_text':text,'width':im.width,'height':im.height,'pages':len(doc),'type_visuel':'premiere_page_pdf','image':f'images/archeologie-{n:03}.webp'})
    print(n,'PDF',len(doc),text[:180].replace('\n',' '),flush=True); return result
   except Exception as e: result['attempts'].append({'url':pdf['url'],'error':str(e)})
 print(n,'FAILED',result['attempts'],flush=True); return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex: results=list(ex.map(work,data))
(ROOT/'sources/recovered.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8')
for batch in range(3):
 rows=results[batch*15:(batch+1)*15]; sheet=Image.new('RGB',(1500,340*((len(rows)+4)//5)),'#dddddd'); d=ImageDraw.Draw(sheet)
 for i,r in enumerate(rows):
  x=(i%5)*300;y=(i//5)*340
  if r.get('image'):
   im=Image.open(ROOT/r['image']); im.thumbnail((286,305)); sheet.paste(im,(x+(300-im.width)//2,y+25))
  d.text((x+10,y+5),str(r['number']),fill='black')
 sheet.save(ROOT/f'documentation/contact-{batch+1}.jpg')
