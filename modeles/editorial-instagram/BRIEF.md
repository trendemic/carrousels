# Brief : carrousel au modèle éditorial benjaminchaminade (LinkedIn et Instagram)

Tu écris le CONTENU d'un carrousel de 10 à 12 slides pour Benjamin Chaminade (Bob), conférencier et consultant français en management, RH et innovation. Public : DRH, comités de direction et managers français. Tu ne fabriques ni images ni photos et tu ne publies rien : tu livres un fichier JSON et une fiche.

## Modèle à reproduire (validé par Bob le 8/11/2026)
Exemple complet dans le dépôt trendemic/carrousels : publies/instagram-modele-generation-z-solitude/source.html (rendu : les slide-*.png du même dossier, ouvre-les avec Read).
Structure : une couverture photo avec un titre en deux temps (l1 blanc, l2 jaune, 3 à 8 mots chacun, tout tient en 4 lignes maximum), puis une alternance de slides « stat » (un grand chiffre puis sa phrase), « texte » (un ou deux paragraphes), « couleur » ou « sombre » (une phrase et une chute en jaune), et une seule slide « photo » (photo de groupe en haut, une question et sa réponse en bas). Le récit va du constat chiffré vers l'angle de Bob, puis une question au lecteur. Le générateur ajoute seul la slide « Suivez-moi » et la slide finale (champ « fin »).
Format exact du JSON : lis la docstring de modeles/editorial-instagram/generer.py. Mets entre 7 et 9 slides dans « slides ».

## Règles de contenu (non négociables)
- Chaque chiffre vient d'une source primaire nommée (institut, auteur ou revue) dont tu as OUVERT et LU la page avant de l'écrire. Pas d'agrégateur, pas de reprise média, jamais de chiffre de mémoire, jamais d'URL inventée. Sources françaises et européennes d'abord ; une donnée américaine est signalée dans le champ « source » de la slide (« donnée américaine »). Une enquête de cabinet ou d'employeur est signalée comme telle. Données les plus récentes disponibles (2025 ou 2026). Gallup est exclu.
- Chaque slide chiffrée porte son champ « source » (court : institut, titre, date).
- Aucune anecdote, aucun client, aucune citation inventés. Aucun « une étude montre ».
- Ne jamais attribuer à Bob un concept d'un autre auteur : nomme l'auteur d'origine. Ses concepts à lui (cités seulement s'ils servent) : enableship, intersocialisation, management régénératif, entreprise invulnérable, futureproofing, donut managérial (d'après Kate Raworth), carte des six cultures d'équipe (d'après Gruenert et Whitaker).
- Voix : Bob en « je » sur les slides d'avis, vouvoiement du lecteur. Style naturel de réseau social permis (phrases courtes, apartés entre parenthèses, une image concrète du quotidien, « c'est » et « on » rares).
- Interdits : la structure « ce n'est pas X, c'est Y » et ses variantes ; le tiret cadratin et le double tiret ; « discrètement », « silencieusement », « sans bruit », « en coulisses » ; « comité » seul pour la direction ; « presque » hors citation d'une catégorie d'enquête ; les adverbes de fréquence non étayés ; un verbe en fin de phrase ; les énumérations de trois éléments ou plus sans « et » ou « ou » avant le dernier ; une majuscule ailleurs qu'au premier mot (hors noms propres). Pas de mot anglais quand un mot français existe, sauf le terme étudié.
- Mise en page : une phrase courte en gras va dans le champ « gras » (ou « accent ») pour commencer sur une nouvelle ligne. Un paragraphe de slide « texte » fait 45 mots au plus ; une slide « texte » en compte 2 au plus. Une slide « stat » : le chiffre, une phrase de 25 mots au plus, et un « gras » de 15 mots au plus. Slides « couleur », « sombre » et « photo » : 25 mots au plus en tout.
- Slide finale (« fin ») : renvoie à l'offre la plus proche du sujet, vérifiée sur le site (https://benjaminchaminade.com/interventions/ pour les conférences, ou une page d'offre plus précise si elle existe et répond en 200). Pas de « commentez X et je vous envoie ».

## Livrables (dans ton dossier de travail, indiqué dans ta mission)
1. contenu.json (valide, au format de generer.py).
2. fiche.md :
   - la source d'inspiration (article, post ou tendance) avec son lien, et ce que tu en as repris ;
   - le texte du post LinkedIn (700 à 1 300 caractères, voix de Bob, même règles ; une ouverture sur une scène que le lecteur vit, l'idée, une vraie question, puis « Les sources sont en commentaire. » ou « Le lien vers l'article est en commentaire. »), suivi exactement de cette signature :
     -------
     Je suis entrepreneur, conférencier et consultant franco-australien en management, RH et innovation. J'aide les comités de direction et les DRH à préparer leurs équipes à l'avenir, en conférence, en atelier ou en mission construite avec eux.
   - le premier commentaire (lien de l'article avec ?utm_source=linkedin&utm_medium=social&utm_campaign=carrousel, ou la liste des sources avec leurs URL) ;
   - la légende Instagram (300 à 600 caractères, 3 à 5 hashtags) ;
   - deux requêtes de recherche de photo en anglais pour Unsplash : « cover » (portrait, une personne ou une scène de travail réaliste, sans visage célèbre ni logo) et « groupe » (paysage, plusieurs personnes) ;
   - la liste numérotée des sources lues (auteur ou institution, titre, date, URL, nature) ;
   - un bloc Réserves (chiffres écartés et pourquoi, interprétations, points à faire valider par Bob).
3. Vérifie le JSON avec : python3 -c "import json;json.load(open('contenu.json'))".
Termine par un résumé de 8 lignes au plus : titre de couverture, source d'inspiration, nombre de sources, réserves principales.
