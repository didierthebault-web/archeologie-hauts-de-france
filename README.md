# Archéologie des Hauts-de-France — V2 fiabilisée

Ouvrir index.html par double-clic en conservant le dossier images/ à côté. Aucun accès au ministère nécessaire pour afficher les visuels. Les liens vers les notices demandent une connexion.

Pour un fichier unique à déplacer ou partager : ouvrir autonome.html (images embarquées).

Pour prévisualiser sur un serveur, depuis ce dossier avec Python installé :

```sh
python -m http.server 8000 --bind 127.0.0.1
```

Puis ouvrir http://127.0.0.1:8000/ ; arrêter le serveur avec Ctrl+C.

## GitHub Pages, ultérieurement

Déposer le contenu de l'archive diffusion dans le dossier destiné à Pages, en conservant les noms et la casse : index.html, images/, publications.json et documentation/. Tous les chemins sont relatifs. Configurer ensuite Pages sur ce dossier. Publication publique demandée ultérieurement : voir documentation/publication-github.md.

## Données et contrôle

publications.json documente 41 références. Les mêmes données de chargement sont intégrées dans index.html pour autoriser file://. Après un changement de données, synchroniser la constante PUBS ; build.py reconstruit les deux HTML depuis les inventaires de sources conservés. La version actuelle est déjà construite et ne nécessite aucune installation.

Voir documentation/rapport-fiabilisation.md, audit-publications.csv, ecarts-collection.csv, controle-images.csv et sources-et-credits.md. Les captures PNG documentent le rendu réel aux trois dimensions demandées. Les trois planches contact montrent les 41 visuels.

## Scripts techniques (archive complète)

collect.py : audit des notices et anciennes images ; recover.py : récupération PDF et rendu ; build.py : génération ; package.py : contrôle de préservation et archives. Ces scripts nécessitent Python, Pillow, BeautifulSoup4 et PyMuPDF. Le dossier .tools de travail n'est pas distribué. Les téléchargements ne sont jamais requis au lancement de l'application.

scripts/browser-check.cjs : tests Playwright ; installer @playwright/test et adapter son import à votre installation. Définir PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH vers Chromium si nécessaire. Les tests produisent les captures et tests-navigateur.json. L'horloge simulée accélère les tests sans modifier les vitesses de l'application.

Les numéros 24, 36, 40, 42, 44 et 46 ne sont pas fabriqués. Les doubles pages originales n°5, 7 et 17 sont conservées sans recadrage. Les crédits disponibles sont consignés sans présumer de droits photographiques supplémentaires.


Les vignettes de Collection exposée ouvrent 39 notices Bibdoc dans un nouvel onglet. Les numéros 45 et 47 conservent la notice ministère en attendant leurs adresses Bibdoc. Voir documentation/notices-bibdoc.md.


Version publique : https://didierthebault-web.github.io/archeologie-hauts-de-france/
Vitesse unique : 2,3 secondes par carte, sans sélecteur. Huit notices bibliographiques intégrées à la page. Les autres seront complétées ultérieurement.


## Version enrichie des notices

39 fiches internes, issues des 39 pages du PDF fourni : cliquer sur Lire la notice sur une grande carte ou une vignette. Seules les notices n°45 et 47 restent à fournir. Les données éditables se trouvent dans notices.json ; build.py les incorpore aux HTML. Les sources et les tests sont décrits dans documentation/notices-bibdoc.md.
