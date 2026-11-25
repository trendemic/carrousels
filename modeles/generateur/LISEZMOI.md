# Générateur de carrousels en 9 pages (Glukoze, .com.au, Reboot Lab et Trendemic)

`python3 build.py specs/<fichier>.json <dossier>` écrit carrousel.html, puis `node ../render.js <dossier> carrousel` produit slide-1.png à slide-9.png et le PDF.
Les marques glukoze et bcau lisent leurs polices et logos dans modeles/glukoze et modeles/benjaminchaminade (à copier dans brands/<marque>/ avant usage).
Reboot Lab : Manrope (OFL), couleurs relevées sur reboot-lab.com le 25/11/2026. Trendemic : General Sans, couleurs relevées sur trendemic.net le 25/11/2026 ; le logo officiel reste à déposer dans brands/trendemic (le modèle affiche pour l'instant le mot trendemic et le slogan en texte).
Balisage des textes : [[surlignage]], {{accent}} et \n pour un saut de ligne. Chaque spec contient aussi le texte du post LinkedIn, le texte court et la légende Instagram.
