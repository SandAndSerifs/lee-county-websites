"""Build every page of the Lee County Websites site from content/ and site.config.json.

Usage:  python3 scripts/build_site.py

Writes into public/:
  index.html                       home page
  services/, areas/, blog/         hubs plus one page per entry
  pricing/, contact/, privacy/, 404.html
  sitemap.xml, robots.txt, llms.txt

No dependencies beyond Python 3. Safe to run again: every output is rebuilt.
"""
import datetime
import hashlib
import html
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
sys.path.insert(0, str(ROOT / "content"))

from services import SERVICES  # noqa: E402
from areas import AREAS  # noqa: E402
from blog import POSTS  # noqa: E402
from samples import SAMPLES  # noqa: E402

CFG = json.loads((ROOT / "site.config.json").read_text(encoding="utf-8"))
SITE = CFG["site_url"].rstrip("/")
NAME = CFG["business_name"]
OWNER = CFG["owner_name"]
TODAY = datetime.date.today().isoformat()
PRIVACY_UPDATED = "2026-11-15"  # change by hand when the privacy wording changes
BIZ_ID = SITE + "/#business"
OG_IMAGE = "/assets/og/lee-county-websites.png"
LOGO = "/assets/img/logo-512.png"

SVC = {s["slug"]: s for s in SERVICES}
AREA = {a["slug"]: a for a in AREAS}
POST = {p["slug"]: p for p in POSTS}
POSTS.sort(key=lambda p: p["date"], reverse=True)

# Town pages that use a sample photo as their header image.
AREA_PHOTO = {"fort-myers-fl": "coffee", "cape-coral-fl": "charter", "fort-myers-beach-fl": "cottage", "lehigh-acres-fl": "hvac"}

esc = lambda s: html.escape(str(s), quote=True)  # noqa: E731


def absu(path):
    return SITE + path


def fmt_date(iso):
    return datetime.date.fromisoformat(iso).strftime("%B %-d, %Y")


def _git(*args):
    try:
        return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None


_ASSET_V = re.compile(rb"\?v=[0-9a-f]+")


def page_date(path):
    """Date a built page last really changed, from git. Cache-tag-only changes don't count."""
    rel = str(pathlib.Path(path).resolve().relative_to(ROOT))
    now = _ASSET_V.sub(b"", pathlib.Path(path).read_bytes())
    log = _git("log", "--format=%H %cs", "--", rel)
    if not log:
        return TODAY
    date = None
    for line in log.decode().split("\n"):
        if not line.strip():
            continue
        sha, d = line.split()
        old = _git("show", f"{sha}:{rel}")
        if old is None or _ASSET_V.sub(b"", old) != now:
            break
        date = d
    return date or TODAY


# ------------------------------------------------------------------ icons and art

ICONS = {
    "browser": '<rect x="6" y="10" width="52" height="40" rx="4"/><path d="M6 20h52"/><circle cx="13" cy="15" r="1.6"/><circle cx="19" cy="15" r="1.6"/><path d="M14 30h20M14 37h28M14 44h14"/>',
    "refresh": '<path d="M50 24a20 20 0 0 0-36-4"/><path d="M12 12v9h9"/><path d="M14 40a20 20 0 0 0 36 4"/><path d="M52 52v-9h-9"/>',
    "pin": '<path d="M32 56s18-17 18-30a18 18 0 0 0-36 0c0 13 18 30 18 30z"/><circle cx="32" cy="26" r="7"/>',
    "spark": '<path d="M32 6l6 18 18 8-18 8-6 18-6-18-18-8 18-8z"/>',
    "print": '<path d="M18 24V8h28v16"/><rect x="8" y="24" width="48" height="20" rx="3"/><path d="M18 38h28v18H18z"/>',
    "shield": '<path d="M32 6l20 8v14c0 14-9 23-20 28C21 51 12 42 12 28V14z"/><path d="M23 31l6 6 12-13"/>',
    "wave": '<path d="M6 24c6-6 12-6 18 0s12 6 18 0 12-6 18 0"/><path d="M6 36c6-6 12-6 18 0s12 6 18 0 12-6 18 0"/><path d="M6 48c6-6 12-6 18 0s12 6 18 0 12-6 18 0"/>',
    "check": '<path d="M12 33l12 12 28-28"/>',
    "chat": '<path d="M10 14h44v28H30l-12 10V42h-8z"/>',
    "doc": '<path d="M16 6h22l12 12v40H16z"/><path d="M38 6v12h12M23 32h18M23 40h18M23 48h12"/>',
    "rocket": '<path d="M32 6c10 8 14 20 12 32H20C18 26 22 14 32 6z"/><circle cx="32" cy="24" r="5"/><path d="M20 38l-8 10h12M44 38l8 10H40M27 46l5 10 5-10"/>',
}


def icon(name, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 64 64" aria-hidden="true">{ICONS[name]}</svg>'


def art(hue, label, icon_name="wave", small="", cls=""):
    """A capsule image drawn in CSS: gradient by hue, big label, faint icon."""
    return (f'<div class="art {cls}" style="--h:{hue}" aria-hidden="true">{icon(icon_name, "art-ic")}'
            f'<span class="art-small">{esc(small)}</span><span class="art-label">{esc(label)}</span></div>')


def photo(sample_id, alt, sizes="(max-width: 900px) 100vw, 60vw", eager=False, cls=""):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img class="{cls}" src="/assets/img/samples/{sample_id}-1280.webp" '
            f'srcset="/assets/img/samples/{sample_id}-640.webp 640w, /assets/img/samples/{sample_id}-1280.webp 1280w" '
            f'sizes="{sizes}" width="1280" height="720" alt="{esc(alt)}" {load} decoding="async">')


LOGO_MARK = ('<svg class="mark" viewBox="0 0 64 64" aria-hidden="true"><defs><linearGradient id="LGID" x1="0" y1="0" x2="1" y2="1">'
             '<stop offset="0" stop-color="#ffb35e"/><stop offset="1" stop-color="#ef5a3a"/></linearGradient></defs>'
             '<rect width="64" height="64" rx="14" fill="url(#LGID)"/>'
             '<path d="M18 34a14 14 0 0 1 28 0z" fill="#fff"/>'
             '<path d="M12 41c5-4 10-4 15 0s10 4 15 0 10-4 10-2" stroke="#fff" stroke-width="3.6" fill="none" stroke-linecap="round"/>'
             '<path d="M12 50c5-4 10-4 15 0s10 4 15 0 10-4 10-2" stroke="#fff" stroke-opacity=".6" stroke-width="3.6" fill="none" stroke-linecap="round"/></svg>')


def logo_link(gid="lg"):
    return (f'<a class="brand" href="/" aria-label="{esc(NAME)} home">{LOGO_MARK.replace("LGID", gid)}'
            '<span class="brand-text"><span class="brand-top">Lee County</span><span class="brand-main">Websites</span></span></a>')


# ------------------------------------------------------------------ head

def gtm_id():
    gid = CFG.get("gtm_container_id", "").strip()
    return gid if re.fullmatch(r"GTM-[A-Z0-9]+", gid) else ""


def tracking_tags():
    out = []
    if CFG.get("gsc_verification"):
        out.append(f'<meta name="google-site-verification" content="{esc(CFG["gsc_verification"])}">')
    gid = gtm_id()
    if gid:
        out.append("<!-- Google Tag Manager -->\n<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\n"
                   "new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],\n"
                   "j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n"
                   "'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\n"
                   f"}})(window,document,'script','dataLayer','{gid}');</script>\n<!-- End Google Tag Manager -->")
    else:
        out.append("<!-- Google Tag Manager: add a container ID (GTM-...) to site.config.json and rebuild. -->")
    return "\n".join(out)


def gtm_noscript():
    gid = gtm_id()
    if not gid:
        return ""
    return (f'<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={gid}" height="0" width="0" '
            'style="display:none;visibility:hidden"></iframe></noscript>')


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + "</script>"


LEE = {"@type": "AdministrativeArea", "name": "Lee County, Florida"}


def founder_ld():
    p = {"@type": "Person", "@id": SITE + "/#founder", "name": CFG.get("owner_full_name") or OWNER,
         "jobTitle": "Web and graphic designer", "url": SITE + "/#about", "worksFor": {"@id": BIZ_ID}}
    if CFG.get("owner_photo"):
        p["image"] = absu(CFG["owner_photo"])
    if CFG.get("owner_profiles"):
        p["sameAs"] = CFG["owner_profiles"]
    return p


def business_ld():
    obj = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "@id": BIZ_ID,
        "name": NAME,
        "url": SITE + "/",
        "image": absu(OG_IMAGE),
        "logo": {"@type": "ImageObject", "url": absu(LOGO), "width": 512, "height": 512},
        "description": "Web design for small businesses in Fort Myers, Cape Coral and the rest of Lee County, Florida: fast, mobile-first websites at fixed prices, plus local SEO, branding and print.",
        "areaServed": [LEE] + [{"@type": "City", "name": a["town"], "containedInPlace": LEE} for a in AREAS],
        "founder": founder_ld(),
        "knowsAbout": ["Web design", "Website redesign", "Local SEO", "Google Business Profile", "Logo design", "Print design"],
        "priceRange": "$500 to $1,500+",
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Website packages",
            "itemListElement": [
                {"@type": "Offer", "name": "Starter website (one page)", "price": "500", "priceCurrency": "USD",
                 "itemOffered": {"@type": "Service", "name": "Starter website"}},
                {"@type": "Offer", "name": "Business website (up to five pages)", "price": "1500", "priceCurrency": "USD",
                 "itemOffered": {"@type": "Service", "name": "Business website"}},
            ],
        },
    }
    if CFG.get("email"):
        obj["email"] = CFG["email"]
    if CFG.get("phone"):
        obj["telephone"] = CFG["phone"]
    if CFG.get("parent_url"):
        obj["parentOrganization"] = {"@type": "Organization", "name": CFG.get("parent_brand", ""), "url": CFG["parent_url"]}
    return obj


def website_ld():
    return {"@context": "https://schema.org", "@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/",
            "name": NAME, "publisher": {"@id": BIZ_ID}}


def crumbs_ld(trail):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": absu(u)} for i, (n, u) in enumerate(trail)]}


def faq_ld(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}


FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,400..800&family=Figtree:ital,wght@0,400..800;1,400&display=swap" rel="stylesheet">')


def head(title, desc, path, lds=(), og_type="website", noindex=False, image=None):
    full = title if NAME in title else f"{title} | {NAME}"
    img = absu(image or OG_IMAGE)
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full)}</title>
<meta name="description" content="{esc(desc)}">
{robots}<link rel="canonical" href="{absu(path)}">
<meta name="theme-color" content="#0a1d1d">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{esc(NAME)}">
<meta property="og:title" content="{esc(full)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{absu(path)}">
<meta property="og:image" content="{img}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">
{FONTS}
<link rel="stylesheet" href="/assets/css/styles.css">
{tracking_tags()}
{"".join(ld(x) for x in lds)}
</head>"""


# ------------------------------------------------------------------ chrome

NAV = [("Services", "/services/"), ("Towns", "/areas/"), ("Pricing", "/pricing/"), ("Blog", "/blog/")]
STORE_NAV = [("Featured", "/#featured"), ("New sites", "/services/small-business-website-design/"),
             ("Redesigns", "/services/website-redesign/"), ("Local SEO", "/services/local-seo/"),
             ("Branding", "/services/logo-and-branding/"), ("Print", "/services/print-design/"),
             ("Care plans", "/services/website-care-plans/")]


def finder_options():
    opts = [(a["place"], f"/areas/{a['slug']}/") for a in AREAS]
    opts += [(s["name"], f"/services/{s['slug']}/") for s in SERVICES]
    opts += [("Pricing", "/pricing/"), ("Blog", "/blog/"), ("Contact", "/contact/")]
    return opts


def header(active=""):
    links = "".join(f'<a href="{u}"{" aria-current=page" if active == u else ""}>{n}</a>' for n, u in NAV)
    store = "".join(f'<a href="{u}">{n}</a>' for n, u in STORE_NAV)
    opts = "".join(f'<option value="{esc(n)}" data-url="{u}"></option>' for n, u in finder_options())
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="gh">
  <div class="gh-in wrap">
    {logo_link()}
    <nav class="gh-nav" id="gh-nav" aria-label="Main">{links}</nav>
    <a class="btn btn-go gh-cta" href="/contact/">Contact</a>
    <button class="gh-menu" type="button" aria-expanded="false" aria-controls="gh-nav" aria-label="Menu"><span></span><span></span><span></span></button>
  </div>
</header>
<div class="sn wrap">
  <nav class="sn-bar" aria-label="Browse services">
    <div class="sn-links">{store}</div>
    <form class="finder" role="search" action="/areas/">
      <label class="sr" for="finder-in">Find your town or a service</label>
      <input id="finder-in" type="search" list="finder-list" placeholder="Find your town or a service" autocomplete="off">
      <datalist id="finder-list">{opts}</datalist>
      <button type="submit" aria-label="Go"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21"/></svg></button>
    </form>
  </nav>
</div>"""


def footer():
    svc = "".join(f'<li><a href="/services/{s["slug"]}/">{esc(s["name"])}</a></li>' for s in SERVICES)
    towns = "".join(f'<li><a href="/areas/{a["slug"]}/">{esc(a["place"])}</a></li>' for a in AREAS)
    parent = ""
    if CFG.get("parent_url"):
        parent = f' A site by {esc(OWNER)} of <a href="{esc(CFG["parent_url"])}">{esc(CFG["parent_brand"])}</a>.'
    mail = f'<li><a href="mailto:{esc(CFG["email"])}">{esc(CFG["email"])}</a></li>' if CFG.get("email") else ""
    return f"""<footer class="ft">
  <div class="wrap ft-grid">
    <div class="ft-brand">{logo_link("lg-ft")}<p>Fixed-price websites for small businesses in Fort Myers, Cape Coral and across Lee County, Florida.</p></div>
    <div><h2>Services</h2><ul>{svc}</ul></div>
    <div><h2>Towns</h2><ul>{towns}</ul></div>
    <div><h2>Company</h2><ul><li><a href="/pricing/">Pricing</a></li><li><a href="/blog/">Blog</a></li><li><a href="/#about">About</a></li><li><a href="/contact/">Contact</a></li>{mail}<li><a href="/privacy/">Privacy</a></li></ul></div>
  </div>
  <div class="wrap ft-base"><p>&copy; <span id="year">2026</span> {esc(NAME)}.{parent}</p></div>
</footer>"""


def page(head_html, body, active=""):
    return (f'{head_html}\n<body>\n{gtm_noscript()}\n{header(active)}\n<main id="main">\n{body}\n</main>\n{footer()}\n'
            '<script src="/assets/js/site.js" defer></script>\n</body>\n</html>\n')


def write(path, text):
    out = PUB / path.strip("/") / "index.html" if path.endswith("/") else PUB / path.lstrip("/")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")


# ------------------------------------------------------------------ shared blocks

def breadcrumbs(trail):
    parts = []
    for i, (n, u) in enumerate(trail):
        if i == len(trail) - 1:
            parts.append(f'<span aria-current="page">{esc(n)}</span>')
        else:
            parts.append(f'<a href="{u}">{esc(n)}</a>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span class="sep">&rsaquo;</span>'.join(parts) + "</nav>"


def tags(items):
    return '<ul class="tags">' + "".join(f"<li>{esc(t)}</li>" for t in items) + "</ul>"


def faq_block(faq, title="Questions"):
    items = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq)
    return f'<section class="block"><h2 class="sh">{esc(title)}</h2><div class="faq">{items}</div></section>'


def buy_box(title, price, sub, topic, cls=""):
    """The purchase strip: a title on the left, price and a green button on the right."""
    return f"""<div class="buy {cls}">
  <div class="buy-text"><h2>{esc(title)}</h2><p>{esc(sub)}</p></div>
  <div class="buy-act"><span class="price">{esc(price)}</span><a class="btn btn-go" href="/contact/?topic={esc(topic.replace(" ", "+"))}">Get started</a></div>
</div>"""


def capsule(href, media, title, sub="", extra=""):
    return f'<a class="cap" href="{href}"><div class="cap-media">{media}</div><div class="cap-body"><h3>{esc(title)}</h3>{f"<p>{esc(sub)}</p>" if sub else ""}{extra}</div></a>'


def area_media(a, cls=""):
    if a["slug"] in AREA_PHOTO:
        s = AREA_PHOTO[a["slug"]]
        return (f'<div class="ph {cls}">{photo(s, "Sample business photo used on the " + a["town"] + " page", sizes="(max-width: 900px) 100vw, 40vw")}'
                f'<span class="ph-label">{esc(a["town"])}</span></div>')
    return art(a["hue"], a["town"], "wave", "Lee County, FL", cls)


def svc_media(s, cls=""):
    return art(s["hue"], s["short"], s["icon"], "Service", cls)


def post_media(p, cls=""):
    return art(p["hue"], p["tag"], "doc", "Blog", cls)


def row_strip(title, items, more=None, cls=""):
    more_html = f'<a class="more" href="{more[1]}">{esc(more[0])}</a>' if more else ""
    return f"""<section class="strip {cls}">
  <div class="strip-head"><h2 class="sh">{esc(title)}</h2>{more_html}
    <div class="strip-arrows"><button type="button" class="arr prev" aria-label="Scroll left">&lsaquo;</button><button type="button" class="arr next" aria-label="Scroll right">&rsaquo;</button></div></div>
  <div class="strip-track">{"".join(items)}</div>
</section>"""


def town_capsules(slugs=None):
    pick = [AREA[s] for s in slugs] if slugs else AREAS
    return [capsule(f'/areas/{a["slug"]}/', area_media(a), a["town"], a["blurb"]) for a in pick]


def svc_capsules(slugs=None):
    pick = [SVC[s] for s in slugs] if slugs else SERVICES
    return [capsule(f'/services/{s["slug"]}/', svc_media(s), s["name"], s["price"]) for s in pick]


def post_capsules(slugs=None):
    pick = [POST[s] for s in slugs] if slugs else POSTS
    return [capsule(f'/blog/{p["slug"]}/', post_media(p), p["title"], f'{p["read_minutes"]} min read') for p in pick]


def cta_band(topic=""):
    t = f"?topic={esc(topic.replace(' ', '+'))}" if topic else ""
    mail = f' or email <a href="mailto:{esc(CFG["email"])}">{esc(CFG["email"])}</a>' if CFG.get("email") else ""
    return f"""<section class="band"><div>
  <h2>Tell me about your business</h2>
  <p>A free 20-minute video call, then a written plan and a fixed price within two days. Send the form{mail}.</p>
</div><a class="btn btn-go btn-lg" href="/contact/{t}">Start a project</a></section>"""


def contact_form():
    fallback = f'Please email me at {esc(CFG["email"])} instead.' if CFG.get("email") else "Please try again in a few minutes."
    chips = "".join(f'<label><input type="checkbox" name="needs" value="{v}"><span>{v}</span></label>'
                    for v in ["Website", "Redesign", "Local SEO", "Logo", "Print", "Spanish pages", "Not sure"])
    return f"""<form class="form" id="contact-form" novalidate data-fallback="{fallback}">
  <div class="field"><label for="cf-name">Your name</label><input id="cf-name" name="name" type="text" autocomplete="name" required></div>
  <div class="field"><label for="cf-email">Email</label><input id="cf-email" name="email" type="email" autocomplete="email" required></div>
  <div class="field"><label for="cf-biz">Business and town</label><input id="cf-biz" name="business" type="text" autocomplete="organization" placeholder="Name, and where you're based"></div>
  <div class="field"><label for="cf-site">Current website</label><input id="cf-site" name="site" type="text" inputmode="url" placeholder="If you have one"></div>
  <fieldset class="field wide chips"><legend>What do you need?</legend>{chips}</fieldset>
  <div class="field"><label for="cf-budget">Budget</label><select id="cf-budget" name="budget">
    <option value="">Choose one</option><option>Starter, $500</option><option>Business, $1,500</option><option>$1,500 to $5,000</option><option>More than $5,000</option><option>Not sure yet</option></select></div>
  <div class="field"><label for="cf-when">Timing</label><select id="cf-when" name="timeline">
    <option value="">Choose one</option><option>Before the winter season</option><option>As soon as possible</option><option>In the next 1 to 3 months</option><option>Just looking for now</option></select></div>
  <div class="field wide"><label for="cf-msg">Tell me about it</label><textarea id="cf-msg" name="message" rows="4" required placeholder="What you do, who your customers are, and what isn't working right now."></textarea></div>
  <div class="hp" aria-hidden="true"><label for="cf-company">Company website</label><input id="cf-company" name="company_site" type="text" tabindex="-1" autocomplete="off"></div>
  <input type="hidden" name="page" value="">
  <div class="form-foot wide"><button class="btn btn-go" type="submit" id="cf-submit">Send it</button><p class="form-status" id="form-status" role="status" aria-live="polite"></p></div>
  <p class="form-note wide">I only use your details to reply to you. <a href="/privacy/">Privacy</a></p>
</form>"""


def about_card():
    mail = f'<p class="about-mail"><a href="mailto:{esc(CFG["email"])}">{esc(CFG["email"])}</a></p>' if CFG.get("email") else ""
    parent = ""
    if CFG.get("parent_url"):
        parent = f' I also run <a href="{esc(CFG["parent_url"])}">{esc(CFG["parent_brand"])}</a>, my design studio.'
    return f"""<div class="about panel" id="about">
  <div class="about-head">
    <picture><source srcset="/assets/img/dan-headshot-192.webp 1x, /assets/img/dan-headshot-384.webp 2x" type="image/webp">
    <img src="/assets/img/dan-headshot-192.jpg" width="96" height="120" alt="Daniel, the designer behind Lee County Websites" loading="lazy"></picture>
    <div><p class="kick">Who you'll work with</p><h2>Hi, I'm {esc(OWNER)}</h2><p class="dim">Web and graphic designer</p></div>
  </div>
  <p>I'm a Florida-based designer, and I build every site on Lee County Websites myself, from the first sketch to launch day. You talk to me, not an account manager, and you get a fixed price before any work starts.{parent}</p>
  <p>We work by video call and email, and I reply within a business day.</p>
  {mail}
</div>"""


# ------------------------------------------------------------------ home

HOME_FAQ = [
    ("How much does a website cost in Fort Myers or Cape Coral?",
     "With me, a one-page Starter site is $500 and a Business site of up to five pages is $1,500, both at a fixed price. Online stores, booking systems and larger sites get a fixed quote after a free 20-minute call."),
    ("How long does a website take?",
     "About two weeks for a Starter site and about four weeks for a Business site, counted from when I have your photos and answers."),
    ("Do you work with businesses all over Lee County?",
     "Yes: Fort Myers, Cape Coral, Bonita Springs, Estero, Lehigh Acres, Sanibel, North Fort Myers, Fort Myers Beach and everywhere in between. We work by video call and email, so it doesn't matter which side of the river you're on."),
    ("Will my site show up on Google?",
     "Every site launches with what Google needs: page titles and descriptions, structured data, a sitemap, Search Console and a cleaned-up Google Business Profile. Nobody can promise the top spot, and I won't."),
    ("Do I own the website?",
     "Yes. The domain, the code and the hosting account are in your name from day one. If we stop working together, nothing is held back."),
    ("Is there a monthly fee?",
     "No. A domain is usually $10 to $20 a year and hosting on Cloudflare is often free. A care plan is optional, for people who'd rather hand off updates."),
    ("Can my site be in Spanish too?",
     "Yes. I can build Spanish versions of your key pages, written as real pages that Google can show to people searching in Spanish."),
    ("What about hurricane season?",
     "Your site is hosted away from Florida, so it stays up when the power doesn't. I set things up so you can post a closure notice in seconds, and a care plan can cover it for you."),
]

PACKAGES = [
    {"id": "starter", "name": "Starter", "price": "$500", "hue": 205, "icon": "browser",
     "tags": ["1 page", "About 2 weeks", "1 round of changes"],
     "text": "One clear page with your services, hours, the towns you cover and a contact form. You send the words and photos, I shape them.",
     "list": ["Phone-first design", "Contact form to your inbox", "Search Console and sitemap", "Google Business Profile check"]},
    {"id": "business", "name": "Business", "price": "$1,500", "hue": 145, "icon": "rocket",
     "tags": ["Up to 5 pages", "About 4 weeks", "Words written with you"],
     "text": "A small site built around how your customers decide, with the words written from a half-hour interview and a quote or booking form.",
     "list": ["Everything in Starter", "Pages for your main services", "Quote or booking form", "Local search setup", "30 days of fixes after launch"]},
    {"id": "custom", "name": "Custom", "price": "Quoted", "hue": 265, "icon": "spark",
     "tags": ["Stores", "Booking systems", "Bigger sites"],
     "text": "Online stores, booking engines, rental calendars, bilingual sites and brand projects. Fixed quote after a free call.",
     "list": ["Written plan within two days", "One fixed price", "Paid half at start, half at launch"]},
    {"id": "care", "name": "Care plan", "price": "Optional", "hue": 185, "icon": "shield",
     "tags": ["Edits on request", "Storm updates", "Cancel any time"],
     "text": "Text me a change and forget about it, including the closure notice when a storm is coming.",
     "list": ["Seasonal hours and menus", "Storm notices on site and Google", "Monthly checks and a short report"]},
]


def featured():
    slides, dots = [], []
    for i, s in enumerate(SAMPLES):
        nav = "".join(f"<span>{esc(n)}</span>" for n in s["nav"])
        pages = "".join(f'<li><span class="pg-ph" style="background-image:url(/assets/img/samples/{s["id"]}-640.webp);background-position:{p}"></span><span class="pg-n">{esc(n)}</span></li>'
                        for n, p in zip(s["pages"], ["50% 40%", "20% 60%", "80% 30%", "50% 90%"]))
        topic = f'A site like {s["name"]}'
        slides.append(f"""<article class="fs" id="fs-{s["id"]}" aria-roledescription="slide" aria-label="{i + 1} of {len(SAMPLES)}: {esc(s["name"])}">
  <div class="fs-media">
    {photo(s["id"], s["alt"], sizes="(max-width: 900px) 100vw, 62vw", eager=(i == 0))}
    <div class="mini" aria-hidden="true"><div class="mini-bar"><b>{esc(s["name"])}</b><span class="mini-nav">{nav}</span><span class="mini-cta">{esc(s["cta"])}</span></div>
      <div class="mini-hero"><span class="mini-k">{esc(s["town"])}</span><span class="mini-h">{esc(s["headline"])}</span><span class="mini-btn">{esc(s["cta"])}</span></div></div>
  </div>
  <div class="fs-info">
    <p class="fs-flag">Sample build &middot; made-up business</p>
    <h3>{esc(s["name"])}</h3>
    <p class="fs-kind">{esc(s["kind"])}, {esc(s["town"])}</p>
    <ul class="fs-pages" aria-label="Pages on this sample">{pages}</ul>
    <p class="fs-note">{esc(s["note"])}</p>
    {tags(s["tags"])}
    <div class="fs-buy"><span class="fs-pkg">{esc(s["package"])}</span><span class="price">{esc(s["price"])}</span><a class="btn btn-go" href="/contact/?topic={esc(topic.replace(" ", "+"))}">Build me one</a></div>
  </div>
</article>""")
        dots.append(f'<button type="button" class="dot" aria-label="Show {esc(s["name"])}" data-i="{i}"{" aria-current=true" if i == 0 else ""}></button>')
    return f"""<section class="feat" id="featured" aria-roledescription="carousel" aria-label="Featured sample builds">
  <h2 class="sh">Featured sample builds</h2>
  <div class="feat-frame">
    <button type="button" class="feat-arr prev" aria-label="Previous sample">&lsaquo;</button>
    <div class="feat-track" tabindex="0">{"".join(slides)}</div>
    <button type="button" class="feat-arr next" aria-label="Next sample">&rsaquo;</button>
  </div>
  <div class="dots">{"".join(dots)}</div>
</section>"""


def tabbed():
    def row(rid, media, title, tag_items, price, href=None):
        tagline = " &middot; ".join(esc(t) for t in tag_items)
        inner = f'<span class="tr-media">{media}</span><span class="tr-main"><span class="tr-title">{esc(title)}</span><span class="tr-tags">{tagline}</span></span><span class="tr-price">{esc(price)}</span>'
        if href:
            return f'<a class="tr" href="{href}" data-pv="{rid}">{inner}</a>'
        return f'<a class="tr" href="/pricing/#{rid}" data-pv="{rid}">{inner}</a>'

    def preview(rid, title, text, items, price, href, label):
        lis = "".join(f"<li>{esc(x)}</li>" for x in items)
        return f'<div class="pv" id="pv-{rid}" hidden><h3>{esc(title)}</h3><p class="pv-price">{esc(price)}</p><p>{esc(text)}</p><ul class="ticks">{lis}</ul><a class="btn btn-blue" href="{href}">{esc(label)}</a></div>'

    pk_rows = "".join(row(p["id"], art(p["hue"], p["name"], p["icon"], "Package", "art-sm"), p["name"], p["tags"], p["price"]) for p in PACKAGES)
    pk_prev = "".join(preview(p["id"], p["name"], p["text"], p["list"], p["price"], f'/pricing/#{p["id"]}', "See the details") for p in PACKAGES)
    sv_rows = "".join(row("s-" + s["slug"], art(s["hue"], s["short"], s["icon"], "Service", "art-sm"), s["name"], s["tags"], s["price"], f'/services/{s["slug"]}/') for s in SERVICES)
    sv_prev = "".join(preview("s-" + s["slug"], s["name"], s["answer"].split(". ")[0] + ".", s["included"][:4], s["price"], f'/services/{s["slug"]}/', "Read more") for s in SERVICES)
    return f"""<section class="tabs-sec" id="packages">
  <div class="tabs" role="tablist" aria-label="Packages and services">
    <button type="button" role="tab" id="tab-pk" aria-controls="panel-pk" aria-selected="true">Packages</button>
    <button type="button" role="tab" id="tab-sv" aria-controls="panel-sv" aria-selected="false" tabindex="-1">Services</button>
  </div>
  <div class="tabs-body">
    <div class="tab-panel" role="tabpanel" id="panel-pk" aria-labelledby="tab-pk"><div class="tr-list">{pk_rows}</div><aside class="pv-wrap" aria-live="polite">{pk_prev}</aside></div>
    <div class="tab-panel" role="tabpanel" id="panel-sv" aria-labelledby="tab-sv" hidden><div class="tr-list">{sv_rows}</div><aside class="pv-wrap" aria-live="polite">{sv_prev}</aside></div>
  </div>
</section>"""


def steps():
    items = [
        ("chat", "Free call", "20 minutes on video. Tell me what you do and what isn't working."),
        ("doc", "Plan and price", "A written plan and one fixed price within two days."),
        ("browser", "Preview link", "Watch the design take shape on a private link and ask for changes."),
        ("rocket", "Launch", "Live on your domain, with Google set up and every login handed to you."),
    ]
    lis = "".join(f'<li>{icon(i)}<h3>{esc(t)}</h3><p>{esc(d)}</p></li>' for i, t, d in items)
    return f'<section class="steps"><h2 class="sh">How a project runs</h2><ol>{lis}</ol></section>'


def build_index():
    path = "/"
    body = f"""<div class="wrap">
<section class="intro">
  <div class="intro-text">
    <p class="kick">Web design &middot; Lee County, Florida</p>
    <h1>Websites for Fort Myers and Cape Coral small businesses</h1>
    <p class="lede">Fast, phone-first websites at a fixed price: one page for $500 or up to five pages for $1,500. Built by hand, set up for Google, and yours from day one.</p>
  </div>
  <ul class="intro-stats">
    <li><b>$500</b><span>Starter site, fixed price</span></li>
    <li><b>2&ndash;4 wk</b><span>From kickoff to launch</span></li>
    <li><b>Yours</b><span>Domain, code and hosting in your name</span></li>
  </ul>
</section>
{featured()}
{row_strip("Browse by town", town_capsules(), ("All Lee County towns", "/areas/"), "towns")}
{tabbed()}
{steps()}
{row_strip("From the blog", post_capsules(), ("All posts", "/blog/"), "posts")}
<div class="two">
  {faq_block(HOME_FAQ, "Common questions")}
  <section class="block" id="contact"><h2 class="sh">Start a project</h2>{about_card()}<div class="panel">{contact_form()}</div></section>
</div>
</div>"""
    lds = [business_ld(), website_ld(), faq_ld(HOME_FAQ)]
    write(path, page(head(f"Fort Myers & Cape Coral Web Design for Small Businesses | {NAME}",
                          "Small business web design in Fort Myers, Cape Coral and Lee County, FL. Fixed-price websites from $500, fast on phones and set up for Google.",
                          path, lds), body, "/"))


# ------------------------------------------------------------------ detail pages

def detail_page(trail, h1, media, answer, facts, tag_items, buy, sections, side, faq, related, topic):
    facts_html = "".join(f"<div><dt>{esc(k)}</dt><dd>{v}</dd></div>" for k, v in facts)
    secs = "".join(f'<section class="block"><h2 class="sh">{esc(t)}</h2><div class="prose">{h}</div></section>' for t, h in sections)
    return f"""<div class="wrap">
{breadcrumbs(trail)}
<h1 class="page-title">{esc(h1)}</h1>
<section class="hero2">
  <div class="hero2-media">{media}</div>
  <div class="hero2-info">
    <p class="answer">{esc(answer)}</p>
    <dl class="facts">{facts_html}</dl>
    {tags(tag_items)}
  </div>
</section>
{buy}
<div class="cols">
  <div class="col-main">{secs}{faq_block(faq)}</div>
  <aside class="col-side">{side}</aside>
</div>
{related}
{cta_band(topic)}
</div>"""


def side_box(title, inner):
    return f'<div class="side-box"><h2>{esc(title)}</h2>{inner}</div>'


def link_list(items):
    return '<ul class="links">' + "".join(f'<li><a href="{u}">{esc(n)}</a></li>' for n, u in items) + "</ul>"


def ticks(items):
    return '<ul class="ticks">' + "".join(f"<li>{esc(x)}</li>" for x in items) + "</ul>"


def build_services():
    for s in SERVICES:
        path = f"/services/{s['slug']}/"
        trail = [("Home", "/"), ("Services", "/services/"), (s["name"], path)]
        towns = [(AREA[a]["place"], f"/areas/{a}/") for a in s["areas"]]
        side = side_box("What's included", ticks(s["included"])) + side_box("Popular in", link_list(towns))
        if s["posts"]:
            side += side_box("Read next", link_list([(POST[p]["title"], f"/blog/{p}/") for p in s["posts"]]))
        others = [x["slug"] for x in SERVICES if x["slug"] != s["slug"]]
        body = detail_page(
            trail, s["h1"], svc_media(s, "art-hero"), s["answer"],
            [("Price", esc(s["price"])), ("Timeline", esc(s["time"])), ("Serving", "Fort Myers, Cape Coral and all of Lee County")],
            s["tags"],
            buy_box(f"Start a {s['short'].lower()} project", s["price"], "Free 20-minute call, then a fixed written quote.", s["name"]),
            [("About this service", f'<p class="lede">{esc(s["lede"])}</p>')] + s["sections"],
            side, s["faq"], row_strip("More services", svc_capsules(others)), s["name"])
        lds = [crumbs_ld(trail), faq_ld(s["faq"]), {
            "@context": "https://schema.org", "@type": "Service", "name": s["name"], "serviceType": s["name"],
            "description": s["answer"], "provider": {"@id": BIZ_ID}, "url": absu(path),
            "areaServed": [LEE] + [{"@type": "City", "name": AREA[a]["town"]} for a in s["areas"]]}]
        write(path, page(head(s["seo_title"], s["description"], path, lds), body, "/services/"))

    path = "/services/"
    trail = [("Home", "/"), ("Services", path)]
    cards = "".join(capsule(f'/services/{s["slug"]}/', svc_media(s), s["name"], s["answer"].split(". ")[0] + ".",
                            f'<span class="cap-price">{esc(s["price"])}</span>') for s in SERVICES)
    body = f"""<div class="wrap">{breadcrumbs(trail)}
<h1 class="page-title">Web design services for Lee County small businesses</h1>
<p class="lede hub-lede">Everything a small business in Fort Myers, Cape Coral or anywhere in Lee County needs to be found and chosen online: a website, a Google listing that works, and a brand and print pieces that match. Every service has a fixed price agreed up front.</p>
<div class="grid">{cards}</div>
{cta_band()}</div>"""
    lds = [crumbs_ld(trail), {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": absu(f'/services/{s["slug"]}/'), "name": s["name"]} for i, s in enumerate(SERVICES)]}]
    write(path, page(head("Web Design Services in Fort Myers & Cape Coral", "Website design, redesigns, local SEO, logos, print and care plans for small businesses in Fort Myers, Cape Coral and Lee County, FL.", path, lds), body, "/services/"))


def build_areas():
    for a in AREAS:
        path = f"/areas/{a['slug']}/"
        trail = [("Home", "/"), ("Towns", "/areas/"), (a["town"], path)]
        side = side_box(f"A {a['town']} site should have", ticks(a["checklist"]))
        side += side_box("Services here", link_list([(SVC[s]["name"], f"/services/{s}/") for s in a["services"]]))
        body = detail_page(
            trail, a["h1"], area_media(a, "art-hero"), a["answer"],
            [("Starter site", "$500, one page"), ("Business site", "$1,500, up to 5 pages"), ("How we work", "Video call and email")],
            [a["town"], "Lee County, FL", "Fixed price", "Phone first"],
            buy_box(f"Get a website for your {a['town']} business", "From $500", "Free 20-minute call, then a fixed written quote.", f"Website in {a['town']}"),
            [(f"Doing business in {a['town']}", f'<p class="lede">{esc(a["lede"])}</p>')] + a["sections"],
            side, a["faq"], row_strip("Nearby towns", town_capsules(a["nearby"])), f"Website in {a['town']}")
        lds = [crumbs_ld(trail), faq_ld(a["faq"]), {
            "@context": "https://schema.org", "@type": "Service", "name": f"Web design in {a['place']}", "serviceType": "Web design",
            "provider": {"@id": BIZ_ID}, "url": absu(path), "description": a["answer"],
            "areaServed": {"@type": "City", "name": a["town"], "containedInPlace": LEE}}]
        write(path, page(head(a["seo_title"], a["description"], path, lds), body, "/areas/"))

    path = "/areas/"
    trail = [("Home", "/"), ("Towns", path)]
    cards = "".join(capsule(f'/areas/{a["slug"]}/', area_media(a), a["place"], a["blurb"]) for a in AREAS)
    body = f"""<div class="wrap">{breadcrumbs(trail)}
<h1 class="page-title">Web design across Lee County, Florida</h1>
<p class="lede hub-lede">I build websites for small businesses in every corner of Lee County, from the canals of Cape Coral to the islands. Each town page covers how people there search and what a good site for a local business should include. Not on the list? I work everywhere in between too.</p>
<div class="grid">{cards}</div>
{cta_band()}</div>"""
    write(path, page(head("Lee County Web Design: Fort Myers, Cape Coral & More", "Small business web design for every Lee County town: Fort Myers, Cape Coral, Bonita Springs, Estero, Lehigh Acres, Sanibel, North Fort Myers and Fort Myers Beach.", path, [crumbs_ld(trail)]), body, "/areas/"))


def build_blog():
    for p in POSTS:
        path = f"/blog/{p['slug']}/"
        trail = [("Home", "/"), ("Blog", "/blog/"), (p["title"], path)]
        others = [x["slug"] for x in POSTS if x["slug"] != p["slug"]][:4]
        body = f"""<div class="wrap">{breadcrumbs(trail)}
<article class="post">
  <header class="post-head">
    <p class="kick">{esc(p["tag"])}</p>
    <h1 class="page-title">{esc(p["title"])}</h1>
    <p class="post-meta">By {esc(OWNER)} &middot; <time datetime="{p["date"]}">{fmt_date(p["date"])}</time> &middot; {p["read_minutes"]} min read</p>
  </header>
  <div class="answer-box"><p class="kick">Short answer</p><p>{esc(p["answer"])}</p></div>
  <div class="prose">{p["body"]}</div>
</article>
{row_strip("More from the blog", post_capsules(others))}
{cta_band()}</div>"""
        lds = [crumbs_ld(trail), {
            "@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "description": p["description"],
            "datePublished": p["date"], "dateModified": p.get("updated", p["date"]), "author": {"@id": SITE + "/#founder"},
            "publisher": {"@id": BIZ_ID}, "mainEntityOfPage": absu(path), "image": absu(OG_IMAGE)}]
        write(path, page(head(p["seo_title"], p["description"], path, lds, og_type="article"), body, "/blog/"))

    path = "/blog/"
    trail = [("Home", "/"), ("Blog", path)]
    cards = "".join(capsule(f'/blog/{p["slug"]}/', post_media(p), p["title"], p["description"],
                            f'<span class="cap-price">{p["read_minutes"]} min read</span>') for p in POSTS)
    body = f"""<div class="wrap">{breadcrumbs(trail)}
<h1 class="page-title">Website advice for Lee County small businesses</h1>
<p class="lede hub-lede">Plain guides on websites, Google and running a business online in Southwest Florida, from storm season to the winter rush.</p>
<div class="grid">{cards}</div>
{cta_band()}</div>"""
    write(path, page(head("Blog: Website Tips for Southwest Florida Businesses", "Practical website, Google Business Profile and local SEO advice for small businesses in Fort Myers, Cape Coral and Lee County.", path, [crumbs_ld(trail)]), body, "/blog/"))


PRICING_FAQ = [
    ("Is the price really fixed?", "Yes. After a free 20-minute call you get a written plan and one price. That's what you pay. If you later want something outside the plan, I quote it before doing any of it."),
    ("How do I pay?", "Half when we start and half at launch, by invoice. Care plans are billed monthly."),
    ("Who writes the words?", "For a Business site, I draft them from a half-hour interview and we edit together. For a Starter site, you send what you have and I tidy it up."),
    ("What will I pay each year after launch?", "Usually $10 to $20 for your domain. Hosting runs on a Cloudflare account in your name and is free or a few dollars a month for most small business sites."),
    ("What if I need more than five pages?", "That's a Custom project. You get a written plan and a fixed quote, usually within two days of our call."),
    ("Do I own the site?", "Yes. Domain, code and hosting are in your name from day one, and I hand over every login at launch."),
]


def build_pricing():
    path = "/pricing/"
    trail = [("Home", "/"), ("Pricing", path)]
    cards = ""
    for p in PACKAGES:
        cards += f"""<article class="pkg" id="{p["id"]}" style="--h:{p["hue"]}">
  <div class="pkg-top">{icon(p["icon"])}<h2>{esc(p["name"])}</h2><p class="pkg-price">{esc(p["price"])}</p></div>
  {tags(p["tags"])}
  <p>{esc(p["text"])}</p>
  {ticks(p["list"])}
  <a class="btn btn-go" href="/contact/?topic={esc(p["name"]).replace(" ", "+")}">Choose {esc(p["name"])}</a>
</article>"""
    extras = [("Logo and brand identity", "Fixed quote", "/services/logo-and-branding/"),
              ("Print pieces (rack cards, door hangers, menus)", "Fixed quote per piece", "/services/print-design/"),
              ("Spanish versions of key pages", "Quoted with the site", "/areas/lehigh-acres-fl/"),
              ("Local SEO for a site I didn't build", "Fixed quote", "/services/local-seo/")]
    rows = "".join(f'<tr><th scope="row"><a href="{u}">{esc(n)}</a></th><td>{esc(v)}</td></tr>' for n, v, u in extras)
    body = f"""<div class="wrap">{breadcrumbs(trail)}
<h1 class="page-title">Website pricing for Lee County small businesses</h1>
<p class="lede hub-lede">Two fixed-price packages cover most small businesses. Anything bigger gets one fixed quote after a free call. No hourly billing and no surprise invoices.</p>
<div class="pkgs">{cards}</div>
<div class="cols">
  <div class="col-main">
    <section class="block"><h2 class="sh">Add-ons and other work</h2><table class="tbl"><tbody>{rows}</tbody></table></section>
    {faq_block(PRICING_FAQ, "Pricing questions")}
  </div>
  <aside class="col-side">{side_box("Every package includes", ticks(["Phone-first design", "Private preview link", "Structured data and sitemap", "Search Console set up", "Domain, code and hosting in your name"]))}
  {side_box("Read more", link_list([("What a website costs in Fort Myers and Cape Coral", "/blog/website-cost-fort-myers-cape-coral/")]))}</aside>
</div>
{cta_band()}</div>"""
    lds = [crumbs_ld(trail), faq_ld(PRICING_FAQ)]
    write(path, page(head("Website Pricing: $500 and $1,500 Fixed-Price Packages", "Fixed website prices for Fort Myers, Cape Coral and Lee County small businesses: Starter $500, Business $1,500, Custom quoted, optional care plans.", path, lds), body, "/pricing/"))


def build_contact():
    path = "/contact/"
    trail = [("Home", "/"), ("Contact", path)]
    mail = f'<li><b>Email</b><a href="mailto:{esc(CFG["email"])}">{esc(CFG["email"])}</a></li>' if CFG.get("email") else ""
    body = f"""<div class="wrap">{breadcrumbs(trail)}
<h1 class="page-title">Start a project</h1>
<p class="lede hub-lede">Tell me a little about your business. I'll reply within a business day to set up a free 20-minute video call.</p>
<div class="cols">
  <div class="col-main"><div class="panel">{contact_form()}</div></div>
  <aside class="col-side">
    {side_box("Other ways to reach me", '<ul class="links plain">' + mail + '<li><b>Hours</b>Monday to Friday, Eastern time</li></ul>')}
    {side_box("What happens next", '<ol class="next"><li>I reply within a business day.</li><li>We talk for 20 minutes by video.</li><li>You get a written plan and fixed price within two days.</li><li>Half to start, and the build begins.</li></ol>')}
  </aside>
</div></div>"""
    write(path, page(head("Contact: Start Your Website Project", "Contact Lee County Websites about a website, redesign, local SEO, logo or print project for your Fort Myers, Cape Coral or Lee County business.", path, [crumbs_ld(trail)]), body, "/contact/"))


def build_privacy():
    path = "/privacy/"
    trail = [("Home", "/"), ("Privacy", path)]
    body = f"""<div class="wrap">{breadcrumbs(trail)}
<h1 class="page-title">Privacy</h1>
<div class="cols"><div class="col-main"><div class="prose panel">
<p>This page explains what this website collects and what happens to it. In short: only what you send me, plus anonymous visit statistics if they're switched on.</p>
<h2>The contact form</h2>
<p>When you send the form, I receive what you typed: your name, email, business, website and message. It's delivered to my inbox by an email service called Resend. I use it only to reply to you and to quote for your project. I don't sell it, share it for marketing or add you to a mailing list.</p>
<h2>Visit statistics</h2>
<p>This site may use Google Tag Manager to load Google Analytics, which counts visits and shows which pages are useful. Google Analytics sets cookies and receives information such as the pages you view, your approximate location and the kind of device you use. I don't use it to identify you. You can block it with your browser's privacy settings.</p>
<h2>Hosting</h2>
<p>The site is hosted on Cloudflare, which processes basic request information, such as IP addresses, to deliver pages and protect the site from abuse.</p>
<h2>Questions</h2>
<p>To ask what I hold about you, or to have it deleted, <a href="/contact/">get in touch</a>.</p>
<p class="post-meta">Last updated {fmt_date(PRIVACY_UPDATED)}.</p>
</div></div></div></div>"""
    write(path, page(head("Privacy", "What the Lee County Websites site collects and how it's used: the contact form, visit statistics and hosting.", path, [crumbs_ld(trail)]), body))


def build_404():
    body = f"""<div class="wrap nf"><p class="kick">Error 404</p><h1 class="page-title">That page isn't here</h1>
<p class="lede">It may have moved. Try one of these instead.</p>
<p class="nf-links"><a class="btn btn-go" href="/">Home</a> <a class="btn btn-blue" href="/services/">Services</a> <a class="btn btn-blue" href="/areas/">Towns</a> <a class="btn btn-blue" href="/contact/">Contact</a></p></div>"""
    (PUB / "404.html").write_text(page(head("Page not found", "This page doesn't exist.", "/404.html", noindex=True), body), encoding="utf-8")


# ------------------------------------------------------------------ SEO files

def build_sitemap():
    urls = ["/", "/pricing/", "/services/", "/areas/", "/blog/", "/contact/"]
    urls += [f"/services/{s['slug']}/" for s in SERVICES]
    urls += [f"/areas/{a['slug']}/" for a in AREAS]
    urls += [f"/blog/{p['slug']}/" for p in POSTS]
    urls += ["/privacy/"]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        f = PUB / "index.html" if u == "/" else PUB / u.strip("/") / "index.html"
        if not f.exists():
            raise SystemExit(f"sitemap lists {u} but {f} does not exist")
        xml.append(f"  <url><loc>{absu(u)}</loc><lastmod>{page_date(f)}</lastmod></url>")
    xml.append("</urlset>")
    (PUB / "sitemap.xml").write_text("\n".join(xml) + "\n", encoding="utf-8")


def build_seo_files():
    (PUB / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    lines = [
        f"# {NAME}", "",
        f"> {NAME} builds fixed-price websites for small businesses in Fort Myers, Cape Coral and the rest of Lee County, Florida. "
        f"Every site is designed and hand-built by {OWNER}, a Florida-based web and graphic designer, and also covers local SEO, logos and print.", "",
        "Key facts:",
        "- Prices (fixed): Starter one-page website $500 (about 2 weeks); Business website up to five pages $1,500 (about 4 weeks); stores, booking systems, bigger sites and brand work get a fixed quote after a free 20-minute call.",
        "- Payment: half at the start, half at launch. Care plans are optional.",
        "- Clients own their domain, code and hosting. Sites are hosted on Cloudflare.",
        "- Areas served: " + ", ".join(a["place"] for a in AREAS) + ", and the rest of Lee County. Projects run by video call and email.",
        f"- Contact: {SITE}/contact/" + (f" or {CFG['email']}" if CFG.get("email") else ""),
        "", "## Services",
    ]
    lines += [f"- [{s['name']}]({absu('/services/' + s['slug'] + '/')}): {s['answer'].split('. ')[0]}." for s in SERVICES]
    lines += ["", "## Towns"]
    lines += [f"- [{a['place']}]({absu('/areas/' + a['slug'] + '/')})" for a in AREAS]
    lines += ["", "## Blog"]
    lines += [f"- [{p['title']}]({absu('/blog/' + p['slug'] + '/')}): {p['answer'].split('. ')[0]}." for p in POSTS]
    lines += ["", "## Optional", f"- [Pricing]({SITE}/pricing/)", f"- [Contact]({SITE}/contact/)", ""]
    (PUB / "llms.txt").write_text("\n".join(lines), encoding="utf-8")


def bust_asset_cache():
    hashes = {}
    for f in list((PUB / "assets" / "css").glob("*.css")) + list((PUB / "assets" / "js").glob("*.js")):
        hashes["/assets/" + f.parent.name + "/" + f.name] = hashlib.sha1(f.read_bytes()).hexdigest()[:8]
    pat = re.compile(r'(href|src)="(/assets/(?:css|js)/[^"?]+)(?:\?v=[0-9a-f]+)?"')
    for pg in PUB.rglob("*.html"):
        text = pg.read_text(encoding="utf-8")
        new = pat.sub(lambda m: f'{m.group(1)}="{m.group(2)}?v={hashes[m.group(2)]}"' if m.group(2) in hashes else m.group(0), text)
        if new != text:
            pg.write_text(new, encoding="utf-8")


def main():
    build_index()
    build_services()
    build_areas()
    build_blog()
    build_pricing()
    build_contact()
    build_privacy()
    build_404()
    build_seo_files()
    bust_asset_cache()
    build_sitemap()
    print("Built", len(list(PUB.rglob("index.html"))), "pages")


if __name__ == "__main__":
    main()
