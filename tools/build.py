# -*- coding: utf-8 -*-
"""Emits the Sentinel site as plain static HTML from one shared shell.

Run:  python tools/build.py
It writes the six pages in the project root. The site never needs this to run;
it just keeps the duplicated header, footer and CTA band in sync.
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, os.pardir)
sys.path.insert(0, HERE)

from group import PARENT, COMPANIES, by_id, BRANDS, LEADERS, CONTACT
from build_icons import sprite as icon_sprite

ORG = "Sentinel Integrated Technologies"
TAGLINE = "towards a #secure world"

NAV = [
    ("index.html", "Home"),
    ("group.html", "The group"),
    ("services.html", "Security systems"),
    ("security-services.html", "Guarding"),
    ("circuitron.html", "Circuitron"),
    ("contact.html", "Contact"),
]

# ----------------------------------------------------------------- icons
def icon(name, size="i-md", style="ph", cls=""):
    """A Phosphor glyph. style is 'ph', 'ph-duotone' or 'ph-fill'."""
    return '<i class="%s ph-%s %s%s" aria-hidden="true"></i>' % (
        style, name, size, (" " + cls) if cls else "")

def duo(name, size="i-2xl"):
    return icon(name, size, "ph-duotone")


_DIMS = {}


def dim(rel):
    """The real pixel size of an asset, so width and height never lie."""
    if rel not in _DIMS:
        from PIL import Image
        with Image.open(os.path.join(OUT, rel.replace("/", os.sep))) as im:
            _DIMS[rel] = im.size
    return _DIMS[rel]


def photo_img(name, alt, sizes, cls="", style="", lazy=True, eager=False):
    """A responsive photograph whose width and height come from the file.

    A declared size that disagrees with the file is a lie the browser reserves
    layout against, so these are read rather than typed."""
    big = "assets/img/photos/%s-1200.jpg" % name
    small = "assets/img/photos/%s-640.jpg" % name
    if not os.path.exists(os.path.join(OUT, small.replace("/", os.sep))):
        small = big
    w, h = dim(big)
    bits = ""
    if cls:
        bits += ' class="%s"' % cls
    bits += ' src="%s" srcset="%s 640w, %s 1200w" sizes="%s"' % (big, small, big, sizes)
    bits += ' alt="%s" width="%d" height="%d"' % (alt, w, h)
    if style:
        bits += ' style="%s"' % style
    if eager:
        bits += ' fetchpriority="high"'
    elif lazy:
        bits += ' loading="lazy"'
    return "<img%s>" % bits


def photo_square(name, alt, sizes, cls="", lazy=True):
    """A square crop, which has its own file rather than a squeezed wide one."""
    src = "assets/img/photos/%s-640.jpg" % name
    w, h = dim(src)
    return ('<img%s src="%s" alt="%s" width="%d" height="%d"%s>'
            % ((' class="%s"' % cls) if cls else "", src, alt, w, h,
               ' loading="lazy"' if lazy else ""))


def si(name, size="i-md", cls=""):
    """A glyph from the Sentinel set. The sprite is inlined once per page, so
    this is a same document reference and needs no extra request."""
    return ('<svg class="si %s%s" aria-hidden="true" focusable="false">'
            '<use href="#si-%s"/></svg>' % (size, (" " + cls) if cls else "", name))

WA_ENQUIRY = ("https://wa.me/263773589461?text="
              "Hello%20Sentinel%2C%20I%20would%20like%20to%20ask%20about%20a%20security%20system%20for%20my%20property.")
# Placeholder: swap for the real chat.whatsapp.com invite link once it exists.
WA_COMMUNITY = "https://chat.whatsapp.com/"

CHEV = '<span class="pbtn__chev">%s</span>' % icon("caret-double-right", "i-sm")
CHEV_SM = icon("caret-double-right", "i-xs")
ARROW = icon("arrow-right", "i-sm")
STAR = icon("star", "i-xs", "ph-fill")


def pbtn(label, href, variant="", attrs=""):
    cls = "pbtn" + ((" " + variant) if variant else "")
    return '<a class="%s" href="%s"%s><span class="pbtn__label">%s</span>%s</a>' % (
        cls, href, attrs, label, CHEV)


def eyebrow(text, variant=""):
    cls = "eyebrow" + ((" " + variant) if variant else "")
    return '<p class="%s">%s<span>%s</span></p>' % (cls, icon("asterisk", "i-xs"), text)


def shead(kicker, title, aside="", cta="", variant="", kv=""):
    right = ('<div class="shead__cta">%s</div>' % cta) if cta else (
        ('<div class="shead__aside">%s</div>' % aside) if aside else "")
    cls = "shead" + ((" " + variant) if variant else "")
    return """      <div class="%s" data-reveal>
        <div>
          %s
          <h2 class="h-2 shead__title">%s</h2>
        </div>
        %s
      </div>
""" % (cls, eyebrow(kicker, kv), title, right)


def ncard(variant, ico, title, text, bullets, href, cta="Explore more"):
    lis = ""
    if bullets:
        lis = ('<ul class="card__list" style="margin-top:1.25rem">'
               + "".join("<li>%s</li>" % b for b in bullets) + "</ul>")
    return """        <article class="ncard ncard--%s" data-reveal>
          <div class="ncard__main">
            <span class="ncard__icon">%s</span>
            <h3 class="h-3">%s</h3>
            <p>%s</p>
            %s
          </div>
          <div class="ncard__foot">
            <a class="ncard__cta" href="%s">%s %s</a>
            <span class="ncard__fill" aria-hidden="true"></span>
          </div>
        </article>
""" % (variant, duo(ico), title, text, lis, href, cta, CHEV_SM)



# -------------------------------------------------- the group, as components
def org_card(c, compact=False):
    """One company in the structure. Compact drops the description."""
    subs = ""
    if c.get("units"):
        # The units sit on the chart's second row, under the column that owns
        # them, so they do not stretch the other companies' cards.
        col = COMPANIES.index(c) + 1
        subs = ('<span class="org__subs" style="grid-column:%d">%s</span>' % (col, "".join(
            '<a class="org__sub" href="%s#%s">%s<small>%s</small></a>'
            % (c["href"], u["id"], u["name"], u["strap"]) for u in c["units"])))
    body = "" if compact else "<p>%s</p>" % c["line"]
    return """        <div class="org__co">
          <a class="org__card" href="%s">
            <span class="org__logo">%s</span>
            <span class="org__role">%s %s</span>
            %s
            <span class="org__caps">%s</span>
            <span class="org__go">%s %s</span>
          </a>
          %s
        </div>
""" % (c["href"], company_logo(c), si(c["icon"], "i-sm"), c["role"], body,
       "".join("<i>%s</i>" % x for x in c["chips"]),
       "Open " + c["short"], CHEV_SM, subs)


def org_chart(compact=False):
    """The structure the Operations Director drew, made clickable."""
    return """      <div class="org%s" data-reveal>
        <a class="org__parent" href="group.html">
          <span class="org__parent-mark">
            <img src="assets/img/brand/mark.svg" alt="" width="44" height="42" loading="lazy">
          </span>
          <span class="org__parent-text">
            <strong>%s</strong>
            <small>%s</small>
          </span>
        </a>
        <span class="org__trunk" aria-hidden="true"></span>
        <div class="org__row">
%s        </div>
      </div>
""" % (" org--compact" if compact else "", PARENT["name"], PARENT["role"],
       "".join(org_card(c, compact) for c in COMPANIES))


NUMBER_WORD = {2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six",
               7: "Seven", 8: "Eight"}


def company_logo(c, h=None, white=False, cls="", lazy=True):
    """A company's own lockup, sized by height so three different shapes read
    at the same optical weight."""
    px = h or c["logo_h"]
    key = "logo_small" if (px <= 52 and "logo_small" in c) else "logo"
    if white:
        key = key + "_white"
    src = c[key]
    iw, ih = c["logo_wh"]
    return ('<img class="clogo%s" src="%s" alt="%s" width="%d" height="%d" '
            'style="height:%dpx;width:%dpx"%s>'
            % ((" " + cls) if cls else "", src, c["name"],
               round(px * iw / ih), px, px, round(px * iw / ih),
               ' loading="lazy"' if lazy else ""))


DIV_PHOTO = {
    # A capability only gets a photograph when there is an honest one for it.
    "k9": ("k9-handler-standing", "A handler with a patrol dog"),
    "response": ("response-night", "A response vehicle on a wet road at night"),
    "events": ("officer-radio", "An officer coordinating by radio"),
    "perimeter": ("vehicle-checkpoint", "A boom barrier at a vehicle entrance"),
    "manned": ("security-officers", "An officer on post at a public event"),
    "communications": ("tech-network", "A fibre patch panel in a network cabinet"),
    "automation": ("tech-smart", "A smart control panel being set"),
    "electronics": ("tech-retail", "Shelves of electronics in a technology store"),
    "security-systems": ("sys-cctv", "A dome camera on a wall bracket"),
    # Loss and shrinkage work happens on a shop floor, so the officer on duty
    # is the honest frame for it until a dedicated one exists.
    "investigations": ("officer-on-duty", "An officer working a retail floor"),
}


def division_card(c, d):
    """A capability inside a company: what it is, then the actual line items."""
    photo = DIV_PHOTO.get(d["id"])
    media = ""
    if photo:
        f, alt = photo
        media = """          <a class="dcard__media" href="contact.html" tabindex="-1" aria-hidden="true">
            %s
          </a>
""" % photo_img(f, alt, "(max-width:720px) 100vw, 30vw")
    return """        <article class="dcard%s" id="%s" data-reveal>
%s          <span class="dcard__ico">%s</span>
          <h3 class="h-3">%s</h3>
          <p>%s</p>
          <ul class="dcard__list">%s</ul>
          <a class="dcard__cta" href="contact.html">Ask about this %s</a>
        </article>
""" % (" dcard--photo" if media else "", d["id"], media, si(d["icon"], "i-xl"),
       d["name"], d["line"],
       "".join("<li>%s</li>" % i for i in d["items"]), CHEV_SM)


UNIT_PHOTO = {
    "circuitstore": ("tech-retail", "Shelves of electronics in a technology store"),
    "ecocircuit": ("tech-ewaste", "Mixed electronic scrap waiting to be sorted"),
}


def unit_panel(c, u):
    """CircuitStore and EcoCircuit: businesses inside a business."""
    f, alt = UNIT_PHOTO[u["id"]]
    media = """          <a class="unit__media" href="contact.html" tabindex="-1" aria-hidden="true">
            %s
          </a>
""" % photo_img(f, alt, "(max-width:980px) 100vw, 45vw")
    return """        <article class="unit" id="%s" data-reveal>
%s          <div class="unit__head">
            <span class="unit__ico">%s</span>
            <div>
              <h3 class="h-3">%s</h3>
              <p class="script unit__strap">%s</p>
            </div>
          </div>
          <p>%s</p>
          <ul class="unit__list">%s</ul>
        </article>
""" % (u["id"], media, si(u["icon"], "i-xl"), u["name"], u["strap"], u["line"],
       "".join("<li>%s%s</li>" % (CHEV_SM, i) for i in u["items"]))

def siblings(current):
    """At the foot of a company page: the other two, so nobody dead ends."""
    others = [c for c in COMPANIES if c["id"] != current]
    cards = "".join("""        <a class="sib" href="%s" data-reveal>
          <span class="sib__logo">%s</span>
          <span class="sib__body"><small>%s</small></span>
          <span class="sib__go" aria-hidden="true">%s</span>
        </a>
""" % (c["href"], company_logo(c, h=32), c["role"], ARROW) for c in others)
    return """  <section class="section section--cream section--tight">
    <div class="container">
%s      <div class="sibs">
%s        <a class="sib sib--all" href="group.html" data-reveal>
          <span class="sib__ico">%s</span>
          <span class="sib__body"><strong>The whole group</strong><small>How the three fit together</small></span>
          <span class="sib__go" aria-hidden="true">%s</span>
        </a>
      </div>
    </div>
  </section>
""" % (shead("Elsewhere in the group", "The rest of Sentinel"), cards,
       si("group-tree", "i-lg"), ARROW)


# ----------------------------------------------------------------- shell
def head(title, desc, canonical):
    return """<!DOCTYPE html>
<html lang="en-ZW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%s</title>
<meta name="description" content="%s">
<meta name="theme-color" content="#06291B">
<link rel="canonical" href="https://www.sentinel.co.zw/%s">

<meta property="og:type" content="website">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:image" content="assets/img/brand/flier-1.jpg">
<meta property="og:locale" content="en_ZW">

<link rel="icon" type="image/svg+xml" href="assets/img/brand/mark.svg">
<link rel="icon" type="image/png" sizes="32x32" href="assets/img/brand/favicon-32.png">
<link rel="apple-touch-icon" href="assets/img/brand/favicon-180.png">

<link rel="preload" href="assets/fonts/manrope-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/manrope-800.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/icons/phosphor.css">
<link rel="stylesheet" href="assets/css/style.css">
<script>document.documentElement.classList.add('js');</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
%s
""" % (title, desc, canonical, title, desc, icon_sprite())


def topbar():
    return """
<!-- ===== Utility bar ===== -->
<div class="topbar">
  <div class="container topbar__inner">
    <ul class="topbar__list">
      <li>%s <a href="about.html">About the group</a></li>
      <li>%s <a href="mailto:info@sentinel.co.zw">info@sentinel.co.zw</a></li>
      <li>%s <a href="tel:+263773589461" class="num">+263 77 358 9461</a></li>
    </ul>
    <div class="topbar__social">
      <span class="script">towards a #secure world</span>
      <a href="https://wa.me/263773589461" aria-label="Message Sentinel on WhatsApp" rel="noopener">%s</a>
      <a href="mailto:info@sentinel.co.zw" aria-label="Email Sentinel">%s</a>
      <a href="tel:+263773589461" aria-label="Call Sentinel">%s</a>
    </div>
  </div>
</div>
""" % (icon("buildings", "i-xs"), icon("envelope-simple", "i-xs"), icon("phone-call", "i-xs"),
       icon("whatsapp-logo", "i-sm", "ph-fill"), icon("envelope-simple", "i-sm", "ph-fill"),
       icon("phone-call", "i-sm", "ph-fill"))


GROUP_HREFS = [c["href"] for c in COMPANIES] + ["group.html"]


def megapanel():
    """The group, laid out under the nav. Every page can see the whole structure
    without leaving the page it is on."""
    cards = ""
    for c in COMPANIES:
        units = ""
        if c.get("units"):
            units = '<span class="mega__units">%s</span>' % " ".join(
                '<a href="%s#%s">%s</a>' % (c["href"], u["id"], u["name"])
                for u in c["units"])
        cards += """        <a class="mega__card" href="%s">
          <span class="mega__logo">%s</span>
          <small>%s</small>
          <span class="mega__chips">%s</span>
          %s
        </a>
""" % (c["href"], company_logo(c, h=34), c["role"],
       "".join("<i>%s</i>" % x for x in c["chips"]), units)
    return """      <div class="mega" id="mega" hidden>
        <div class="container mega__inner">
          <a class="mega__parent" href="group.html">
            <span class="mega__mark">%s</span>
            <span>
              <strong>%s</strong>
              <small>%s</small>
            </span>
            <span class="mega__go">See the structure %s</span>
          </a>
          <div class="mega__grid">
%s          </div>
        </div>
      </div>
""" % (si("group-tree", "i-lg"), PARENT["name"] + ", the group", PARENT["line"],
       CHEV_SM, cards)


def header(active):
    items = ""
    for h, l in NAV:
        on = ' aria-current="page"' if h == active else ""
        if h == "group.html":
            cur = ' data-within="true"' if active in GROUP_HREFS else ""
            items += ('        <li class="nav__has-mega"><a class="nav__link" '
                      'href="%s"%s%s aria-expanded="false" aria-controls="mega" '
                      'data-mega>%s %s</a></li>\n'
                      % (h, on, cur, l, icon("caret-down", "i-xs")))
        else:
            items += '        <li><a class="nav__link" href="%s"%s>%s</a></li>\n' % (h, on, l)
    drawer = "\n".join(
        '    <a href="%s">%s <span class="num">%02d</span></a>' % (h, l, i + 1)
        for i, (h, l) in enumerate(NAV + [("about.html", "About")]))
    return """
<!-- ===== Header ===== -->
<header class="header">
  <div class="container header__inner">
    <a class="brand" href="index.html" aria-label="%s, home">
      <img class="brand__light" src="assets/img/brand/sentinel-logo-compact-white.svg" alt="%s" width="328" height="140">
      <img class="brand__dark" src="assets/img/brand/sentinel-logo-compact.svg" alt="" width="328" height="140" aria-hidden="true">
    </a>

    <nav class="nav" aria-label="Primary">
      <ul class="nav__list">
%s      </ul>
%s    </nav>

    <div class="header__cta">%s</div>

    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="drawer" aria-label="Open menu">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>

<div class="drawer" id="drawer">
  <nav class="drawer__list" aria-label="Mobile">
%s
  </nav>
  <div class="drawer__foot">
    <a href="tel:+263773589461" class="num">+263 77 358 9461</a>
    <a href="mailto:info@sentinel.co.zw">info@sentinel.co.zw</a>
    <p>29 Tweed Road, Eastlea, Harare</p>
    %s
  </div>
</div>

<main id="main">
""" % (ORG, ORG, items, megapanel(), pbtn("Book a site survey", "contact.html"), drawer,
       pbtn("Book a site survey", "contact.html", "pbtn--block"))


CTA = """
  <!-- ===== CTA ===== -->
  <section class="section section--tight">
    <div class="container">
      <div class="cta" data-reveal>
        <div class="cta__inner">
          <div>
            %s
            <h2 class="h-2">Book a free site survey</h2>
            <p>We walk your property, write up where you are exposed, and price the fix. No charge.</p>
          </div>
          <div class="cta__actions">
            %s
            %s
          </div>
        </div>
      </div>
    </div>
  </section>
""" % (eyebrow("Next step", "eyebrow--dark"),
       pbtn("Book a site survey", "contact.html", "pbtn--light"),
       pbtn("+263 77 358 9461", "tel:+263773589461", "pbtn--outline"))


FOOTER = """
</main>

<!-- ===== Footer ===== -->
<footer class="footer">
  <div class="container">
    <div class="footer__top">
      <div class="footer__brand">
        <a href="index.html" aria-label="%s, home">
          <img src="assets/img/brand/sentinel-logo-white.svg" alt="%s" width="328" height="140" loading="lazy">
        </a>
        <p class="script footer__tagline">towards a #secure world</p>
        <p>A Zimbabwean security group: electronic systems, guarding operations and technology, run as three companies under one standard.</p>
        <div class="socials">
          <a href="https://wa.me/263773589461" aria-label="Message Sentinel on WhatsApp" rel="noopener">%s</a>
          <a href="mailto:info@sentinel.co.zw" aria-label="Email Sentinel">%s</a>
          <a href="tel:+263773589461" aria-label="Call Sentinel">%s</a>
        </div>
      </div>

      <div>
        <h4>The group</h4>
        <ul class="footer__links">
          <li><a href="group.html">How we are structured</a></li>
          <li><a href="services.html">Sentinel Integrated Technologies</a></li>
          <li><a href="security-services.html">Sentinel Security Services</a></li>
          <li><a href="circuitron.html">Circuitron Systems</a></li>
          <li><a href="circuitron.html#circuitstore">CircuitStore</a></li>
          <li><a href="circuitron.html#ecocircuit">EcoCircuit</a></li>
        </ul>
      </div>

      <div>
        <h4>What we do</h4>
        <ul class="footer__links">
          <li><a href="services.html#cctv">CCTV surveillance</a></li>
          <li><a href="services.html#alarms">Intruder alarms</a></li>
          <li><a href="services.html#access">Access control</a></li>
          <li><a href="services.html#gates">Gate automation</a></li>
          <li><a href="security-services.html#manned">Manned guarding</a></li>
          <li><a href="security-services.html#response">Alarm response</a></li>
          <li><a href="renewable-energy.html">Solar and backup power</a></li>
          <li><a href="about.html">About the group</a></li>
        </ul>
      </div>

      <div>
        <h4>Get in touch</h4>
        <ul class="footer__contact">
          <li>%s<span>29 Tweed Road,<br>Eastlea, Harare, Zimbabwe</span></li>
          <li>%s<span class="num">
              <a href="tel:+263773589461">+263 77 358 9461</a>
              <a href="tel:+263772568361">+263 77 256 8361</a>
              <a href="tel:+263242006157">+263 24 200 6157</a>
            </span></li>
          <li>%s<a href="mailto:info@sentinel.co.zw">info@sentinel.co.zw</a></li>
        </ul>
      </div>
    </div>

    <div class="footer__bottom">
      <p style="margin:0">&copy; <span data-year class="num">2026</span> Sentinel Integrated Technologies (PVT) Ltd</p>
      <nav aria-label="Legal">
        <a href="privacy.html">Privacy policy</a>
        <a href="contact.html">Contact</a>
        <a href="https://unsplash.com/?utm_source=sentinel&amp;utm_medium=referral" rel="noopener">Photography: Unsplash</a>
      </nav>
    </div>
  </div>
</footer>

<!-- ===== Floating contact rail ===== -->
<div class="fab-rail">
  <button class="to-top" type="button" aria-label="Back to top">%s</button>

  <div class="wa" data-wa>
    <div class="wa__panel" id="wa-panel" role="dialog" aria-label="Contact Sentinel on WhatsApp">
      <div class="wa__head">
        %s
        <span>
          <strong>Sentinel on WhatsApp</strong>
          <span>Usually replies within the hour</span>
        </span>
      </div>
      <div class="wa__body">
        <a class="wa__opt" href="%s" target="_blank" rel="noopener">
          %s
          <span>
            <strong>Make an enquiry</strong>
            <small>Prices and site surveys</small>
          </span>
          %s
        </a>
        <a class="wa__opt" href="%s" target="_blank" rel="noopener">
          %s
          <span>
            <strong>Join the community</strong>
            <small>Security tips from our team</small>
          </span>
          %s
        </a>
      </div>
      <p class="wa__foot">Opens WhatsApp. Standard message rates apply.</p>
    </div>

    <button class="wa__toggle" type="button" data-wa-toggle
            aria-expanded="false" aria-controls="wa-panel" aria-label="Contact us on WhatsApp">
      %s
      %s
    </button>
  </div>
</div>

<script src="assets/js/main.js" defer></script>
</body>
</html>
""" % (ORG, ORG,
       icon("whatsapp-logo", "i-sm", "ph-fill"), icon("envelope-simple", "i-sm", "ph-fill"),
       icon("phone-call", "i-sm", "ph-fill"),
       icon("map-pin", "i-sm"), icon("phone-call", "i-sm"), icon("envelope-simple", "i-sm"),
       icon("arrow-up", "i-sm"),
       icon("whatsapp-logo", "i-md", "ph-fill"),
       WA_ENQUIRY, icon("chat-circle-dots", "i-md", "ph-duotone"), icon("caret-double-right", "i-xs"),
       WA_COMMUNITY, icon("users-three", "i-md", "ph-duotone"), icon("caret-double-right", "i-xs"),
       icon("whatsapp-logo", "i-md", "ph-fill", "wa__open"), icon("x", "i-md", "ph", "wa__close"))


def phero(label, title, lead, pic=None, alt=""):
    if pic:
        media = """    <div class="phero__media">
      %s
    </div>
    <div class="phero__scrim"></div>
""" % photo_img(pic, alt, "70vw", lazy=False, eager=True)
        cls = "phero"
    else:
        media, cls = "", "phero phero--plain"
    return """
  <section class="%s">
%s    <div class="container">
      <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a> <i class="sep">/</i> <span>%s</span></nav>
      <h1 class="h-1">%s</h1>
      <p class="lead">%s</p>
    </div>
  </section>
""" % (cls, media, label, title, lead)


def client_logo(slug, alt, lazy=True):
    rel = "assets/img/clients/%s.png" % slug
    w, h = dim(rel)
    return ('<img src="%s" alt="%s" width="%d" height="%d"%s>'
            % (rel, alt, w, h, ' loading="lazy"' if lazy else ""))


IMG_SRC = re.compile(r'<img\b[^>]*?\bsrc="(assets/[^"]+\.(?:jpg|png))"[^>]*>')


def size_images(html):
    """Give every local <img> the width and height of the file it points at.

    Typed dimensions produced six wrong pairs in one round, including a square
    tile declared as a 2:1 banner. Reading them removes the whole class."""
    def one(m):
        tag, src = m.group(0), m.group(1)
        w, h = dim(src)
        tag = re.sub(r'\s+(?:width|height)="\d+"', "", tag)
        return tag[:-1].rstrip() + ' width="%d" height="%d">' % (w, h)
    return IMG_SRC.sub(one, html)


def write(name, title, desc, body, cta=True):
    html = head(title, desc, name) + topbar() + header(name) + body + (CTA if cta else "") + FOOTER
    html = size_images(html)
    with io.open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("wrote", name, len(html))


CLIENTS = """
  <!-- ===== Clients ===== -->
  <section class="clients section--white" id="clients" aria-label="Clients">
    <div class="container">
      <p class="clients__label">Trusted across Zimbabwe</p>
      <div class="marquee">
        <div class="marquee__track">
          <div class="marquee__group">
            <a href="about.html#clients" aria-label="Ecobank, a Sentinel client"><img src="assets/img/clients/ecobank.png" alt="Ecobank" loading="lazy"></a>
            <a href="about.html#clients" aria-label="Green Fuel, a Sentinel client"><img src="assets/img/clients/green-fuel.png" alt="Green Fuel" loading="lazy"></a>
            <a href="about.html#clients" aria-label="ProBrands, a Sentinel client"><img src="assets/img/clients/probrands.png" alt="ProBrands" loading="lazy"></a>
            <a href="about.html#clients" aria-label="Cottco Holdings, a Sentinel client"><img src="assets/img/clients/cottco.png" alt="Cottco Holdings Limited" loading="lazy"></a>
          </div>
          <div class="marquee__group" aria-hidden="true">
            <a href="about.html#clients" tabindex="-1"><img src="assets/img/clients/ecobank.png" alt="" loading="lazy"></a>
            <a href="about.html#clients" tabindex="-1"><img src="assets/img/clients/green-fuel.png" alt="" loading="lazy"></a>
            <a href="about.html#clients" tabindex="-1"><img src="assets/img/clients/probrands.png" alt="" loading="lazy"></a>
            <a href="about.html#clients" tabindex="-1"><img src="assets/img/clients/cottco.png" alt="" loading="lazy"></a>
          </div>
        </div>
      </div>
    </div>
  </section>
"""

STEPS = [
    ("01", "Survey", "We walk the site with you and write up where you are exposed. This costs you nothing, whether or not you go ahead with us."),
    ("02", "Specify", "You get the camera positions, cable routes, power requirements and coverage in writing, with a price against each line."),
    ("03", "Install", "Our own technicians do the work, commission the system and train whoever will be using it every day."),
    ("04", "Maintain", "Servicing on a schedule, health checks on the equipment, and a number you can call at any hour."),
]

def steps_block():
    out = '      <div class="steps">\n'
    for n, t, p in STEPS:
        out += ('        <a class="step" href="contact.html" data-reveal>'
                '<span class="step__n num">%s</span>'
                '<h3>%s</h3><p>%s</p></a>\n' % (n, t, p))
    return out + "      </div>\n"


# ================================================================= HOME
home = """
  <!-- ===== Hero ===== -->
  <section class="hero">
    <div class="hero__media" aria-hidden="true" data-hero-carousel>
      <div class="hero__slide is-active" style="--pos:72%% 34%%;--expo:2.45">
        <img  src="assets/img/photos/control-room-monitoring-1200.jpg"
             srcset="assets/img/photos/control-room-monitoring-640.jpg 640w, assets/img/photos/control-room-monitoring-1200.jpg 1200w"
             sizes="100vw" alt="An operator watching a wall of live camera feeds" width="1200" height="608" fetchpriority="high">
      </div>
      <div class="hero__slide" style="--pos:58%% 38%%;--expo:0.95">
        <img data-slide-src data-src="assets/img/photos/security-officers-1200.jpg"
             data-srcset="assets/img/photos/security-officers-640.jpg 640w, assets/img/photos/security-officers-1200.jpg 1200w"
             sizes="100vw" alt="A security officer on post at a public event" width="1200" height="608">
      </div>
      <div class="hero__slide" style="--pos:70%% 40%%;--expo:0.64">
        <img data-slide-src data-src="assets/img/photos/technician-panel-1200.jpg"
             data-srcset="assets/img/photos/technician-panel-640.jpg 640w, assets/img/photos/technician-panel-1200.jpg 1200w"
             sizes="100vw" alt="A technician wiring an electrical panel on site" width="1200" height="608">
      </div>
      <div class="hero__slide" style="--pos:64%% 34%%;--expo:0.90">
        <img data-slide-src data-src="assets/img/photos/operator-night-shift-1200.jpg"
             data-srcset="assets/img/photos/operator-night-shift-640.jpg 640w, assets/img/photos/operator-night-shift-1200.jpg 1200w"
             sizes="100vw" alt="A monitoring desk on night shift" width="1200" height="608">
      </div>
    </div>
    <div class="hero__unify" aria-hidden="true"></div>
    <div class="hero__vignette" aria-hidden="true"></div>
    <div class="hero__grid" aria-hidden="true"></div>
    <div class="hero__scrim"></div>

    <div class="container">
      <div class="hero__content">
        <a class="hero__badge" href="about.html#recognition">
          <span class="stars">%s%s%s</span>
          Award winning in <b class="num">2014, 2015 and 2016</b>
        </a>

        <h1 class="h-hero">Your <span class="accent-lime">security</span><br>is our business</h1>

        <p class="hero__lead">
          Three companies across Zimbabwe: the systems that watch a site, the officers
          who hold it, and the technology that connects both.
        </p>

        <div class="hero__actions">
          %s
          <dl class="hero__call">
            <a class="rbtn" href="tel:+263773589461" aria-label="Call Sentinel">%s</a>
            <div><dt>Call us</dt><dd class="num">+263 77 358 9461</dd></div>
          </dl>
        </div>

        <dl class="hero__facts">
          <div class="hero__fact"><dt class="num">3</dt><dd>Companies</dd></div>
          <div class="hero__fact"><dt class="num">10</dt><dd>Provinces</dd></div>
          <div class="hero__fact"><dt class="num">24/7</dt><dd>Response</dd></div>
          <div class="hero__fact"><dt class="num">2016</dt><dd>Since</dd></div>
        </dl>

        <div class="hero__dots" data-hero-dots>
          <button class="hero__dot is-active" type="button" data-hero-dot aria-label="Show image 1 of 4"></button>
          <button class="hero__dot" type="button" data-hero-dot aria-label="Show image 2 of 4"></button>
          <button class="hero__dot" type="button" data-hero-dot aria-label="Show image 3 of 4"></button>
          <button class="hero__dot" type="button" data-hero-dot aria-label="Show image 4 of 4"></button>
        </div>
      </div>
    </div>
  </section>
""" % (STAR, STAR, STAR, pbtn("Book a free site survey", "contact.html"),
       icon("phone-call", "i-md")) + CLIENTS + """
  <!-- ===== The group ===== -->
  <section class="section section--cream ruled" id="group">
    <div class="container">
""" + shead("One group, three companies",
            "Everything a site needs, under one roof",
            cta=pbtn("See the structure", "group.html", "pbtn--dark"),
            variant="shead--wide") + org_chart() + """    </div>
  </section>
  <!-- ===== Approach ===== -->
  <section class="section section--cream ruled">
    <div class="container">
""" + shead("Our approach",
            "Residential, commercial and industrial",
            "Every job starts with a site survey and ends with a maintenance plan, whether "
            "it is three cameras on a house or a factory perimeter.") + """
      <div class="grid g-3">
""" + ncard("white", "house-line", "Residential",
            "Alarms, cameras, gate motors and lighting for the house and the wall around it.",
            ["Intruder alarm on call day and night", "CCTV you can check from your phone",
             "Electric gate motors", "Driveway lighting"],
            "services.html#residential") + ncard("lime", "buildings", "Commercial",
            "Offices, shops and shared buildings where staff and visitors move through all day.",
            ["Security design and installation", "Biometric and card access control",
             "Turnstiles and boom gates", "Systems talking to each other"],
            "services.html#commercial") + ncard("dark", "factory", "Industrial",
            "Plant, yard and logistics sites that need cameras, plate readers and gate control working as one.",
            ["Video management systems", "Number plate readers",
             "Gate automation and parking", "Health monitoring on devices"],
            "services.html#industrial") + """      </div>
    </div>
  </section>

  <!-- ===== Who we are ===== -->
  <section class="section section--white">
    <div class="container split">
      <div class="bento" data-reveal>
        <a class="bento__hero" href="about.html" aria-label="About Sentinel">
          <img src="assets/img/photos/officer-radio-1200.jpg"
               srcset="assets/img/photos/officer-radio-640.jpg 640w, assets/img/photos/officer-radio-1200.jpg 1200w"
               sizes="(max-width:980px) 100vw, 45vw" alt="An officer coordinating a site by radio">
        </a>
        <a class="bento__stat" href="contact.html">
          %s
          <strong class="num">24/7</strong>
          <span>Someone on the phone<br>at any hour</span>
        </a>
        <a class="bento__tile" href="services.html#access" aria-label="Access control">
          <img src="assets/img/photos/tile-access-640.jpg"
               alt="A facial recognition reader at an entrance">
        </a>
      </div>

      <div data-reveal>
        %s
        <h2 class="h-2">One group, one number to call</h2>
        <p class="lead">
          An accredited Zimbabwean group covering electronic security, guarding
          operations and the technology that ties them together.
        </p>
        <p>
          Our own technicians and our own officers do the work, then stay on to maintain
          it. You call us, not four contractors.
        </p>

        <div class="byline">
          %s
          <a class="byline__person" href="about.html">
            <span class="byline__avatar">%s</span>
            <span>
              <strong>Accredited and insured</strong>
              <span>Based in Harare, working countrywide</span>
            </span>
          </a>
        </div>

        <div class="grid g-2" style="margin-top:2.25rem">
          <a class="ministat" href="about.html#recognition">
            <div class="ministat__stars">%s%s%s%s%s</div>
            <div class="ministat__num num">3</div>
            <p class="ministat__label">Best Service Award<br><span class="muted num" style="font-weight:500">2014, 2015 and 2016</span></p>
          </a>
          <div class="ministat">
            <h3>Where we work</h3>
            <div class="tags">
              <a href="#corporate">Corporate</a><a href="#banking">Banking</a><a href="#government">Government</a>
              <a href="#manufacturing">Manufacturing</a><a href="#construction">Construction</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ===== Services ===== -->
  <section class="section section--cream" id="services">
    <div class="container">
""" % (duo("check-circle", "i-xl"), eyebrow("Who we are"),
       pbtn("More about us", "about.html"),
       duo("shield-check", "i-md"), STAR, STAR, STAR, STAR, STAR) + shead(
    "Our services",
    "The systems we install and look after",
    cta=pbtn("See all services", "services.html", "pbtn--dark")) + """
      <div class="grid g-3">
"""

# The six cards on the home page are the six capabilities of the technologies
# company, read straight from the group data so the anchors cannot drift.
SERVICES = [(d["id"], d["icon"], d["name"], d["line"], d["items"][:3])
            for d in by_id("technologies")["divisions"]]

for anchor, ico, title, text, bullets in SERVICES:
    home += """        <article class="card card--hoverdark" data-reveal>
          <span class="card__icon">%s</span>
          <h3 class="h-4">%s</h3>
          <p>%s</p>
          <ul class="card__list">%s</ul>
          <a class="plink" href="services.html#%s">Read more %s</a>
        </article>
""" % (si(ico, "i-xl"), title, text, "".join("<li>%s</li>" % b for b in bullets), anchor, ARROW)

home += """      </div>
    </div>
  </section>

  <!-- ===== Process ===== -->
  <section class="section section--dark ruled">
    <div class="container">
""" + shead("How we work", "From the first call to the handover",
            "The same four stages on every job. You see the specification and the price "
            "before any work starts.",
            kv="eyebrow--dark") + steps_block() + """    </div>
  </section>

  <!-- ===== Sectors ===== -->
  <section class="section section--white" id="sectors">
    <div class="container">
""" + shead("Who we work for", "Where our systems run every day",
            "Banks, factories, government departments, building sites and homes. Most of "
            "our work sits in the five below.") + """
      <div class="rows">
"""

SECTOR_IDS = ["corporate", "banking", "government", "manufacturing", "construction"]
SECTORS = [
 ("Corporate offices", "Reception access control, visitor passes, cover on boardrooms and server rooms, cameras across every floor."),
 ("Banking and financial services", "Man traps, strongroom interlocks, cameras over cash handling, and recordings kept long enough to satisfy an audit."),
 ("Government", "High security and anti terror access equipment, controlled perimeters and control room operation."),
 ("Manufacturing and industry", "Plate readers on weighbridges and gates, cameras over the yard, time and attendance across shifts."),
 ("Construction", "Cameras up quickly on a new site, cover on plant and materials, and access control that moves as the build moves."),
]
for i, (t, p) in enumerate(SECTORS, 1):
    home += """        <a class="row" id="%s" href="contact.html" data-reveal>
          <span class="row__n num">%02d</span>
          <span class="row__body"><h3>%s</h3><p>%s</p></span>
          <span class="row__go" aria-hidden="true">%s</span>
        </a>
""" % (SECTOR_IDS[i - 1], i, t, p, ARROW)

home += """      </div>
    </div>
  </section>

  <!-- ===== Solar ===== -->
  <section class="section section--lime ruled">
    <div class="container split">
      <div data-reveal>
        %s
        <h2 class="h-2">Solar PV for homes, businesses and power plants</h2>
        <p class="script script--lg">keeping the cameras on when the grid is off</p>
        <p class="lead" style="color:var(--ink-2)">
          One of the leading solar PV companies in Zimbabwe. We handle the build, then the
          maintenance that keeps the panels producing.
        </p>
        <div style="margin-top:2rem">%s</div>
      </div>
      <div class="grid g-2" data-reveal>
        <a class="ministat" href="renewable-energy.html" style="background:var(--g-dark);color:var(--on-dark-soft)">
          <span class="card__icon" style="background:rgba(255,255,255,.1);color:var(--lime)">%s</span>
          <h3 style="color:#fff">Durability</h3>
          <p style="color:var(--on-dark-soft);font-size:.93rem;margin:0">Built for dust, heat, storms and the load an actual Zimbabwean site puts on them.</p>
        </a>
        <a class="ministat" href="renewable-energy.html" style="background:var(--white)">
          <span class="card__icon">%s</span>
          <h3>Reliability</h3>
          <p style="font-size:.93rem;margin:0">Panels that perform without compromise, backed by a service schedule.</p>
        </a>
        <a class="ministat" href="renewable-energy.html" style="background:var(--white)">
          <span class="card__icon">%s</span>
          <h3>Output</h3>
          <p style="font-size:.93rem;margin:0">More energy over the life of the system, so the saving stays predictable.</p>
        </a>
        <a class="ministat" href="renewable-energy.html" style="background:var(--g-mid);color:rgba(255,255,255,.78)">
          <span class="card__icon" style="background:rgba(255,255,255,.14);color:#fff">%s</span>
          <h3 style="color:#fff">Maintenance</h3>
          <p style="color:rgba(255,255,255,.78);font-size:.93rem;margin:0">Cleaning, string checks and battery health on a fixed schedule.</p>
        </a>
      </div>
    </div>
  </section>
""" % (eyebrow("Renewable energy", "eyebrow--lime"),
       pbtn("Look at solar", "renewable-energy.html", "pbtn--dark"),
       duo("shield-check", "i-lg"), duo("sun", "i-lg"), duo("lightning", "i-lg"), duo("wrench", "i-lg"))

write("index.html",
      "Sentinel Integrated Technologies | Electronic Security in Zimbabwe",
      "CCTV, intruder alarms, access control, fire detection and physical access control across Zimbabwe. Based in Harare, support at any hour, award winning in 2014, 2015 and 2016.",
      home)


# ================================================================= ABOUT
about = phero("About", "A decade of guarding, turned into a group",
  "Sentinel started in 2016 with officers on gates. The technology work grew out of that, "
  "and in 2026 it became a company of its own. Three businesses now, built on the same ten "
  "years of ground truth.",
  "officer-on-duty", "A Sentinel officer on foot patrol") + """
  <section class="section section--white">
    <div class="container split">
      <div class="bento" data-reveal>
        <a class="bento__hero" href="services.html" aria-label="Our services">
          <img src="assets/img/photos/security-officers-1200.jpg"
               srcset="assets/img/photos/security-officers-640.jpg 640w, assets/img/photos/security-officers-1200.jpg 1200w"
               sizes="(max-width:980px) 100vw, 45vw" alt="A security officer on post">
        </a>
        <a class="bento__tile" href="services.html#cctv" aria-label="CCTV surveillance">
          <img src="assets/img/photos/tile-night-640.jpg"
               alt="A monitoring desk on night shift">
        </a>
        <a class="bento__stat" href="index.html#sectors">
          %s
          <strong class="num">5</strong>
          <span>Sectors we work in<br>every week</span>
        </a>
      </div>

      <div data-reveal>
        %s
        <h2 class="h-2">How the group came about</h2>
        <p class="lead">
          We work for organisations that cannot afford a gap in cover: offices, banks,
          government departments, factories and building sites.
        </p>
        <p>
          Guarding came first. Covering those sites meant learning cameras, alarms and access
          control properly, and that work outgrew the guarding business. So we gave it a
          company of its own.
        </p>
        <p>
          Each business now holds its own staff, stock and service schedule. The group exists
          so a client who needs all three still deals with one number.
        </p>
        <div class="tags" style="margin-top:1.75rem">
          <a href="#recognition">Accredited Zimbabwean firm</a><a href="contact.html">Based in Harare</a>
          <a href="group.html">Three operating companies</a><a href="contact.html">Support at any hour</a>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--cream ruled">
    <div class="container">
""" % (duo("scan-smiley", "i-xl"), eyebrow("Who we are")) + shead(
  "The structure", "Three companies, one standard",
  cta=pbtn("See the structure", "group.html", "pbtn--dark"),
  variant="shead--wide") + org_chart(compact=True) + """    </div>
  </section>

  <section class="section section--white">
    <div class="container">
""" + shead("Who runs it", "The people accountable for it") + """
      <div class="grid g-2">
""" + "".join("""        <article class="leader" data-reveal>
          <div class="leader__head">
            <span class="leader__ico">%s</span>
            <div>
              <h3 class="h-3">%s</h3>
              <p class="leader__role">%s</p>
            </div>
          </div>
          <p>%s</p>
          <ul class="leader__quals">%s</ul>
        </article>
""" % (si(l["icon"], "i-xl"), l["name"], l["role"], l["line"],
       "".join("<li>%s</li>" % q for q in l["quals"])) for l in LEADERS) + """      </div>
    </div>
  </section>

  <section class="section section--cream">
    <div class="container">
""" + shead(
  "What drives us", "Mission, vision and values",
  "Three statements we are happy to be held to.") + """
      <div class="grid g-3">
""" + ncard("white", "target", "Mission",
            "Reliable, professional security within a legal and ethical framework, so clients "
            "have peace of mind. Scalable solutions, priced so they can actually be bought.",
            [], "contact.html", "Talk to us") \
    + ncard("lime", "compass", "Vision",
            "A customer centred market leader in integrated security, and a smarter, safer, "
            "better connected future for the places we work in.",
            [], "group.html", "See the group") \
    + ncard("dark", "shield-check", "Values",
            "Integrity, commitment, innovation, quality and excellence. We set our standards by "
            "what clients expect, then try to beat it.",
            [], "contact.html", "Work with us") + """      </div>
    </div>
  </section>

  <section class="section section--white">
    <div class="container">
""" + shead("Why clients stay", "Six things we will not cut corners on",
            "Not selling points. The standard every job is held to.") + """
      <div class="grid g-3">
"""

WHY = [
 ("clock-countdown", "We turn up when we said",
  "Our people arrive at the time we gave you, in uniform, with the right parts on the vehicle. A missed appointment is a failure like any other."),
 ("graduation-cap", "Training does not stop",
  "Threats change and so does the equipment. Our technicians keep training on what we install, rather than learning it once."),
 ("tag", "Prices you can pick apart",
  "We quote the system your risk calls for, line by line, so you can question any of it. No lump sums."),
 ("magnifying-glass", "Independent auditing",
  "We assess and audit security risk, including systems we did not install. If yours is good enough, we will say so."),
 ("headset", "Someone answers at 2am",
  "A system nobody can fix overnight protects nothing. Our support runs the same hours your risk does."),
 ("handshake", "One company, start to finish",
  "Design, supply, installation and maintenance all sit with us, so there is nobody to point at."),
]
for ico, t, p in WHY:
    about += """        <a class="card card--hoverdark" href="contact.html" data-reveal>
          <span class="card__icon">%s</span>
          <h3 class="h-4">%s</h3>
          <p>%s</p>
          <span class="plink">Talk to us %s</span>
        </a>
""" % (duo(ico, "i-lg"), t, p, ARROW)

about += """      </div>
    </div>
  </section>

  <section class="section section--dark" id="recognition">
    <div class="container">
""" + shead("Recognition", "Best Service Award, three years running",
            "Named Best Service Award in 2014, in 2015 and again in 2016.", kv="eyebrow--dark") + """
      <div class="grid g-3">
        <a class="card card--dark card--hoverlime" href="contact.html" data-reveal>
          <img class="award-mark" src="assets/img/brand/award-2014-white.png" alt="" aria-hidden="true"
               width="120" height="118" loading="lazy">
          <h3 class="h-4 num">2014</h3><p>Best Service Award</p>
        </a>
        <a class="card card--dark card--hoverlime" href="contact.html" data-reveal>
          <img class="award-mark" src="assets/img/brand/award-2015-white.png" alt="" aria-hidden="true"
               width="120" height="118" loading="lazy">
          <h3 class="h-4 num">2015</h3><p>Best Service Award</p>
        </a>
        <a class="card card--dark card--hoverlime" href="contact.html" data-reveal>
          <img class="award-mark" src="assets/img/brand/award-2016-white.png" alt="" aria-hidden="true"
               width="120" height="118" loading="lazy">
          <h3 class="h-4 num">2016</h3><p>Best Service Award</p>
        </a>
      </div>
    </div>
  </section>
""" + CLIENTS

write("about.html",
      "About the Sentinel group | " + ORG,
      "An accredited Zimbabwean security firm supplying electronic security, control room operations and physical access control to corporate, banking, government, manufacturing and construction clients.",
      about)


# ================================================================= SERVICES
DIV_ICON = {d["id"]: d["icon"] for c in COMPANIES for d in c["divisions"]}


def detail(anchor, kicker, title, lead, bullets, photo, alt, flip):
    lis = "".join("<li>%s</li>" % b for b in bullets)
    media = """        <div data-reveal>
          %s
        </div>
""" % photo_img(photo, alt, "(max-width:980px) 100vw, 45vw",
                style="border-radius:var(--corner-xl);aspect-ratio:4/3;object-fit:cover;width:100%")
    text = """        <div data-reveal>
          <span class="dmark">%s</span>
          %s
          <h2 class="h-2" style="font-size:clamp(1.6rem,2.8vw,2.3rem)">%s</h2>
          <p class="lead">%s</p>
          <ul class="card__list" style="margin-top:1.4rem">%s</ul>
          <div style="margin-top:2rem">%s</div>
        </div>
""" % (si(DIV_ICON.get(anchor, "perimeter"), "i-2xl"), eyebrow(kicker), title, lead, lis,
       pbtn("Ask for a quotation", "contact.html"))
    inner = (media + text) if flip else (text + media)
    return """      <div class="split" id="%s" style="scroll-margin-top:calc(var(--header-h) + 28px);padding-block:clamp(2.5rem,5vw,4rem)">
%s      </div>
""" % (anchor, inner)


_tech = by_id("technologies")
services = phero(_tech["role"], _tech["name"], _tech["lead"],
  "sys-access", "A fob presented to a door reader") + """
  <section class="section section--white">
    <div class="container split split--narrow">
      <div data-reveal>
        %s
        <h2 class="h-2">%s</h2>
        <p class="script script--lg">%s</p>
        <p class="lead">%s</p>
        <div style="margin-top:2rem">%s</div>
      </div>
      <div class="cfacts" data-reveal>
        <span class="cfacts__logo">%s</span>
        <div class="cfact"><dt>Part of</dt><dd><a href="group.html">%s, the group</a></dd></div>
        <div class="cfact"><dt>Registered as</dt><dd>%s</dd></div>
        <div class="cfact"><dt>Serves</dt><dd>%s</dd></div>
        <div class="cfact"><dt>How we work</dt><dd>%s</dd></div>
      </div>
    </div>
  </section>
""" % (eyebrow("What we carry"), _tech["headline"], _tech["strap"], _tech["blurb"],
       pbtn("Book a site survey", "contact.html", "pbtn--dark"),
       company_logo(_tech, h=58), PARENT["name"], _tech["legal"],
       ", ".join(_tech["sectors"]), " &rsaquo; ".join(_tech["process"])) + """
  <section class="section section--cream">
    <div class="container">
""" + shead("Where we work", "Three kinds of site, one standard of work",
            "The scope of a job changes with the site. How carefully we specify it does not.") + """
      <div class="grid g-3">
""" + ncard("white", "house-line", "Residential",
            "Alarms, cameras, gate motors and lighting for the house and the wall around it.",
            ["Intruder alarm on call day and night", "CCTV you can check from your phone",
             "Electric gate motors", "Driveway lighting"],
            "contact.html", "Get a price") + ncard("lime", "buildings", "Commercial",
            "Offices, shops and shared buildings where staff and visitors move through all day.",
            ["Security design and installation", "Biometric and card access control",
             "Turnstiles and boom gates", "Systems talking to each other"],
            "contact.html", "Get a price") + ncard("dark", "factory", "Industrial",
            "Plant, yard and logistics sites needing cameras, plate readers and gate control as one system.",
            ["Video management systems", "Number plate readers",
             "Gate automation and parking", "Health monitoring on devices"],
            "contact.html", "Get a price") + """      </div>
    </div>
  </section>

  <section class="section section--white">
    <div class="container">
"""
services = services.replace('<article class="ncard ncard--white"', '<article class="ncard ncard--white" id="residential"', 1)
services = services.replace('<article class="ncard ncard--lime"', '<article class="ncard ncard--lime" id="commercial"', 1)
services = services.replace('<article class="ncard ncard--dark"', '<article class="ncard ncard--dark" id="industrial"', 1)

services += shead("Capabilities", "Six systems, one integrated job",
                  "Each one is something we staff for, train for and keep stock for.")

DETAILS = [
 ("cctv", "Surveillance", "CCTV and video surveillance",
  "Camera systems for homes and businesses, laid out around your actual blind spots, sightlines "
  "and lighting rather than a standard drawing.",
  ["IP and analogue cameras", "Remote viewing from anywhere",
   "Recording and playback", "Camera upgrades on an existing cable run",
   "Optics that work after dark"],
  "sys-cctv", "A dome camera on a wall bracket"),
 ("alarms", "Detection", "Intruder and alarm systems",
  "Systems meant to put someone off before they get in, and to record an incident already under way "
  "so you have something to act on afterwards.",
  ["Motion sensors and perimeter beams", "Door and window contacts",
   "Panic and duress buttons", "Zones you can arm separately",
   "Battery backup through an outage"],
  "sys-alarms", "An external alarm sounder on a building"),
 ("access", "Identity", "Access control and man traps",
  "Door control for a small business upward, making a building both safer and easier to move "
  "around, from one reception door to a group of sites.",
  ["Biometric, card and PIN readers", "Door controllers and interlocks",
   "Man traps for cash areas and strongrooms", "Visitor management and temporary codes",
   "Time and attendance integration"],
  "access-terminal", "Access control at a reception desk"),
 ("gates", "Vehicles", "Gate automation and vehicle control",
  "The gate is the first thing a site is judged on and the first thing that fails, so we fit "
  "motors rated for the traffic you actually put through them.",
  ["Automatic gates and gate motors", "Boom gates and road blockers",
   "Turnstiles and pedestrian lanes", "Safety sensors and remote access",
   "Number plate driven entry"],
  "sys-gates", "The motor and gear rack on a sliding gate"),
 ("intercoms", "Entry", "Video intercoms",
  "See who is at the gate before you open it, from the house, the office or a phone anywhere "
  "with a signal.",
  ["Audio and video door stations", "Residential and estate intercoms",
   "Commercial entry systems", "Visitor identification",
   "Wired to the access control system"],
  "sys-intercom", "A video door station beside an entrance"),
 ("fire", "Life safety", "Fire detection and perimeter",
  "Fire sensors that buy people time to get out, and an energised perimeter that holds the line "
  "while help is on the way.",
  ["Addressable and conventional panels", "Smoke, heat and flame detection",
   "Sounders and evacuation systems", "Electric fencing and perimeter beams",
   "Testing and certification on a schedule"],
  "sys-fire", "A fire sounder and call point on a ceiling"),
]
for i, d in enumerate(DETAILS):
    services += detail(*d, flip=(i % 2 == 1))

services += """    </div>
  </section>

  <section class="section section--dark ruled">
    <div class="container">
""" + shead("How we work", "From the first call to the handover",
            "Four stages, the same on every job whatever the scale.", kv="eyebrow--dark") + steps_block() + """    </div>
  </section>

  <section class="section section--cream">
    <div class="container container--narrow">
""" + shead("Questions", "Things people ask us first", "", variant="shead--center") + """
      <div class="accordion" data-reveal>
"""

FAQ = [
 ("Do you charge for the site survey?",
  "No. The survey and the risk assessment are free anywhere we work in Zimbabwe, and you keep the written specification either way."),
 ("Can you work on a system another company installed?",
  "Yes. We audit, repair, extend and take over maintenance on existing systems. If yours is sound we will say so, rather than sell you a new one."),
 ("Do you cover sites outside Harare?",
  "We are based in Eastlea, Harare, and work countrywide. Tell us where the site is and we will confirm travel and response times up front."),
 ("What happens when the power goes out?",
  "Every system we design has battery backup sized to your risk. For long outages we add solar through our renewable energy division."),
 ("Can I view my cameras remotely?",
  "Yes, securely, on a phone or a desktop. Permissions are set per user, so staff only see the cameras they are supposed to."),
]
for i, (q, a) in enumerate(FAQ, 1):
    services += """        <div class="acc__item">
          <h3 style="margin:0">
            <button class="acc__btn" type="button" aria-expanded="false" aria-controls="faq%d">
              %s<span class="acc__icon" aria-hidden="true"></span>
            </button>
          </h3>
          <div class="acc__panel" id="faq%d" data-open="false"><div><p>%s</p></div></div>
        </div>
""" % (i, q, i, a)

services += """      </div>
    </div>
  </section>
"""

services += siblings("technologies")

write("services.html",
      "Sentinel Integrated Technologies: CCTV, alarms, access control and fire | " + ORG,
      "CCTV and video surveillance, intruder alarms, access control and man traps, gate "
      "automation, video intercoms and fire detection, designed and installed as one system "
      "across Zimbabwe.",
      services)


# ================================================================= SOLAR
solar = phero("Renewable Energy", "Solar PV for homes, businesses and power plants",
  "One of the leading solar PV companies in Zimbabwe. We handle the engineering, "
  "procurement and construction, then the maintenance that keeps it producing.") + """
  <section class="section section--white">
    <div class="container split">
      <div data-reveal>
        %s
        <h2 class="h-2">Panels that keep your bill down and your site running</h2>
        <p class="script script--lg">towards a #secure world</p>
        <p class="lead">
          Cutting a bill and surviving an outage are the same job. We size, supply and
          maintain systems that carry the loads you actually run.
        </p>
        <p>
          That covers the whole life of the system, from design and procurement through to
          the servicing that holds output to the business case.
        </p>
        <div style="margin-top:2rem">%s</div>
      </div>
      <div data-reveal>
        <img src="assets/img/photos/power-solar-1200.jpg"
             srcset="assets/img/photos/power-solar-640.jpg 640w, assets/img/photos/power-solar-1200.jpg 1200w"
             sizes="(max-width:980px) 100vw, 45vw"
             style="border-radius:var(--corner-xl);aspect-ratio:3/2;object-fit:cover;width:100%%"
             alt="A rooftop solar array above a city" width="1200" height="800" loading="lazy">
      </div>
    </div>
  </section>

  <section class="section section--cream">
    <div class="container">
""" % (eyebrow("Solar PV"), pbtn("Ask for a solar assessment", "contact.html")) + shead(
  "Why Sentinel solar", "Three things a system gets judged on",
  "Once the installers have gone, this is what you are left with.") + """
      <div class="grid g-3">
""" + ncard("white", "shield-check", "Durability",
            "Built for real conditions: dust, heat, storms and the load profile of an "
            "actual Zimbabwean site.",
            [], "contact.html", "Talk to us") \
    + ncard("lime", "sun", "Reliability",
            "Panels that perform without compromise, backed by a service schedule rather "
            "than a handshake.",
            [], "contact.html", "Talk to us") \
    + ncard("dark", "lightning", "Output",
            "More energy over the life of the system, so the saving you were promised holds "
            "up.",
            [], "contact.html", "Talk to us") + """      </div>
    </div>
  </section>

  <section class="section section--dark">
    <div class="container">
""" + shead("What we deliver", "Building it, then keeping it producing",
            "One contract for the build. One for everything after it.", kv="eyebrow--dark") + """
      <div class="grid g-2">
        <a class="card card--dark card--hoverlime" href="contact.html" data-reveal>
          <span class="card__icon">%s</span>
          <h3 class="h-3">Solar PV EPC</h3>
          <p>Everything under one contract: yield modelling, electrical design, installation, grid or hybrid integration, then commissioning.</p>
          <ul class="card__list">
            <li>Load audit and yield modelling</li>
            <li>Array, inverter and storage sizing</li>
            <li>Structural mounting and cabling</li>
            <li>Commissioning and training</li>
          </ul>
          <span class="plink">Ask for a quotation %s</span>
        </a>
        <a class="card card--dark card--hoverlime" href="contact.html" data-reveal>
          <span class="card__icon">%s</span>
          <h3 class="h-3">Operations and maintenance</h3>
          <p>The part most installers skip. Panels get dirty, strings drift and batteries age, so servicing is what keeps output up.</p>
          <ul class="card__list">
            <li>Scheduled cleaning and checks</li>
            <li>Performance monitoring</li>
            <li>Inverter and battery health checks</li>
            <li>Fault response and spares</li>
          </ul>
          <span class="plink">Ask for a quotation %s</span>
        </a>
      </div>
    </div>
  </section>

  <section class="section section--white">
    <div class="container">
""" % (duo("solar-panel", "i-lg"), ARROW, duo("wrench", "i-lg"), ARROW) + shead(
  "Who we power", "Three markets, the same engineering") + """
      <div class="rows">
"""
for i, (t, p) in enumerate([
  ("Homes", "Bring the bill down and ride out load shedding without a generator, with the alarm, gate motor and cameras still live."),
  ("Businesses", "Offices, shops, warehousing and light industry. Lower running costs, and trading hours that survive a grid interruption."),
  ("Power plants", "Utility scale Solar PV as a full EPC package, with a maintenance contract that holds performance to the model."),
], 1):
    solar += """        <a class="row" href="contact.html" data-reveal>
          <span class="row__n num">%02d</span>
          <span class="row__body"><h3>%s</h3><p>%s</p></span>
          <span class="row__go" aria-hidden="true">%s</span>
        </a>
""" % (i, t, p, ARROW)

solar += """      </div>
    </div>
  </section>

  <section class="section section--cream">
    <div class="container">
""" + shead("Renewable energy division", "Talk to the solar team directly") + """
      <div class="grid g-2">
        <div class="office" data-reveal>
          <h3>Sunway City</h3>
          <p>870 Marula Road, Sunway City, Harare</p>
          <a href="tel:+263783248006" class="num">+263 783 248 006</a>
          <a href="tel:+263242006157" class="num">+263 24 200 6157</a>
          <a href="mailto:info@sentinel.co.zw">info@sentinel.co.zw</a>
        </div>
        <div class="office" data-reveal>
          <h3>Head office, Eastlea</h3>
          <p>29 Tweed Road, Eastlea, Harare</p>
          <a href="tel:+263773589461" class="num">+263 77 358 9461</a>
          <a href="tel:+263772568361" class="num">+263 77 256 8361</a>
          <a href="mailto:info@sentinel.co.zw">info@sentinel.co.zw</a>
        </div>
      </div>
    </div>
  </section>
"""

write("renewable-energy.html",
      "Renewable Energy: Solar PV in Zimbabwe | Sentinel Integrated Technologies",
      "Solar PV engineering, procurement and construction, plus operations and maintenance, for homes, businesses and power plants in Zimbabwe.",
      solar)



# ================================================================= THE GROUP
def group_detail(c, ground):
    """A company in full: what it is, then every capability it carries."""
    rows = ""
    for i, d in enumerate(c["divisions"], 1):
        rows += """          <a class="drow" href="%s#%s" data-reveal>
            <span class="drow__n num">%02d</span>
            <span class="drow__ico">%s</span>
            <span class="drow__body">
              <h4>%s</h4>
              <p>%s</p>
            </span>
            <span class="drow__go" aria-hidden="true">%s</span>
          </a>
""" % (c["href"], d["id"], i, si(d["icon"], "i-lg"), d["name"],
       ", ".join(d["items"][:4]) + ".", ARROW)

    units = ""
    if c.get("units"):
        units = """          <div class="gdetail__units">%s</div>
""" % "".join("""<a class="gunit" href="%s#%s">%s<span><strong>%s</strong><small>%s</small></span></a>"""
              % (c["href"], u["id"], si(u["icon"], "i-md"), u["name"], u["strap"])
              for u in c["units"])

    kv = "eyebrow--dark" if ground == "dark" else ""
    return """  <section class="section section--%s" id="%s">
    <div class="container">
%s      <div class="gdetail">
        <div class="gdetail__intro" data-reveal>
          <span class="gdetail__logo">%s</span>
          <p class="gdetail__legal">%s</p>
          <p class="lead">%s</p>
          <p class="script gdetail__strap">%s</p>
          <dl class="gdetail__meta">
            <div><dt>Serves</dt><dd>%s</dd></div>
            <div><dt>How it works</dt><dd>%s</dd></div>
          </dl>
          <div style="margin-top:1.75rem">%s</div>
        </div>
        <div class="gdetail__rows">
%s        </div>
      </div>
%s    </div>
  </section>
""" % (ground, c["id"],
       shead(c["role"], c["name"], kv=kv),
       company_logo(c, h=52, white=(ground == "dark")),
       c["legal"], c["lead"], c["strap"],
       ", ".join(c["sectors"]), " &rsaquo; ".join(c["process"]),
       pbtn("Open " + c["short"], c["href"],
            "pbtn--light" if ground == "dark" else "pbtn--dark"),
       rows, units)


grp = phero("The group", "Three companies, one standard of work",
  "Sentinel runs as a group. One company builds the electronic systems, one runs the "
  "people on the ground, and one carries the technology business. This is how they "
  "fit together.",
  "control-room-monitoring", "The Sentinel control room during a night shift") + """
  <section class="section section--white">
    <div class="container">
""" + shead("The structure", "What sits where",
            "Each company holds its own licences, staff and discipline. The group "
            "exists so a client needs one number, not three.",
            variant="shead--wide") + org_chart() + """    </div>
  </section>
"""

for _c, _g in zip(COMPANIES, ["cream", "dark", "white"]):
    grp += group_detail(_c, _g)

grp += """  <section class="section section--cream">
    <div class="container">
""" + shead("Who runs it", "The people accountable for it") + """
      <div class="grid g-2">
""" + "".join("""        <article class="leader" data-reveal>
          <div class="leader__head">
            <span class="leader__ico">%s</span>
            <div>
              <h3 class="h-3">%s</h3>
              <p class="leader__role">%s</p>
            </div>
          </div>
          <p>%s</p>
          <ul class="leader__quals">%s</ul>
        </article>
""" % (si(l["icon"], "i-xl"), l["name"], l["role"], l["line"],
       "".join("<li>%s</li>" % q for q in l["quals"])) for l in LEADERS) + """      </div>
    </div>
  </section>
"""

write("group.html",
      "The Sentinel group: three companies under one standard | " + ORG,
      "Sentinel Integrated Technologies, Sentinel Security Services and Circuitron "
      "Systems: how the Sentinel group is structured and what each company does.",
      grp)


# ============================================================= COMPANY PAGES
def company_page(cid, hero_photo, hero_alt, title, desc):
    c = by_id(cid)
    body = phero(c["role"], c["name"], c["lead"], hero_photo, hero_alt) + """
  <section class="section section--white">
    <div class="container split split--narrow">
      <div data-reveal>
        %s
        <h2 class="h-2">%s</h2>
        <p class="script script--lg">%s</p>
        <p class="lead">%s</p>
        <div style="margin-top:2rem">%s</div>
      </div>
      <div class="cfacts" data-reveal>
        <span class="cfacts__logo">%s</span>
        <div class="cfact"><dt>Part of</dt><dd><a href="group.html">%s, the group</a></dd></div>
        <div class="cfact"><dt>Registered as</dt><dd>%s</dd></div>
        <div class="cfact"><dt>Serves</dt><dd>%s</dd></div>
        <div class="cfact"><dt>How we work</dt><dd>%s</dd></div>
      </div>
    </div>
  </section>

  <section class="section section--cream ruled">
    <div class="container">
""" % (eyebrow("What we carry"), c["headline"], c["strap"], c["blurb"],
       pbtn("Book a site survey", "contact.html", "pbtn--dark"),
       company_logo(c, h=58),
       PARENT["name"], c["legal"], ", ".join(c["sectors"]),
       " &rsaquo; ".join(c["process"])) + shead(
        "Capabilities", "What this company does",
        "%s lines of work, each with its own team and its own spares."
        % NUMBER_WORD[len(c["divisions"])],
        variant="shead--wide") + """
      <div class="dgrid">
""" + "".join(division_card(c, d) for d in c["divisions"]) + """      </div>
    </div>
  </section>
"""
    if c.get("units"):
        body += """  <section class="section section--dark">
    <div class="container">
""" + shead("The ecosystem", "Two businesses inside the business",
            "Circuitron reaches the market two more ways: a shop and a recycling "
            "route.", kv="eyebrow--dark") + """
      <div class="grid g-2">
""" + "".join(unit_panel(c, u) for u in c["units"]) + """      </div>
    </div>
  </section>
"""
    body += siblings(cid)
    write(c["href"], title, desc, body)


company_page("guarding", "security-officers",
  "A Sentinel officer on post at a public event",
  "Sentinel Security Services: manned guarding, dog units and armed response | " + ORG,
  "Manned guarding, event security, 24 hour alarm monitoring and armed response, dog "
  "units, perimeter protection and investigations across all ten provinces of Zimbabwe.")

company_page("circuitron", "circuitron-bench",
  "Patch cabling in a Circuitron network cabinet",
  "Circuitron Systems: technology, communications and electronics | " + ORG,
  "Circuitron Systems delivers security systems, two way radio and networking, smart "
  "building automation, computers and power, plus CircuitStore retail and EcoCircuit "
  "electronic waste recovery.")

# ================================================================= CONTACT
contact = phero("Contact", "Tell us about your site",
  "A free survey and risk assessment, anywhere in Zimbabwe. Send the details and our "
  "technical team will come back to you.",
  "technician-panel", "A technician checking a site on a tablet") + """
  <section class="section section--white">
    <div class="container contact-grid">
      <div data-reveal>
        %s
        <h2 class="h-2" style="font-size:clamp(1.7rem,2.8vw,2.3rem)">Head office</h2>

        <div class="cinfo">
          <span class="cinfo__icon">%s</span>
          <div><h3>Address</h3><p>29 Tweed Road,<br>Eastlea, Harare, Zimbabwe</p></div>
        </div>
        <div class="cinfo">
          <span class="cinfo__icon">%s</span>
          <div><h3>Telephone</h3>
            <a href="tel:+263773589461" class="num">+263 77 358 9461</a>
            <a href="tel:+263772568361" class="num">+263 77 256 8361</a>
            <a href="tel:+263242006157" class="num">+263 24 200 6157</a>
          </div>
        </div>
        <div class="cinfo">
          <span class="cinfo__icon">%s</span>
          <div><h3>Email</h3><a href="mailto:info@sentinel.co.zw">info@sentinel.co.zw</a></div>
        </div>
        <div class="cinfo">
          <span class="cinfo__icon">%s</span>
          <div><h3>Hours</h3><p class="num">Monday to Friday, 08:00 to 17:00<br><span class="accent">Support runs at any hour</span></p></div>
        </div>

        <div style="margin-top:2rem">%s</div>
      </div>

      <div class="formcard" data-reveal>
        <h2 class="h-3">Ask for a site survey</h2>
        <p class="muted" style="margin-bottom:1.75rem">Free, and no obligation.</p>

        <form data-contact-form novalidate>
          <div class="form-grid">
            <div class="field"><label for="name">Your name</label>
              <input id="name" name="name" type="text" autocomplete="name" placeholder="Tendai Moyo" required></div>
            <div class="field"><label for="company">Company</label>
              <input id="company" name="company" type="text" autocomplete="organization" placeholder="Optional"></div>
            <div class="field"><label for="email">Email</label>
              <input id="email" name="email" type="email" autocomplete="email" placeholder="you@company.co.zw" required></div>
            <div class="field"><label for="phone">Phone</label>
              <input id="phone" name="phone" type="tel" autocomplete="tel" placeholder="+263 77 000 0000"></div>
            <div class="field"><label for="service">What do you need?</label>
              <select id="service" name="service">
                <option>CCTV surveillance</option><option>Intruder alarms</option>
                <option>Access control</option><option>Fire detection</option>
                <option>Man traps</option><option>Physical access control</option>
                <option>Solar and renewable energy</option><option>Security risk assessment</option>
                <option>Something else</option>
              </select></div>
            <div class="field"><label for="location">Site location</label>
              <input id="location" name="location" type="text" placeholder="Harare, Bulawayo, elsewhere"></div>
            <div class="field field--full"><label for="message">Tell us about the site</label>
              <textarea id="message" name="message" placeholder="Size of the property, what is already installed, and what worries you."></textarea></div>
          </div>

          <button class="pbtn pbtn--block" type="submit" style="margin-top:1.5rem">
            <span class="pbtn__label">Send enquiry</span>%s
          </button>
          <p class="form-note">This opens your email app with the details filled in. Prefer to talk? Call <a href="tel:+263773589461" class="num">+263 77 358 9461</a>.</p>
          <p class="form-status" role="status"></p>
        </form>
      </div>
    </div>
  </section>

  <section class="section section--tight section--cream">
    <div class="container">
""" % (eyebrow("Get in touch"),
       duo("map-pin", "i-md"), duo("phone-call", "i-md"),
       duo("envelope-simple", "i-md"), duo("clock", "i-md"),
       pbtn("Message us on WhatsApp", "https://wa.me/263773589461", attrs=' rel="noopener"'),
       CHEV) + shead("Our locations", "Two addresses in Harare") + """
      <div class="grid g-2">
        <div class="office" data-reveal>
          <h3>Head office, Eastlea</h3>
          <p>29 Tweed Road, Eastlea, Harare</p>
          <a href="tel:+263242006157" class="num">+263 24 200 6157</a>
          <a href="mailto:info@sentinel.co.zw">info@sentinel.co.zw</a>
        </div>
        <div class="office" data-reveal>
          <h3>Renewable energy, Sunway City</h3>
          <p>870 Marula Road, Sunway City, Harare</p>
          <a href="tel:+263783248006" class="num">+263 783 248 006</a>
          <a href="mailto:info@sentinel.co.zw">info@sentinel.co.zw</a>
        </div>
      </div>
    </div>
  </section>

  <section class="map-wrap" aria-label="Map of our head office">
    <div class="map-wrap__fallback" aria-hidden="true">
      <strong>29 Tweed Road, Eastlea</strong>
      <span>Harare, Zimbabwe</span>
      <a href="https://www.google.com/maps/search/?api=1&amp;query=29+Tweed+Road%2C+Eastlea%2C+Harare%2C+Zimbabwe" rel="noopener">Open in Google Maps</a>
    </div>
    <iframe class="map-embed"
      src="https://www.google.com/maps?q=29%20Tweed%20Road%2C%20Eastlea%2C%20Harare%2C%20Zimbabwe&output=embed"
      title="Map showing 29 Tweed Road, Eastlea, Harare"
      loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
  </section>
"""

write("contact.html",
      "Contact: Book a Free Site Survey | Sentinel Integrated Technologies",
      "Contact Sentinel Integrated Technologies in Harare, Zimbabwe. Free site survey and security risk assessment. Call +263 77 358 9461 or email info@sentinel.co.zw.",
      contact, cta=False)


# ================================================================= PRIVACY
privacy = phero("Privacy policy", "Privacy policy",
  "How Sentinel Integrated Technologies handles the information you share with us.") + """
  <section class="section section--white">
    <div class="container container--narrow prose">
      <p><em>Last updated: September 2026.</em></p>

      <h2>Who we are</h2>
      <p>Sentinel Integrated Technologies is a security solutions provider registered in Zimbabwe, with
      its head office at 29 Tweed Road, Eastlea, Harare. If you have a question about this
      policy, write to us at <a href="mailto:info@sentinel.co.zw">info@sentinel.co.zw</a>.</p>

      <h2>What we collect</h2>
      <ul>
        <li>The contact details you send through our enquiry form: name, company, email, telephone number and site location.</li>
        <li>The content of your enquiry, including anything you tell us about the site you want secured.</li>
        <li>Basic technical information your browser sends when you visit this website, such as page requests and approximate location.</li>
      </ul>

      <h2>How we use it</h2>
      <ul>
        <li>To answer your enquiry and arrange a site survey.</li>
        <li>To prepare a specification and a quotation.</li>
        <li>To provide support and maintenance if you become a client.</li>
        <li>To meet our legal and contractual obligations.</li>
      </ul>

      <h2>Information about your premises</h2>
      <p>Anything you tell us about your premises, your existing security arrangements or your
      vulnerabilities is treated as confidential. Access is limited to the members of our team who
      need it to deliver your project, and we do not pass it to third parties except where the law
      requires it.</p>

      <h2>Sharing</h2>
      <p>We do not sell your information. We share it only with suppliers and subcontractors working
      on your project, and only as far as they need it to do the work.</p>

      <h2>Retention</h2>
      <p>Enquiry records are kept for as long as we need them to respond and to meet legal
      obligations. Project and maintenance records are kept for the life of the contract and a
      reasonable period afterwards.</p>

      <h2>Your choices</h2>
      <p>You can ask us to correct or delete what we hold about you, or to stop contacting you, by
      writing to <a href="mailto:info@sentinel.co.zw">info@sentinel.co.zw</a>.</p>

      <h2>Cookies and third party content</h2>
      <p>This website loads an embedded Google map on the contact page. Google may set cookies or
      receive your IP address under its own privacy terms. Fonts and icons are served from this site
      rather than from a third party.</p>

      <h2>Changes</h2>
      <p>We may update this policy from time to time. The date at the top of the page shows when it
      was last revised.</p>
    </div>
  </section>
"""

write("privacy.html",
      "Privacy Policy | Sentinel Integrated Technologies",
      "How Sentinel Integrated Technologies collects, uses and protects the information you share with us.",
      privacy, cta=False)

print("done")
