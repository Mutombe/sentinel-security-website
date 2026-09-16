# Build a trimmed, subsetted Phosphor bundle: only the icons this site uses.
import re, os
from fontTools.ttLib import TTFont
from fontTools import subset

os.chdir(r"C:\Users\PC\documents\sentinel\assets\icons")

ICONS = """security-camera bell-ringing fingerprint fire-extinguisher door-open barricade
house-line buildings factory clock-countdown graduation-cap tag magnifying-glass headset
handshake target compass shield-check sun lightning wrench solar-panel map-pin phone-call
envelope-simple clock whatsapp-logo facebook-logo linkedin-logo caret-double-right
arrow-right arrow-up check-circle star asterisk eye scan-smiley identification-badge""".split()

STYLES = [
    ("regular", "regular.css", "Phosphor.woff2",         "Phosphor",         "ph"),
    ("duotone", "duotone.css", "Phosphor-Duotone.woff2", "Phosphor-Duotone", "ph-duotone"),
    ("fill",    "fill.css",    "Phosphor-Fill.woff2",    "Phosphor-Fill",    "ph-fill"),
]

CONTENT_RE = re.compile(r'content:\s*"\\([0-9a-fA-F]+)"')

out = ['/* Phosphor Icons (MIT) - subset to the glyphs this site uses.',
       '   Upstream: https://phosphoricons.com (@phosphor-icons/web 2.1.1) */', '']

for style, css, woff, fam, cls in STYLES:
    src = open(css, encoding='utf-8').read()
    codes, rules = set(), []
    for name in ICONS:
        for pseudo in (':before', ':after'):
            pat = re.compile(r'\.' + re.escape(cls) + r'\.ph-' + re.escape(name) + pseudo + r'\s*\{([^}]*)\}')
            m = pat.search(src)
            if not m:
                continue
            body = ' '.join(m.group(1).split())
            rules.append('.%s.ph-%s%s{%s}' % (cls, name, pseudo, body))
            for c in CONTENT_RE.findall(body):
                codes.add(int(c, 16))

    font = TTFont(woff)
    opts = subset.Options()
    opts.layout_features = ['*']
    opts.desubroutinize = True
    s = subset.Subsetter(options=opts)
    s.populate(unicodes=sorted(codes))
    s.subset(font)
    font.flavor = 'woff2'
    dst = woff.replace('.woff2', '-subset.woff2')
    font.save(dst)
    print('%-8s %3d glyphs  %6d -> %5d bytes' % (style, len(codes), os.path.getsize(woff), os.path.getsize(dst)))

    out.append('@font-face{font-family:"%s";src:url("%s") format("woff2");'
               'font-weight:normal;font-style:normal;font-display:block}' % (fam, dst))
    out.append('.%s{font-family:"%s"!important;speak:never;font-style:normal;font-weight:normal;'
               'font-variant:normal;text-transform:none;line-height:1;display:inline-block;'
               '-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}' % (cls, fam))
    out.extend(rules)
    out.append('')

open('phosphor.css', 'w', encoding='utf-8').write('\n'.join(out))
print('phosphor.css', os.path.getsize('phosphor.css'), 'bytes')

for f in ('regular.css', 'duotone.css', 'fill.css',
          'Phosphor.woff2', 'Phosphor-Duotone.woff2', 'Phosphor-Fill.woff2'):
    os.remove(f)
print('removed upstream originals')
