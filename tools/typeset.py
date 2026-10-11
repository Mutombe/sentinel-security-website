# -*- coding: utf-8 -*-
"""Set a line of type as an SVG path.

Sign artwork goes to a sign maker, who will not have the font. Live text in an
SVG also fails the moment it is used as an <img>. So the type is outlined: the
glyph contours come straight out of the woff2 and become one path.

Only what signs need: a single line, one weight, optional tracking, and
left/centre/right alignment.
"""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, os.pardir, "assets", "fonts")

_CACHE = {}


def _font(weight):
    if weight not in _CACHE:
        path = os.path.join(FONTS, "manrope-%d.woff2" % weight)
        f = TTFont(path)
        _CACHE[weight] = (f, f.getGlyphSet(), f.getBestCmap(),
                          f["head"].unitsPerEm, f["hmtx"])
    return _CACHE[weight]


def width(text, size, weight=800, tracking=0.0):
    """Advance width of a line, in the same units as `size`."""
    _f, _gs, cmap, upem, hmtx = _font(weight)
    total = 0.0
    for i, ch in enumerate(text):
        g = cmap.get(ord(ch))
        if g is None:
            g = cmap.get(ord(" "))
        total += hmtx[g][0] / upem * size
        if i < len(text) - 1:
            total += tracking * size
    return total


def path(text, size, x, y, weight=800, tracking=0.0, anchor="start"):
    """One path for the whole line. `y` is the baseline."""
    _f, gs, cmap, upem, hmtx = _font(weight)
    w = width(text, size, weight, tracking)
    if anchor == "middle":
        x -= w / 2.0
    elif anchor == "end":
        x -= w
    scale = size / upem
    out = []
    pen_x = x
    for ch in text:
        g = cmap.get(ord(ch)) or cmap.get(ord(" "))
        spen = SVGPathPen(gs)
        # y is flipped: font units go up, SVG goes down.
        tpen = TransformPen(spen, (scale, 0, 0, -scale, pen_x, y))
        gs[g].draw(tpen)
        d = spen.getCommands()
        if d:
            out.append(d)
        pen_x += hmtx[g][0] / upem * size + tracking * size
    return " ".join(out)


def block(lines, size, x, y, leading, **kw):
    """Several lines sharing one path, stacked from the first baseline."""
    return " ".join(path(t, size, x, y + i * leading, **kw)
                    for i, t in enumerate(lines) if t)
