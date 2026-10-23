# -*- coding: utf-8 -*-
"""Build the Sentinel Integrated Technologies lockups from the supplied art.

The client supplied the lockup as two background removals off a white
original, one inked green and one knocked out white. That matters for how
they are read: in a background removal an edge pixel carries full alpha and a
colour blended toward white, rather than the partial alpha a vector export
would give it. Reading that blend back out as coverage recovers a clean one
channel mask, and painting the one mask twice is what keeps the green file and
the knockout in exact register. They cannot drift, because they are the same
shape.

The compact lockup is not a crop of the full one. The shield keeps its height
and the two remaining lines of type are re-centred against it, which is how
the lockup it replaces was built, and the only way to drop the entity line
without shrinking the mark along with it.

Sources live outside the repository. Set SENTINEL_LOGO_SRC if they are
somewhere other than the default.

Run:  python tools/sit_lockup.py
"""
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, os.pardir)
BRAND = os.path.join(ROOT, "assets", "img", "brand")
SRC = os.environ.get("SENTINEL_LOGO_SRC",
                     r"C:\Users\PC\Downloads\New folder (3)")
# Only the green file is read. The knockout is painted from the same mask, so
# the supplied white version is a cross check rather than an input.
GREEN_FILE = "7aeaed79-2b61-455b-8cff-07428c8c6757_removalai_preview.png"

# --g-mid, the green every other lockup on the site is drawn in. The supplied
# art inks at #01662E, close enough that the difference is JPEG drift rather
# than a decision, and far enough to read as a second green beside the UI.
BRAND_GREEN = (0x0C, 0x69, 0x34)

# Coverage is held to 32 steps. The art never renders above 58px, a quarter of
# the file's own height, so the browser averages any step away long before it
# could show; what it buys is half the file size, because the alpha channel
# keeps long flat runs. Resampling the art smaller does the opposite, inventing
# a distinct value per pixel: 456px wide came out half again bigger than the
# 555px it was made from, so the art is kept at the size it arrived.
ALPHA_STEPS = 32
INK_FLOOR = 0.08          # what counts as ink when measuring
DROP_BELOW = 0.004        # coverage this faint is rounding noise, not edge


def coverage(im):
    """A one channel mask, read back out of a removal off white paper."""
    a = np.asarray(im).astype(np.float64)
    rgb, alpha = a[..., :3], a[..., 3] / 255.0

    flat = np.asarray(im).reshape(-1, 4)
    solid = flat[flat[:, 3] > 250]
    vals, counts = np.unique(solid[:, :3], axis=0, return_counts=True)
    ink = vals[counts.argmax()].astype(np.float64)

    # c = ink*k + 255*(1-k), solved per channel and averaged.
    k = ((255.0 - rgb) / np.maximum(255.0 - ink, 1.0)).mean(axis=2)
    m = np.clip(k, 0.0, 1.0) * alpha
    m[m < DROP_BELOW] = 0.0
    return m, tuple(int(v) for v in ink)


def bbox(m):
    ys, xs = np.nonzero(m > INK_FLOOR)
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def runs(occ):
    out, start = [], None
    for i, v in enumerate(occ):
        if v and start is None:
            start = i
        elif not v and start is not None:
            out.append((start, i))
            start = None
    if start is not None:
        out.append((start, len(occ)))
    return out


def paint(m, colour):
    h, w = m.shape
    out = np.zeros((h, w, 4), dtype=np.uint8)
    out[..., 0], out[..., 1], out[..., 2] = colour
    q = np.rint(np.clip(m, 0.0, 1.0) * ALPHA_STEPS) / ALPHA_STEPS
    out[..., 3] = np.clip(np.rint(q * 255.0), 0, 255).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def write(m, name, colour):
    p = os.path.join(BRAND, name)
    paint(m, colour).save(p, optimize=True)
    print("  %-30s %dx%d  %6d bytes"
          % (name, m.shape[1], m.shape[0], os.path.getsize(p)))


def main():
    path = os.path.join(SRC, GREEN_FILE)
    if not os.path.exists(path):
        print("no source art at %s\nset SENTINEL_LOGO_SRC" % path)
        return 1

    mask, ink = coverage(Image.open(path).convert("RGBA"))
    print("supplied ink #%02X%02X%02X, redrawn in #%02X%02X%02X"
          % (ink + BRAND_GREEN))

    whole = bbox(mask)

    # The shield is the ink left of the gutter, and the gutter is the widest
    # empty column run inside the artwork rather than a measured constant, so
    # re-exported art with different spacing still splits in the right place.
    cols = (mask > INK_FLOOR).any(axis=0)
    gaps = [g for g in runs(~cols) if whole[0] < g[0] < whole[2]]
    if not gaps:
        print("no gutter between the shield and the type")
        return 1
    gutter = max(gaps, key=lambda g: g[1] - g[0])

    shield_box = bbox(mask[:, :gutter[0]])
    tb = bbox(mask[:, gutter[1]:])
    type_box = (tb[0] + gutter[1], tb[1], tb[2] + gutter[1], tb[3])
    lines = runs((mask[:, gutter[1]:] > INK_FLOOR).any(axis=1))
    if len(lines) != 3:
        print("expected three lines of type, found %d" % len(lines))
        return 1
    print("shield %s, type %s, lines %s" % (shield_box, type_box, lines))

    full = mask[whole[1]:whole[3], whole[0]:whole[2]]

    pad = type_box[0] - shield_box[2]
    shield = mask[shield_box[1]:shield_box[3], shield_box[0]:shield_box[2]]
    two = mask[lines[0][0]:lines[1][1], type_box[0]:type_box[2]]
    ch, sw = shield.shape[0], shield.shape[1]
    comp = np.zeros((ch, sw + pad + two.shape[1]))
    comp[:, :sw] = shield
    top = (ch - two.shape[0]) // 2
    comp[top:top + two.shape[0], sw + pad:] = two
    cb = bbox(comp)
    comp = comp[cb[1]:cb[3], cb[0]:cb[2]]

    print("written:")
    write(full, "sit-lockup.png", BRAND_GREEN)
    write(full, "sit-lockup-white.png", (255, 255, 255))
    write(comp, "sit-lockup-compact.png", BRAND_GREEN)
    write(comp, "sit-lockup-compact-white.png", (255, 255, 255))
    if full.shape != comp.shape:
        print("note: the two lockups trim to different boxes, so group.py "
              "needs a logo_wh for each")
    return 0


if __name__ == "__main__":
    sys.exit(main())
