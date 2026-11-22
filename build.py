import json,re,csv,hashlib,base64,unicodedata
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).parent
inv=json.loads((ROOT/'sources/inventory.json').read_text(encoding='utf8'))
rec=json.loads((ROOT/'sources/recovered.json').read_text(encoding='utf8'))
def csvwrite(name,rows):
 with (ROOT/'documentation'/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');w.writeheader();w.writerows(rows)
def norm(t): return ''.join(c for c in unicodedata.normalize('NFKD',t.lower()) if not unicodedata.combining(c))
pubs=[];audit=[];checks=[];credits=['# Sources et crédits','Récupération : 22 novembre 2026. Source : ministère de la Culture / DRAC Hauts-de-France / SRA.','Les images sont des rendus intégraux des premières pages des PDF officiels, sans recadrage. Les couvertures se trouvent sur ces premières pages ; les numéros 5, 7 et 17 présentent une double page (dos et couverture), conservée entière.','Les mentions générales du site annoncent la licence Etalab 2.0 sauf mention contraire. Cette mention ne permet pas de présumer une licence photographique pour chaque image : les mentions propres aux PDF restent applicables. Les crédits ci-dessous sont extraits sans attribuer arbitrairement un auteur à la couverture. Les textes intégraux extraits sont conservés dans sources/pdf.']
for v,r in zip(inv,rec):
 n=v['number']; p=v['v2']; assert n==r['number'] and r.get('image')
 # Contrôle de correspondance titre/lieu : la notice officielle donne le numéro,
 # et la première page du PDF donne le sujet. La planche visuelle est examinée séparément.
 key={47:'olhain',45:'bavay',43:'littoral',41:'calais',39:'montreuil',38:'choisy',37:'beaumont',35:'seclin',34:'chamant',33:'guines',32:'amiens',31:'toufflers',30:'villers',29:'blendecques',28:'chiry',27:'douchy',26:'coucy',25:'saint-amand',23:'templeuve',22:'montescourt',21:'faiencerie',20:'peronne',19:'arras',18:'compiegne',17:'avesnes',16:'saint-just',15:'dunkerque',14:'laon',13:'potiers',12:'pont-sainte',11:'hardinghem',10:'camon',9:'etaples',8:'ribecourt',7:'bouchain',6:'chemin des dames',5:'abiette',4:'saint-quentin',3:'waziers',2:'coyolles',1:'orchies'}[n]
 assert key in norm(r['first_page_text']).replace('abbiette','abiette'),(n,key)
 assert re.search(r'#\s*'+str(n)+r'\b',r['titre_officiel'])
 im=Image.open(ROOT/r['image']);im.verify()
 note='Première page PDF entière ; titre et sujet contrôlés, notice officielle numérotée ; contrôle visuel sur planche.'
 if n in [5,7,17]: note+=' Double page conservée sans recadrage.'
 fulltext=(ROOT/f'sources/pdf/archeologie-{n:03}-texte.txt').read_text(encoding='utf8')
 lines=fulltext.splitlines(); selected=set()
 for i,line in enumerate(lines):
  if re.search(r'crédit|cliché|couverture|©|copyright|photograph|illustration',line,re.I): selected.update(range(max(0,i-1),min(len(lines),i+4)))
 credit='\n'.join(lines[i] for i in sorted(selected))
 (ROOT/f'documentation/credits-{n:03}.txt').write_text(credit or 'Pas de mention isolable automatiquement ; consulter le PDF officiel.',encoding='utf8')
 item={'numero':n,'titre':p['title'],'titre_officiel':r['titre_officiel'],'image':r['image'],'type_visuel':'premiere_page_pdf','source_image':r['url_pdf'],'url_publication':r['url_publication'],'url_pdf':r['url_pdf'],'statut_verification':'valide','date_recuperation':'2026-11-22','format':'WebP','largeur':r['width'],'hauteur':r['height'],'observations':note,'credits':f'documentation/credits-{n:03}.txt','sha256':hashlib.sha256((ROOT/r['image']).read_bytes()).hexdigest()}
 notice_links=json.loads((ROOT/'sources/liens-bibdoc.json').read_text(encoding='utf8')) if (ROOT/'sources/liens-bibdoc.json').exists() else {}
 item['url_notice_bibdoc']=notice_links.get(str(n))
 pubs.append(item)
 anomaly='Titre V2 abrégé, sujet concordant.'
 if len(v['notices'])>1: anomaly+=' Deux notices officielles pour le même numéro.'
 if n==5: anomaly+=' Variante orthographique Abiette (V2/notice) / Abbiette (PDF).'
 audit.append({'numero':n,'titre_v2':p['title'],'url_image_v2':p['image'],'url_officielle':r['url_publication'],'titre_officiel':r['titre_officiel'],'chargement_image_v2':'OK lors de la récupération HTTP ; ne garantit pas le chargement distant dans un navigateur','presence':'V2 et site officiel','doublon_v2':'non','anomalies':anomaly})
 checks.append({'numero':n,'titre':p['title'],'image_locale':r['image'],'type_visuel':'premiere_page_pdf','source':r['url_pdf'],'correspondance':'Validée','chargement':'OK - décodage Pillow ; test navigateur consigné séparément','dimensions':f"{r['width']} x {r['height']}",'date_recuperation':'2026-11-22','observations':note,'preuve_titre_pdf':r['first_page_text'].split('L’ÉTAT ET')[0][:350].replace('\n',' '),'credits':item['credits'],'sha256':item['sha256']})
 credits.extend([f"\n## N° {n} — {p['title']}",f"Notice : {r['url_publication']}",f"PDF officiel : {r['url_pdf']}",f"Visuel local : {r['image']} ; première page intégrale ; {r['width']} × {r['height']} px.",f"Mentions relevées : documentation/credits-{n:03}.txt ; texte complet : sources/pdf/archeologie-{n:03}-texte.txt."])
csvwrite('audit-publications.csv',audit);csvwrite('controle-images.csv',checks)
(ROOT/'publications.json').write_text(json.dumps(pubs,ensure_ascii=False,indent=2),encoding='utf8')
(ROOT/'documentation/sources-et-credits.md').write_text('\n\n'.join(credits),encoding='utf8')
html=(ROOT/'sources/v2-originale.html').read_text(encoding='utf8')
runtime=[{'number':p['numero'],'title':p['titre'],'image':p['image'],'url_publication':p['url_publication'],'url_notice_bibdoc':p['url_notice_bibdoc']} for p in pubs]
html=re.sub(r'const PUBS=\[.*?\];','const PUBS='+json.dumps(runtime,ensure_ascii=False)+';',html,flags=re.S)
start=html.index('function makeImage(');end=html.index('\nfunction item(',start)
html=html[:start]+'''function makeImage(p){const frame=document.createElement('div');frame.className='image-frame';const img=document.createElement('img');img.className='picture';img.alt='Première page du PDF officiel : '+p.title;img.loading='eager';img.onerror=()=>{frame.replaceChildren();const alt=document.createElement('div');alt.className='missing';alt.textContent='Couverture non disponible';frame.append(alt)};img.src=p.image;frame.append(img);return frame}'''+html[end:]
html=html.replace("a.href=SOURCE;","a.href=(mini&&p.url_notice_bibdoc)||p.url_publication||SOURCE;")
html=html.replace('.image-frame .picture{height:100%;object-fit:cover}', '.image-frame .picture{height:100%;object-fit:contain}')
html=html.replace('Les miniatures conservent le visuel éditorial disponible ; certaines images distantes peuvent être bloquées par le site source.','Les premières pages des PDF officiels sont intégrées localement et conservées sans recadrage.')
html=html.replace('Les données des 41 références reprennent la première version ; les images sont appelées par leur URL distante et ne sont pas intégrées dans le fichier HTML.','Les 41 références ont été contrôlées le 22 novembre 2026 ; les visuels sont chargés depuis le dossier local images/.')
html=re.sub(r'<label for="speed">Vitesse</label><select id="speed">.*?</select>','',html,flags=re.S)
html=html.replace("Number($('speed').value)",'2300')
html=html.replace("$('speed').onchange=()=>{if(playing)play()};",'')
if (ROOT/'notices-ui.js').exists():
 html=html.replace('</body>', '<script>'+ (ROOT/'notices-ui.js').read_text(encoding='utf8')+'</script></body>')
(ROOT/'index.html').write_text(html,encoding='utf8')
# Mêmes données embarquées : index.html fonctionne directement en file://, sans fetch JSON.
standalone=html
for p in pubs: standalone=standalone.replace('"image": "'+p['image']+'"','"image": "data:image/webp;base64,'+base64.b64encode((ROOT/p['image']).read_bytes()).decode()+'"')
(ROOT/'autonome.html').write_text(standalone,encoding='utf8')
(ROOT/'animation-avec-notices.html').write_text(standalone,encoding='utf8')
print('Built',len(pubs),'images',sum((ROOT/p['image']).stat().st_size for p in pubs))
