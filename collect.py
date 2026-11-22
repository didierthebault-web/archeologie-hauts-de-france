import sys,json,re,urllib.request,urllib.parse,concurrent.futures,time
from pathlib import Path
ROOT=Path(__file__).parent
sys.path.insert(0,str(ROOT/'.tools'))
from bs4 import BeautifulSoup
SOURCE='https://www.culture.gouv.fr/regions/drac-hauts-de-france/ressources-documentaires/les-publications-des-hauts-de-france-du-service-regional-de-l-archeologie-sra/plaquettes-archeologie-en-hauts-de-france'
for d in ['sources/notices','sources/images-originales','sources/pdf','images','documentation','scripts']: (ROOT/d).mkdir(parents=True,exist_ok=True)
def get(url,path):
 if path.exists(): return path.read_bytes()
 req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
 for attempt in range(3):
  try:
   with urllib.request.urlopen(req,timeout=50) as r: b=r.read()
   path.write_bytes(b); return b
  except Exception:
   if attempt==2: raise
   time.sleep(1)
html=Path(r'C:\Users\didie\Downloads\archeologie_hauts_de_france_galerie_cumulative_v2.html').read_text(encoding='utf8')
(ROOT/'sources/v2-originale.html').write_text(html,encoding='utf8')
pubs=json.loads(re.search(r'const PUBS=(\[.*?\]);',html,re.S).group(1))
soup=BeautifulSoup(get(SOURCE,ROOT/'sources/collection.html'),'html.parser')
links={}
for a in soup.select('a[href]'):
 t=a.get_text(' ',strip=True); m=re.search(r'#\s*(\d+)',t)
 if m: links.setdefault(int(m[1]),[]).append({'title':t,'url':urllib.parse.urljoin(SOURCE,a['href'])})
(ROOT/'sources/official-links.json').write_text(json.dumps(links,ensure_ascii=False,indent=2),encoding='utf8')
def work(p):
 n=p['number']; out={'number':n,'v2':p,'notices':[]}
 for j,link in enumerate({x['url']:x for x in links.get(n,[])}.values()):
  try:
   b=get(link['url'],ROOT/f'sources/notices/{n:03}-{j}.html'); s=BeautifulSoup(b,'html.parser')
   pdfs=[]
   for a in s.select('a[href]'):
    u=urllib.parse.urljoin(link['url'],a['href'])
    if '.pdf' in u.lower() or '/media/' in u.lower() and ('télécharg' in a.get_text().lower()): pdfs.append({'url':u,'label':a.get_text(' ',strip=True)})
   out['notices'].append({**link,'h1':s.h1.get_text(' ',strip=True) if s.h1 else '', 'pdfs':pdfs,'text':s.get_text(' ',strip=True)})
  except Exception as e: out['notices'].append({**link,'error':str(e)})
 try:
  from PIL import Image
  import io
  b=get(p['image'],ROOT/f'sources/images-originales/v2-{n:03}.bin'); im=Image.open(io.BytesIO(b)); im.verify(); out['old_image_status']='OK'
 except Exception as e: out['old_image_status']=str(e)
 (ROOT/f'sources/notices/{n:03}.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
 print(n,len(out['notices']),[(x.get('h1'),len(x.get('pdfs',[]))) for x in out['notices']],flush=True)
 return out
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex: results=list(ex.map(work,pubs))
(ROOT/'sources/inventory.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8')
print('OFFICIAL NUMBERS',sorted(links),flush=True)
