import json,csv,re,zipfile,hashlib
from pathlib import Path
ROOT=Path(__file__).parent
p=json.loads((ROOT/'publications.json').read_text(encoding='utf8'))
links=json.loads((ROOT/'sources/official-links.json').read_text(encoding='utf8'))
official=json.loads((ROOT/'sources/official-60.json').read_text(encoding='utf8'))
extra=[x for x in official if not re.search(r'#\s*\d+',x['titre'])]
gaps=sorted(set(range(1,48))-{x['numero'] for x in p})
with (ROOT/'documentation/ecarts-collection.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,delimiter=';');w.writerow(['numero','categorie','titre','url','observation'])
 for n in gaps:w.writerow([n,'Numéro non retrouvé','','','Absent V2 et liste officielle consultée ; existence non tranchée ; aucun numéro fabriqué.'])
 for x in extra:w.writerow(['','Officiel absent V2, sans numéro affiché',x['titre'],x['url'],'Document complémentaire ; non ajouté à la série animée.'])
 for n in [27,37]:
  for x in links[str(n)]:w.writerow([n,'Doublon de notice officiel',x['title'],x['url'],'Une seule carte V2 ; plusieurs occurrences et deux URL de notices.'])
old=(ROOT/'sources/v2-originale.html').read_text(encoding='utf8');new=(ROOT/'index.html').read_text(encoding='utf8')
functions=['drawFeatured','drawArchive','update','advance','stop','play','navigate']
for name in functions:
 pattern=r'function '+name+r'\(.*?(?=\nfunction |\n\$\(|\n</script>)'
 assert re.search(pattern,old,re.S)[0].replace("Number($('speed').value)",'2300')==re.search(pattern,new,re.S)[0],name
assert old[old.index("$('play').onclick"):].split('</script>')[0].replace("$('speed').onchange=()=>{if(playing)play()};",'')==new[new.index("$('play').onclick"):].split('</script>')[0]
css=lambda h:re.search(r'<style>(.*?)</style>',h,re.S)[1]
assert css(old).replace('object-fit:cover','object-fit:contain')==css(new)
(ROOT/'documentation/controle-preservation.json').write_text(json.dumps({'fonctions_animation_identiques':functions,'evenements_et_initialisation_identiques':True,'css_identique_sauf':'object-fit: cover devient contain pour les images','ordre_numeros_identique':True},ensure_ascii=False,indent=2),encoding='utf8')
report='''# Rapport de fiabilisation — 22 novembre 2026

## Résultat

41 références V2 auditées, 41 notices numérotées concordantes et 41 premières pages de PDF officiels récupérées et utilisées. Chaque première page porte le titre ou le sujet correspondant à la notice. Le contrôle associe la notice numérotée, le titre extrait du PDF et l'examen visuel individuel sur les trois planches de contact. 0 référence V2 non retrouvée ; 0 doublon dans la V2 ; 0 image indisponible parmi les 41 références.

Décompte exclusif par mode d'obtention : 0 couverture récupérée comme fichier image indépendant ; 41 premières pages de PDF (contenant les couvertures authentiques) ; 0 illustration éditoriale ; 0 visuel indisponible. Aucun visuel généré ni substitution entre publications.

Les 41 images distantes de la V2 ont répondu et ont été décodées lors de cet audit HTTP. Cela ne réfute pas les échecs intermittents précédemment constatés dans le navigateur. La correction élimine cette dépendance distante pour tous les visuels.

## Périmètre documentaire et anomalies

La page officielle, sa liste éditoriale et l'affichage limit=60 ont été examinés. Les mêmes 41 numéros sont retrouvés. Le contrôle porte sur cette source et ses notices, sans prétendre constituer un catalogue exhaustif de tous les fonds SRA.

Numéros non retrouvés entre 1 et 47 : 24, 36, 40, 42, 44, 46. Leur absence sur cette source n'établit pas leur inexistence. Ils ne sont ni ajoutés ni renumérotés.

Deux notices distinctes pour chacun des numéros 27 et 37. Une seule carte conservée par numéro. Les titres V2 sont souvent abrégés : titres officiels complets enregistrés en parallèle, sans changement des titres affichés. Variante Abiette (V2 et notice) / Abbiette (PDF n°5) consignée.

Une publication officielle complémentaire, « L'archéologie du Canal Seine-Nord Europe : résultats des diagnostics 2020-2025 », figure dans la liste et est absente de la V2. Aucun numéro de cette série n'est affiché dans son titre ou sa notice ; elle n'est pas ajoutée arbitrairement aux 41 cartes. Voir ecarts-collection.csv pour son URL.

Les PDF n°5, 7 et 17 commencent par une double page dos/couverture. Cette page est conservée intégralement, dans ses proportions, sans recadrage. Elle apparaît donc plus petite à hauteur égale. Aucun titre n'est coupé pour remplir le cadre.

## Modifications ciblées

URL d'images remplacées par images/archeologie-NNN.webp. Données embarquées synchronisées avec publications.json ; aucun fetch nécessaire, compatible file:// et hébergement sous un sous-répertoire GitHub Pages. Les cartes pointent vers la notice individuelle vérifiée. Message de secours : « Couverture non disponible », seulement sur erreur d'image locale.

Une seule modification CSS : object-fit:contain au lieu de cover sur les images afin de conserver les pages entières. Toutes les autres règles CSS, les sept fonctions de l'animation, les gestionnaires de commandes et l'initialisation sont identiques à la V2. Titre fixe, ordre des numéros, taille des cartes, groupes de cinq, transitions et vitesses conservés. Les notes décrivant les anciennes dépendances distantes sont actualisées.

## Tests

Chromium réel avec Playwright, horloge de page contrôlée pour parcourir tout le cycle sans attendre plusieurs minutes. Intervalle de départ testé : 3 600 ms, avec aucune carte à 3 599 ms et une carte à 3 600 ms. Pause, reprise, transfert, navigation, redémarrage, neuf groupes et fin à 41/41 : OK.

41 fichiers WebP décodés par Pillow puis dans Chromium ; 41 chemins distincts ; object-fit:contain. Aucune erreur JavaScript, aucune requête externe nécessaire ; toutes les requêtes HTTP externes bloquées dans le test. Remplacement explicite testé avec un chemin local inexistant. Index et HTML autonome testés via file:// ; index également testé via serveur HTTP local.

Captures pleine page prises avec fenêtres 1920×1080, 1366×768 et 600×900 ; aucune barre de débordement horizontal. La page défile verticalement comme la V2 quand la galerie s'accumule. Contrôle visuel des trois planches et des captures, plus une capture du premier groupe de cinq grandes cartes. Les textes tronqués par les règles de lignes de la V2 sont conservés.

Les résultats détaillés sont dans tests-navigateur.json et controle-preservation.json. Aucun déploiement GitHub effectué ; compatibilité des chemins préparée, pas de test sur un site GitHub Pages publié.

## Sources, droits et limites

PDF originaux, réponses HTML officielles et anciens visuels conservés dans sources/. Le répertoire documentation contient une extraction des mentions de crédits par publication et sources-et-credits.md. Ces extractions regroupent plusieurs crédits et ne constituent pas une attribution certaine d'auteur à chaque photographie de couverture. Les PDF restent la référence pour les droits particuliers ; aucune nouvelle licence photographique n'est inventée.

Les anciennes images sont conservées avec extension .bin (octets téléchargés inchangés), leur format réel et leurs dimensions figurent dans inventaire-originaux.csv. Les PDF sont les originaux des visuels effectivement utilisés. Empreintes SHA-256 des WebP consignées dans publications.json et controle-images.csv.

## Livraison

index.html + images/ : version web, double-clic et GitHub Pages. autonome.html : fichier unique avec les 41 WebP embarqués. publications.json : métadonnées et chemins. Archive complète : application, contrôles, scripts et sources, sans outils Python installés. Archive diffusion : application, images, métadonnées et documentation ; sans PDF et originaux volumineux. Environ 8,2 Mo de WebP contre 137,4 Mo de PDF originaux.
'''
report+='\n\n## Complément : notices Bibdoc\n\n39 liens directs fournis par l’utilisateur intégrés aux vignettes de Collection exposée, dans les deux HTML. Les n°45 et 47 conservent leur notice ministère, faute d’adresse Bibdoc fournie. Voir notices-bibdoc.md et liens-notices.csv pour la provenance, les limites de vérification et les anomalies du catalogue. Les grandes cartes conservent leur lien ministère.\n'
report=report.replace('Aucun déploiement GitHub effectué ; compatibilité des chemins préparée, pas de test sur un site GitHub Pages publié.','Publication publique sur GitHub Pages demandée dans la dernière étape ; voir publication-github.md pour le résultat du déploiement.')
report+='\n\n## Dernière adaptation demandée\n\nSélecteur de vitesse retiré ; vitesse unique de 2,3 secondes par carte. Les fonctions de lecture et le gestionnaire de vitesse ont été adaptés uniquement pour fixer cette durée. Les huit fiches intégrées restent accessibles depuis les grandes cartes et la galerie. Les autres notices seront ajoutées ultérieurement.\n'
(ROOT/'documentation/rapport-fiabilisation.md').write_text(report,encoding='utf8')
if (ROOT/'notices.json').exists():
 with (ROOT/'documentation/rapport-fiabilisation.md').open('a',encoding='utf8') as f:
  f.write('\n\n## Enrichissement depuis le PDF des notices\n\n39 fiches internes intégrées (31 nouvelles et huit recontrôlées), avec auteurs, collaborateurs disponibles, date, description, notes, résumés et sujets. Source : les 39 captures du PDF fourni. Correspondances et divergences documentées dans controle-notices.csv ; tests dans tests-notices-completes.json. Seuls les n°45 et 47 restent sans fiche fournie.\n')
readme='''# Archéologie des Hauts-de-France — V2 fiabilisée

Ouvrir index.html par double-clic en conservant le dossier images/ à côté. Aucun accès au ministère nécessaire pour afficher les visuels. Les liens vers les notices demandent une connexion.

Pour un fichier unique à déplacer ou partager : ouvrir autonome.html (images embarquées).

Pour prévisualiser sur un serveur, depuis ce dossier avec Python installé :

```sh
python -m http.server 8000 --bind 127.0.0.1
```

Puis ouvrir http://127.0.0.1:8000/ ; arrêter le serveur avec Ctrl+C.

## GitHub Pages, ultérieurement

Déposer le contenu de l'archive diffusion dans le dossier destiné à Pages, en conservant les noms et la casse : index.html, images/, publications.json et documentation/. Tous les chemins sont relatifs. Configurer ensuite Pages sur ce dossier. Aucun dépôt ni publication n'a été créé lors de cette intervention.

## Données et contrôle

publications.json documente 41 références. Les mêmes données de chargement sont intégrées dans index.html pour autoriser file://. Après un changement de données, synchroniser la constante PUBS ; build.py reconstruit les deux HTML depuis les inventaires de sources conservés. La version actuelle est déjà construite et ne nécessite aucune installation.

Voir documentation/rapport-fiabilisation.md, audit-publications.csv, ecarts-collection.csv, controle-images.csv et sources-et-credits.md. Les captures PNG documentent le rendu réel aux trois dimensions demandées. Les trois planches contact montrent les 41 visuels.

## Scripts techniques (archive complète)

collect.py : audit des notices et anciennes images ; recover.py : récupération PDF et rendu ; build.py : génération ; package.py : contrôle de préservation et archives. Ces scripts nécessitent Python, Pillow, BeautifulSoup4 et PyMuPDF. Le dossier .tools de travail n'est pas distribué. Les téléchargements ne sont jamais requis au lancement de l'application.

scripts/browser-check.cjs : tests Playwright ; installer @playwright/test et adapter son import à votre installation. Définir PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH vers Chromium si nécessaire. Les tests produisent les captures et tests-navigateur.json. L'horloge simulée accélère les tests sans modifier les vitesses de l'application.

Les numéros 24, 36, 40, 42, 44 et 46 ne sont pas fabriqués. Les doubles pages originales n°5, 7 et 17 sont conservées sans recadrage. Les crédits disponibles sont consignés sans présumer de droits photographiques supplémentaires.
'''
readme+='\n\nLes vignettes de Collection exposée ouvrent 39 notices Bibdoc dans un nouvel onglet. Les numéros 45 et 47 conservent la notice ministère en attendant leurs adresses Bibdoc. Voir documentation/notices-bibdoc.md.\n'
readme=readme.replace('Aucun dépôt ni publication n’a été créé lors de cette intervention.','Publication publique demandée ultérieurement : voir documentation/publication-github.md.').replace("Aucun dépôt ni publication n'a été créé lors de cette intervention.",'Publication publique demandée ultérieurement : voir documentation/publication-github.md.')
readme+='\n\nVersion publique : https://didierthebault-web.github.io/archeologie-hauts-de-france/\nVitesse unique : 2,3 secondes par carte, sans sélecteur. Huit notices bibliographiques intégrées à la page. Les autres seront complétées ultérieurement.\n'
(ROOT/'README.md').write_text(readme,encoding='utf8')
if (ROOT/'notices.json').exists():
 with (ROOT/'README.md').open('a',encoding='utf8') as f:
  f.write('\n\n## Version enrichie des notices\n\n39 fiches internes, issues des 39 pages du PDF fourni : cliquer sur Lire la notice sur une grande carte ou une vignette. Seules les notices n°45 et 47 restent à fournir. Les données éditables se trouvent dans notices.json ; build.py les incorpore aux HTML. Les sources et les tests sont décrits dans documentation/notices-bibdoc.md.\n')
from PIL import Image
with (ROOT/'documentation/inventaire-originaux.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,delimiter=';');w.writerow(['numero','fichier','format','largeur','hauteur','sha256'])
 for x in p:
  path=ROOT/f"sources/images-originales/v2-{x['numero']:03}.bin";im=Image.open(path)
  w.writerow([x['numero'],path.relative_to(ROOT).as_posix(),im.format,im.width,im.height,hashlib.sha256(path.read_bytes()).hexdigest()])
files=[x for x in ROOT.rglob('*') if x.is_file() and not any(part in x.parts for part in ['.tools','.git','.publish','__pycache__'])]
for kind in ['complet','diffusion']:
 target=ROOT.parent/f'archeologie-hauts-de-france-{kind}.zip'
 with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for f in files:
   rel=f.relative_to(ROOT)
   if kind=='diffusion' and (rel.parts[0]=='sources' or f.suffix in ['.py','.cjs']):continue
   z.write(f,Path('archeologie-hauts-de-france')/rel)
 with zipfile.ZipFile(target) as z: assert z.testzip() is None
 print(target.name,target.stat().st_size)
