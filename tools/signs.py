# -*- coding: utf-8 -*-
"""The Sentinel site signage.

A security company's signs are two jobs in one object. They warn, and they are
the company's largest advertising surface: every client gate carries one, for
years, in public. The reference sets are all yellow and black, which does the
first job and none of the second, because every sign on every gate looks the
same.

So the set splits into three registers, and the split is the whole idea.

  statutory   A real hazard. Yellow and black, ISO shapes, no brand liberties.
              Electric fencing is the only genuine hazard Sentinel installs,
              and the sign for it must be understood by someone who reads no
              English, so it is set in three languages.

  deterrent   Not a hazard, a declaration: cameras, dogs, response, access.
              These carry the Sentinel dark green and lime. On a street where
              every sign is yellow, a dark green one is read as a company
              rather than as generic hazard furniture, and lime on g-900 is
              12:1, so nothing is given up in legibility.

  presence    The billboard. Shield, name, response number. No warning at all.

Run:  python tools/signs.py            writes assets/signs/*.svg
      python tools/signs.py --sheet p  plus a proof page
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, os.pardir)
OUT = os.path.join(ROOT, "assets", "signs")
sys.path.insert(0, HERE)

import typeset
from sign_glyphs import GLYPHS, CUTS, EXTRA

# ------------------------------------------------------------------ colour
INK = "#051D14"          # g-900, the deterrent field
DEEP = "#03140E"         # g-950, the foot bar
LIME = "#A9EE6E"
WHITE = "#FFFFFF"
HAZARD = "#FFD200"       # ISO safety yellow
BLACK = "#000000"
MUTED = "#9FB3A6"

# The shield, from the logo, at its own 589 x 568 scale.
SHIELD = ("M0 0H589V401L423 567H166L0 401Z"
          "M41 41H548V386L408 526H181L41 386Z")
SHIELD_BARS = [(96, 82, 391, 41), (96, 171, 391, 41), (96, 260, 391, 41),
               (96, 377, 391, 41), (96, 123, 41, 48), (446, 123, 41, 48),
               (274, 212, 41, 48), (96, 301, 41, 76), (199, 452, 191, 41)]


def shield(x, y, h, colour):
    s = h / 568.0
    bars = "".join("M%g %gh%gv%gh-%gZ" % (bx, by, bw, bh, bw)
                   for bx, by, bw, bh in SHIELD_BARS)
    return ('<g transform="translate(%g %g) scale(%g)" fill="%s">'
            '<path fill-rule="evenodd" d="%s"/><path d="%s"/></g>'
            % (x, y, s, colour, SHIELD, bars))


def glyph(name, x, y, size, colour, field):
    """A solid pictogram. Knockouts are painted in the field colour rather than
    masked, which keeps the file simple enough for a sign maker to open."""
    sc = size / 100.0
    out = ['<g transform="translate(%g %g) scale(%g)">' % (x, y, sc)]
    for d, rule in GLYPHS[name]:
        out.append('<path d="%s" fill="%s" fill-rule="%s"/>' % (d, colour, rule))
    for key in CUTS.get(name, []):
        for d, rule in GLYPHS[key]:
            out.append('<path d="%s" fill="%s" fill-rule="%s"/>' % (d, field, rule))
    for key in EXTRA.get(name, []):
        for d, rule in GLYPHS[key]:
            out.append('<path d="%s" fill="%s" fill-rule="%s"/>' % (d, colour, rule))
    out.append("</g>")
    return "".join(out)


def fit(text, size, max_w, weight=800, tracking=0.0, floor=0.5):
    """Shrink a line until it fits the sign. Overflowing type on a sign is not
    a near miss, it is an unreadable sign."""
    w = typeset.width(text, size, weight, tracking)
    if w <= max_w:
        return size
    return max(size * floor, size * max_w / w)


def t(text, size, x, y, colour, weight=800, tracking=0.0, anchor="middle",
      max_w=None):
    if max_w:
        size = fit(text, size, max_w, weight, tracking)
    d = typeset.path(text, size, x, y, weight=weight, tracking=tracking, anchor=anchor)
    return '<path d="%s" fill="%s"/>' % (d, colour)


# ------------------------------------------------------------------ roster
CONTACT = "+263 77 358 9461"

SIGN_GLYPH = {
    "cctv": "camera",
    "armed-response": "response",
    "guard-dogs": "dog",
    "access-control": "reader",
    "alarm-monitored": "alarm",
}

SIGNS = [
    # ------------------------------------------------------- statutory
    {
        "id": "electric-fence",
        "title": "Electric fence warning",
        "register": "statutory",
        "shape": "hazard",
        "size_mm": (220, 300),
        "icon": "electric-fence",
        "lines": ["DANGER", "ELECTRIC FENCE"],
        "languages": [("Shona", "NGOZI: MAGETSI"), ("Ndebele", "INGOZI: UGESI")],
        "use": "Every 10m along an energised fence, both faces, and at every "
               "gate and corner. Required wherever the fence is energised.",
    },

    # ------------------------------------------------------- deterrent
    {
        "id": "cctv",
        "title": "CCTV in operation",
        "register": "deterrent",
        "shape": "portrait",
        "size_mm": (300, 400),
        "icon": "cam-dome",
        "lines": ["CCTV", "IN OPERATION"],
        "sub": "Recorded and monitored 24 hours a day",
        "use": "At every vehicle and pedestrian entrance, and at the boundary "
               "of any area a camera covers.",
    },
    {
        "id": "armed-response",
        "title": "Armed response",
        "register": "deterrent",
        "shape": "portrait",
        "size_mm": (300, 400),
        "icon": "patrol",
        "lines": ["ARMED", "RESPONSE"],
        "sub": "Monitored by the Sentinel control room",
        "use": "On the gate and the street boundary. This is the one that "
               "changes a decision, so it goes where it is read first.",
    },
    {
        "id": "guard-dogs",
        "title": "Guard dogs on patrol",
        "register": "deterrent",
        "shape": "portrait",
        "size_mm": (300, 400),
        "icon": "k9",
        "lines": ["GUARD DOGS", "ON PATROL"],
        "sub": "Do not enter without an escort",
        "use": "Where dogs actually work, and nowhere else. A dog sign on a "
               "site with no dog teaches people the signs are bluffs.",
    },
    {
        "id": "access-control",
        "title": "Access controlled",
        "register": "deterrent",
        "shape": "portrait",
        "size_mm": (300, 400),
        "icon": "access-reader",
        "lines": ["ACCESS", "CONTROLLED"],
        "sub": "Report to reception. All visitors are logged",
        "use": "At the pedestrian gate and reception door of a controlled site.",
    },
    {
        "id": "alarm-monitored",
        "title": "Alarm monitored",
        "register": "deterrent",
        "shape": "landscape",
        "size_mm": (300, 200),
        "icon": "alarm-panel",
        "lines": ["ALARM MONITORED"],
        "sub": "Linked to armed response",
        "use": "Beside the door a keyholder uses, and on the window of a shop "
               "or office where it is read from the pavement.",
    },

    # -------------------------------------------------------- presence
    {
        "id": "protected-by",
        "title": "Protected by Sentinel",
        "register": "presence",
        "shape": "landscape",
        "size_mm": (300, 200),
        "icon": None,
        "lines": ["PROTECTED BY"],
        "sub": CONTACT,
        "use": "The billboard. One per site, at eye height where someone "
               "waiting at the gate will read it.",
    },

    # --------------------------------------------------------- utility
    {
        "id": "asset-tag",
        "title": "Equipment asset tag",
        "register": "deterrent",
        "shape": "tag",
        "size_mm": (80, 50),
        "icon": None,
        "lines": ["MAINTAINED BY SENTINEL"],
        "sub": "Asset        Serviced",
        "use": "On every panel, recorder, motor and reader Sentinel installs. "
               "It is how a technician knows the history, and how a client "
               "knows who to call.",
    },
]


# ------------------------------------------------------------------ layout
def triangle(cx, top, width, field, edge, sw):
    """The ISO warning triangle, as an element."""
    hh = width * 0.866
    return ('<path d="M%g %g L%g %g L%g %g Z" fill="%s" stroke="%s" '
            'stroke-width="%g" stroke-linejoin="round"/>'
            % (cx, top, cx + width / 2, top + hh, cx - width / 2, top + hh,
               field, edge, sw))


def frame(shape, w, h, field, edge):
    """The sign's outline. Rounded for the brand shapes, square for the
    statutory plate, because a hazard sign should not look designed."""
    if shape == "hazard":
        return ('<rect x="3" y="3" width="%g" height="%g" rx="4" fill="%s" '
                'stroke="%s" stroke-width="6"/>' % (w - 6, h - 6, field, edge))
    r = {"tag": 6, "landscape": 14, "portrait": 18}.get(shape, 16)
    return ('<rect x="3" y="3" width="%g" height="%g" rx="%g" fill="%s" '
            'stroke="%s" stroke-width="6"/>' % (w - 6, h - 6, r, field, edge))


def foot(w, h, depth, bar, ink, accent, line=None):
    """The Sentinel bar: who is behind the sign, and the number to call."""
    y = h - depth
    out = ['<path d="M%g %gh%gv%ga0 0 0 0 0h-%gZ" fill="%s"/>'
           % (3, y, w - 6, depth - 3 - 14, w - 6, bar)]
    out = ['<rect x="3" y="%g" width="%g" height="%g" fill="%s"/>'
           % (y, w - 6, depth - 6, bar)]
    sh = depth * 0.46
    out.append(shield(22, y + (depth - sh) / 2 - 2, sh, accent))
    tx = 22 + sh * (589.0 / 568.0) + 14
    out.append(t("SENTINEL", depth * 0.30, tx, y + depth * 0.46,
                 ink, weight=800, tracking=0.03, anchor="start"))
    out.append(t(line or CONTACT, depth * 0.21, tx, y + depth * 0.76,
                 accent, weight=700, tracking=0.01, anchor="start"))
    return "".join(out)


def build(sign):
    w, h = sign["size_mm"]
    reg = sign["register"]
    shape = sign["shape"]
    parts = []

    if reg == "statutory":
        field, edge, ink, accent, bar = HAZARD, BLACK, BLACK, BLACK, BLACK
    else:
        field, edge, ink, accent, bar = INK, LIME, WHITE, LIME, DEEP

    parts.append(frame(shape, w, h, field, edge))

    # ---------------------------------------------------------- statutory
    if shape == "hazard":
        tw = w * 0.56
        parts.append(triangle(w / 2, 22, tw, HAZARD, BLACK, 7))
        parts.append(glyph("bolt", w / 2 - tw * .17, 22 + tw * .30, tw * .34,
                           BLACK, HAZARD))
        parts.append(t(sign["lines"][0], 40, w / 2, 170, BLACK, 800, .01,
                       max_w=w - 36))
        parts.append(t(sign["lines"][1], 20, w / 2, 194, BLACK, 800, .02,
                       max_w=w - 36))
        parts.append('<rect x="%g" y="204" width="%g" height="2.5" fill="%s"/>'
                     % (w * .24, w * .52, BLACK))
        y = 226
        for _name, text in sign["languages"]:
            parts.append(t(text, 15, w / 2, y, BLACK, 700, .02, max_w=w - 40))
            y += 19
        parts.append(foot(w, h, 42, BLACK, HAZARD, HAZARD))
        return svg(w, h, parts, sign)

    # --------------------------------------------------------------- tag
    if shape == "tag":
        parts.append(t(sign["lines"][0], 6.4, w / 2, 15, accent, 800, .04, max_w=w - 16))
        parts.append('<rect x="9" y="21" width="%g" height="15" rx="3" fill="none" '
                     'stroke="%s" stroke-width="1" opacity=".45"/>' % (w - 18, MUTED))
        parts.append('<rect x="%g" y="21" width="1" height="15" fill="%s" opacity=".45"/>'
                     % (w / 2, MUTED))
        parts.append(t("ASSET", 3.8, 14, 27, MUTED, 700, .08, "start"))
        parts.append(t("SERVICED", 3.8, w - 14, 27, MUTED, 700, .08, "end"))
        parts.append(t(CONTACT, 5.2, w / 2, 45, ink, 700, .02, max_w=w - 16))
        return svg(w, h, parts, sign)

    # ---------------------------------------------------------- presence
    if sign["id"] == "protected-by":
        parts.append(shield(w / 2 - 33, 26, 64, LIME))
        parts.append(t("PROTECTED BY", 13, w / 2, 118, MUTED, 700, .16, max_w=w * .7))
        parts.append(t("SENTINEL", 38, w / 2, 156, WHITE, 800, .02, max_w=w - 56))
        parts.append('<rect x="%g" y="166" width="%g" height="2.5" fill="%s"/>'
                     % (w * .30, w * .40, LIME))
        parts.append(t(CONTACT, 15, w / 2, 186, LIME, 700, .02, max_w=w - 56))
        return svg(w, h, parts, sign)

    # --------------------------------------------------------- landscape
    if shape == "landscape":
        parts.append(glyph(SIGN_GLYPH[sign["id"]], 24, h / 2 - 58, 64, accent, field))
        parts.append(t(sign["lines"][0], 26, 108, h / 2 - 6, ink, 800, .01, "start",
                       max_w=w - 132))
        parts.append(t(sign["sub"], 12.5, 108, h / 2 + 16, accent, 700, .01, "start",
                       max_w=w - 132))
        parts.append(foot(w, h, 46, bar, ink, accent))
        return svg(w, h, parts, sign)

    # ---------------------------------------------------------- portrait
    parts.append(glyph(SIGN_GLYPH[sign["id"]], w / 2 - 54, 42, 108, accent, field))
    size = 40.0
    for line in sign["lines"]:
        size = min(size, fit(line, 40, w - 56, 800, .005))
    y = 212
    for line in sign["lines"]:
        parts.append(t(line, size, w / 2, y, ink, 800, .005))
        y += size * 1.06
    parts.append('<rect x="%g" y="%g" width="%g" height="3" fill="%s"/>'
                 % (w * .22, y - 14, w * .56, accent))
    parts.append(t(sign["sub"], 13.5, w / 2, y + 14, accent, 700, .01, max_w=w - 44))
    parts.append(foot(w, h, 72, bar, ink, accent))
    return svg(w, h, parts, sign)


def svg(w, h, parts, sign):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %g %g" '
            'width="%gmm" height="%gmm" role="img" aria-label="%s">%s</svg>\n'
            % (w, h, w, h, " ".join(sign["lines"]), "".join(parts)))


def main():
    os.makedirs(OUT, exist_ok=True)
    for s in SIGNS:
        doc = build(s)
        p = os.path.join(OUT, s["id"] + ".svg")
        io.open(p, "w", encoding="utf-8", newline="\n").write(doc)
        print("%-18s %-10s %4dx%-4d mm  %6d bytes"
              % (s["id"], s["register"], s["size_mm"][0], s["size_mm"][1], len(doc)))
    if "--sheet" in sys.argv:
        write_sheet(sys.argv[sys.argv.index("--sheet") + 1])


def write_sheet(path):
    cells = ""
    for s in SIGNS:
        w, h = s["size_mm"]
        cells += ('<figure class="%s"><img src="%s.svg" style="width:%gpx;height:%gpx" alt="">'
                  '<figcaption><b>%s</b><span>%s &middot; %d &times; %d mm</span>'
                  '<small>%s</small></figcaption></figure>'
                  % (s["register"], s["id"], w * 0.9, h * 0.9, s["id"],
                     s["register"], w, h, s["use"]))
    html = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>Sentinel signage</title>
<style>
body{margin:0;padding:26px;background:#E9EBE3;font:13px/1.45 system-ui,sans-serif;color:#06291B}
h1{font-size:19px;margin:0 0 4px}
p.i{margin:0 0 20px;color:#55655B;max-width:76ch}
.g{display:flex;flex-wrap:wrap;gap:20px;align-items:flex-start}
figure{margin:0;background:#fff;padding:16px;border-radius:12px;width:320px;
border:1px solid #D5DACF}
figure img{display:block;margin:0 auto 12px}
figcaption b{display:block;font-size:13px}
figcaption span{display:block;font-size:11px;color:#55655B;margin:2px 0 6px;
text-transform:uppercase;letter-spacing:.06em}
figcaption small{color:#55655B;font-size:11.5px}
</style></head><body>
<h1>Sentinel site signage</h1>
<p class="i">Statutory signs keep the hazard code. Deterrent and presence signs
carry the brand, because on a street where every sign is yellow a dark green
one is read as a company rather than as furniture.</p>
<div class="g">%s</div></body></html>""" % cells
    io.open(path, "w", encoding="utf-8", newline="\n").write(html)
    print("wrote", path)


if __name__ == "__main__":
    main()
