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
from signs import SIGNS
from focus import attr as focus_attr
from build_icons import sprite as icon_sprite
import bullets

ORG = "Sentinel Integrated Technologies"
TAGLINE = "towards a #secure world"

NAV = [
    ("index.html", "Home"),
    ("group.html", "The group"),
    ("services.html", "Security systems"),
    ("security-services.html", "Manned security"),
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
    # The subject box travels with the image, so the page can keep it whole
    # at whatever size the frame turns out to be.
    bits += focus_attr(name)
    if style:
        bits += ' style="%s"' % style
    if eager:
        bits += ' fetchpriority="high"'
    elif lazy:
        bits += ' loading="lazy"'
    return "<img%s>" % bits


PORTRAIT_W = (405, 608, 810)


def photo_portrait(name, alt, sizes, cls=""):
    """A photograph kept in the shape it was taken in.

    These came off a phone at 810 by 1080 and are shown at 3:4, so nothing is
    cropped and nothing is enlarged past what the camera recorded. Three
    steps rather than two because the widest of them is where the bytes are,
    and a phone asking for a 170px column should not be sent it."""
    src = "assets/img/photos/%s-810.jpg" % name
    w, h = dim(src)
    sets = ", ".join("assets/img/photos/%s-%d.jpg %dw" % (name, x, x)
                     for x in PORTRAIT_W)
    return ('<img%s src="%s" srcset="%s" sizes="%s" alt="%s" '
            'width="%d" height="%d"%s loading="lazy">'
            % ((' class="%s"' % cls) if cls else "", src, sets, sizes, alt,
               w, h, focus_attr(name)))


def wall(items, cols=None):
    """Photographs from Sentinel's own sites, in a row, each saying what it is.

    The pictures are portrait and small, which is what honest phone
    photography off a site looks like. Rather than stretch them into the
    wide frames the stock photography uses, they are given a shape of their
    own: a row of tall frames with a caption under each, so the caption can
    do the work of placing the picture in the page it sits on."""
    n = cols or len(items)
    figs = ""
    for i, (slot, ico, cap) in enumerate(items):
        # The sizes hint has to agree with what the stylesheet actually does
        # on a phone, or the browser picks a file for a column that is not
        # the column it gets: a pair stacks, and a row of three leads with
        # the first one across the full width.
        wide = n == 2 or i == 0
        figs += """        <figure class="wall__fig" data-reveal>
          <div class="wall__frame">
            %s
          </div>
          <figcaption class="wall__cap">
            <span class="wall__ico" aria-hidden="true">%s</span>
            <span>%s</span>
          </figcaption>
        </figure>
""" % (photo_portrait(slot, PHOTO_ALT[slot],
                      "(max-width:640px) %dvw, %dvw"
                      % (92 if wide else 46, 84 // n)),
       ico, cap)
    return '      <div class="wall wall--n%d">\n%s      </div>\n' % (n, figs)


# The alt text lives with the photograph rather than with each use of it, so
# the same picture cannot end up described two different ways.
PHOTO_ALT = {
    "team-office":     "Four of the Sentinel team outside the office",
    "team-pair":       "Two Sentinel colleagues outside the office",
    "team-site":       "Two Sentinel staff talking through a site under construction",
    "install-cabling": "A technician running cable into a wall mounted equipment cabinet",
    "install-camera":  "A dome camera and floodlight under an eave, with the warning sign below",
    "sign-wall":       "A Sentinel CCTV warning sign fixed to a brick wall",
    "sign-entrance":   "Two Sentinel staff at a building entrance, the CCTV sign on the wall beside them",
}


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

# The group's own pages. Facebook's numeric form is what the page itself
# hands out; LinkedIn's "viewAsMember" parameter is a preview flag for the
# person who owns the page and means nothing to a visitor, so it is dropped.
FACEBOOK = "https://www.facebook.com/profile.php?id=61594591624503"
LINKEDIN = "https://www.linkedin.com/company/sentinelzw/"

# Offsite, so each one opens beside the page rather than taking a reader off
# it, and rel keeps the new tab from reaching back into this one.
OFFSITE = ' target="_blank" rel="noopener"'

CHEV = '<span class="pbtn__chev">%s</span>' % icon("caret-double-right", "i-sm")
CHEV_SM = icon("caret-double-right", "i-xs")
ARROW = icon("arrow-right", "i-sm")
STAR = icon("star", "i-xs", "ph-fill")


def pbtn(label, href, variant="", attrs="", brief=None):
    """A pill. `brief` gives a shorter wording for narrow screens.

    Both are in the markup and one is display:none at a time, which hides it
    from a screen reader too - so the announced name always matches the one
    on screen, which is what a voice user reading the button aloud needs."""
    cls = "pbtn" + ((" " + variant) if variant else "")
    if brief:
        label = ('<span class="lbl-full">%s</span>'
                 '<span class="lbl-brief">%s</span>' % (label, brief))
    return '<a class="%s" href="%s"%s><span class="pbtn__label">%s</span>%s</a>' % (
        cls, href, attrs, label, CHEV)


# ---------------------------------------------------------------- cross links
# Keyword -> destination. Longest phrases first is handled at match time, so
# the order here is just readability. Every href is checked against the built
# pages by the link audit, so a typo cannot ship.
CROSSLINKS = {
    # Written from the words the copy uses, not the industry's. Longest
    # phrase wins, so "access control" is read before "access".

    # ---- electronic security: services.html ----------------------------
    "CCTV surveillance":      "services.html#cctv",
    "CCTV":                   "services.html#cctv",
    "camera systems":         "services.html#cctv",
    "cameras":                "services.html#cctv",
    "intruder detection":     "services.html#alarms",
    "intruder alarms":        "services.html#alarms",
    "alarms":                 "services.html#alarms",
    "access control":         "services.html#access",
    "plate readers":          "services.html#access",
    "visitor passes":         "services.html#access",
    "turnstiles":             "services.html#access",
    "readers":                "services.html#access",
    "gate automation":        "services.html#gates",
    "gate motors":            "services.html#gates",
    "gates":                  "services.html#gates",
    "fire detection":         "services.html#fire",
    "fire sensors":           "services.html#fire",
    "detectors":              "services.html#fire",
    "video intercoms":        "services.html#intercoms",
    "intercoms":              "services.html#intercoms",
    "residential security":   "services.html#residential",
    "commercial security":    "services.html#commercial",
    "integrated security":    "services.html",
    "security systems":       "services.html",

    # ---- manned security: security-services.html ------------------------
    "protective asset management": "security-services.html#manned",
    "manned security":        "security-services.html#manned",
    "officers":               "security-services.html#manned",
    "event security":         "security-services.html#events",
    "crowd management":       "security-services.html#events",
    "armed response":         "security-services.html#response",
    "alarm monitoring":       "security-services.html#response",
    "control room":           "security-services.html#response",
    "dog units":              "security-services.html#k9",
    "dog unit":               "security-services.html#k9",
    "electric fencing":       "security-services.html#perimeter",
    "perimeter":              "security-services.html#perimeter",
    "investigations":         "security-services.html#investigations",
    "risk assessment":        "security-services.html#investigations",

    # ---- technology: circuitron.html -------------------------------------
    "building automation":    "circuitron.html#automation",
    "home automation":        "circuitron.html#automation",
    "smart home":             "circuitron.html#automation",
    "two way radios":         "circuitron.html#communications",
    "radios":                 "circuitron.html#communications",
    "networking":             "circuitron.html#communications",
    "networks":               "circuitron.html#communications",
    "structured cabling":     "circuitron.html#communications",
    "network hardware":       "circuitron.html#electronics",
    "CircuitStore":           "circuitron.html#circuitstore",
    "EcoCircuit":             "circuitron.html#ecocircuit",
    "old electronics":        "circuitron.html#ecocircuit",
    "recycling":              "circuitron.html#ecocircuit",
    "Circuitron":             "circuitron.html",

    # ---- the rest of the group -------------------------------------------
    "site signage":           "signage.html",
    "signage":                "signage.html",
    "safety signs":           "signage.html",
    "solar":                  "renewable-energy.html",
    "renewable energy":       "renewable-energy.html",
    "battery backup":         "renewable-energy.html",
    "backup power":           "renewable-energy.html",
    "the group":              "group.html",
    "three companies":        "group.html",
    "our accreditations":     "about.html#recognition",
    "accredited":             "about.html#recognition",
    "our clients":            "about.html#clients",
    "site survey":            "contact.html",
    "free survey":            "contact.html",
    # Not place names. "Eastlea" was linked here once and landed inside a
    # postal address, where a link to the contact page is noise rather than
    # a cross reference.
}


_WORD_EDGE = " \t\n,.:;!?()[]\u2014/\u2019'\"-"


def autolink(text, max_links=2, exclude=(), only=None):
    """Link known phrases inside a run of prose.

    Only the first occurrence of each phrase is linked, matches may not
    overlap, and `max_links` caps the whole block: past two or three, a
    paragraph stops reading as prose and starts reading as a directory.
    """
    if not text or "<a " in text:
        return text

    low = text.lower()
    taken = []
    allowed = CROSSLINKS if only is None else [k for k in CROSSLINKS if k in only]
    for kw in sorted(allowed, key=len, reverse=True):
        if len(taken) >= max_links or kw in exclude:
            continue
        k = kw.lower()
        at = low.find(k)
        while at != -1:
            before = text[at - 1] if at else " "
            after = text[at + len(k)] if at + len(k) < len(text) else " "
            edge = before in _WORD_EDGE and after in _WORD_EDGE
            clash = any(at < e and at + len(k) > b for b, e, _ in taken)
            if edge and not clash:
                if any(CROSSLINKS[t] == CROSSLINKS[kw] for _, _, t in taken):
                    break
                taken.append((at, at + len(k), kw))
                break
            at = low.find(k, at + 1)

    if not taken:
        return text

    out, end = [], 0
    for b, e, kw in sorted(taken):
        out.append(text[end:b])
        out.append('<a class="clink" href="%s">%s</a>' % (CROSSLINKS[kw], text[b:e]))
        end = e
    out.append(text[end:])
    return "".join(out)


# Running prose that may carry a cross link: a plain paragraph, or a lead.
# Not an overline, not a script line, not the hero copy over a photograph,
# and not the small meta lines under an organisation chart - a link in those
# reads as a mistake.
PROSE_P = re.compile(r'<p(| class="lead")>(.*?)</p>', re.S)
ANY_A = re.compile(r"<a\b[^>]*>.*?</a>", re.S)


def crosslink(html, name):
    """Link known phrases through every paragraph of prose on the page.

    One destination per page, so a reader meeting "cameras" three times is
    not offered the same door three times; at most two links in a paragraph,
    past which prose starts reading as a directory; and nothing that points
    at the page already being read.
    """
    i, j = html.find("<main"), html.find("</main>")
    if i < 0 or j < 0:
        return html
    before, body, after = html[:i], html[i:j], html[j:]

    # Destinations already spent, plus every destination on this very page.
    spent = set(re.findall(r'<a class="clink" href="([^"]+)"', body))
    spent.update(h for h in CROSSLINKS.values() if h.split("#")[0] == name)

    # A paragraph already inside a link cannot hold another one: a card that
    # is itself an anchor would nest them, which no browser forgives.
    inside = [(m.start(), m.end()) for m in ANY_A.finditer(body)]

    def one(m):
        text = m.group(2)
        if "<a " in text or any(b <= m.start() and m.end() <= e for b, e in inside):
            return m.group(0)
        free = [k for k in CROSSLINKS if CROSSLINKS[k] not in spent]
        if not free:
            return m.group(0)
        linked = autolink(text, max_links=2, only=free)
        for h in re.findall(r'<a class="clink" href="([^"]+)"', linked):
            spent.add(h)
        return "<p%s>%s</p>" % (m.group(1), linked)

    return before + PROSE_P.sub(one, body) + after


def award_seam():
    """The three laurels, centred on the join between two bands.

    The artwork already reads "Best Service Award" and the year, so the
    plate adds only what the laurels cannot say: that it was three years in
    a row. White, because it has to sit on the light band above and the dark
    one below at the same time.
    """
    marks = "".join(
        '<img src="assets/img/brand/award-%d.png" alt="" aria-hidden="true" '
        'loading="lazy" width="120" height="118">' % y
        for y in (2014, 2015, 2016))
    return """  <a class="seam" href="about.html#recognition"
     aria-label="Best Service Award in 2014, 2015 and 2016. Read about our recognition.">
    <span class="seam__plate">
      <span class="seam__marks">%s</span>
      <span class="seam__note">Best Service Award<strong>three years running</strong></span>
      <span class="seam__go" aria-hidden="true">%s</span>
    </span>
  </a>
""" % (marks, CHEV_SM)


def secbg(name, alt="", pos="50% 45%"):
    """The photographic ground behind a section.

    The picture is decorative here, so it takes an empty alt and the section's
    own heading carries the meaning. It loads lazily: none of these are above
    the fold."""
    return ('    <div class="secbg" style="--pos:%s">%s</div>\n'
            % (pos, photo_img(name, alt, "100vw", lazy=True)))


def eyebrow(text, variant=""):
    """A section overline. Kept under the old name so every call site still
    reads naturally; the pill it used to render is gone."""
    cls = "overline" + ((" " + variant.replace("eyebrow--", "overline--"))
                        if variant else "")
    return '<p class="%s">%s</p>' % (cls, text)


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


def ncard(variant, ico, title, text, bullets, href, cta="See the detail"):
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
            <a class="ncard__cta stretch" href="%s">%s %s</a>
            <span class="ncard__fill" aria-hidden="true"></span>
          </div>
        </article>
""" % (variant, duo(ico), title, text, lis, href, cta, CHEV_SM)



# -------------------------------------------------- the group, as components
ORG_FIELD = {"technologies": "org--a", "guarding": "org--b", "circuitron": "org--c"}

# A company whose own identity differs from the group's. The value is the
# theme class, and the same table drives the hero panel, the hero tab and the
# column in the chart, so the three cannot disagree about what blue is.
BRAND_THEME = {"circuitron": "theme-circuitron"}


def org_chart(compact=False):  # noqa: the flag is kept for call sites
    """Three companies as a comparison, not a tree.

    Rows line up across the columns so the eye reads across: what each one is,
    what it does, who it serves, what it trades as. An empty cell is
    information, which is why only Circuitron shows anything in the last row."""
    heads = rows_role = rows_line = rows_serves = rows_trades = rows_go = ""
    for c in COMPANIES:
        f = ORG_FIELD[c["id"]]
        # Every plate carries a white mark on a colour. Circuitron used to
        # carry its full colour mark on green, where its own blue vanished.
        mark = c.get("logo_small_white", c["logo_white"])
        # The theme travels down the whole column, not just the plate: the
        # chart is read down as well as across, and a blue plate over four
        # green rows would look like a mistake rather than like a company.
        t = (" " + BRAND_THEME[c["id"]]) if c["id"] in BRAND_THEME else ""
        heads += ('        <a class="org__col %s%s" href="%s" aria-label="%s">'
                  '<span class="org__field"><img src="%s" alt="%s" width="%d" height="%d" '
                  'loading="lazy"></span></a>\n'
                  % (f, t, c["href"], c["name"], mark, c["name"],
                     round(42 * c["logo_wh"][0] / c["logo_wh"][1]), 42))
        rows_role += '        <span class="org__role%s">%s</span>\n' % (t, c["role"])
        rows_line += '        <p class="org__line%s">%s</p>\n' % (t, c["chart_line"])
        rows_serves += '        <p class="org__serves%s">%s</p>\n' % (
            t, " &middot; ".join(c["sectors"][:3]))
        rows_trades += '        <p class="org__trades%s">%s</p>\n' % (
            t, " &middot; ".join(u["name"] for u in c["units"]) if c.get("units")
            else '<span class="org__none">&mdash;</span>')
        rows_go += ('        <a class="org__go%s" href="%s">%s %s</a>\n'
                    % (t, c["href"], c["short"], CHEV_SM))

    return """      <div class="org" data-reveal>
        <div class="org__row org__row--head">
%s        </div>
        <div class="org__row">
%s        </div>
        <div class="org__row org__row--line">
%s        </div>
        <div class="org__row org__row--label" aria-hidden="true">
          <span>Serves</span><span>Serves</span><span>Serves</span>
        </div>
        <div class="org__row">
%s        </div>
        <div class="org__row org__row--label" aria-hidden="true">
          <span>Trades as</span><span>Trades as</span><span>Trades as</span>
        </div>
        <div class="org__row">
%s        </div>
        <div class="org__row org__row--go">
%s        </div>
      </div>
""" % (heads, rows_role, rows_line, rows_serves, rows_trades, rows_go) + org_list()


def org_list():
    """The phone form. Three rows, a colour bar each, nothing else.

    At thirty pixels the two Sentinel lockups are indistinguishable, so the
    phone gets no logos at all: the bar does the distinguishing and the role
    label orients before the name does."""
    out = ""
    for c in COMPANIES:
        out += """        <a class="orgrow %s" href="%s">
          <span class="orgrow__text">
            <small>%s</small>
            <strong>%s</strong>
          </span>
          <span class="orgrow__go" aria-hidden="true">%s</span>
        </a>
""" % (ORG_FIELD[c["id"]]
       + ((" " + BRAND_THEME[c["id"]]) if c["id"] in BRAND_THEME else ""),
       c["href"], c["role"], c["short"], CHEV_SM)
    return '      <div class="orglist" data-reveal>\n%s      </div>\n' % out




def org_parent():
    """The group itself, as a line in the section header rather than a node."""
    return ('<a class="orgparent" href="group.html">'
            '<img src="assets/img/brand/mark.svg" alt="" width="22" height="21" loading="lazy">'
            '<span><b>%s</b> %s</span></a>' % (PARENT["name"], PARENT["role"].lower()))


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
    "k9": ("k9-handler-standing", "A Sentinel handler with a patrol dog"),
    "response": ("response-night", "A response vehicle on a wet road at night"),
    "events": ("officer-radio", "An officer working a gatehouse by radio"),
    "perimeter": ("vehicle-checkpoint", "Officers and a dog unit at an estate gate"),
    "manned": ("officers-warehouse", "Officers patrolling a warehouse yard"),
    "communications": ("tech-network", "A fibre patch panel in a network cabinet"),
    "automation": ("tech-smart", "A smart home panel being set from a phone"),
    "electronics": ("tech-retail", "Security and smart home equipment of the kind CircuitStore carries"),
    "security-systems": ("sys-cctv", "A dome camera on a wall bracket"),
    # Loss and shrinkage work happens on a shop floor, so the officer on duty
    # is the honest frame for it until a dedicated one exists.
    "investigations": ("officer-on-duty", "Sentinel officers on post at an office entrance"),
}


def ambient(name):
    """The blurred copy of a card's own photograph, behind the card.

    Decorative and already described by the real image above it, so it is
    hidden from assistive technology."""
    return ('<img class="dcard__bleed" src="assets/img/photos/%s-640.jpg" '
            'alt="" aria-hidden="true" loading="lazy" width="640" height="480">\n          '
            % name)


def division_card(c, d):
    d = dict(d, line=autolink(d["line"], max_links=1))
    """A capability inside a company: what it is, then the actual line items."""
    photo = DIV_PHOTO.get(d["id"])
    href = DIV_HREF.get(d["id"], DIV_HREF_DEFAULT)
    media = ""
    if photo:
        f, alt = photo
        # Not an anchor. The card already has one, on its heading, and a
        # second one over the picture would be a tab stop that announces
        # nothing and goes to the same place.
        media = """          <div class="dcard__media">
            %s
          </div>
""" % photo_img(f, alt, "(max-width:720px) 100vw, 30vw")
    return """        <article class="dcard%s" id="%s" data-reveal>
          %s%s          <span class="dcard__ico" data-obstacle>%s</span>
          <h3 class="h-3"><a class="stretch" href="%s">%s</a></h3>
          <p>%s</p>
          <ul class="dcard__list">%s</ul>
        </article>
""" % (" dcard--photo" if media else "", d["id"],
       ambient(DIV_PHOTO[d["id"]][0]) if media else "",
       media, si(d["icon"], "i-xl"),
       href, d["name"], d["line"],
       "".join("<li>%s</li>" % i for i in d["items"]))


# Where a capability card goes when it is clicked. Most lead to the survey,
# because that is the next step for someone reading about a capability; two
# have a better home on the site itself.
DIV_HREF = {
    "security-systems": "services.html",
    "electronics":      "circuitron.html#circuitstore",
}
DIV_HREF_DEFAULT = "contact.html"


UNIT_PHOTO = {
    "circuitstore": ("tech-retail", "Security and smart home equipment of the kind CircuitStore carries"),
    "ecocircuit": ("tech-ewaste", "Mixed electronic scrap waiting to be sorted"),
}


def unit_panel(c, u):
    u = dict(u, blurb=autolink(u.get("blurb", ""), max_links=2)) if u.get("blurb") else u
    """CircuitStore and EcoCircuit: businesses inside a business."""
    f, alt = UNIT_PHOTO[u["id"]]
    media = """          <div class="unit__media">
            %s
          </div>
""" % photo_img(f, alt, "(max-width:980px) 100vw, 45vw")
    return """        <article class="unit" id="%s" data-reveal>
%s          <div class="unit__head">
            <span class="unit__ico">%s</span>
            <div>
              <h3 class="h-3"><a class="stretch" href="contact.html">%s</a></h3>
              <p class="script unit__strap">%s</p>
            </div>
          </div>
          <p>%s</p>
          <ul class="unit__list">%s</ul>
        </article>
""" % (u["id"], media, si(u["icon"], "i-xl"), u["name"], u["strap"], u["line"],
       "".join("<li>%s</li>" % i for i in u["items"]))

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
<link rel="preload" href="assets/fonts/marker.woff2" as="font" type="font/woff2" crossorigin>
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
      <a href="%s" aria-label="Sentinel on Facebook"%s>%s</a>
      <a href="%s" aria-label="Sentinel on LinkedIn"%s>%s</a>
      <a class="topbar__hide-sm" href="mailto:info@sentinel.co.zw" aria-label="Email Sentinel">%s</a>
      <a class="topbar__hide-sm" href="tel:+263773589461" aria-label="Call Sentinel">%s</a>
    </div>
  </div>
</div>
""" % (icon("buildings", "i-xs"), icon("envelope-simple", "i-xs"), icon("phone-call", "i-xs"),
       icon("whatsapp-logo", "i-sm", "ph-fill"),
       FACEBOOK, OFFSITE, icon("facebook-logo", "i-sm", "ph-fill"),
       LINKEDIN, OFFSITE, icon("linkedin-logo", "i-sm", "ph-fill"),
       icon("envelope-simple", "i-sm", "ph-fill"),
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
      <img class="brand__light" src="assets/img/brand/sit-lockup-white.png" alt="%s" width="555" height="214">
      <img class="brand__dark" src="assets/img/brand/sit-lockup.png" alt="" width="555" height="214" aria-hidden="true">
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
  <div class="drawer__top">
    <a class="drawer__brand" href="index.html" aria-label="%s home">
      <img src="assets/img/brand/sit-lockup-white.png" alt="" width="555" height="214">
    </a>
    <button class="drawer__close" type="button" data-drawer-close aria-label="Close menu">
      <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
        <path d="M6 6 18 18M18 6 6 18"/>
      </svg>
    </button>
  </div>
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
""" % (ORG, ORG, items, megapanel(), pbtn("Book a site survey", "contact.html", brief="Free survey"), ORG, drawer,
       pbtn("Book a site survey", "contact.html", "pbtn--block"))


CTA = ("""
  <!-- ===== CTA ===== -->
  <section class="section section--tight">
    <div class="container">
      <div class="cta cta--photo" data-reveal>
%s        <div class="cta__inner" data-obstacle>
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
""" % (secbg("response-night", pos="54% 46%").rstrip(),
       eyebrow("Book it", "eyebrow--dark"),
       pbtn("Book a site survey", "contact.html", "pbtn--light"),
       pbtn("+263 77 358 9461", "tel:+263773589461", "pbtn--outline")))


FOOTER = """
</main>

<!-- ===== Footer ===== -->
<footer class="footer">
  <div class="container">
    <div class="footer__top">
      <div class="footer__brand">
        <a href="index.html" aria-label="%s, home">
          <img src="assets/img/brand/sit-lockup-white.png" alt="%s" width="555" height="214" loading="lazy">
        </a>
        <p class="script footer__tagline">towards a #secure world</p>
        <p>A Zimbabwean security group: electronic systems, manned security and technology, run as three companies under one standard.</p>
        <div class="socials">
          <a href="https://wa.me/263773589461" aria-label="Message Sentinel on WhatsApp" rel="noopener">%s</a>
          <a href="%s" aria-label="Sentinel on Facebook"%s>%s</a>
          <a href="%s" aria-label="Sentinel on LinkedIn"%s>%s</a>
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
          <li><a href="security-services.html#manned">Protective asset management</a></li>
          <li><a href="security-services.html#response">Alarm response</a></li>
          <li><a href="renewable-energy.html">Solar and backup power</a></li>
          <li><a href="signage.html">Site signage</a></li>
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
      <p style="margin:0">&copy; <span data-year class="num">2026</span> Sentinel Integrated Technologies (Private) Limited</p>
      <nav aria-label="Legal">
        <a href="privacy.html">Privacy policy</a>
        <a href="contact.html">Contact</a>
        <a href="about.html#recognition">Best Service Award 2014, 2015, 2016</a>
        <a class="footer__by" href="https://bitstudio.co.zw" rel="noopener">Engineered by <strong>Bit Studio</strong></a>
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
       icon("whatsapp-logo", "i-sm", "ph-fill"),
       FACEBOOK, OFFSITE, icon("facebook-logo", "i-sm", "ph-fill"),
       LINKEDIN, OFFSITE, icon("linkedin-logo", "i-sm", "ph-fill"),
       icon("envelope-simple", "i-sm", "ph-fill"),
       icon("phone-call", "i-sm", "ph-fill"),
       icon("map-pin", "i-sm"), icon("phone-call", "i-sm"), icon("envelope-simple", "i-sm"),
       icon("arrow-up", "i-sm"),
       icon("whatsapp-logo", "i-md", "ph-fill"),
       WA_ENQUIRY, icon("chat-circle-dots", "i-md", "ph-duotone"), icon("caret-double-right", "i-xs"),
       WA_COMMUNITY, icon("users-three", "i-md", "ph-duotone"), icon("caret-double-right", "i-xs"),
       icon("whatsapp-logo", "i-md", "ph-fill", "wa__open"), icon("x", "i-md", "ph", "wa__close"))


# The second photograph in each interior hero, keyed on the first. Chosen so
# the pair says something the single picture could not: the team and then the
# dog unit, the reader and then the camera, the bench and then the rack.
PHERO_PAIR = {
    "officer-on-duty":         ("officers-warehouse",
                                "Officers on a warehouse contract"),
    "sys-access":              ("sys-cctv",
                                "A camera covering an approach"),
    "officers-team":           ("k9-handler-standing",
                                "A handler and dog on a site patrol"),
    "circuitron-bench":        ("tech-network",
                                "A patch panel in a network cabinet"),
    "control-room-monitoring": ("security-officers",
                                "Two officers at the start of a shift"),
    "sys-cctv":                ("sys-gates",
                                "An automated gate on a commercial entrance"),
    "technician-panel":        ("vehicle-checkpoint",
                                "An officer checking a vehicle at a gate"),
}


def phero(label, title, lead, pic=None, alt=""):
    lead = autolink(lead, max_links=2)
    if pic:
        shots = ['      <div class="phero__slide is-active">%s</div>\n'
                 % photo_img(pic, alt, "70vw", lazy=False, eager=True)]
        second = PHERO_PAIR.get(pic)
        if second:
            shots.append('      <div class="phero__slide">%s</div>\n'
                         % photo_img(second[0], second[1], "70vw"))
        switcher = ""
        if second:
            switcher = (
                # A group of toggles, not a tablist: a tablist promises tab
                # panels and there are none here, only two pictures behind
                # the same heading.
                '    <div class="pswitch" role="group" '
                'aria-label="Hero picture">\n'
                + "".join(
                    '      <button class="pswitch__seg%s" type="button" '
                    'aria-pressed="%s" '
                    'aria-label="Show picture %d of 2" data-phero-go="%d">'
                    '<span class="num">%02d</span></button>\n'
                    % (" is-active" if k == 0 else "",
                       "true" if k == 0 else "false",
                       k + 1, k, k + 1)
                    for k in (0, 1))
                + "    </div>\n")
        media = """    <div class="phero__media"%s>
%s    </div>
    <div class="phero__scrim"></div>
%s""" % (" data-phero" if second else "", "".join(shots), switcher)
        cls = "phero"
    else:
        media, cls = "", "phero phero--plain"
    return """
  <section class="%s">
%s    <div class="container" data-obstacle>
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


SELF_LINK = re.compile(r'<a class="clink" href="([^"#]*)(?:#[^"]*)?">(.*?)</a>', re.S)


def drop_self_links(html, name):
    """A page that cross links to itself is noise, so the link is unwrapped
    and the phrase reads as ordinary text."""
    def one(m):
        return m.group(2) if m.group(1) in ("", name) else m.group(0)
    return SELF_LINK.sub(one, html)


# ------------------------------------------------------------- photo bands
# page -> list of (photograph, focal point), one per dark band on that page,
# in document order. A band with None stays flat, so the alternation can be
# tuned without unpicking the markup.
PHOTO_BANDS = {
    "index.html":            [("technician-panel", "58% 42%")],
    # None skips a band: the team section is dark but carries photographs of
    # its own, and a photograph behind photographs is just noise. The
    # recognition band keeps the picture.
    "about.html":            [None, ("officers-team", "50% 34%")],
    "services.html":         [("sys-cctv", "54% 44%")],
    "renewable-energy.html": [("power-solar", "50% 48%")],
    "circuitron.html":       [("tech-retail", "52% 46%")],
    "signage.html":          [("vehicle-checkpoint", "56% 44%")],
    "group.html":            [("officers-warehouse", "52% 40%")],
    "security-services.html": [],
}

# The closing call to action on every page, which is the other half of the
# alternation: the last band a reader sees is photographic.
CTA_BAND = ("response-night", "54% 46%")

DARK_BAND = re.compile(r'<section class="section section--dark([^"]*)"([^>]*)>')


def photo_bands(html, name):
    """Turn the flat dark bands on this page into photographic ones."""
    picks = list(PHOTO_BANDS.get(name, []))

    def one(m):
        if not picks:
            return m.group(0)
        pick = picks.pop(0)
        if pick is None:
            return m.group(0)
        photo, pos = pick
        return ('<section class="section section--dark section--photo%s"%s>\n%s'
                % (m.group(1), m.group(2), secbg(photo, pos=pos).rstrip("\n")))

    html = DARK_BAND.sub(one, html)

    # The band's own copy column sits on top of the picture, so the
    # engine is told to steer each subject into what the text leaves free.
    out, at = [], 0
    for m in re.finditer(r'<section class="section section--dark section--photo', html):
        stop = html.find('</section>', m.start())
        if stop < 0:
            continue
        block = html[m.start():stop]
        out.append(html[at:m.start()])
        out.append(block.replace('<div class="container">',
                                 '<div class="container" data-obstacle>', 1))
        at = stop
    out.append(html[at:])
    return ''.join(out)

# --------------------------------------------------------- entrance gestures
# A class on a container, and the gesture its children arrive with. The order
# matters only in that each pattern is applied once.
GESTURES = [
    ("steps",   "zip"),     # the four process steps close in from both sides
    ("figures", "count"),   # the numbers run up to their value
    ("rows",    "slide"),   # sector rows arrive in sequence
    ("dgrid",   "deal"),    # capability cards land like a dealt hand
    ("g-3",     "deal"),
    ("bento",   "scale"),   # the picture settles rather than fades
    ("orglist", "slide"),
    ("signgrid", "deal"),
    ("gdetail__rows", "slide"),
]

GEST_RE = [(re.compile(r'(<(?:div|dl|ul|ol)\s+class="%s")(?![^>]*data-anim)' % re.escape(c)), g)
           for c, g in GESTURES]

SHEAD_TITLE = re.compile(r'<h2 class="([^"]*\bshead__title\b[^"]*)"(?![^>]*data-anim)')
SECBG = re.compile(r'<div class="secbg"(?![^>]*data-reveal)')
FIG_DT = re.compile(r'<dt([^>]*)>(\s*)(\d[\d,]*)(\s*)</dt>')


def gestures(html):
    """Give each kind of block the entrance that suits it."""
    for rx, g in GEST_RE:
        html = rx.sub(lambda m, g=g: '%s data-anim="%s"' % (m.group(1), g), html)

    # A section heading is uncovered rather than moved: the type stays put and
    # the clip travels, which keeps a long heading from sliding under its own
    # overline.
    html = SHEAD_TITLE.sub(
        lambda m: '<h2 class="%s" data-reveal data-anim="wipe"' % m.group(1), html)

    # The photographic ground settles from slightly over size.
    html = SECBG.sub('<div class="secbg" data-reveal data-anim="scale"', html)

    # The figure keeps its final value in the markup; the attribute only tells
    # the script what to count to.
    html = FIG_DT.sub(lambda m: m.group(0) if "data-count" in m.group(1)
                      else '<dt%s data-count="%s">%s%s%s</dt>'
                      % (m.group(1), m.group(3).replace(",", ""),
                         m.group(2), m.group(3), m.group(4)), html)
    return html

# Every line item carries the glyph for the thing it names. One pass over the
# finished page rather than four call sites, so a list written as literal
# markup is marked the same way as one built from a table.
BULLET_UL = re.compile(
    r'<ul class="(?:card__list|dcard__list|unit__list|footer__links'
    r'|leader__quals)[^"]*"[^>]*>.*?</ul>', re.S)
BULLET_LI = re.compile(r"<li>(.*?)</li>", re.S)
TAGS = re.compile(r"<[^>]+>")


def bullet_icons(html):
    """Prepend each line item's own icon, chosen in bullets.py."""
    def one_li(m):
        inner = m.group(1)
        if 'class="li-ico"' in inner:
            return m.group(0)
        spec = bullets.pick(TAGS.sub("", inner).strip())
        if not spec:
            return m.group(0)                      # the build refuses these below
        kind, glyph = spec.split(":", 1)
        mark = si(glyph, "i-sm") if kind == "si" else icon(glyph, "i-sm")
        return ('<li><span class="li-ico" aria-hidden="true">%s</span>'
                "<span>%s</span></li>" % (mark, inner))

    return BULLET_UL.sub(lambda m: BULLET_LI.sub(one_li, m.group(0)), html)


# The texture order. Read down, it alternates between line work and point
# work so no two neighbours feel the same even before the page rotates it.
PATTERNS = ["graph", "weave", "hatch", "cross", "scan", "grid", "trace", "rings"]

# Where each page starts in that list, so the home page and the about page
# do not open with the same grain. Primes against the length, so a page
# stepping through the list never falls into another page's phase.
PAT_START = {
    "index.html": 0, "about.html": 3, "services.html": 5,
    "security-services.html": 2, "circuitron.html": 6, "group.html": 1,
    "signage.html": 4, "renewable-energy.html": 7, "contact.html": 2,
    "privacy.html": 5,
}

# A company page draws its grain from its own run rather than from the whole
# pool, so the texture changes with the palette instead of being the one
# thing the three worlds still share. There are only eight textures and the
# sets overlap, but no two companies open on the same one and each set leans
# the way that company's work looks: scanlines and wiring for the systems
# business, a woven, patrolled grain for the officers, board traces for
# Circuitron.
PAT_SETS = {
    "technologies": ["scan", "grid", "trace", "cross"],
    "guarding":     ["hatch", "weave", "cross", "graph"],
    "circuitron":   ["trace", "rings", "grid", "graph"],
}

SECTION_TAG = re.compile(r'<section class="(section[^"]*)"')


def patterns(html, name):
    """One texture per band, in sequence, no two neighbours alike."""
    pool = PAT_SETS.get(THEMES.get(name), PATTERNS)
    at = [PAT_START.get(name, 0) % len(pool)]
    themed = THEMES.get(name) in PAT_SETS

    def pick(default, i):
        """The components below choose a texture by hand rather than taking
        the next one in the run. On a group page those hand picks stand; on
        a company page they are pulled back into that company's four, so the
        whole page speaks one grain instead of the bands speaking one and
        the cards another."""
        return pool[i % len(pool)] if themed else default

    def one(m):
        cls = m.group(1)
        if "section--photo" in cls or "pat-" in cls:
            return m.group(0)          # a photograph is texture enough
        p = pool[at[0] % len(pool)]
        at[0] += 1
        return '<section class="%s pat pat-%s"' % (cls, p)

    html = SECTION_TAG.sub(one, html)

    # The notched card takes its texture on the article rather than on the
    # body, because it is two surfaces - the body and the filler beside the
    # tab - and the property has to inherit to both or they meet at a seam.
    for i, (cls, pat) in enumerate((("ncard ncard--white", "graph"),
                                    ("ncard ncard--lime", "hatch"),
                                    ("ncard ncard--dark", "grid"),
                                    ("ncard ncard--green", "trace"))):
        html = html.replace('class="%s"' % cls,
                            'class="%s pat-%s"' % (cls, pick(pat, i)))

    # The components that paint their own. The four process steps read left
    # to right through four textures, which is the one place on the site
    # where a sequence of patterns means something: it is a sequence of
    # stages.
    for cls, pats in (("step", [pick("scan", 0), pick("cross", 1),
                                pick("trace", 2), pick("weave", 3)]),
                      ("unit", [pick("trace", 2), pick("rings", 3)]),
                      ("bento__stat", [pick("hatch", 1)])):
        k = [0]

        def one(m, pats=pats, k=k):
            p = pats[k[0] % len(pats)]
            k[0] += 1
            return m.group(0)[:-1] + ' pat pat-%s"' % p

        html = re.sub(r'class="%s(?: [A-Za-z0-9 _-]+)?"' % re.escape(cls),
                      one, html)

    # The two bands that are not .section but are still bands.
    html = html.replace('<section class="cta"',
                        '<section class="cta pat pat-%s"' % pick("trace", 2), 1)
    html = html.replace('<footer class="footer"',
                        '<footer class="footer pat pat-%s"' % pick("rings", 3), 1)
    html = html.replace('<section class="clients section--white"',
                        '<section class="clients section--white pat pat-%s"'
                        % pick("scan", 0), 1)
    return html


# The paragraphs that arrive a word at a time: a band's opening sentence and
# the aside beside a section heading. Not body copy - a hundred words
# arriving one by one is a wait, not an effect.
STREAM = re.compile(r'<(p|div) class="(lead|shead__aside)"(?![^>]*data-stream)')


def streaming(html):
    return STREAM.sub(lambda m: '<%s class="%s" data-stream'
                      % (m.group(1), m.group(2)), html)


# A page may carry its own company's colours. The class goes on <main>, so the
# group's header and footer keep the group's green.
# A company page is that company's world, so the theme rides on <html> and
# not on <main>. The utility bar, the header, the drawer and the footer are
# all emitted outside <main>; scoped there the palette stopped at the content
# and the chrome stayed in group green, which read as the group site wearing
# a different logo rather than as the company's own place.
THEMES = {
    "circuitron.html": "circuitron",
    "security-services.html": "guarding",
    "services.html": "technologies",
}

# The address bar on a phone, which is chrome we do not draw ourselves. It
# takes the theme's darkest ground, the same colour the footer lands on.
THEME_COLOR = {
    "circuitron": "#051229",
    "guarding": "#180809",
    "technologies": "#021A1A",
}


def theme(html, name):
    slug = THEMES.get(name)
    if not slug:
        return html
    html = html.replace(
        '<html lang="en-ZW">',
        '<html lang="en-ZW" class="theme-%s" data-company="%s">' % (slug, slug), 1)
    return html.replace(
        '<meta name="theme-color" content="#06291B">',
        '<meta name="theme-color" content="%s">' % THEME_COLOR[slug], 1)


ATTR = re.compile(' (src|alt|width|height)="([^"]*)"')


def _retag(tag, src, alt, w, h):
    """Rewrite one <img>'s source, alt and box, leaving its other attributes
    (the class, aria-hidden, loading) exactly as they were."""
    vals = {"src": src, "alt": alt, "width": str(w), "height": str(h)}

    def one(m):
        key = m.group(1)
        # An alt that was deliberately empty stays empty: that image is
        # aria-hidden and the one beside it already carries the name.
        if key == "alt" and m.group(2) == "":
            return m.group(0)
        return ' %s="%s"' % (key, vals[key])
    return ATTR.sub(one, tag)


IMG = re.compile(r'<img [^>]*>')


def company_brand(html, name):
    """On a company page the chrome wears that company's own mark.

    Only the chrome: the lockup also appears inside the content of these
    pages, in the mega menu, the hero, the group column and the facts card,
    and those are the parent group's mark doing a different job. So this
    walks the four places the shell emits a brand and leaves every other
    image alone. Sentinel Integrated Technologies already shows its own
    lockup there, so it is a no-op for that page.
    """
    slug = THEMES.get(name)
    if not slug:
        return html
    c = by_id(slug)
    w, h = c["logo_wh"]

    # The header pair: a white mark over the transparent bar, the full colour
    # one once the bar goes solid.
    for cls, src in (("brand__light", c["logo_white"]), ("brand__dark", c["logo"])):
        m = re.search(r'<img class="%s" [^>]*>' % cls, html)
        if m:
            html = html[:m.start()] + _retag(m.group(0), src, c["name"], w, h)                 + html[m.end():]

    # The drawer and the footer: one mark each, the next <img> after the
    # wrapper, both knocked out white because both sit on a dark ground.
    for wrapper in ("drawer__brand", "footer__brand"):
        a = re.search(r'class="%s"' % wrapper, html)
        if not a:
            continue
        m = IMG.search(html, a.end())
        if m:
            html = html[:m.start()]                 + _retag(m.group(0), c["logo_white"], c["name"], w, h)                 + html[m.end():]
    return html


def write(name, title, desc, body, cta=True):
    html = head(title, desc, name) + topbar() + header(name) + body + (CTA if cta else "") + FOOTER
    html = photo_bands(html, name)
    html = patterns(html, name)
    html = crosslink(html, name)
    html = streaming(html)
    html = bullet_icons(html)
    html = theme(html, name)
    html = company_brand(html, name)
    html = gestures(html)
    html = drop_self_links(html, name)
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
def hero_block():
    """Three panels, three photographs, one tab row that names the
    companies. Built from the group data so a fourth company would appear
    here without anyone remembering to add it."""
    slides = panels = tabs = ''
    for i, c in enumerate(COMPANIES):
        h = c['hero']
        on = i == 0
        src = 'assets/img/photos/%s' % h['photo']
        if on:
            img = ('<img src="%s-1200.jpg" srcset="%s-640.jpg 640w, '
                   '%s-1200.jpg 1200w" sizes="100vw" alt="%s"%s '
                   'fetchpriority="high">'
                   % (src, src, src, h['alt'], focus_attr(h['photo'])))
        else:
            img = ('<img data-slide-src data-src="%s-1200.jpg" '
                   'data-srcset="%s-640.jpg 640w, %s-1200.jpg 1200w" '
                   'sizes="100vw" alt="%s"%s>'
                   % (src, src, src, h['alt'], focus_attr(h['photo'])))
        slides += ('      <div class="hero__slide%s" style="--pos:%s;--expo:%s">'
                   '\n        %s\n      </div>\n'
                   % (' is-active' if on else '', h['pos'], h['expo'], img))

        # A company with colours of its own says so, and the theme class
        # does the rest: accent word, both buttons, the phone icon.
        brand = BRAND_THEME.get(c["id"], "")
        panels += ("""
          <div class="hero__panel%s%s" id="hp-%d" role="tabpanel" aria-labelledby="ht-%d"%s>
            <div class="hero__id">
              <img class="hero__lockup" src="%s" alt="%s" width="%d" height="%d" loading="%s">
            </div>
            <%s class="h-hero">%s<span class="accent-lime">%s</span>%s</%s>
            <p class="hero__lead">%s</p>
            <div class="hero__actions">
              %s
              %s
              <dl class="hero__call">
                <a class="rbtn" href="tel:+263773589461" aria-label="Call Sentinel">%s</a>
                <div><dt>Call us</dt><dd class="num">+263 77 358 9461</dd></div>
              </dl>
            </div>
          </div>
""" % (' is-active' if on else '', (' ' + brand) if brand else '',
       i + 1, i + 1,
       (' data-brand="%s"' % c['id']) if brand else '',
       c.get('logo_small_white', c['logo_white']), c['name'],
       round(40 * c['logo_wh'][0] / c['logo_wh'][1]), 40,
       'eager' if on else 'lazy',
       'h1' if on else 'h2',
       h['h1'][0], h['h1'][1], h['h1'][2],
       'h1' if on else 'h2', h['lead'],
       pbtn(h['cta'][0], h['cta'][1]),
       pbtn(h['cta2'][0], h['cta2'][1], 'pbtn--ghost'),
       icon('phone-call', 'i-md')))

        tabs += ("""
          <button class="hero__tab%s%s" type="button" role="tab" id="ht-%d"
                  aria-controls="hp-%d" aria-selected="%s" tabindex="%d" data-hero-tab>
            <span class="hero__tab-rail" aria-hidden="true"><i></i></span>
            <span class="hero__tab-n num">%02d</span>
            <span class="hero__tab-text"><strong>%s</strong><small>%s</small></span>
          </button>
""" % (' is-active' if on else '', (' ' + brand) if brand else '',
       i + 1, i + 1,
       'true' if on else 'false', 0 if on else -1, i + 1,
       c['tab'][0], c['tab'][1]))

    return ("""
  <!-- ===== Hero ===== -->
  <section class="hero" data-hero>
    <div class="hero__media" aria-hidden="true">
%s    </div>
    <div class="hero__unify" aria-hidden="true"></div>
    <div class="hero__vignette" aria-hidden="true"></div>
    <div class="hero__grid" aria-hidden="true"></div>
    <div class="hero__tint" aria-hidden="true"></div>
    <div class="hero__scrim"></div>

    <div class="container">
      <div class="hero__content" data-obstacle>
        <div class="hero__panels">
%s        </div>
        <div class="hero__tabs" role="tablist" aria-label="The Sentinel group">
%s        </div>
      </div>
    </div>
  </section>
""" % (slides, panels, tabs))


home = hero_block() + CLIENTS + """

  <!-- ===== The group ===== -->
  <section class="section section--open section--cream" id="group">
    <div class="container">
""" + shead("One group, three companies",
            "Everything a site needs, under one roof",
            aside="Each company holds its own licence, its own staff and its own "
                  "discipline. You deal with one number." + org_parent(),
            variant="shead--wide") + org_chart() + """    </div>
  </section>
  <!-- ===== Who we are ===== -->
  <section class="section section--white">
    <div class="container split">
      <div class="bento" data-reveal>
        <a class="bento__hero" href="about.html" aria-label="About Sentinel">
          <img src="assets/img/photos/officer-radio-1200.jpg"
               srcset="assets/img/photos/officer-radio-640.jpg 640w, assets/img/photos/officer-radio-1200.jpg 1200w"
               sizes="(max-width:980px) 100vw, 45vw" alt="An officer working a gatehouse checkpoint by radio" data-focus="30 7 42 27">
        </a>
        <a class="bento__stat" href="contact.html">
          <strong class="num">24/7</strong>
          <span>Someone on the phone<br>at any hour</span>
        </a>
        <a class="bento__tile" href="services.html#access" aria-label="Access control">
          <img src="assets/img/photos/tile-access-640.jpg"
               alt="A facial recognition reader at an entrance">
        </a>
      </div>

      <div data-reveal>
        <p class="overline">Who we are</p>
        <h2 class="h-2">One group, one number to call</h2>
        <p class="lead">
          """+ autolink("An accredited Zimbabwean group covering electronic security, "
                       "manned security and the technology that ties them "
                       "together.", max_links=2) +"""
        </p>
        <p>
          Our own technicians and our own officers do the work, then stay on to maintain
          it. You call us, not four contractors.
        </p>

        <dl class="figures">
          <div><dt class="num">10</dt><dd>provinces covered</dd></div>
          <div><dt class="num">2016</dt><dd>trading since</dd></div>
          <div><dt class="num">3</dt><dd>companies, one standard</dd></div>
        </dl>

        <div style="margin-top:2rem">""" + pbtn("More about the group", "about.html", "pbtn--dark") + """</div>
      </div>
    </div>
  </section>

""" + award_seam() + """
  <!-- ===== Process ===== -->
  <section class="section section--dark">
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
"""

write("index.html",
      "Sentinel Integrated Technologies | Electronic Security in Zimbabwe",
      "CCTV, intruder alarms, access control, fire detection and physical access control across Zimbabwe. Based in Harare, support at any hour, award winning in 2014, 2015 and 2016.",
      home)


# ================================================================= ABOUT
about = phero("About", "A decade of manned security, turned into a group",
  "Sentinel started in 2016 with officers on gates. The technology work grew out of that, "
  "and in 2026 it became a company of its own. Three businesses now, built on the same ten "
  "years of ground truth.",
  "officer-on-duty", "Sentinel officers on post at an office entrance") + """
  <section class="section section--white">
    <div class="container split">
      <div class="bento" data-reveal>
        <a class="bento__hero" href="services.html" aria-label="Our services">
          <img src="assets/img/photos/security-officers-1200.jpg"
               srcset="assets/img/photos/security-officers-640.jpg 640w, assets/img/photos/security-officers-1200.jpg 1200w"
               sizes="(max-width:980px) 100vw, 45vw" alt="Officers and a dog unit on patrol at dusk" data-focus="30 7 61 35">
        </a>
        <a class="bento__tile" href="services.html#cctv" aria-label="CCTV surveillance">
          <img src="assets/img/photos/tile-night-640.jpg"
               alt="An operator watching a wall of live camera feeds">
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
          Manned security came first. Covering those sites meant learning cameras, alarms
          and access control properly, and that work outgrew the manned security
          business. So we gave it a
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

  <section class="section section--cream">
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

  <section class="section section--dark">
    <div class="container">
""" + shead("The team", "The people who do the work",
            "Not models and not stock. Our own staff, at our own office and "
            "on a client's site, photographed this October.",
            kv="eyebrow--dark") + wall([
    ("team-office", icon("users-three", "i-sm", "ph-fill"),
     "Four of the team outside the office, Harare"),
    ("team-pair", icon("handshake", "i-sm", "ph-fill"),
     "Technical and operations, between jobs"),
    ("team-site", icon("map-pin", "i-sm", "ph-fill"),
     "A site walk before a quotation is written"),
]) + """    </div>
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
            [], "contact.html", "What drives us") \
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
        </a>
""" % (duo(ico, "i-lg"), t, p)

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
    lead = autolink(lead, max_links=2)
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
        </div>
""" % (si(DIV_ICON.get(anchor, "perimeter"), "i-2xl"), eyebrow(kicker), title, lead, lis)
    inner = (media + text) if flip else (text + media)
    return """      <div class="split" id="%s" style="scroll-margin-top:calc(var(--header-h) + 28px);padding-block:clamp(2.5rem,5vw,4rem)">
%s      </div>
""" % (anchor, inner)


_tech = by_id("technologies")
services = phero(_tech["role"], _tech["name"], _tech["lead"],
  "sys-access", "A reader being used at a door") + """
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
  "access-terminal", "A facial recognition reader at an entrance"),
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

  <section class="section section--dark">
    <div class="container">
""" + shead("How we work", "From the first call to the handover",
            "Four stages, the same on every job whatever the scale.", kv="eyebrow--dark") + steps_block() + """    </div>
  </section>

  <section class="section section--white">
    <div class="container">
""" + shead("On site", "What the work actually looks like",
            "A cabinet being cabled, a camera under an eave, and the sign "
            "that tells people it is there.") + wall([
    ("install-cabling", icon("wrench", "i-sm", "ph-fill"),
     "Running cable into a wall cabinet on a fit out"),
    ("install-camera", icon("eye", "i-sm", "ph-fill"),
     "A dome camera and floodlight, sign below"),
]) + """    </div>
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
SIGN_LEAD = autolink(
    "Every sign on every gate in Harare is yellow and black. That does the "
    "warning job and none of the other one, because nothing distinguishes one "
    "company&#8217;s sign from the next.", max_links=1)

SOLAR_LEAD = autolink(
    "Cutting a bill and surviving an outage are the same job. We size, supply "
    "and maintain systems that carry the loads you actually run.", max_links=2)

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
          %s
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
""" % (eyebrow("Solar PV"), SOLAR_LEAD,
       pbtn("Ask for a solar assessment", "contact.html")) + shead(
  "Why Sentinel solar", "Three things a system gets judged on",
  "Once the installers have gone, this is what you are left with.") + """
      <div class="grid g-3">
""" + ncard("white", "shield-check", "Durability",
            "Built for real conditions: dust, heat, storms and the load profile of an "
            "actual Zimbabwean site.",
            [], "contact.html", "How we are built") \
    + ncard("lime", "sun", "Reliability",
            "Panels that perform without compromise, backed by a service schedule rather "
            "than a handshake.",
            [], "contact.html", "Work with us") \
    + ncard("dark", "lightning", "Output",
            "More energy over the life of the system, so the saving you were promised holds "
            "up.",
            [], "contact.html", "Ask a question") + """      </div>
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
          <span class="plink">What this covers %s</span>
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
          <span class="plink">What is included %s</span>
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
       c["legal"], autolink(c["lead"], max_links=2), c["strap"],
       ", ".join(c["sectors"]), " &rsaquo; ".join(c["process"]),
       pbtn("Open " + c["short"], c["href"],
            "pbtn--light" if ground == "dark" else "pbtn--dark"),
       rows, units)


grp = phero("The group", "Three companies, one standard of work",
  "Sentinel runs as a group. One company builds the electronic systems, one runs the "
  "people on the ground, and one carries the technology business. This is how they "
  "fit together.",
  "control-room-monitoring", "A Sentinel operator in the control room") + """
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

  <section class="section section--cream">
    <div class="container">
""" % (eyebrow("What we carry"), c["headline"], c["strap"],
       autolink(c["blurb"], max_links=2),
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


company_page("guarding", "officers-team",
  "A Sentinel team outside the branch",
  "Sentinel Security Services: manned security, dog units and armed response | " + ORG,
  "Protective asset management, event security, 24 hour alarm monitoring and armed "
  "response, dog units, perimeter protection and investigations across all ten provinces of Zimbabwe.")

company_page("circuitron", "circuitron-bench",
  "Patch cabling in a Circuitron network cabinet",
  "Circuitron Systems: technology, communications and electronics | " + ORG,
  "Circuitron Systems delivers security systems, two way radio and networking, smart "
  "building automation, computers and power, plus CircuitStore retail and EcoCircuit "
  "electronic waste recovery.")


# ================================================================== SIGNAGE
REGISTERS = [
    ("statutory", "Statutory", "bolt",
     "A real hazard, so the hazard code is kept exactly: ISO yellow, a black "
     "triangle, no brand liberties. Energised fencing is the only genuine "
     "hazard we install, and the sign has to be understood by someone who "
     "reads no English, so it carries three languages."),
    ("deterrent", "Deterrent", "shield",
     "Not a hazard, a declaration: cameras, dogs, response, access. These "
     "carry the Sentinel dark green. On a street where every sign is yellow, "
     "a dark green one is read as a company rather than as hazard furniture, "
     "and lime on that green measures 12:1, so nothing is given up."),
    ("presence", "Presence", "mark",
     "No warning at all. The shield, the name and the number, at eye height "
     "where someone waiting at the gate will read it. Every client site is a "
     "billboard that runs for years."),
]

WALK = [
    ("Street boundary", "armed-response",
     "The first sign, read from a vehicle before anyone stops. It is the one "
     "that changes a decision, so nothing else competes with it here."),
    ("Vehicle gate", "cctv",
     "At the point someone has to wait. Cameras and response together, facing "
     "the driver rather than the house."),
    ("Fence line", "electric-fence",
     "Along the energised run, on both faces, and at every corner and gate. "
     "These are not optional and they are not a deterrent, they are a warning."),
    ("Pedestrian entrance", "access-control",
     "Where a visitor is expected to stop and be logged. Paired with the "
     "intercom so the instruction and the means are in one place."),
    ("Building entry", "alarm-monitored",
     "Beside the door a keyholder uses, and on the glass of a shop or office "
     "where it is read from the pavement."),
    ("Equipment", "asset-tag",
     "On every panel, recorder, motor and reader. It is how a technician knows "
     "the history and how a client knows who to call."),
]

SPEC = [
    ("Material", "3mm aluminium composite for gate and wall signs. 1.5mm "
                 "aluminium for fence signs, which take weather on both faces."),
    ("Print", "UV stable solvent print on the face, matt laminated. Matt, "
              "because a gloss sign at the wrong angle is a mirror."),
    ("Reflective", "Class 1 retroreflective on the street boundary and gate "
                   "signs wherever the approach is unlit."),
    ("Fixing", "Four stainless screws with caps into the wall or gate frame. "
               "Structural tape on glass and on anything that must not be "
               "drilled."),
    ("Height", "Centre at 1.5 to 1.8m where a person reads it. Fence signs go "
               "at the height of the energised wires, not above them."),
    ("Artwork", "Every sign is vector with the type already outlined, so a "
                "sign maker needs no fonts and nothing reflows. Scale to any "
                "size from the same file."),
]


def sign_card(sign, note=None):
    w, h = sign["size_mm"]
    scale = 150.0 / max(w, h)
    return """        <figure class="signcard signcard--%s" data-reveal>
          <div class="signcard__plate">
            <img src="assets/signs/%s.svg" alt="%s"
                 width="%d" height="%d" style="width:%gpx" loading="lazy">
          </div>
          <figcaption>
            <strong><a class="stretch" href="contact.html">%s</a></strong>
            <span class="signcard__meta">%s &middot; %d &times; %d mm</span>
            <small>%s</small>
          </figcaption>
        </figure>
""" % (sign["register"], sign["id"],
       sign["title"] + " sign",
       w, h, round(w * scale), sign["title"],
       sign["register"], w, h, note or sign["use"])


SIGN_BY_ID = {x["id"]: x for x in SIGNS}

sg = phero("Site signage", "The part of the system they actually read",
  "A camera is a deterrent only if someone believes it is there. The sign on "
  "the gate does that work, and it does it every day for years, which makes it "
  "the largest advertising surface the group owns.",
  "sys-cctv", "A dome camera mounted on a wall") + """
  <section class="section section--white">
    <div class="container split split--narrow">
      <div data-reveal>
        %s
        <h2 class="h-2">Three registers, and the split is the point</h2>
        <p class="script script--lg">read before anything else</p>
        <p class="lead">
          %s
        </p>
        <p>
          So we split the set. Where there is a genuine hazard the code is kept
          exactly, because safety is not a place to be interesting. Everywhere
          else the signs are Sentinel green, and they are recognised from across
          a street.
        </p>
        <div style="margin-top:2rem">%s</div>
      </div>
      <div class="cfacts" data-reveal>
        <div class="cfact"><dt>In the set</dt><dd>%d signs</dd></div>
        <div class="cfact"><dt>Artwork</dt><dd>Vector, type outlined</dd></div>
        <div class="cfact"><dt>Languages</dt><dd>English, Shona, Ndebele</dd></div>
        <div class="cfact"><dt>Fitted by</dt><dd><a href="services.html">Sentinel Integrated Technologies</a></dd></div>
      </div>
    </div>
  </section>

  <section class="section section--cream">
    <div class="container">
""" % (eyebrow("Why they look like this"), SIGN_LEAD,
       pbtn("Ask about signage", "contact.html", "pbtn--dark"),
       len(SIGNS)) + shead(
        "The set", "Eight signs, and where each one goes",
        "A sign in the wrong place teaches people to ignore the rest of them.",
        variant="shead--wide") + """
      <div class="signgrid">
""" + "".join(sign_card(x) for x in SIGNS) + """      </div>
    </div>
  </section>

  <section class="section section--dark">
    <div class="container">
""" + shead("Walking a site", "Where the signs go, in the order they are read",
            "This is the survey we do on handover, and it is the same walk "
            "whether the site is a house or a depot.", kv="eyebrow--dark") + """
      <div class="walk">
"""
for _i, (_place, _sid, _note) in enumerate(WALK, 1):
    _s = SIGN_BY_ID[_sid]
    sg += """        <div class="walkstep" data-reveal>
          <span class="walkstep__n num">%02d</span>
          <div class="walkstep__body">
            <h3>%s</h3>
            <p>%s</p>
          </div>
          <a class="walkstep__sign" href="assets/signs/%s.svg" aria-label="%s artwork">
            <img src="assets/signs/%s.svg" alt="" width="%d" height="%d" loading="lazy">
          </a>
        </div>
""" % (_i, _place, _note, _sid, _s["title"], _sid,
       _s["size_mm"][0], _s["size_mm"][1])

sg += """      </div>
    </div>
  </section>

  <section class="section section--cream">
    <div class="container">
""" + shead("On a real wall", "Where these end up",
            "The drawings above are the artwork. This is the same sign on a "
            "client's wall, which is the only place it has to work.") + wall([
    ("sign-wall", icon("shield-check", "i-sm", "ph-fill"),
     "The CCTV warning sign fixed at eye height on a brick wall"),
    ("sign-entrance", icon("scan-smiley", "i-sm", "ph-fill"),
     "The same sign at a building entrance, read on the way in"),
]) + """    </div>
  </section>

  <section class="section section--white">
    <div class="container">
""" + shead("Specification", "What the sign maker needs",
            "Everything here is settled, so a quotation is a price rather than "
            "a conversation.") + """
      <div class="spec">
""" + "".join("""        <div class="spec__row" data-reveal>
          <dt>%s</dt><dd>%s</dd>
        </div>
""" % (k, v) for k, v in SPEC) + """      </div>
    </div>
  </section>
"""

write("signage.html",
      "Site signage: the signs on a Sentinel protected property | " + ORG,
      "The Sentinel sign set: statutory electric fence warnings in three "
      "languages, CCTV, armed response, dog unit, access control and alarm "
      "signs, with the specification a sign maker can quote from.",
      sg)

# ================================================================= CONTACT
contact = phero("Contact", "Tell us about your site",
  "A free survey and risk assessment, anywhere in Zimbabwe. Send the details and our "
  "technical team will come back to you.",
  "technician-panel", "A technician checking a rack on a tablet") + """
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
        <div class="cinfo">
          <span class="cinfo__icon">%s</span>
          <div><h3>Follow us</h3>
            <a class="cinfo__social" href="%s"%s>%s Sentinel on Facebook</a>
            <a class="cinfo__social" href="%s"%s>%s Sentinel on LinkedIn</a>
          </div>
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
       duo("users-three", "i-md"),
       FACEBOOK, OFFSITE, icon("facebook-logo", "i-sm", "ph-fill"),
       LINKEDIN, OFFSITE, icon("linkedin-logo", "i-sm", "ph-fill"),
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

# A line item with no icon means a line nobody chose a glyph for. That is the
# exact failure this was built to prevent, so it stops the build rather than
# shipping a bullet that silently falls back to nothing.
_missed = bullets.missed()
if _missed:
    raise SystemExit("no icon chosen for these line items:\n  "
                     + "\n  ".join(sorted(set(_missed))))

print("done")
