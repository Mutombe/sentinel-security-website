# -*- coding: utf-8 -*-
"""Turn tools/icons.py into one SVG sprite, plus a contact sheet for checking.

Run:  python tools/build_icons.py
Writes assets/icons/sentinel.svg (the sprite) and, with --sheet, a local
proof page that shows every glyph at 20, 24, 32 and 64 px.
"""
import io, os, sys, re

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from icons import ICONS

ROOT = os.path.join(HERE, os.pardir)
SPRITE = os.path.join(ROOT, "assets", "icons", "sentinel.svg")


def squeeze(s):
    return re.sub(r">\s+<", "><", re.sub(r"\s+", " ", s)).strip()


def sprite():
    out = ['<svg xmlns="http://www.w3.org/2000/svg" style="display:none">']
    for name, (title, body) in ICONS.items():
        out.append(
            '<symbol id="si-%s" viewBox="0 0 24 24" fill="none" '
            'stroke="currentColor" stroke-width="1.5" stroke-linecap="round" '
            'stroke-linejoin="round"><title>%s</title>%s</symbol>'
            % (name, title, squeeze(body)))
    out.append("</svg>")
    return "".join(out) + "\n"


def sheet():
    cells = []
    for name, (title, body) in ICONS.items():
        uses = "".join(
            '<svg class="g" style="width:%dpx;height:%dpx" aria-hidden="true">'
            '<use href="#si-%s"/></svg>' % (s, s, name) for s in (20, 24, 32, 64))
        cells.append('<figure><div class="row">%s</div>'
                     '<figcaption>%s<small>%s</small></figcaption></figure>'
                     % (uses, name, title))
    return """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>Sentinel icon proof</title><style>
:root{--ink:#06291B;--lime:#A9EE6E}
body{margin:0;padding:28px;font:14px/1.4 system-ui,sans-serif;background:#F7F7EF;color:var(--ink)}
h1{font-size:18px;margin:0 0 20px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px}
figure{margin:0;padding:14px;background:#fff;border:1px solid #E3E6E0;border-radius:12px}
.row{display:flex;align-items:flex-end;gap:12px;min-height:72px}
.g{color:var(--ink)}
figcaption{margin-top:10px;font-size:12px;font-weight:700;display:flex;justify-content:space-between;gap:8px}
figcaption small{font-weight:400;opacity:.55}
.dark{background:#06291B;margin-top:24px;padding:20px;border-radius:14px}
.dark figure{background:#093522;border-color:rgba(255,255,255,.1)}
.dark .g{color:var(--lime)}
.dark figcaption{color:#fff}
</style></head><body>
<h1>Sentinel icon set, %d glyphs at 20 / 24 / 32 / 64 px</h1>
%s
<div class="grid">%s</div>
<div class="dark"><div class="grid">%s</div></div>
</body></html>
""" % (len(ICONS), sprite(), "".join(cells), "".join(cells))


if __name__ == "__main__":
    s = sprite()
    with io.open(SPRITE, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)
    print("wrote assets/icons/sentinel.svg  %d glyphs  %d bytes" % (len(ICONS), len(s)))
    if "--sheet" in sys.argv:
        p = sys.argv[sys.argv.index("--sheet") + 1]
        with io.open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(sheet())
        print("wrote", p)
