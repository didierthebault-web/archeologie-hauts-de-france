# Notices bibliographiques intégrées

39 fiches détaillées sont intégrées dans l'animation, à partir des 39 captures du PDF fourni par l'utilisateur. Cette version ajoute 31 fiches aux huit premières et recontrôle l'ensemble.

Un clic sur une carte portant « Lire la notice » ouvre la fiche dans la page, depuis la zone centrale comme depuis la galerie cumulative. L'animation se met en pause et reprend à la fermeture uniquement si elle était en lecture avant l'ouverture. La vitesse reste fixée à 2,3 secondes par carte.

Les fiches présentent le titre, les auteurs, les collaborateurs lorsqu'ils figurent dans la capture, la collectivité éditrice, la coordination, la langue, le dépôt légal, la description matérielle, la collection, les notes bibliographiques, le résumé et les sujets. Les résumés sont reformulés à partir des captures, ce qui est précisé dans la fiche.

## Sources et données

- notices.json contient les 39 fiches et le numéro de page source de chaque capture.
- publications.json associe les références aux images, aux liens et aux notices.
- sources/notices-bibdoc/ contient les captures WebP et les reconnaissances de texte brutes. Ces OCR bruts peuvent contenir des erreurs et ne sont pas les données affichées.
- Le PDF source est conservé dans sources/notices-bibdoc/Presentation-5.pdf.
- documentation/controle-notices.csv donne les correspondances et les anomalies.

Les titres, auteurs, dates et descriptions ont été contrôlés sur les captures. Les erreurs de reconnaissance de caractères ont été corrigées. Les données sont incorporées dans les HTML lors de la construction : aucune connexion à Bibdoc ni requête JSON externe n'est requise pour lire une fiche.

## Lacunes et divergences

Deux notices ne figurent pas dans le PDF : n°45 (Bavay, trompette romaine) et n°47 (Bois d'Olhain). Aucune fiche n'est inventée ; leurs liens vers le ministère sont conservés.

Guînes : la capture indique n°30, la série officielle n°33. Laon : le résumé indique 18e alors que la collection indique n°14. Ribécourt : le titre parle de dépôts funéraires, alors que son résumé et le PDF officiel précisent non funéraires. Péronne : la description indique [6] pages et le résumé 8 pages. Étaples : le colophon signale un dépôt légal erroné de 2016, la publication est cataloguée 2019. Le couvent de l'Abbiette : le titre mentionne la fin du XVIIIe siècle et le résumé la fin du XVIIe siècle. Ces divergences sont signalées dans les fiches concernées.

Les liens Bibdoc ont été fournis par l'utilisateur ; l'accès automatisé au catalogue reste refusé. Une nouvelle vérification en ligne des notices n'est donc pas annoncée.

## Vérifications

scripts/check-all-notices.cjs vérifie dans Chromium les 39 fiches depuis la zone centrale et les 39 fiches depuis la galerie, dans index.html et autonome.html, ainsi que le contenu de chaque fiche et l'affichage étroit. Résultats : documentation/tests-notices-completes.json. Le test de l'animation et des 41 couvertures est conservé dans scripts/browser-check.cjs.
