# Rapport de fiabilisation — 22 novembre 2026

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

Les résultats détaillés sont dans tests-navigateur.json et controle-preservation.json. Publication publique sur GitHub Pages demandée dans la dernière étape ; voir publication-github.md pour le résultat du déploiement.

## Sources, droits et limites

PDF originaux, réponses HTML officielles et anciens visuels conservés dans sources/. Le répertoire documentation contient une extraction des mentions de crédits par publication et sources-et-credits.md. Ces extractions regroupent plusieurs crédits et ne constituent pas une attribution certaine d'auteur à chaque photographie de couverture. Les PDF restent la référence pour les droits particuliers ; aucune nouvelle licence photographique n'est inventée.

Les anciennes images sont conservées avec extension .bin (octets téléchargés inchangés), leur format réel et leurs dimensions figurent dans inventaire-originaux.csv. Les PDF sont les originaux des visuels effectivement utilisés. Empreintes SHA-256 des WebP consignées dans publications.json et controle-images.csv.

## Livraison

index.html + images/ : version web, double-clic et GitHub Pages. autonome.html : fichier unique avec les 41 WebP embarqués. publications.json : métadonnées et chemins. Archive complète : application, contrôles, scripts et sources, sans outils Python installés. Archive diffusion : application, images, métadonnées et documentation ; sans PDF et originaux volumineux. Environ 8,2 Mo de WebP contre 137,4 Mo de PDF originaux.


## Complément : notices Bibdoc

39 liens directs fournis par l’utilisateur intégrés aux vignettes de Collection exposée, dans les deux HTML. Les n°45 et 47 conservent leur notice ministère, faute d’adresse Bibdoc fournie. Voir notices-bibdoc.md et liens-notices.csv pour la provenance, les limites de vérification et les anomalies du catalogue. Les grandes cartes conservent leur lien ministère.


## Dernière adaptation demandée

Sélecteur de vitesse retiré ; vitesse unique de 2,3 secondes par carte. Les fonctions de lecture et le gestionnaire de vitesse ont été adaptés uniquement pour fixer cette durée. Les huit fiches intégrées restent accessibles depuis les grandes cartes et la galerie. Les autres notices seront ajoutées ultérieurement.


## Enrichissement depuis le PDF des notices

39 fiches internes intégrées (31 nouvelles et huit recontrôlées), avec auteurs, collaborateurs disponibles, date, description, notes, résumés et sujets. Source : les 39 captures du PDF fourni. Correspondances et divergences documentées dans controle-notices.csv ; tests dans tests-notices-completes.json. Seuls les n°45 et 47 restent sans fiche fournie.
