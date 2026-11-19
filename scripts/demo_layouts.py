"""Page templates for the demo sites that have their own layout (content/demos.py "layout").

Each layout is a complete, separate design: its own header, hero, sections, footer,
fonts and stylesheet, so no two demos share a template. The fishing charter demo
uses the original template in build_site.py.

build_site.py calls build(smp, d, h), where h carries the shared helpers.
"""

FONT_URLS = {
    "pro": "https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600;700&display=swap",
    "cafe": "https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..800;1,9..144,400..700&family=Work+Sans:wght@400;500;600;700&display=swap",
    "coastal": "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Jost:wght@300;400;500;600&display=swap",
}
FAV = {"pro": ("19b5fe", "0a1a33"), "cafe": ("d2603a", "fff6e8"), "coastal": ("16324f", "f6f1e8")}

ICONS = {
    "price": '<path d="M12 3v18M16.5 7H10a3 3 0 0 0 0 6h4a3 3 0 0 1 0 6H7"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
    "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
}


def svg(path, cls=""):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{path}</svg>')


class Ctx:
    def __init__(self, smp, d, h):
        self.smp, self.d, self.h = smp, d, h
        self.e = h.esc
        self.id = smp["id"]
        self.base = f"/work/{self.id}/"
        self.act_slug, self.act_label = d["action"]
        self.act = f"{self.base}{self.act_slug}/"
        self.links = [(pg["nav"], f'{self.base}{pg["slug"]}/') for pg in d["pages"]]
        self.tel = h.tel(smp["phone"])
        self.layout = d["layout"]

    def nav(self, cur, links=None):
        return "".join(f'<a href="{u}"{" aria-current=page" if u == cur else ""}>{self.e(n)}</a>' for n, u in (links or self.links))

    def head(self, cur, title, desc):
        e, smp = self.e, self.smp
        full = f"{title} | {smp['name']}" if title else f"{smp['name']} | {smp['kind']}"
        bg, fg = FAV[self.layout]
        fav = (f"data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='8' fill='%23{bg}'/>"
               f"<text x='16' y='22' font-family='Georgia' font-weight='700' font-size='18' fill='%23{fg}' text-anchor='middle'>{smp['name'][0]}</text></svg>")
        return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="noindex">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(full)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{self.h.absu(cur)}">
<meta property="og:image" content="{self.h.absu(f"/assets/img/samples/{self.id}-1280.webp")}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{fav}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONT_URLS[self.layout]}" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/demo-{self.id}.css">
{self.h.tracking_tags()}
</head>"""

    def credit(self):
        return f'Website by <a href="/">{self.e(self.h.NAME)}</a>'

    def form(self, ap, prefix):
        e = self.e
        out = []
        for i, (label, kind, opts) in enumerate(ap["form"]):
            fid = f"f{i}"
            if kind == "select":
                ctl = f'<select id="{fid}">' + "".join(f"<option>{e(o)}</option>" for o in opts) + "</select>"
            elif kind == "textarea":
                ctl = f'<textarea id="{fid}" rows="4"></textarea>'
            else:
                ctl = f'<input id="{fid}" type="{kind}">'
            wide = " wide" if kind == "textarea" else ""
            out.append(f'<div class="{prefix}-field{wide}"><label for="{fid}">{e(label)}</label>{ctl}</div>')
        return (f'<form class="{prefix}-form" data-demo>{"".join(out)}<div class="{prefix}-field wide">'
                f'<button class="{prefix}-btn" type="submit">{e(ap["button"])}</button>'
                f'<p class="d-status {prefix}-status" role="status" aria-live="polite"></p></div></form>')

    def write(self, slug, html):
        self.h.write(f"{self.base}{slug}/" if slug else self.base, html)


def leader_rows(cols, rows, e):
    """Menu-board rows for the cafe layout: name, dotted leader, price(s)."""
    hours = len(cols) > 1 and cols[1].lower() == "open"
    out = []
    for r in rows:
        vals = [v for v in r[1:] if v and v != "-"]
        price = " to ".join(vals) if hours else " / ".join(vals)
        out.append(f'<li><span class="cf-item"><b>{e(r[0])}</b></span><span class="cf-dots"></span><span class="cf-price">{e(price)}</span></li>')
    note = ""
    if not hours and len([c for c in cols[1:] if c]) > 1:
        note = f'<p class="cf-colnote">{e(" / ".join(c for c in cols[1:] if c))}</p>'
    return note, "".join(out)


# ===================================================================== A/C company: "pro"

SNOW = '<path d="M12 2v20M3.3 7l17.4 10M20.7 7L3.3 17M9 3.5l3 2.5 3-2.5M9 20.5l3-2.5 3 2.5"/>'


def pro_block(c, b):
    e, smp = c.e, c.smp
    kind, heading = b[0], b[1]
    if kind == "cards":
        items = b[2] or smp["cards"]
        link = c.links[0][1] if b[2] is None else None
        tiles = ""
        for n, (t, dsc, pr) in enumerate(items, 1):
            inner = f'<span class="hv-num">0{n}</span><h3>{e(t)}</h3><p>{e(dsc)}</p><span class="hv-go">{e(pr)} <i aria-hidden="true">&rarr;</i></span>'
            tiles += f'<a class="hv-tile" href="{link}">{inner}</a>' if link else f'<div class="hv-tile">{inner}</div>'
        return f'<section class="hv-sec hv-ice"><div class="hv-in"><p class="hv-eye">Services</p><h2>{e(heading)}</h2><div class="hv-tiles">{tiles}</div></div></section>'
    if kind == "features":
        icons = list(ICONS.values())
        feats = "".join(f'<div class="hv-feat"><span class="hv-ico">{svg(icons[n % 3])}</span><h3>{e(t)}</h3><p>{e(dsc)}</p></div>' for n, (t, dsc) in enumerate(b[2]))
        return f'<section class="hv-sec hv-dark"><div class="hv-in"><h2>{e(heading)}</h2><div class="hv-feats">{feats}</div></div></section>'
    if kind == "list":
        items = "".join(f"<li>{e(x)}</li>" for x in b[2])
        return (f'<section class="hv-sec"><div class="hv-in hv-split"><div><h2>{e(heading)}</h2><ul class="hv-checks">{items}</ul></div>'
                f'<aside class="hv-callcard"><p class="hv-eye">Not sure what\'s wrong?</p><a class="hv-bigphone" href="{c.tel}">{e(smp["phone"])}</a>'
                f'<p>Talk to a real person, 7 days a week.</p></aside></div></section>')
    if kind == "table":
        cols = "".join(f'<th scope="col">{e(x)}</th>' for x in b[2])
        rows = "".join("<tr>" + "".join((f'<th scope="row">{e(x)}</th>' if i == 0 else f"<td>{e(x)}</td>") for i, x in enumerate(r)) + "</tr>" for r in b[3])
        return f'<section class="hv-sec"><div class="hv-in"><h2>{e(heading)}</h2><div class="hv-table"><table><thead><tr>{cols}</tr></thead><tbody>{rows}</tbody></table></div></div></section>'
    if kind == "text":
        paras = "".join(f"<p>{e(x)}</p>" for x in b[2])
        return f'<section class="hv-sec hv-tight"><div class="hv-in"><div class="hv-note"><h2>{e(heading)}</h2>{paras}</div></div></section>'
    if kind == "faq":
        items = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in b[2])
        return f'<section class="hv-sec"><div class="hv-in"><h2>{e(heading)}</h2><div class="hv-faq">{items}</div></div></section>'
    raise SystemExit(kind)


def pro_page(c, cur, title, desc, body):
    e, smp, d = c.e, c.smp, c.d
    return f"""{c.head(cur, title, desc)}
<body class="hv">
<div class="hv-strip"><div class="hv-in"><span>{e(d["hours"])}</span><a href="{c.tel}">Emergency? <b>{e(smp["phone"])}</b></a></div></div>
<header class="hv-head"><div class="hv-in hv-head-in">
  <a class="hv-logo" href="{c.base}"><span class="hv-mark">{svg(SNOW)}</span><span><b>{e(smp["name"])}</b><small>{e(d["logo_sub"])}</small></span></a>
  <nav class="hv-nav" aria-label="Main">{c.nav(cur)}<a href="{c.act}"{" aria-current=page" if cur == c.act else ""}>{e(c.act_label)}</a></nav>
  <a class="hv-callbox" href="{c.tel}"><small>Call 7 days</small><b>{e(smp["phone"])}</b></a>
  <details class="hv-menu"><summary aria-label="Menu"><i></i><i></i><i></i></summary><nav aria-label="Menu">{c.nav(cur)}<a href="{c.act}">{e(c.act_label)}</a></nav></details>
</div></header>
<main>
{body}
<section class="hv-cta"><div class="hv-in"><h2>{e(d["band"])}</h2><div><a class="hv-bigphone" href="{c.tel}">{e(smp["phone"])}</a><a class="hv-btn hv-btn-dark" href="{c.act}">{e(c.act_label)}</a></div></div></section>
</main>
<footer class="hv-foot"><div class="hv-in hv-foot-grid">
  <div><p class="hv-logo"><span class="hv-mark">{svg(SNOW)}</span><span><b>{e(smp["name"])}</b><small>{e(d["logo_sub"])}</small></span></p><p>{e(d["tagline"])}</p></div>
  <div><h2>Call or email</h2><p><a href="{c.tel}">{e(smp["phone"])}</a><br><a href="mailto:{e(d["email"])}">{e(d["email"])}</a></p></div>
  <div><h2>Service area</h2><p>{e(d["area"])}</p></div>
  <div><h2>Services</h2><ul>{"".join(f'<li><a href="{u}">{e(n)}</a></li>' for n, u in c.links)}<li><a href="{c.act}">{e(c.act_label)}</a></li></ul></div>
</div><p class="hv-in hv-credit">{c.credit()}</p></footer>
<div class="hv-mbar"><a href="{c.tel}">Call now</a><a href="{c.act}">{e(c.act_label)}</a></div>
<script src="/assets/js/demo.js" defer></script>
</body>
</html>
"""


def pro_build(c):
    e, smp, d, h = c.e, c.smp, c.d, c.h
    hero = f"""<section class="hv-hero"><div class="hv-in hv-hero-in">
  <div class="hv-hero-copy"><p class="hv-pill"><i></i>Techs out today across Lee County</p><h1>{e(smp["headline"])}</h1><p class="hv-sub">{e(smp["sub"])}</p>
  <p class="hv-acts"><a class="hv-btn" href="{c.act}">{e(c.act_label)}</a><a class="hv-btn hv-btn-ghost" href="{c.tel}">Call {e(smp["phone"])}</a></p>
  <ul class="hv-trust"><li>Licensed and insured</li><li>Upfront prices</li><li>All major brands</li></ul></div>
  <div class="hv-hero-img">{h.photo(c.id, "", sizes="(max-width: 860px) 100vw, 50vw", eager=True, cls="hv-img")}<p class="hv-badge"><b>Same day</b>when you call before noon</p></div>
</div></section>"""
    c.write("", pro_page(c, c.base, "", smp["sub"], hero + "".join(pro_block(c, b) for b in d["home"])))
    for pg in d["pages"]:
        cur = f'{c.base}{pg["slug"]}/'
        top = f'<section class="hv-top"><div class="hv-in"><p class="hv-crumbs"><a href="{c.base}">Home</a> / {e(pg["title"])}</p><h1>{e(pg["title"])}</h1><p>{e(pg["intro"])}</p></div></section>'
        c.write(pg["slug"], pro_page(c, cur, pg["title"], pg["intro"], top + "".join(pro_block(c, b) for b in pg["blocks"])))
    ap = d["action_page"]
    top = f'<section class="hv-top"><div class="hv-in"><p class="hv-crumbs"><a href="{c.base}">Home</a> / {e(ap["title"])}</p><h1>{e(ap["title"])}</h1><p>{e(ap["intro"])}</p></div></section>'
    side = (f'<aside class="hv-callcard"><p class="hv-eye">Faster by phone</p><a class="hv-bigphone" href="{c.tel}">{e(smp["phone"])}</a>'
            f'<p>{e(d["hours"])}</p><p><a href="mailto:{e(d["email"])}">{e(d["email"])}</a></p></aside>')
    body = top + f'<section class="hv-sec"><div class="hv-in hv-formwrap">{c.form(ap, "hv")}{side}</div></section>'
    c.write(c.act_slug, pro_page(c, c.act, ap["title"], ap["intro"], body))


# ===================================================================== Coffee shop: "cafe"

WAVE = ('<svg class="cf-wave" viewBox="0 0 1440 60" preserveAspectRatio="none" aria-hidden="true">'
        '<path d="M0 30 C 120 0 240 60 360 30 S 600 0 720 30 960 60 1080 30 1320 0 1440 30 V60 H0Z"/></svg>')
SQUIGGLE = ('<svg class="cf-squig" viewBox="0 0 120 12" aria-hidden="true"><path d="M2 6 Q 12 0 22 6 T 42 6 T 62 6 T 82 6 T 102 6 T 118 6" '
            'fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>')


def cafe_block(c, b):
    e, smp = c.e, c.smp
    kind, heading = b[0], b[1]
    if kind == "cards":
        items = b[2] or smp["cards"]
        rows = "".join(f'<li><span class="cf-item"><b>{e(t)}</b><small>{e(dsc)}</small></span><span class="cf-dots"></span><span class="cf-price">{e(pr)}</span></li>' for t, dsc, pr in items)
        more = f'<p class="cf-more"><a href="{c.links[0][1]}">Full menu &rarr;</a></p>' if b[2] is None else ""
        return f'<section class="cf-sec"><div class="cf-in"><div class="cf-board"><h2>{e(heading)}</h2><ul class="cf-leaders">{rows}</ul>{more}</div></div></section>'
    if kind == "features":
        blobs = "".join(f'<div class="cf-blob cf-blob-{n}"><h3>{e(t)}</h3><p>{e(dsc)}</p></div>' for n, (t, dsc) in enumerate(b[2]))
        return f'<section class="cf-sec"><div class="cf-in"><h2 class="cf-center">{e(heading)}</h2>{SQUIGGLE}<div class="cf-blobs">{blobs}</div></div></section>'
    if kind == "list":
        items = "".join(f"<li>{e(x)}</li>" for x in b[2])
        return f'<section class="cf-sec"><div class="cf-in cf-center-wrap"><h2>{e(heading)}</h2><ul class="cf-chips">{items}</ul></div></section>'
    if kind == "table":
        note, rows = leader_rows(b[2], b[3], e)
        return f'<section class="cf-sec"><div class="cf-in"><div class="cf-board cf-board-light"><h2>{e(heading)}</h2>{note}<ul class="cf-leaders">{rows}</ul></div></div></section>'
    if kind == "text":
        paras = "".join(f"<p>{e(x)}</p>" for x in b[2])
        return f'<section class="cf-sec"><div class="cf-in"><div class="cf-text"><h2>{e(heading)}</h2>{paras}</div></div></section>'
    if kind == "faq":
        items = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in b[2])
        return f'<section class="cf-sec"><div class="cf-in"><h2>{e(heading)}</h2><div class="cf-faq">{items}</div></div></section>'
    raise SystemExit(kind)


def cafe_page(c, cur, title, desc, body):
    e, smp, d = c.e, c.smp, c.d
    left, right = c.links[:2], c.links[2:]
    pill = f'<a class="cf-pill" href="{c.act}">{e(c.act_label)}</a>'
    return f"""{c.head(cur, title, desc)}
<body class="cf">
<p class="cf-ribbon">{e(d["ribbon"])}</p>
<header class="cf-head"><div class="cf-in cf-head-in">
  <nav class="cf-nav cf-nav-l" aria-label="Main">{c.nav(cur, left)}</nav>
  <a class="cf-logo" href="{c.base}"><span class="cf-logo-name">{e(d["logo_name"])}</span><span class="cf-logo-sub">{e(d["logo_sub"])}</span></a>
  <nav class="cf-nav cf-nav-r" aria-label="More">{c.nav(cur, right)}{pill}</nav>
  <details class="cf-menu"><summary aria-label="Menu"><i></i><i></i></summary><nav aria-label="Menu">{c.nav(cur)}{pill}</nav></details>
</div></header>
<main>
{body}
<section class="cf-band"><div class="cf-in"><p class="cf-script">See you soon.</p><p>{e(d["hours"])}</p><p><a class="cf-btn cf-btn-light" href="{c.act}">{e(c.act_label)}</a></p></div></section>
</main>
<footer class="cf-foot"><div class="cf-in cf-foot-grid">
  <div><p class="cf-logo cf-logo-foot"><span class="cf-logo-name">{e(d["logo_name"])}</span><span class="cf-logo-sub">{e(d["logo_sub"])}</span></p></div>
  <div><h2>Hours</h2><p>{e(d["hours"])}</p></div>
  <div><h2>Find us</h2><p>{e(d["area"])}</p></div>
  <div><h2>Say hi</h2><p><a href="{c.tel}">{e(smp["phone"])}</a><br><a href="mailto:{e(d["email"])}">{e(d["email"])}</a></p></div>
</div><p class="cf-in cf-credit">{c.credit()}</p></footer>
<script src="/assets/js/demo.js" defer></script>
</body>
</html>
"""


def cafe_build(c):
    e, smp, d, h = c.e, c.smp, c.d, c.h
    hero = f"""<section class="cf-hero"><div class="cf-in cf-hero-in">
  <div class="cf-hero-copy"><p class="cf-kick">{e(smp["kicker"])}</p><h1>{d["headline_html"]}</h1><p class="cf-sub">{e(smp["sub"])}</p>
  <p class="cf-acts"><a class="cf-btn" href="{c.links[0][1]}">{e(smp["cta"])}</a><a class="cf-link" href="{c.act}">{e(c.act_label)} &rarr;</a></p></div>
  <div class="cf-arch">{h.photo(c.id, "", sizes="(max-width: 860px) 90vw, 42vw", eager=True, cls="cf-img")}<span class="cf-sticker">Baked<br>daily</span></div>
</div>{WAVE}</section>"""
    c.write("", cafe_page(c, c.base, "", smp["sub"], hero + "".join(cafe_block(c, b) for b in d["home"])))
    for pg in d["pages"]:
        cur = f'{c.base}{pg["slug"]}/'
        top = f'<section class="cf-top"><div class="cf-in"><p class="cf-kick">{e(d["logo_name"])}</p><h1>{e(pg["title"])}</h1>{SQUIGGLE}<p>{e(pg["intro"])}</p></div></section>'
        c.write(pg["slug"], cafe_page(c, cur, pg["title"], pg["intro"], top + "".join(cafe_block(c, b) for b in pg["blocks"])))
    ap = d["action_page"]
    top = f'<section class="cf-top"><div class="cf-in"><p class="cf-kick">{e(d["logo_name"])}</p><h1>{e(ap["title"])}</h1>{SQUIGGLE}<p>{e(ap["intro"])}</p></div></section>'
    slip = f'<div class="cf-slip"><p class="cf-slip-head">Order slip</p>{c.form(ap, "cf")}</div>'
    side = f'<aside class="cf-side"><h2>Pick up at the counter</h2><p>{e(d["hours"])}</p><p>Questions? <a href="{c.tel}">{e(smp["phone"])}</a></p></aside>'
    c.write(c.act_slug, cafe_page(c, c.act, ap["title"], ap["intro"], top + f'<section class="cf-sec"><div class="cf-in cf-formwrap">{slip}{side}</div></section>'))


# ===================================================================== Beach cottages: "coastal"

ROMAN = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii"]


def coastal_block(c, b):
    e, smp = c.e, c.smp
    kind, heading = b[0], b[1]
    if kind == "cards":
        items = b[2] or smp["cards"]
        cots = "".join(f'<article class="ct-cot ct-cot-{n % 4}"><p class="ct-no">No. {n + 1}</p><h3>{e(t)}</h3><p>{e(dsc)}</p><p class="ct-price">{e(pr)}</p></article>' for n, (t, dsc, pr) in enumerate(items))
        more = f'<p class="ct-more"><a href="{c.links[0][1]}">View the cottages</a></p>' if b[2] is None else ""
        return f'<section class="ct-sec"><div class="ct-in"><p class="ct-kick ct-center">Stay with us</p><h2 class="ct-center">{e(heading)}</h2><div class="ct-cots">{cots}</div>{more}</div></section>'
    if kind == "features":
        cols = "".join(f'<div><h3>{e(t)}</h3><p>{e(dsc)}</p></div>' for t, dsc in b[2])
        return f'<section class="ct-sec ct-white"><div class="ct-in"><h2 class="ct-center">{e(heading)}</h2><div class="ct-cols">{cols}</div></div></section>'
    if kind == "list":
        items = "".join(f'<li><span>{ROMAN[n]}.</span>{e(x)}</li>' for n, x in enumerate(b[2]))
        return f'<section class="ct-sec"><div class="ct-in ct-split"><div><p class="ct-kick">Around the island</p><h2>{e(heading)}</h2></div><ol class="ct-roman">{items}</ol></div></section>'
    if kind == "table":
        cols = "".join(f'<th scope="col">{e(x)}</th>' for x in b[2])
        rows = "".join("<tr>" + "".join((f'<th scope="row">{e(x)}</th>' if i == 0 else f"<td>{e(x)}</td>") for i, x in enumerate(r)) + "</tr>" for r in b[3])
        return f'<section class="ct-sec"><div class="ct-in"><h2 class="ct-center">{e(heading)}</h2><div class="ct-table"><table><thead><tr>{cols}</tr></thead><tbody>{rows}</tbody></table></div></div></section>'
    if kind == "text":
        paras = "".join(f"<p>{e(x)}</p>" for x in b[2])
        return f'<section class="ct-sec"><div class="ct-in ct-text"><h2>{e(heading)}</h2>{paras}</div></section>'
    if kind == "faq":
        items = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in b[2])
        return f'<section class="ct-sec ct-white"><div class="ct-in"><h2 class="ct-center">{e(heading)}</h2><div class="ct-faq">{items}</div></div></section>'
    raise SystemExit(kind)


def coastal_page(c, cur, title, desc, body, over=False):
    e, smp, d = c.e, c.smp, c.d
    return f"""{c.head(cur, title, desc)}
<body class="ct">
<header class="ct-head{" ct-over" if over else ""}"><div class="ct-in ct-head-in">
  <nav class="ct-nav" aria-label="Main">{c.nav(cur)}</nav>
  <a class="ct-logo" href="{c.base}"><span>{e(d["logo_name"])}</span><small>{e(d["logo_sub"])}</small></a>
  <a class="ct-book" href="{c.act}">{e(c.act_label)}</a>
  <details class="ct-menu"><summary aria-label="Menu"><i></i><i></i></summary><nav aria-label="Menu">{c.nav(cur)}<a href="{c.act}">{e(c.act_label)}</a></nav></details>
</div></header>
<main>
{body}
<section class="ct-band"><div class="ct-in"><p class="ct-kick">Plan your stay</p><h2>{e(d["tagline"])}</h2><p><a class="ct-btn" href="{c.act}">{e(c.act_label)}</a></p></div></section>
</main>
<footer class="ct-foot"><div class="ct-in">
  <p class="ct-logo ct-logo-foot"><span>{e(d["logo_name"])}</span><small>{e(d["logo_sub"])}</small></p>
  <nav class="ct-foot-nav" aria-label="Footer">{c.nav(cur)}<a href="{c.act}">{e(c.act_label)}</a></nav>
  <p>{e(d["area"])}</p>
  <p><a href="{c.tel}">{e(smp["phone"])}</a> &nbsp;&middot;&nbsp; <a href="mailto:{e(d["email"])}">{e(d["email"])}</a></p>
  <p>{e(d["hours"])}</p>
  <p class="ct-credit">{c.credit()}</p>
</div></footer>
<a class="ct-mbook" href="{c.act}">{e(c.act_label)}</a>
<script src="/assets/js/demo.js" defer></script>
</body>
</html>
"""


def coastal_build(c):
    e, smp, d, h = c.e, c.smp, c.d, c.h
    guests = "".join(f"<option>{n} guest{'s' if n > 1 else ''}</option>" for n in range(1, 7))
    hero = f"""<section class="ct-hero">{h.photo(c.id, "", sizes="100vw", eager=True, cls="ct-hero-img")}
  <div class="ct-hero-copy"><p class="ct-kick">{e(smp["kicker"])}</p><h1>{e(smp["headline"])}</h1><p>{e(smp["sub"])}</p></div>
</section>
<form class="ct-bookbar" action="{c.act}" method="get">
  <label>Arrival<input type="date"></label><label>Departure<input type="date"></label>
  <label>Guests<select>{guests}</select></label><button type="submit">{e(c.act_label)}</button>
</form>"""
    c.write("", coastal_page(c, c.base, "", smp["sub"], hero + "".join(coastal_block(c, b) for b in d["home"]), over=True))

    def top(t, intro):
        return (f'<section class="ct-top"><div class="ct-top-copy"><p class="ct-kick">{e(d["logo_name"])}</p><h1>{e(t)}</h1><p>{e(intro)}</p></div>'
                f'<div class="ct-top-img">{h.photo(c.id, "", sizes="(max-width: 860px) 100vw, 50vw", cls="ct-img")}</div></section>')
    for pg in d["pages"]:
        cur = f'{c.base}{pg["slug"]}/'
        c.write(pg["slug"], coastal_page(c, cur, pg["title"], pg["intro"], top(pg["title"], pg["intro"]) + "".join(coastal_block(c, b) for b in pg["blocks"])))
    ap = d["action_page"]
    side = f'<aside class="ct-side"><p class="ct-kick">Prefer to talk?</p><p><a href="{c.tel}">{e(smp["phone"])}</a></p><p>{e(d["hours"])}</p></aside>'
    body = top(ap["title"], ap["intro"]) + f'<section class="ct-sec"><div class="ct-in ct-formwrap">{c.form(ap, "ct")}{side}</div></section>'
    c.write(c.act_slug, coastal_page(c, c.act, ap["title"], ap["intro"], body))


BUILDERS = {"pro": pro_build, "cafe": cafe_build, "coastal": coastal_build}


def build(smp, d, h):
    BUILDERS[d["layout"]](Ctx(smp, d, h))
