#!/usr/bin/env python3
"""Construit carrousel.html (9 pages, 1080x1350) pour une marque à partir d'un spec JSON.

Usage : python3 build.py spec.json dossier_sortie
Marques : glukoze, bcau, rebootlab, trendemic.
Balisage dans les textes : [[texte]] = surlignage, {{texte}} = couleur d'accent, \n = saut de ligne.
"""
import json, os, re, shutil, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))

CSS_COMMON = """
*{box-sizing:border-box;margin:0;padding:0}
p,h1,h2{text-wrap:pretty}
body{background:#888}
.page{width:1080px;height:1350px;position:relative;overflow:hidden;padding:110px 100px 0;display:flex;flex-direction:column}
.foot{position:absolute;left:100px;right:100px;bottom:70px;display:flex;justify-content:space-between;align-items:center;font-size:26px}
.blob{position:absolute;border-radius:50%}
.rows{margin-top:56px;display:flex;flex-direction:column;gap:22px}
.row{display:flex;align-items:center;gap:34px;background:#fff;padding:32px 40px}
.row .n{flex:0 0 78px;height:78px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-size:42px}
.row .d{flex:0 0 36px;height:36px;border-radius:50%}
.row p{font-size:42px;line-height:1.25}
.rows.dense{margin-top:40px;gap:16px}.rows.dense .row{padding:22px 36px}.rows.dense .row .n{flex-basis:68px;height:68px;font-size:36px}
.note{margin-top:46px;font-size:38px;line-height:1.35}
.bottom{margin-top:auto;margin-bottom:250px}
.swipe{display:flex;align-items:center;gap:20px}
.swipe b{display:inline-block;width:90px;height:4px;position:relative}
.swipe b:after{content:"";position:absolute;right:-2px;top:-9px;border:11px solid transparent;border-right:0}
.tag{display:inline-flex;align-items:center;gap:18px;font-size:30px;letter-spacing:.12em;text-transform:uppercase;padding:18px 30px;border-radius:60px;align-self:flex-start}
.tag i{width:22px;height:22px;border-radius:50%;display:block}
.endurl{align-self:flex-end;text-align:right}
"""

BRANDS = {
 'glukoze': dict(
  fonts="""@font-face{font-family:Expose;font-weight:700;src:url(Expose-Bold.woff2) format('woff2')}
@font-face{font-family:Bespoke;font-weight:400;src:url(BespokeSans-Regular.woff2) format('woff2')}""",
  css="""body{font-family:Bespoke,sans-serif;color:#192a3d}
.page{background:#f6f3ee}.page.dark{background:#192a3d;color:#fff}
h1,h2,.kicker,.num,.row .n,.tag,.swipe,.dom{font-family:Expose;font-weight:700}
h1{font-size:140px;line-height:.98;letter-spacing:-.02em}h2{font-size:92px;line-height:1.03;letter-spacing:-.015em}
p{font-size:46px;line-height:1.32}.big{font-size:56px;line-height:1.26}
.kicker{font-size:30px;letter-spacing:.14em;text-transform:uppercase;color:#44c3cc;margin-bottom:46px}
.muted{color:#5d6b7a}.dark .muted{color:rgba(255,255,255,.8)}
.foot{color:#5d6b7a;letter-spacing:.02em}.dark .foot{color:rgba(255,255,255,.6)}.foot img{height:38px}.num{font-size:24px}
.hl{background:linear-gradient(transparent 62%,rgba(68,195,204,.45) 62%)}.dark .hl{background:none;color:#44c3cc}
.acc{color:#44c3cc}.row{border-radius:24px}.bar{border-left:10px solid #44c3cc;padding-left:50px}
.swipe b{background:#44c3cc}.swipe b:after{border-left:16px solid #44c3cc}""",
  palette=['#44c3cc','#01cc9e','#ff5959','#ff99bb','#192a3d'],
  tagstyles={'ok':('rgba(1,204,158,.14)','#008f6f','#01cc9e'),'ko':('rgba(255,89,89,.13)','#d83c3c','#ff5959')},
  logo='logo-glukoze.svg', logo_w='logo-glukoze-blanc.svg', pill=False,
  assets=['Expose-Bold.woff2','BespokeSans-Regular.woff2','logo-glukoze.svg','logo-glukoze-blanc.svg'],
  blobs_cover=[(620,'#44c3cc','right:-220px;top:-200px;opacity:.95'),(170,'#ff5959','right:330px;top:250px'),(90,'#01cc9e','right:190px;top:430px'),(56,'#ff99bb','right:470px;top:440px')],
  blobs_end=[(520,'#44c3cc','left:-200px;bottom:-160px;opacity:.95'),(120,'#ff5959','left:150px;bottom:470px'),(64,'#01cc9e','left:320px;bottom:420px')],
  lang='fr'),
 'bcau': dict(
  fonts="""@font-face{font-family:Kompot;font-weight:400;src:url(kompotsans-webfont.woff2) format('woff2')}
@font-face{font-family:Mulish;font-weight:400;src:url(mulish-regular-webfont.woff2) format('woff2')}
@font-face{font-family:Mulish;font-weight:700;src:url(mulish-bold-webfont.woff2) format('woff2')}""",
  css="""body{font-family:Mulish,sans-serif;color:#333}
.page{background:#fbf9f5}.page.dark{background:#5353bc;color:#fff}
h1,h2,.row .n,.dom{font-family:Kompot;font-weight:400}
h1{font-size:118px;line-height:.95}h2{font-size:92px;line-height:1}
p{font-size:46px;line-height:1.35}.big{font-size:54px;line-height:1.28}
.kicker,.num,.tag,.swipe{font-weight:700}
.kicker{font-size:28px;letter-spacing:.16em;text-transform:uppercase;color:#ff6a00;margin-bottom:46px}.dark .kicker{color:#f7cf0b}
.muted{color:#6b6b72}.dark .muted{color:rgba(255,255,255,.85)}
.foot{color:#6b6b72}.dark .foot{color:rgba(255,255,255,.7)}.foot img{height:34px}.num{font-size:26px;letter-spacing:.05em}
.hl{background:linear-gradient(transparent 60%,rgba(247,207,11,.7) 60%)}.dark .hl{background:none;color:#f7cf0b}
.acc{color:#5353bc}.dark .acc{color:#f7cf0b}.row{border-radius:26px;border:2px solid #efebe3}.bar{border-left:10px solid #ff6a00;padding-left:46px}
.swipe{color:#fff}.swipe b{background:#f7cf0b}.swipe b:after{border-left:16px solid #f7cf0b}""",
  palette=['#5353bc','#ff6a00','#55dbde','#f7cf0b','#3e3e9a'],
  tagstyles={'ok':('rgba(83,83,188,.12)','#3e3e9a','#5353bc'),'ko':('rgba(255,106,0,.13)','#c45200','#ff6a00')},
  logo='logo-benjamin-chaminade.svg', logo_w='BC_logo1_simple_blanc.svg', pill=True,
  assets=['kompotsans-webfont.woff2','mulish-regular-webfont.woff2','mulish-bold-webfont.woff2','logo-benjamin-chaminade.svg','BC_logo1_simple_blanc.svg'],
  blobs_cover=[(150,'#f7cf0b','right:110px;top:120px'),(560,'#55dbde','right:-260px;bottom:-240px;opacity:.85')],
  blobs_end=[(480,'#55dbde','left:-200px;bottom:-180px;opacity:.9'),(120,'#f7cf0b','left:170px;bottom:430px'),(60,'#ff6a00','left:330px;bottom:380px')],
  lang='en'),
 'rebootlab': dict(
  fonts="""@font-face{font-family:Manrope;font-weight:400;src:url(manrope-latin-400-normal.woff2) format('woff2')}
@font-face{font-family:Manrope;font-weight:700;src:url(manrope-latin-700-normal.woff2) format('woff2')}
@font-face{font-family:Manrope;font-weight:800;src:url(manrope-latin-800-normal.woff2) format('woff2')}""",
  css="""body{font-family:Manrope,sans-serif;color:#062644}
.page{background:#F0ECEA}.page.dark{background:#062644;color:#fff}
h1,h2{font-weight:800;letter-spacing:-.025em}
h1{font-size:120px;line-height:1.0}h2{font-size:84px;line-height:1.06}
p{font-size:44px;line-height:1.36}.big{font-size:54px;line-height:1.28}
.kicker,.num,.tag,.swipe,.row .n,.dom{font-weight:800}
.kicker{font-size:28px;letter-spacing:.14em;text-transform:uppercase;color:#054FB9;margin-bottom:44px}.dark .kicker{color:#89CE00}
.muted{color:#4a5d70}.dark .muted{color:rgba(255,255,255,.82)}
.foot{color:#4a5d70}.dark .foot{color:rgba(255,255,255,.7)}.foot img{height:40px}.num{font-size:26px}
.hl{background:linear-gradient(transparent 60%,rgba(137,206,0,.55) 60%)}.dark .hl{background:none;color:#89CE00}
.acc{color:#054FB9}.dark .acc{color:#89CE00}.row{border-radius:10px}.bar{border-left:10px solid #89CE00;padding-left:46px}
.swipe b{background:#89CE00}.swipe b:after{border-left:16px solid #89CE00}
.cta{display:inline-block;background:#89CE00;color:#062644;border-radius:10px;padding:22px 34px;font-weight:800;font-size:34px}""",
  palette=['#054FB9','#89CE00','#F05322','#062644','#054FB9'],
  tagstyles={'ok':('rgba(137,206,0,.22)','#3d6b00','#89CE00'),'ko':('rgba(240,83,34,.14)','#b8381a','#F05322')},
  logo='rebootlab.svg', logo_w='rebootlab-blanc.svg', pill=False,
  assets=['manrope-latin-400-normal.woff2','manrope-latin-700-normal.woff2','manrope-latin-800-normal.woff2','rebootlab.svg','rebootlab-blanc.svg'],
  blobs_cover=[(560,'#89CE00','right:-230px;top:-210px'),(120,'#F05322','right:330px;top:300px'),(70,'#054FB9','right:220px;top:470px')],
  blobs_end=[(460,'#89CE00','left:-190px;bottom:-170px'),(100,'#F05322','left:170px;bottom:420px')],
  lang='fr'),
 'trendemic': dict(
  fonts="""@font-face{font-family:'General Sans';font-weight:400;src:url(GeneralSans-400.woff2) format('woff2')}
@font-face{font-family:'General Sans';font-weight:500;src:url(GeneralSans-500.woff2) format('woff2')}
@font-face{font-family:'General Sans';font-weight:600;src:url(GeneralSans-600.woff2) format('woff2')}
@font-face{font-family:'General Sans';font-weight:700;src:url(GeneralSans-700.woff2) format('woff2')}""",
  css="""body{font-family:'General Sans',sans-serif;color:#10333D}
.page{background:#F5F5F7}.page.dark{background:#10333D;color:#fff}
h1,h2{font-weight:600;letter-spacing:-.02em}
h1{font-size:118px;line-height:1.0}h2{font-size:84px;line-height:1.06}
p{font-size:44px;line-height:1.36;font-weight:400}.big{font-size:52px;line-height:1.28}
.kicker,.num,.tag,.swipe,.row .n,.dom{font-weight:600}
.kicker{font-size:28px;letter-spacing:.14em;text-transform:uppercase;color:#f2601f;margin-bottom:44px}.dark .kicker{color:#FF6A2B}
.muted{color:#3D5A63}.dark .muted{color:rgba(255,255,255,.8)}
.foot{color:#3D5A63}.dark .foot{color:rgba(255,255,255,.7)}.num{font-size:26px}
.wm{font-weight:600;font-size:40px;letter-spacing:-.01em;line-height:1}.wm small{display:block;font-weight:500;font-size:19px;letter-spacing:.02em;margin-top:6px;opacity:.85}
.hl{background:linear-gradient(transparent 60%,rgba(255,106,43,.35) 60%)}.dark .hl{background:none;color:#FF6A2B}
.acc{color:var(--fam,#FF6A2B)}.dark .acc{color:#FF6A2B}.row{border-radius:16px;border:1px solid rgba(16,51,61,.14)}
.bar{background:#fff;border-radius:16px;padding:40px 46px;border:1px solid rgba(16,51,61,.14)}
.swipe b{background:#FF6A2B}.swipe b:after{border-left:16px solid #FF6A2B}
.chip{display:inline-flex;align-items:center;gap:16px;border-radius:60px;padding:14px 26px;font-weight:600;font-size:28px;letter-spacing:.04em;align-self:flex-start;background:rgba(255,255,255,.12);color:#fff}
.chip i{width:20px;height:20px;border-radius:50%;background:var(--fam,#FF6A2B);display:block}""",
  palette=['var(--fam)','#FF6A2B','#3D5A63','var(--fam)','#10333D'],
  tagstyles={'ok':('rgba(61,90,99,.12)','#10333D','#3D5A63'),'ko':('rgba(255,106,43,.14)','#c2410c','#FF6A2B')},
  logo=None, logo_w=None, pill=False,
  assets=['GeneralSans-400.woff2','GeneralSans-500.woff2','GeneralSans-600.woff2','GeneralSans-700.woff2'],
  blobs_cover=[(600,'var(--fam)','right:-250px;top:-220px;opacity:.9'),(110,'#FF6A2B','right:330px;top:330px')],
  blobs_end=[(480,'var(--fam)','left:-200px;bottom:-180px;opacity:.9'),(90,'#FF6A2B','left:180px;bottom:430px')],
  lang='en'),
}


def fmt(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\[\[(.+?)\]\]', r'<span class="hl">\1</span>', t)
    t = re.sub(r'\{\{(.+?)\}\}', r'<span class="acc">\1</span>', t)
    # espaces insécables français
    t = re.sub(r' ([?!:;])', r'&nbsp;\1', t)
    t = re.sub(r'(\d) (?=\w)', r'\1&nbsp;', t)
    t = re.sub(r' (à|de|en|et|sur|of|to|than) (\d)', r' \1&nbsp;\2', t)
    t = re.sub(r'(la|le|les|du|un|une|of|the) (1re|1er|2e|2de)', r'\1&nbsp;\2', t)
    t = t.replace('« ', '«&nbsp;').replace(' »', '&nbsp;»')
    t = t.replace('\n', '<br>')
    return t


def logo_html(b, dark):
    if b['logo'] is None:
        return '<span class="wm">trendemic<small>A world of ideas for better leadership</small></span>'
    if b['pill'] and dark:
        return '<span style="background:#fff;border-radius:40px;padding:16px 28px;display:inline-flex"><img src="%s" alt="" style="height:40px"></span>' % b['logo']
    return '<img src="%s" alt="">' % (b['logo_w'] if dark else b['logo'])


def blobs(lst):
    return ''.join('<div class="blob" style="width:%dpx;height:%dpx;background:%s;%s"></div>' % (s, s, c, st) for s, c, st in lst)


def page(b, p, i, n):
    t = p['type']
    dark = t in ('cover', 'dark', 'end') or p.get('dark')
    cls = 'page dark' if dark else 'page'
    inner = ''
    if p.get('kicker'):
        inner += '<div class="kicker">%s</div>' % fmt(p['kicker'])
    if t == 'cover':
        inner = blobs(b['blobs_cover'])
        if p.get('chip'):
            inner += '<span class="chip" style="position:relative;margin-top:40px"><i></i>%s</span>' % fmt(p['chip'])
        inner += '<div style="margin-top:auto;margin-bottom:250px;position:relative">'
        inner += '<div class="kicker">%s</div><h1>%s</h1>' % (fmt(p['kicker']), fmt(p['title']))
        inner += '<p class="big muted" style="margin-top:50px;max-width:840px">%s</p></div>' % fmt(p['sub'])
        foot = '<div class="foot" style="z-index:2">%s<span class="swipe"><b></b></span></div>' % logo_html(b, True)
        return '<section class="%s" data-label="Couverture">%s%s</section>' % (cls, inner, foot)
    if t == 'end':
        inner = blobs(b['blobs_end']) + '<div style="position:relative">' + inner
        inner += '<h2>%s</h2>' % fmt(p['h2'])
        if p.get('sub'):
            inner += '<p class="big muted" style="margin-top:46px">%s</p>' % fmt(p['sub'])
        inner += '</div><div class="bottom endurl" style="position:relative"><p style="font-size:34px" class="muted">%s</p>' % fmt(p['label'])
        inner += '<p class="dom" style="font-size:50px;margin-top:10px">%s</p><p style="font-size:32px;margin-top:4px" class="muted">%s</p></div>' % (html.escape(p['domain']), html.escape(p['path']))
        foot = '<div class="foot" style="justify-content:flex-end">%s</div>' % logo_html(b, True)
        return '<section class="%s" data-label="Fin">%s%s</section>' % (cls, inner, foot)
    if t == 'tag':
        bg, fg, dot = b['tagstyles'][p.get('tone', 'ok')]
        inner += '<span class="tag" style="background:%s;color:%s"><i style="background:%s"></i>%s</span>' % (bg, fg, dot, fmt(p['tag']))
    if p.get('h2'):
        inner += '<h2 style="%s">%s</h2>' % ('margin-top:60px;' if t == 'tag' else '', fmt(p['h2']))
    if p.get('muted'):
        inner += '<p class="big muted" style="margin-top:46px">%s</p>' % fmt(p['muted'])
    for k, para in enumerate(p.get('paras', [])):
        inner += '<p style="margin-top:%dpx">%s</p>' % (60 if k == 0 else 32, fmt(para))
    if p.get('rows'):
        inner += '<div class="rows%s">' % (' dense' if len(p['rows']) >= 5 else '')
        for k, r in enumerate(p['rows']):
            col = b['palette'][k % len(b['palette'])]
            mark = ('<span class="n" style="background:%s">%d</span>' % (col, k + 1)) if p.get('numbered') else ('<span class="d" style="background:%s"></span>' % col)
            inner += '<div class="row">%s<p>%s</p></div>' % (mark, fmt(r))
        inner += '</div>'
    if p.get('note'):
        inner += '<p class="note muted">%s</p>' % fmt(p['note'])
    if p.get('bottom'):
        inner += '<div class="bottom %s"><p class="big">%s</p></div>' % ('bar' if p.get('bar', True) else '', fmt(p['bottom']))
    foot = '<div class="foot">%s<span class="num">%d/%d</span></div>' % (logo_html(b, dark), i, n)
    return '<section class="%s" data-label="Page %d">%s%s</section>' % (cls, i, inner, foot)


def build(spec, out):
    b = BRANDS[spec['brand']]
    os.makedirs(out, exist_ok=True)
    for a in b['assets']:
        shutil.copy(os.path.join(HERE, 'brands', spec['brand'], a), out)
    fam = spec.get('fam', '#2f6690')
    pages = spec['pages']
    assert len(pages) == 9, len(pages)
    body = '\n'.join(page(b, p, i + 1, len(pages)) for i, p in enumerate(pages))
    doc = '<!doctype html><html lang="%s"><head><meta charset="utf-8"><style>%s%s:root{--fam:%s}%s</style></head><body>%s</body></html>' % (
        b['lang'], b['fonts'], CSS_COMMON, fam, b['css'], body)
    doc = doc.replace('class="page', 'data-document-role="page" class="page')
    open(os.path.join(out, 'carrousel.html'), 'w').write(doc)


if __name__ == '__main__':
    build(json.load(open(sys.argv[1])), sys.argv[2])
