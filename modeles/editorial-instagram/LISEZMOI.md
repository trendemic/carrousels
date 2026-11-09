# Modèle éditorial benjaminchaminade (LinkedIn et Instagram)

Carrousel de 10 à 12 slides en 1080×1350 : couverture photo, chiffres sourcés, avis de Bob, slide « Suivez-moi » et slide finale vers une offre.
Exemple complet validé par Bob le 8/11/2026 : publies/instagram-modele-generation-z-solitude/.

1. Écrire contenu.json selon BRIEF.md (format décrit dans generer.py, exemple dans exemple-contenu.json).
2. Copier dans le dossier de travail les polices, les logos et rendu.js, et placer photos/cover.png (portrait 4:5) et photos/groupe.png (paysage).
3. python3 generer.py contenu.json <dossier> puis node <dossier>/rendu.js : slide-1.png à slide-N.png.
4. Construire le PDF à partir des PNG (PIL), jamais par l'impression du HTML (elle coupe les paragraphes).
