# -*- coding: utf-8 -*-
"""Fetch and subset the accent face.

The accent font carries a handful of short lines, so shipping a whole latin
face for them is waste. This pulls the woff2 Google serves, subsets it to the
characters the built pages actually use, and writes it into assets/fonts.

Run:  python tools/fetch_accent.py
"""
import io, os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, os.pardir)
FONTS = os.path.join(ROOT, "assets", "fonts")

FAMILY = "Caveat"
WEIGHTS = "400;600"
PIN = 600          # the one weight the accent lines use
OUT = "caveat.woff2"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")


def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    return data if binary else data.decode("utf-8")


def used_characters():
    """Every character that appears inside an element carrying .script."""
    chars = set(" ")
    for f in os.listdir(ROOT):
        if not f.endswith(".html"):
            continue
        html = io.open(os.path.join(ROOT, f), encoding="utf-8").read()
        for m in re.finditer(r'class="[^"]*\bscript\b[^"]*"[^>]*>(.*?)</', html, re.S):
            text = re.sub(r"<[^>]+>", "", m.group(1))
            text = text.replace("&amp;", "&").replace("&rsquo;", "’")
            chars.update(text)
    return {c for c in chars if c.isprintable()}


def main():
    css = get("https://fonts.googleapis.com/css2?family=%s:wght@%s&display=swap"
              % (FAMILY.replace(" ", "+"), WEIGHTS))
    # The latin block is the last one Google emits and the one we need.
    blocks = re.findall(r"/\*\s*([a-z-]+)\s*\*/\s*@font-face\s*\{(.*?)\}", css, re.S)
    latin = [b for name, b in blocks if name == "latin"]
    if not latin:
        raise SystemExit("no latin block in:\n" + css[:600])
    url = re.search(r"url\((https://[^)]+\.woff2)\)", latin[0]).group(1)
    print("fetching", url)
    raw = get(url, binary=True)

    tmp = os.path.join(FONTS, "_accent_full.woff2")
    io.open(tmp, "wb").write(raw)
    print("full face %d bytes" % len(raw))

    chars = used_characters()
    print("characters in use: %d  %s" % (len(chars), "".join(sorted(chars))))

    try:
        from fontTools import subset
    except ImportError:
        os.replace(tmp, os.path.join(FONTS, OUT))
        print("fontTools not available; shipped the full face")
        return

    # Caveat ships as a variable face. Only one weight is used, so pinning the
    # axis drops the variation tables before subsetting.
    pinned = tmp
    try:
        from fontTools.ttLib import TTFont
        from fontTools.varLib import instancer
        f = TTFont(tmp)
        if "fvar" in f:
            instancer.instantiateVariableFont(f, {"wght": PIN}, inplace=True)
            pinned = os.path.join(FONTS, "_accent_pinned.ttf")
            f.save(pinned)
            print("pinned wght=%d" % PIN)
    except Exception as e:
        print("could not pin the axis (%s); subsetting the variable face" % e)

    out = os.path.join(FONTS, OUT)
    subset.main([
        pinned,
        "--text=%s" % "".join(sorted(chars)),
        "--flavor=woff2",
        "--layout-features=kern,liga,calt,clig",
        "--output-file=%s" % out,
    ])
    for f_ in (tmp, pinned):
        if os.path.exists(f_) and f_ != out:
            os.remove(f_)
    print("subset %s  %d bytes" % (OUT, os.path.getsize(out)))


if __name__ == "__main__":
    main()
