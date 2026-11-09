"""Génère carrousel.html (modèle éditorial benjaminchaminade, 1080x1350) à partir d'un fichier JSON.

Usage : python3 generer.py contenu.json dossier_sortie
Le dossier de sortie doit contenir photos/cover.png et, si une slide « photo » est utilisée, photos/groupe.png.

Format JSON :
{
  "kicker_couverture": "Travail",
  "titre_l1": "La génération Z se sent seule.",
  "titre_l2": "Son meilleur club : le bureau.",
  "slides": [
    {"type": "stat", "kicker": "Les chiffres", "stat": "37 %", "texte": "...", "gras": "...", "source": "..."},
    {"type": "texte", "kicker": "Le quartier", "paragraphes": [{"texte": "...", "gras": "..."}], "source": "..."},
    {"type": "couleur" | "sombre", "kicker": "Mon avis", "texte": "...", "accent": "..."},
    {"type": "photo", "kicker": "...", "texte": "...", "accent": "..."}
  ],
  "fin": {"kicker": "Pour vos managers", "h2_a": "Une équipe se", "h2_b": "fabrique.", "texte": "...",
          "cta": "DÉCOUVRIR MES CONFÉRENCES →", "url_affichee": "BENJAMINCHAMINADE.COM/INTERVENTIONS"}
}
Règle de Bob : une phrase courte en gras (champ « gras » ou « accent ») commence toujours sur une nouvelle ligne.
Les sauts de ligne voulus s'écrivent avec \n dans le texte.
"""
import html
import json
import re
import sys
from pathlib import Path

NBSP = "&nbsp;"


def esc(t):
    t = html.escape(t or "", quote=False)
    t = re.sub(r"(\d) %", r"\1" + NBSP + "%", t)
    t = re.sub(r"(\d) (\d{3})", r"\1" + NBSP + r"\2", t)
    t = re.sub(r" ([?!:;»])", NBSP + r"\1", t)
    t = t.replace("« ", "«" + NBSP)
    return t.replace("\n", "<br>")


def para(texte, gras):
    out = esc(texte)
    if gras:
        out += (" " if out else "") + '<b class="nl">' + esc(gras) + "</b>"
    return "<p>" + out + "</p>"


def main():
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = Path(sys.argv[2])
    style = (Path(__file__).parent / "style.css").read_text(encoding="utf-8")
    slides = data["slides"]
    n = len(slides) + 3
    dots = "".join('<i class="on"></i>' if i == 0 else "<i></i>" for i in range(n))
    parts = [
        f"""<section class="page cover">
<img class="bg" src="photos/cover.png" alt="">
<div class="shade"></div>
<div class="pill"><img src="logo-benjamin-chaminade.svg" alt="Benjamin Chaminade"></div>
<div class="txt"><div class="kicker">{esc(data['kicker_couverture'])}</div>
<h1>{esc(data['titre_l1'])}<br><span>{esc(data['titre_l2'])}</span></h1></div>
<div class="dots">{dots}</div>
</section>"""
    ]
    first_white = True
    for s in slides:
        t = s["type"]
        src = f'<div class="src">{esc(s["source"])}</div>' if s.get("source") else ""
        if t in ("stat", "texte"):
            top = f'<div class="top"><span class="kicker">{esc(s["kicker"])}</span><img src="logo-benjamin-chaminade.svg" alt=""></div>'
            if t == "stat":
                body = '<p><span class="stat">' + esc(s["stat"]) + "</span>" + para(s.get("texte", ""), s.get("gras"))[3:]
            else:
                body = "".join(para(p.get("texte", ""), p.get("gras")) for p in s["paragraphes"])
            swipe = '<div class="swipe">LA SUITE →</div>' if first_white else ""
            first_white = False
            parts.append(f'<section class="page white">{top}<div class="body">{body}</div>{src}{swipe}</section>')
        elif t in ("couleur", "sombre"):
            cls = "solid" if t == "couleur" else "solid dark"
            acc = f' <em>{esc(s["accent"])}</em>' if s.get("accent") else ""
            parts.append(f'<section class="page {cls}"><div class="wrap"><div class="kicker">{esc(s["kicker"])}</div><p>{esc(s["texte"])}{acc}</p></div></section>')
        elif t == "photo":
            acc = f' <em>{esc(s["accent"])}</em>' if s.get("accent") else ""
            parts.append(f'<section class="page split"><img class="ph" src="photos/groupe.png" alt=""><div class="band"><div class="kicker">{esc(s["kicker"])}</div><p>{esc(s["texte"])}{acc}</p></div></section>')
        else:
            raise SystemExit("type inconnu : " + t)
    parts.append("""<section class="page solid dark center"><div class="wrap"><div class="kicker">@benjaminchaminade</div>
<p>Suivez-moi pour d’autres idées sur <em class="in">le management</em> et <em class="in">l’avenir du travail.</em></p>
<span class="btn">LA SUITE →</span></div></section>""")
    f = data["fin"]
    parts.append(f"""<section class="page end"><img class="logo" src="logo-benjamin-chaminade.svg" alt="Benjamin Chaminade">
<div class="wrap"><div class="kicker">{esc(f['kicker'])}</div>
<h2>{esc(f['h2_a'])} <span>{esc(f['h2_b'])}</span></h2>
<p>{esc(f['texte'])}</p>
<span class="cta">{esc(f['cta'])}</span>
<div class="url">{esc(f['url_affichee'])}</div></div></section>""")
    doc = '<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n' + style + "\n</head>\n<body>\n" + "\n\n".join(parts) + "\n</body>\n</html>\n"
    (out / "carrousel.html").write_text(doc, encoding="utf-8")
    print("ok", n, "slides")


if __name__ == "__main__":
    main()
