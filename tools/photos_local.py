# -*- coding: utf-8 -*-
"""Bring the client's own photography into the site.

The Unsplash set was contextually wrong in the places that matter most. A
Zimbabwean security company showing European crowds, a Japanese electronics
shop and white hands on its readers is describing somebody else's business, and
on a site whose whole argument is "we are here, we know these sites", that is
not a small thing.

Every photograph with people in it now comes from the client's own supplied
files: officers in Sentinel uniform at Sentinel sites, and licensed stock of
Black African subjects where no Sentinel frame exists for the subject.

Sources live outside the repository, because they are large originals. Set
SENTINEL_PHOTO_SRC if they are somewhere other than the default.

Run:  python tools/photos_local.py          crop and resize every mapping
      python tools/photos_local.py <slot>   just one
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, os.pardir)
PHOTOS = os.path.join(ROOT, "assets", "img", "photos")
SRC = os.environ.get("SENTINEL_PHOTO_SRC",
                     r"C:\Users\PC\Downloads\Sentinel Brochure")

sys.path.insert(0, HERE)
from photo_plan import SLOTS

HERO = [(640, 324), (1200, 608)]
PHERO = [(640, 320), (1200, 600)]
DETAIL = [(640, 480), (1200, 900)]
TILE = [(640, 640)]
WIDE = [(640, 427), (1200, 800)]

# slot file -> (source, focus x, focus y, sizes, note)
# The focus point is where the crop keeps its subject when the aspect changes:
# 0.5, 0.5 is the centre, lower y keeps heads in frame.
LOCAL = {
    # ---- Sentinel's own people, in Sentinel uniform, at Sentinel sites ----
    "security-officers": (
        "Sentinel Security Patrol at Sunset.png", 0.42, 0.46, HERO,
        "Officers and a dog unit on patrol at dusk"),
    "officers-team": (
        "Sentinel Security Team at Headquarters.png", 0.50, 0.42, PHERO,
        "A Sentinel team outside the branch"),
    "officers-warehouse": (
        "Sentinel Warehouse Security Patrol.png", 0.46, 0.46, WIDE,
        "Officers and a dog unit patrolling a warehouse yard"),
    "officer-on-duty": (
        "Sentinel Guards at Modern Office Entrance.png", 0.50, 0.40, PHERO,
        "Sentinel officers on post at an office entrance"),
    "officer-radio": (
        "Sentinel Security Gatehouse Checkpoint.png", 0.38, 0.44, WIDE,
        "An officer working a gatehouse checkpoint by radio"),
    "k9-handler-standing": (
        "Sentinel K9 Security Team.png", 0.44, 0.50, WIDE,
        "A Sentinel handler with a patrol dog"),
    "vehicle-checkpoint": (
        "176f250b-72fd-4da4-a46e-21bf026940f8.png", 0.44, 0.46, WIDE,
        "An officer and a dog unit at an estate gate"),

    # ---- licensed stock, where no Sentinel frame exists for the subject ----
    "control-room-monitoring": (
        "iStock-2191799484.jpg", 0.50, 0.44, HERO,
        "An operator watching a wall of live camera feeds"),
    "tile-night": (
        "iStock-2191799484.jpg", 0.52, 0.42, TILE,
        "An operator watching a wall of live camera feeds"),
    "technician-panel": (
        "iStock-1340944124.jpg", 0.52, 0.46, HERO,
        "A technician checking a rack on a tablet"),
    "sys-access": (
        "iStock-2229982720.jpg", 0.48, 0.46, DETAIL,
        "A reader being used at a door"),
    "tech-smart": (
        "iStock-2285750632.jpg", 0.50, 0.44, WIDE,
        "A smart home panel being set from a phone"),
    "tech-retail": (
        "All-Equipment-in-the-Vivint-Home-Security-System.webp", 0.50, 0.50, WIDE,
        "Security and smart home equipment of the kind CircuitStore carries"),
    "power-solar": (
        "panels-electricity-order-sunlight.webp", 0.50, 0.52, WIDE,
        "A solar array in full sun"),
}


def crop_to(im, w, h, fx, fy):
    """Crop to the target aspect around a focus point, then resize.

    Cropping to the centre loses heads when a 3:2 frame becomes 2:1, so each
    mapping says where its subject is."""
    sw, sh = im.size
    want = w / float(h)
    have = sw / float(sh)
    if have > want:                      # too wide: trim the sides
        nw = int(round(sh * want))
        x = int(round(fx * sw - nw / 2.0))
        x = max(0, min(sw - nw, x))
        box = (x, 0, x + nw, sh)
    else:                                # too tall: trim top and bottom
        nh = int(round(sw / want))
        y = int(round(fy * sh - nh / 2.0))
        y = max(0, min(sh - nh, y))
        box = (0, y, sw, y + nh)
    return im.crop(box).resize((w, h), 1)   # 1 = LANCZOS


def main(only=None):
    from PIL import Image
    os.makedirs(PHOTOS, exist_ok=True)
    missing = []
    for name, (src, fx, fy, sizes, alt) in sorted(LOCAL.items()):
        if only and name not in only:
            continue
        path = os.path.join(SRC, src)
        if not os.path.exists(path):
            missing.append(src)
            continue
        im = Image.open(path).convert("RGB")
        for w, h in sizes:
            out = os.path.join(PHOTOS, "%s-%d.jpg" % (name, w))
            crop_to(im, w, h, fx, fy).save(out, "JPEG", quality=84,
                                           optimize=True, progressive=True)
            print("%-26s %-28s %4dx%-4d %5dKB"
                  % (name, os.path.basename(out), w, h,
                     os.path.getsize(out) // 1024))
    if missing:
        print("\nnot found in %s:" % SRC)
        for m in missing:
            print("   ", m)


if __name__ == "__main__":
    main(sys.argv[1:] or None)
