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

def photo(sample_id, alt, sizes="(max-width: 900px) 100vw, 60vw", eager=False, cls=""):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img class="{cls}" src="/assets/img/samples/{sample_id}-1280.webp" '
            f'srcset="/assets/img/samples/{sample_id}-640.webp 640w, /assets/img/samples/{sample_id}-1280.webp 1280w" '
            f'sizes="{sizes}" width="1280" height="720" alt="{esc(alt)}" {load} decoding="async">')


def mock_caption(smp):
    return f'<figcaption>Sample design: {esc(smp["kind"].lower())} website, shown on a laptop and a phone.</figcaption>'


def site_mock(smp, sizes="(max-width: 900px) 100vw, 50vw", eager=False):
    """A sample website drawn in HTML: a browser window with the desktop layout and a
    phone with the mobile layout. Everything inside is decorative; the wrapper carries
    one text description for screen readers."""
    i = smp["id"]
    initial = smp["name"][0]
    label = f'Sample website design for a {smp["kind"].lower()} business in {smp["town"]}, shown on a laptop and a phone'
    nav = "".join(f"<span>{esc(n)}</span>" for n in smp["nav"])
    cards = "".join(f'<div class="ms-card"><p class="ms-ct">{esc(t)}</p><p class="ms-cd">{esc(d)}</p><p class="ms-cp">{esc(pr)}</p></div>'
                    for t, d, pr in smp["cards"])
    pcards = "".join(f'<div class="mp-row"><span>{esc(t)}</span><b>{esc(pr)}</b></div>' for t, d, pr in smp["cards"][:2])
    img = photo(i, "", sizes=sizes, eager=eager, cls="ms-img")
    pimg = photo(i, "", sizes="160px", eager=eager, cls="ms-img")
    return f"""<div class="mk mk-{i}" role="img" aria-label="{esc(label)}">
  <div class="mk-desk">
    <div class="mk-chrome"><span class="mk-dots"><i></i><i></i><i></i></span><span class="mk-tab"><b class="mk-fav">{esc(initial)}</b>{esc(smp["name"])}</span></div>
    <div class="mk-urlbar"><span class="mk-arrows">&#8249; &#8250;</span><span class="mk-addr"><svg viewBox="0 0 10 12" aria-hidden="true"><path d="M2 5V3.5a3 3 0 0 1 6 0V5h1v7H1V5zm1.5 0h3V3.5a1.5 1.5 0 0 0-3 0z"/></svg><i></i></span></div>
    <div class="ms">
      <div class="ms-nav"><span class="ms-logo"><b class="ms-mark">{esc(initial)}</b>{esc(smp["name"])}</span><span class="ms-links">{nav}</span><span class="ms-btn">{esc(smp["cta"])}</span></div>
      <div class="ms-hero">{img}<div class="ms-copy"><p class="ms-kick">{esc(smp["kicker"])}</p><p class="ms-h">{esc(smp["headline"])}</p><p class="ms-sub">{esc(smp["sub"])}</p><p class="ms-acts"><span class="ms-btn">{esc(smp["cta"])}</span><span class="ms-btn2">{esc(smp["phone"])}</span></p></div></div>
      <div class="ms-cards">{cards}</div>
    </div>
  </div>
  <div class="mk-phone"><div class="mp">
    <div class="mp-status"><span>9:41</span><span class="mp-notch"></span><span class="mp-bat"></span></div>
    <div class="ms-nav mp-nav"><span class="ms-logo"><b class="ms-mark">{esc(initial)}</b>{esc(smp["name"])}</span><span class="mp-burger"><i></i><i></i><i></i></span></div>
    <div class="mp-hero">{pimg}<p class="ms-h">{esc(smp["headline"])}</p></div>
    <div class="mp-body"><span class="ms-btn mp-block">{esc(smp["cta"])}</span>{pcards}</div>
    <div class="mp-call">&#9742; {esc(smp["phone"])}</div>
  </div></div>
</div>"""


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


def ga4_id():
    gid = CFG.get("ga4_id", "").strip()
    return gid if re.fullmatch(r"G-[A-Z0-9]+", gid) else ""


def first_sentence(text):
    first = text.split(". ")[0]
    return first if first.endswith((".", "!", "?")) else first + "."


def tracking_tags():
    out = []
    gaid = ga4_id()
    if gaid:
        out.append(f'<!-- Google tag (gtag.js) -->\n<script async src="https://www.googletagmanager.com/gtag/js?id={gaid}"></script>\n'
                   "<script>\n  window.dataLayer = window.dataLayer || [];\n  function gtag(){dataLayer.push(arguments);}\n"
                   f"  gtag('js', new Date());\n\n  gtag('config', '{gaid}');\n</script>")
    if CFG.get("gsc_verification"):
        out.append(f'<meta name="google-site-verification" content="{esc(CFG["gsc_verification"])}">')
    gid = gtm_id()
    if gid:
        out.append("<!-- Google Tag Manager -->\n<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\n"
                   "new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],\n"
                   "j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n"
                   "'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\n"
                   f"}})(window,document,'script','dataLayer','{gid}');</script>\n<!-- End Google Tag Manager -->")
    elif not gaid:
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
        "knowsAbout": ["Web design", "Website redesign", "Local SEO", "Google Business Profile", "AI search visibility", "Structured data", "Logo design", "Print design"],
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
    # Keep titles to about 60 characters so Google shows them whole; the brand
    # suffix is dropped when it would push past that (Google shows the site name anyway).
    full = title if NAME in title or len(f"{title} | {NAME}") > 62 else f"{title} | {NAME}"
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
<meta name="theme-color" content="#ffffff">
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

NAV = [("Services", "/services/"), ("Pricing", "/pricing/"), ("Towns", "/areas/"), ("Blog", "/blog/")]


def header(active=""):
    links = "".join(f'<a href="{u}"{" aria-current=page" if active == u else ""}>{n}</a>' for n, u in NAV)
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="gh">
  <div class="gh-in wrap">
    {logo_link()}
    <nav class="gh-nav" id="gh-nav" aria-label="Main">{links}<a class="gh-nav-contact" href="/contact/">Contact</a></nav>
    <a class="btn btn-go gh-cta" href="/contact/">Get a free quote</a>
    <button class="gh-menu" type="button" aria-expanded="false" aria-controls="gh-nav" aria-label="Menu"><span></span><span></span><span></span></button>
  </div>
</header>"""


def footer():
    svc = "".join(f'<li><a href="/services/{s["slug"]}/">{esc(s["name"])}</a></li>' for s in SERVICES)
    towns = "".join(f'<li><a href="/areas/{a["slug"]}/">{esc(a["town"])}</a></li>' for a in AREAS)
    parent = ""
    if CFG.get("parent_url"):
        parent = f' A site by {esc(OWNER)} of <a href="{esc(CFG["parent_url"])}">{esc(CFG["parent_brand"])}</a>.'
    mail = f'<p class="ft-mail"><a href="mailto:{esc(CFG["email"])}">{esc(CFG["email"])}</a></p>' if CFG.get("email") else ""
    return f"""<footer class="ft">
  <div class="wrap ft-grid">
    <div class="ft-brand">{logo_link("lg-ft")}<p>Fixed-price websites for small businesses in Fort Myers, Cape Coral and across Lee County, Florida.</p>{mail}</div>
    <div><h2>Services</h2><ul>{svc}</ul></div>
    <div><h2>Towns</h2><ul>{towns}</ul></div>
    <div><h2>More</h2><ul><li><a href="/pricing/">Pricing</a></li><li><a href="/blog/">Blog</a></li><li><a href="/#about">About</a></li><li><a href="/contact/">Contact</a></li><li><a href="/privacy/">Privacy</a></li></ul></div>
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


def faq_block(faq, title="Questions"):
    items = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq)
    return f'<section class="sec"><h2>{esc(title)}</h2><div class="faq">{items}</div></section>'


def area_media(a):
    """A town page shows a sample photo when one fits that town; otherwise nothing."""
    if a["slug"] not in AREA_PHOTO:
        return ""
    sid = AREA_PHOTO[a["slug"]]
    smp = next(x for x in SAMPLES if x["id"] == sid)
    return f'<figure class="shot">{site_mock(smp, sizes="(max-width: 760px) 80vw, 600px")}{mock_caption(smp)}</figure>'


def cta_band(topic=""):
    t = f"?topic={esc(topic.replace(' ', '+'))}" if topic else ""
    mail = f' You can also email <a href="mailto:{esc(CFG["email"])}">{esc(CFG["email"])}</a>.' if CFG.get("email") else ""
    return f"""<section class="cta">
  <h2>Tell me about your business</h2>
  <p>A free 20-minute video call, then a written plan with one fixed price within two days.{mail}</p>
  <a class="btn btn-go btn-lg" href="/contact/{t}">Get a free quote</a>
</section>"""


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
    parent = ""
    if CFG.get("parent_url"):
        parent = f' I also run <a href="{esc(CFG["parent_url"])}">{esc(CFG["parent_brand"])}</a>, my design studio.'
    return f"""<section class="sec about" id="about">
  <picture><source srcset="/assets/img/dan-headshot-192.webp 1x, /assets/img/dan-headshot-384.webp 2x" type="image/webp">
  <img src="/assets/img/dan-headshot-192.jpg" width="96" height="120" alt="Daniel, the designer behind Lee County Websites" loading="lazy"></picture>
  <div>
    <h2>Hi, I'm {esc(OWNER)}</h2>
    <p>I'm a Florida-based web and graphic designer, and I build every Lee County Websites site myself, from the first sketch to launch day. You talk to me, not an account manager, and you get a fixed price before any work starts.{parent}</p>
    <p class="dim">We work by video call and email, and I reply within a business day.</p>
  </div>
</section>"""


# ------------------------------------------------------------------ home

HOME_FAQ = [
    ("How much does a website cost in Fort Myers or Cape Coral?",
     "Two flat prices cover most businesses: $500 for a Starter site (one page) and $1,500 for a Business site (up to five pages). Online stores, booking systems and larger builds get one written price after a free 20-minute chat."),
    ("How long does a website take?",
     "About two weeks for a Starter site and about four weeks for a Business site, counted from when I have your photos and answers."),
    ("Do you work with businesses all over Lee County?",
     "Yes: Fort Myers, Cape Coral, Bonita Springs, Estero, Lehigh Acres, Sanibel, North Fort Myers, Fort Myers Beach and everywhere in between. We work by video call and email, so it doesn't matter which side of the river you're on."),
    ("Will my site show up on Google?",
     "Every site launches with what Google needs: page titles and descriptions, structured data, a sitemap, Search Console and a cleaned-up Google Business Profile. Nobody can promise the top spot, and I won't."),
    ("Can people find my business through ChatGPT or Google's AI answers?",
     "They can, and every site I build is set up for it: AI search crawlers are allowed in, each page answers real customer questions in its first lines, and your details match across Google, Bing and your site. No one can promise an AI will recommend you, but it will have accurate facts to work with."),
    ("Do I own the website?",
     "Yes. Your domain, code and hosting account are registered to you from the start. If you ever move on, you take everything with you."),
    ("Is there a monthly fee?",
     "No. Plan on roughly $10 to $20 a year for the domain, and Cloudflare hosting often costs nothing. A care plan is optional, for people who'd rather hand off updates."),
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


def steps():
    items = [
        ("Free call", "20 minutes on video. Tell me what you do and what isn't working."),
        ("Plan and price", "A written plan and one fixed price within two days."),
        ("Preview link", "Watch the design take shape on a private link and ask for changes."),
        ("Launch", "Live on your domain, with Google set up and every login handed to you."),
    ]
    lis = "".join(f'<li><h3>{esc(t)}</h3><p>{esc(d)}</p></li>' for t, d in items)
    return f'<section class="sec"><h2>How a project works</h2><ol class="steps">{lis}</ol></section>'


def card_list(items):
    """Plain link cards: title, a short line, and an optional meta line."""
    return '<ul class="cards">' + "".join(
        f'<li><a href="{u}"><span class="c-t">{esc(t)}</span><span class="c-d">{esc(d)}</span>'
        + (f'<span class="c-m">{esc(m)}</span>' if m else "") + "</a></li>" for t, d, m, u in items) + "</ul>"


def build_index():
    path = "/"
    hero = next(x for x in SAMPLES if x["id"] == "charter")
    svc = card_list([(s["name"], " \u00b7 ".join(s["tags"]), s["price"], f'/services/{s["slug"]}/') for s in SERVICES])
    pk = "".join(f'<li><h3>{esc(p["name"])}</h3><p class="pk-price">{esc(p["price"])}</p><p>{esc(p["text"])}</p></li>' for p in PACKAGES if p["id"] != "care")
    towns = "".join(f'<li><a href="/areas/{a["slug"]}/">{esc(a["town"])}</a></li>' for a in AREAS)
    body = f"""<section class="hero"><div class="wrap hero-in">
  <div class="hero-text">
    <p class="eyebrow">Web design in Lee County, Florida</p>
    <h1>Websites for Fort Myers and Cape Coral small businesses</h1>
    <p class="lede">Clear, fast websites at a fixed price: one page for $500, or up to five pages for $1,500. Built by hand, set up for Google, and yours from day one.</p>
    <p class="hero-act"><a class="btn btn-go btn-lg" href="/contact/">Get a free quote</a><a class="text-link" href="/pricing/">See pricing</a></p>
  </div>
  <figure class="hero-shot">{site_mock(hero, sizes="(max-width: 900px) 85vw, 40vw", eager=True)}{mock_caption(hero)}</figure>
</div></section>
<div class="wrap">
<section class="sec"><h2>What I can do for you</h2><p class="sec-lede">Everything a small business needs to be found and chosen online, at a price agreed before any work starts.</p>{svc}</section>
<section class="sec"><h2>Simple, fixed pricing</h2><ul class="pk">{pk}</ul><p><a class="text-link" href="/pricing/">Full pricing and what's included</a></p></section>
{steps()}
<section class="sec"><h2>Serving all of Lee County</h2><p class="sec-lede">I work with businesses across the county by video call and email. Each town page covers how people there search.</p><ul class="towns">{towns}</ul></section>
{about_card()}
{faq_block(HOME_FAQ, "Common questions")}
{cta_band()}
</div>"""
    lds = [business_ld(), website_ld(), faq_ld(HOME_FAQ)]
    write(path, page(head(f"Fort Myers & Cape Coral Web Design | {NAME}",
                          "Small business web design in Fort Myers, Cape Coral and Lee County, FL. Fixed-price websites from $500, fast on phones and set up for Google.",
                          path, lds), body, "/"))


# ------------------------------------------------------------------ detail pages

def detail_page(trail, h1, answer, facts, topic, media, sections, faq, related_title, related, cta_label="Get a free quote"):
    facts_html = "".join(f"<li><span>{esc(k)}</span>{v}</li>" for k, v in facts)
    secs = "".join(f'<section class="sec"><h2>{esc(t)}</h2><div class="prose">{h}</div></section>' for t, h in sections)
    t = esc(topic.replace(" ", "+"))
    return f"""<div class="wrap narrow">
{breadcrumbs(trail)}
<header class="page-head">
  <h1>{esc(h1)}</h1>
  <p class="lede">{esc(answer)}</p>
  <ul class="facts">{facts_html}</ul>
  <p><a class="btn btn-go" href="/contact/?topic={t}">{esc(cta_label)}</a></p>
</header>
{media}
{secs}
{faq_block(faq)}
<section class="sec"><h2>{esc(related_title)}</h2>{related}</section>
{cta_band(topic)}
</div>"""


def link_list(items):
    return '<ul class="links">' + "".join(f'<li><a href="{u}">{esc(n)}</a></li>' for n, u in items) + "</ul>"


def ticks(items):
    return '<ul class="ticks">' + "".join(f"<li>{esc(x)}</li>" for x in items) + "</ul>"


def build_services():
    for s in SERVICES:
        path = f"/services/{s['slug']}/"
        trail = [("Home", "/"), ("Services", "/services/"), (s["name"], path)]
        others = [x for x in SERVICES if x["slug"] != s["slug"]]
        included = ("What's included", ticks(s["included"]))
        where = ("Popular in", '<p class="inline-links">' + " \u00b7 ".join(f'<a href="/areas/{a}/">{esc(AREA[a]["town"])}</a>' for a in s["areas"]) + "</p>")
        reading = [("Read next", link_list([(POST[p]["title"], f"/blog/{p}/") for p in s["posts"]]))] if s["posts"] else []
        body = detail_page(
            trail, s["h1"], s["answer"],
            [("Price", esc(s["price"])), ("Timeline", esc(s["time"]))], s["name"], "",
            [("About this service", f'<p>{esc(s["lede"])}</p>')] + s["sections"] + [included, where] + reading,
            s["faq"], "Other services", link_list([(x["name"], f'/services/{x["slug"]}/') for x in others]))
        lds = [crumbs_ld(trail), faq_ld(s["faq"]), {
            "@context": "https://schema.org", "@type": "Service", "name": s["name"], "serviceType": s["name"],
            "description": s["answer"], "provider": {"@id": BIZ_ID}, "url": absu(path),
            "areaServed": [LEE] + [{"@type": "City", "name": AREA[a]["town"]} for a in s["areas"]]}]
        write(path, page(head(s["seo_title"], s["description"], path, lds), body, "/services/"))

    path = "/services/"
    trail = [("Home", "/"), ("Services", path)]
    cards = card_list([(s["name"], first_sentence(s["answer"]), s["price"], f'/services/{s["slug"]}/') for s in SERVICES])
    body = f"""<div class="wrap">{breadcrumbs(trail)}
<header class="page-head"><h1>Web design services for Lee County small businesses</h1>
<p class="lede">Everything a small business in Fort Myers, Cape Coral or anywhere in Lee County needs to be found and chosen online: a website, a Google listing that works, and a brand and print pieces that match. Every service has a fixed price agreed up front.</p></header>
{cards}
{cta_band()}</div>"""
    lds = [crumbs_ld(trail), {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": absu(f'/services/{s["slug"]}/'), "name": s["name"]} for i, s in enumerate(SERVICES)]}]
    write(path, page(head("Web Design Services in Fort Myers & Cape Coral", "Website design, redesigns, local SEO, AI search visibility, logos, print and care plans for small businesses in Fort Myers, Cape Coral and Lee County, FL.", path, lds), body, "/services/"))


def build_areas():
    for a in AREAS:
        path = f"/areas/{a['slug']}/"
        trail = [("Home", "/"), ("Towns", "/areas/"), (a["town"], path)]
        checklist = (f"A {a['town']} site should have", ticks(a["checklist"]))
        services = ("Services here", link_list([(SVC[x]["name"], f"/services/{x}/") for x in a["services"]]))
        body = detail_page(
            trail, a["h1"], a["answer"],
            [("Starter site", "$500, one page"), ("Business site", "$1,500, up to 5 pages")], f"Website in {a['town']}", area_media(a),
            [(f"Doing business in {a['town']}", f'<p>{esc(a["lede"])}</p>')] + a["sections"] + [checklist, services],
            a["faq"], "Nearby towns", link_list([(AREA[n]["place"], f"/areas/{n}/") for n in a["nearby"]]))
        lds = [crumbs_ld(trail), faq_ld(a["faq"]), {
            "@context": "https://schema.org", "@type": "Service", "name": f"Web design in {a['place']}", "serviceType": "Web design",
            "provider": {"@id": BIZ_ID}, "url": absu(path), "description": a["answer"],
            "areaServed": {"@type": "City", "name": a["town"], "containedInPlace": LEE}}]
        write(path, page(head(a["seo_title"], a["description"], path, lds), body, "/areas/"))

    path = "/areas/"
    trail = [("Home", "/"), ("Towns", path)]
    cards = card_list([(a["place"], a["blurb"], "", f'/areas/{a["slug"]}/') for a in AREAS])
    body = f"""<div class="wrap">{breadcrumbs(trail)}
<header class="page-head"><h1>Web design across Lee County, Florida</h1>
<p class="lede">I build websites for small businesses in every corner of Lee County, from the canals of Cape Coral to the islands. Each town page covers how people there search and what a good site for a local business should include. Not on the list? I work everywhere in between too.</p></header>
{cards}
{cta_band()}</div>"""
    write(path, page(head("Lee County Web Design: Fort Myers, Cape Coral & More", "Small business web design for every Lee County town: Fort Myers, Cape Coral, Bonita Springs, Estero, Lehigh Acres, Sanibel, North Fort Myers and Fort Myers Beach.", path, [crumbs_ld(trail)]), body, "/areas/"))


def build_blog():
    for p in POSTS:
        path = f"/blog/{p['slug']}/"
        trail = [("Home", "/"), ("Blog", "/blog/"), (p["title"], path)]
        others = [x for x in POSTS if x["slug"] != p["slug"]][:4]
        body = f"""<div class="wrap narrow">{breadcrumbs(trail)}
<article class="post">
  <header class="page-head">
    <p class="eyebrow">{esc(p["tag"])}</p>
    <h1>{esc(p["title"])}</h1>
    <p class="post-meta">By {esc(OWNER)} &middot; <time datetime="{p["date"]}">{fmt_date(p["date"])}</time> &middot; {p["read_minutes"]} min read</p>
  </header>
  <div class="answer-box"><p class="eyebrow">Short answer</p><p>{esc(p["answer"])}</p></div>
  <div class="prose">{p["body"]}</div>
</article>
<section class="sec"><h2>More from the blog</h2>{link_list([(x["title"], f'/blog/{x["slug"]}/') for x in others])}</section>
{cta_band()}</div>"""
        lds = [crumbs_ld(trail), {
            "@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "description": p["description"],
            "datePublished": p["date"], "dateModified": p.get("updated", p["date"]), "author": {"@id": SITE + "/#founder"},
            "publisher": {"@id": BIZ_ID}, "mainEntityOfPage": absu(path), "image": absu(OG_IMAGE)}]
        write(path, page(head(p["seo_title"], p["description"], path, lds, og_type="article"), body, "/blog/"))

    path = "/blog/"
    trail = [("Home", "/"), ("Blog", path)]
    cards = card_list([(p["title"], p["description"], f'{p["read_minutes"]} min read', f'/blog/{p["slug"]}/') for p in POSTS])
    body = f"""<div class="wrap">{breadcrumbs(trail)}
<header class="page-head"><h1>Website advice for Lee County small businesses</h1>
<p class="lede">Plain guides on websites, Google and running a business online in Southwest Florida, from storm season to the winter rush.</p></header>
{cards}
{cta_band()}</div>"""
    write(path, page(head("Blog: Website Tips for Southwest Florida Businesses", "Practical website, Google Business Profile and local SEO advice for small businesses in Fort Myers, Cape Coral and Lee County.", path, [crumbs_ld(trail)]), body, "/blog/"))


PRICING_FAQ = [
    ("Is the price really fixed?", "Yes. A free 20-minute chat, then one written price for the whole job, and that's the bill. Anything new you ask for later gets priced before I touch it."),
    ("How do I pay?", "Two invoices: 50% to start and 50% when the site goes live. Care plans are invoiced each month."),
    ("Who writes the words?", "On a Business site, I draft the copy after a half-hour interview, then we refine it together. On a Starter site, send me whatever text you've got and I'll polish it."),
    ("What will I pay each year after launch?", "Roughly $10 to $20 for the domain. Hosting lives on a Cloudflare account registered to you, and most small business sites pay nothing or a couple of dollars monthly."),
    ("What if my site needs more than five pages?", "Then it's a Custom project: a written plan and one flat price, normally within two days of our chat."),
    ("Who owns the finished site?", "You do. The domain, code and hosting are registered to you from the start, and every login is yours on launch day."),
]


def build_pricing():
    path = "/pricing/"
    trail = [("Home", "/"), ("Pricing", path)]
    cards = ""
    for p in PACKAGES:
        cards += f"""<article class="pkg" id="{p["id"]}">
  <h2>{esc(p["name"])}</h2><p class="pk-price">{esc(p["price"])}</p>
  <p class="pkg-tags">{" &middot; ".join(esc(t) for t in p["tags"])}</p>
  <p>{esc(p["text"])}</p>
  {ticks(p["list"])}
  <a class="btn {"btn-go" if p["id"] == "business" else "btn-line"}" href="/contact/?topic={esc(p["name"]).replace(" ", "+")}">Choose {esc(p["name"])}</a>
</article>"""
    extras = [("Logo and brand identity", "Fixed quote", "/services/logo-and-branding/"),
              ("Print pieces (rack cards, door hangers, menus)", "Fixed quote per piece", "/services/print-design/"),
              ("Spanish versions of key pages", "Quoted with the site", "/areas/lehigh-acres-fl/"),
              ("Local SEO for a site I didn't build", "Fixed quote", "/services/local-seo/"),
              ("AI search review for a site I didn't build", "Fixed quote", "/services/ai-search-visibility/")]
    rows = "".join(f'<tr><th scope="row"><a href="{u}">{esc(n)}</a></th><td>{esc(v)}</td></tr>' for n, v, u in extras)
    body = f"""<div class="wrap">{breadcrumbs(trail)}
<header class="page-head"><h1>Website pricing for Lee County small businesses</h1>
<p class="lede">Two fixed-price packages cover most small businesses. Anything bigger gets one fixed quote after a free call. No hourly billing and no surprise invoices.</p></header>
<div class="pkgs">{cards}</div>
<div class="narrow-in">
<section class="sec"><h2>Every package includes</h2>{ticks(["Phone-first design", "Private preview link", "Structured data and sitemap", "AI search crawlers allowed in", "Search Console set up", "Domain, code and hosting in your name"])}</section>
<section class="sec"><h2>Add-ons and other work</h2><table class="tbl"><tbody>{rows}</tbody></table></section>
{faq_block(PRICING_FAQ, "Pricing questions")}
<p>More detail: <a href="/blog/website-cost-fort-myers-cape-coral/">What a website costs in Fort Myers and Cape Coral</a>.</p>
</div>
{cta_band()}</div>"""
    lds = [crumbs_ld(trail), faq_ld(PRICING_FAQ)]
    write(path, page(head("Website Pricing: $500 and $1,500 Fixed-Price Packages", "Fixed website prices for Fort Myers, Cape Coral and Lee County small businesses: Starter $500, Business $1,500, Custom quoted, optional care plans.", path, lds), body, "/pricing/"))


def build_contact():
    path = "/contact/"
    trail = [("Home", "/"), ("Contact", path)]
    mail = f'<li><b>Email</b><a href="mailto:{esc(CFG["email"])}">{esc(CFG["email"])}</a></li>' if CFG.get("email") else ""
    body = f"""<div class="wrap">{breadcrumbs(trail)}
<div class="contact">
  <div class="contact-main">
    <header class="page-head"><h1>Start a project</h1><p class="lede">Tell me a little about your business. I'll reply within a business day to set up a free 20-minute video call.</p></header>
    {contact_form()}
  </div>
  <aside class="contact-side">
    <h2>Other ways to reach me</h2>
    <ul class="plain">{mail}<li><b>Hours</b>Monday to Friday, Eastern time</li></ul>
    <h2>What happens next</h2>
    <ol class="next"><li>You hear back from me within one business day.</li><li>We have a 20-minute video chat.</li><li>A written plan with one flat price arrives inside two days.</li><li>You pay the first half and the build begins.</li></ol>
  </aside>
</div></div>"""
    write(path, page(head("Contact: Start Your Website Project", "Contact Lee County Websites about a website, redesign, local SEO, logo or print project for your Fort Myers, Cape Coral or Lee County business.", path, [crumbs_ld(trail)]), body, "/contact/"))


def build_privacy():
    path = "/privacy/"
    trail = [("Home", "/"), ("Privacy", path)]
    body = f"""<div class="wrap narrow">{breadcrumbs(trail)}
<header class="page-head"><h1>Privacy</h1></header>
<div class="prose">
<p>Here's everything this site gathers about visitors and where it goes. The short version: whatever you choose to send through the form, and, when analytics is on, anonymous numbers about visits.</p>
<h2>Messages you send</h2>
<p>The contact form passes along the details you enter (name, email, business name, website and your message) to my inbox through Resend, an email delivery service. I read them so I can answer you and price your project, and that's all. Your details are never sold, never passed to marketers and never added to a newsletter.</p>
<h2>Analytics</h2>
<p>Google Tag Manager may load Google Analytics here so I can see how many people visit and which pages they find helpful. Analytics uses cookies and collects things like the pages viewed, a rough location and your device type. I look at the totals, not at individuals, and your browser's privacy controls can switch it off.</p>
<h2>Where the site runs</h2>
<p>Cloudflare serves these pages. To do that and to keep out attacks, it handles basic connection details such as your IP address.</p>
<h2>Your information</h2>
<p>If you'd like to know what I have on file about you, or want it removed, <a href="/contact/">send me a message</a>.</p>
<p class="post-meta">Last updated {fmt_date(PRIVACY_UPDATED)}.</p>
</div></div>"""
    write(path, page(head("Privacy", "What the Lee County Websites site collects and how it's used: the contact form, visit statistics and hosting.", path, [crumbs_ld(trail)]), body))


def build_404():
    body = f"""<div class="wrap narrow nf"><p class="eyebrow">Error 404</p><h1>That page isn't here</h1>
<p class="lede">It may have moved. Try one of these instead.</p>
<p class="nf-links"><a class="btn btn-go" href="/">Home</a> <a class="text-link" href="/services/">Services</a> <a class="text-link" href="/areas/">Towns</a> <a class="text-link" href="/contact/">Contact</a></p></div>"""
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
    ai_bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User",
               "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended", "Bingbot"]
    robots = ("# Search engines and AI assistants are welcome to read and cite this site.\n"
              + "".join(f"User-agent: {b}\n" for b in ai_bots) + "Allow: /\nDisallow: /api/\n\n"
              + f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {SITE}/sitemap.xml\n")
    (PUB / "robots.txt").write_text(robots, encoding="utf-8")
    lines = [
        f"# {NAME}", "",
        f"> {NAME} builds fixed-price websites for small businesses in Fort Myers, Cape Coral and the rest of Lee County, Florida. "
        f"Every site is designed and hand-built by {OWNER}, a Florida-based web and graphic designer, and also covers local SEO, logos and print.", "",
        "Key facts:",
        "- Prices (fixed): Starter one-page website $500 (about 2 weeks); Business website up to five pages $1,500 (about 4 weeks); stores, booking systems, bigger sites and brand work are priced as one flat number after a free 20-minute chat.",
        "- Payment: half at the start, half at launch. Care plans are optional.",
        "- Clients own their domain, code and hosting. Sites are hosted on Cloudflare.",
        "- Areas served: " + ", ".join(a["place"] for a in AREAS) + ", and the rest of Lee County. Projects run by video call and email.",
        f"- Contact: {SITE}/contact/" + (f" or {CFG['email']}" if CFG.get("email") else ""),
        "", "## Services",
    ]
    lines += [f"- [{s['name']}]({absu('/services/' + s['slug'] + '/')}): {first_sentence(s['answer'])}" for s in SERVICES]
    lines += ["", "## Towns"]
    lines += [f"- [{a['place']}]({absu('/areas/' + a['slug'] + '/')})" for a in AREAS]
    lines += ["", "## Blog"]
    lines += [f"- [{p['title']}]({absu('/blog/' + p['slug'] + '/')}): {first_sentence(p['answer'])}" for p in POSTS]
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
