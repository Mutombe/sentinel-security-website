# -*- coding: utf-8 -*-
"""Source the site's photography from Unsplash.

Every photograph on this site has a job: a named slot in tools/photo_plan.py
says what has to be in the frame and where it is used. This script searches
Unsplash for each slot, writes the candidates out as a contact sheet so a human
can choose, then downloads the chosen ones at the two sizes the markup asks
for and records the credit.

Unsplash requires three things of an API client, and all three are handled:
  1. attribution to the photographer and to Unsplash (assets/img/photos/CREDITS.md
     and a credit line rendered on the page),
  2. a call to the photo's download endpoint when a photo is actually used,
  3. hotlinking is not required for API downloads, but the download trigger is.

Usage:
    set UNSPLASH_ACCESS_KEY=...
    python tools/photos.py search            # search every slot, write a sheet
    python tools/photos.py search cctv alarms   # or named slots only
    python tools/photos.py fetch             # download whatever CHOICES names
    python tools/photos.py triggers          # acknowledge downloads to Unsplash
    python tools/photos.py credits           # rewrite CREDITS.md from the store
"""
import io, json, os, sys, time, urllib.request, urllib.parse, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, os.pardir)
PHOTOS = os.path.join(ROOT, "assets", "img", "photos")
STORE = os.path.join(HERE, "photo_store.json")
SHEET = os.path.join(HERE, os.pardir, "tools", "photo_candidates.html")

API = "https://api.unsplash.com"
KEY = os.environ.get("UNSPLASH_ACCESS_KEY", "")

sys.path.insert(0, HERE)
from photo_plan import SLOTS, CHOICES


def _get(path, **params):
    if not KEY:
        raise SystemExit("UNSPLASH_ACCESS_KEY is not set")
    url = API + path + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "Authorization": "Client-ID " + KEY,
        "Accept-Version": "v1",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def load_store():
    if os.path.exists(STORE):
        return json.load(io.open(STORE, encoding="utf-8"))
    return {"candidates": {}, "used": {}}


def save_store(st):
    io.open(STORE, "w", encoding="utf-8", newline="\n").write(
        json.dumps(st, indent=1, ensure_ascii=False))


# ------------------------------------------------------------------ search
def search(only=None, per_slot=1, per_page=24):
    st = load_store()
    slots = [s for s in SLOTS if not only or s["id"] in only]
    for slot in slots:
        if not only and len(st["candidates"].get(slot["id"], [])) >= per_page:
            print("%-22s already searched" % slot["id"])
            continue
        found = list(st["candidates"].get(slot["id"], []))
        seen = {c["id"] for c in found}
        for q in slot["queries"][:per_slot]:
            try:
                res = _get("/search/photos", query=q, per_page=per_page,
                           orientation=slot.get("orientation", "landscape"),
                           content_filter="high")
            except urllib.error.HTTPError as e:
                if e.code == 403:
                    print("  rate limit reached; %d slots still to do" %
                          sum(1 for x in slots if x["id"] not in st["candidates"]))
                    save_store(st); write_sheet(st); return
                print("  ! %s: %s" % (q, e))
                time.sleep(2)
                continue
            for p in res.get("results", []):
                if p["id"] in seen:
                    continue
                seen.add(p["id"])
                found.append({
                    "id": p["id"],
                    "query": q,
                    "w": p["width"], "h": p["height"],
                    "colour": p.get("color"),
                    "alt": (p.get("alt_description") or "").strip(),
                    "desc": (p.get("description") or "").strip(),
                    "thumb": p["urls"]["small"],
                    "raw": p["urls"]["raw"],
                    "download_location": p["links"]["download_location"],
                    "html": p["links"]["html"],
                    "by": p["user"]["name"],
                    "by_url": p["user"]["links"]["html"],
                    "by_user": p["user"]["username"],
                })
            time.sleep(0.4)
        st["candidates"][slot["id"]] = found
        save_store(st)
        print("%-22s %3d candidates" % (slot["id"], len(found)))
    write_sheet(st)


def write_sheet(st):
    rows = []
    for slot in SLOTS:
        cands = st["candidates"].get(slot["id"], [])
        chosen = CHOICES.get(slot["id"])
        cells = "".join(
            '<figure%s><img src="%s&w=320&h=214&fit=crop" loading="lazy" '
            'width="320" height="214" alt="">'
            '<figcaption><code>%s</code><span>%s</span>'
            '<small>%s</small></figcaption></figure>'
            % (' class="on"' if c["id"] == chosen else "", c["thumb"],
               c["id"], (c["alt"] or c["query"])[:58], c["by"])
            for c in cands)
        rows.append(
            '<section><h2>%s <small>%s</small></h2>'
            '<p class="want">%s</p><div class="grid">%s</div></section>'
            % (slot["id"], slot["use"], slot["want"], cells))
    html = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>Photo candidates</title><style>
body{margin:0;padding:24px;background:#F7F7EF;color:#06291B;font:14px/1.45 system-ui,sans-serif}
h1{font-size:20px;margin:0 0 6px} h2{font-size:15px;margin:28px 0 2px}
h2 small{font-weight:400;opacity:.6;font-size:12px;margin-left:8px}
.want{margin:2px 0 10px;font-size:12.5px;color:#55655B}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px}
figure{margin:0;background:#fff;border:1px solid #E4E6DA;border-radius:10px;overflow:hidden}
figure.on{border-color:#0C6934;box-shadow:0 0 0 2px #0C6934}
figure img{width:100%%;height:auto;display:block;aspect-ratio:3/2;object-fit:cover}
figcaption{padding:7px 9px;font-size:11px}
figcaption code{display:block;font-size:10px;opacity:.55}
figcaption span{display:block;margin:2px 0}
figcaption small{opacity:.6}
</style></head><body>
<h1>Photo candidates, %d slots</h1>
<p class="want">Pick one id per slot and put it in CHOICES in tools/photo_plan.py, then run
<code>python tools/photos.py fetch</code>.</p>
%s</body></html>""" % (len(SLOTS), "".join(rows))
    io.open(SHEET, "w", encoding="utf-8", newline="\n").write(html)
    print("wrote", os.path.relpath(SHEET, ROOT))


# ------------------------------------------------------------------- fetch
def fetch(only=None):
    from PIL import Image
    st = load_store()
    os.makedirs(PHOTOS, exist_ok=True)
    for slot in SLOTS:
        sid = slot["id"]
        if only and sid not in only:
            continue
        pid = CHOICES.get(sid)
        if not pid:
            print("%-22s no choice yet" % sid)
            continue
        cand = next((c for c in st["candidates"].get(sid, []) if c["id"] == pid), None)
        if cand is None:
            try:
                p = _get("/photos/" + pid)
            except urllib.error.HTTPError as e:
                print("%-22s %s" % (sid, e)); continue
            cand = {"id": p["id"], "raw": p["urls"]["raw"], "alt": p.get("alt_description") or "",
                    "download_location": p["links"]["download_location"],
                    "html": p["links"]["html"], "by": p["user"]["name"],
                    "by_url": p["user"]["links"]["html"], "by_user": p["user"]["username"],
                    "w": p["width"], "h": p["height"]}

        # Unsplash asks for this call whenever a photo is actually used.
        try:
            _get(cand["download_location"].replace(API, ""))
        except Exception as e:
            print("   (download trigger failed: %s)" % e)

        for width, height in slot["sizes"]:
            url = "%s&w=%d&h=%d&fit=crop&crop=%s&q=82&fm=jpg" % (
                cand["raw"], width * 2, height * 2, slot.get("crop", "entropy"))
            out = os.path.join(PHOTOS, "%s-%d.jpg" % (slot["file"], width))
            req = urllib.request.Request(url, headers={"Authorization": "Client-ID " + KEY})
            with urllib.request.urlopen(req, timeout=60) as r, io.open(out, "wb") as f:
                f.write(r.read())
            im = Image.open(out).convert("RGB")
            im = im.resize((width, height), Image.LANCZOS)
            im.save(out, "JPEG", quality=82, optimize=True, progressive=True)
            print("%-22s %-28s %dx%d  %5dKB" % (sid, os.path.basename(out),
                                                width, height,
                                                os.path.getsize(out) // 1024))
        st["used"][sid] = {k: cand[k] for k in
                           ("id", "by", "by_url", "by_user", "html", "alt")}
        st["used"][sid]["file"] = slot["file"]
        save_store(st)
        time.sleep(0.3)
    credits()


# ----------------------------------------------------------------- credits
def credits():
    st = load_store()
    used = st.get("used", {})
    lines = ["# Photography credits", "",
             "Every photograph on this site comes from Unsplash and is used under the",
             "[Unsplash licence](https://unsplash.com/license). The photographers are",
             "credited below and on the page itself.", "",
             "| Slot | File | Photographer | Photo |", "|---|---|---|---|"]
    for sid in sorted(used):
        u = used[sid]
        lines.append("| `%s` | `%s` | [%s](%s?utm_source=sentinel&utm_medium=referral) | [link](%s) |"
                     % (sid, u["file"], u["by"], u["by_url"], u["html"]))
    lines += ["", "Generated by `tools/photos.py credits`."]
    out = os.path.join(PHOTOS, "CREDITS.md")
    io.open(out, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    print("wrote", os.path.relpath(out, ROOT), "(%d photos)" % len(used))


def triggers(only=None):
    """Fire the Unsplash download endpoint for each photo in use.

    The API asks for this whenever a photo is actually used. A demo key allows
    50 requests an hour, so a bulk fetch usually exhausts the budget before it
    gets here. Re run this once the window resets; it is idempotent and records
    which ones have been acknowledged.
    """
    st = load_store()
    done = st.setdefault("triggered", [])
    for sid, u in sorted(st.get("used", {}).items()):
        if sid in done or (only and sid not in only):
            continue
        try:
            p = _get("/photos/" + u["id"])
            _get(p["links"]["download_location"].replace(API, ""))
        except urllib.error.HTTPError as e:
            if e.code == 403:
                print("rate limit reached; %d still to acknowledge"
                      % sum(1 for x in st["used"] if x not in done))
                save_store(st); return
            print("%-20s %s" % (sid, e)); continue
        done.append(sid)
        save_store(st)
        print("%-20s acknowledged" % sid)
        time.sleep(0.3)
    print("all %d acknowledged" % len(done))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "search"
    names = sys.argv[2:] or None
    {"search": search,
     "more": lambda n: search(n, per_slot=4),
     "sheet": lambda _n: write_sheet(load_store()),
     "fetch": fetch,
     "triggers": triggers,
     "credits": lambda *_: credits()}[cmd](names)
