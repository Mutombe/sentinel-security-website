# Sentinel Security Technology website

A static site. No build step required, no dependencies. Open `index.html` or
upload the whole folder to any web host.

```
index.html              Home
about.html              About us
services.html           Services (anchors: #residential #commercial #industrial
                                   #cctv #alarms #access #fire #man-traps #physical)
renewable-energy.html   Solar PV division
contact.html            Contact + enquiry form + map
privacy.html            Privacy policy
robots.txt, sitemap.xml SEO
assets/css/style.css    The whole design system (one file, sectioned and commented)
assets/js/main.js       Header, drawer, reveals, accordion, form
assets/fonts/           Manrope (body, headings, numbers), Grand Hotel (accents)
assets/icons/           Phosphor, subset to the glyphs in use
assets/img/             brand, clients, photos
tools/build.py          Optional page generator (see "Editing pages")
tools/subset_icons.py   Rebuilds the Phosphor subset when you need a new glyph
WEB-DESIGN-PRINCIPLES.md  The design rules this build follows
```

## Design system

Everything is driven by CSS custom properties at the top of `style.css`.

### Type

Three roles, all self hosted. Nothing is fetched from Google.

| Role | Face | Files |
|---|---|---|
| Body, headings and every number | **Manrope** 400/500/600/700/800 | `assets/fonts/manrope-*.woff2` |
| Symbolic accents | **Grand Hotel** | `assets/fonts/grandhotel.woff2` |

Grand Hotel is an upright connected script, chosen over an oblique brush face so
it sits level with the grid rather than leaning across it. It appears only on
short symbolic phrases (the `towards a #secure_world` tagline in the utility bar
and footer, and one accent line on the solar sections) through the `.script`
class. Numbers carry `.num`, which switches on Manrope's lining and tabular
figures so columns of figures line up.

Both faces are SIL OFL, so both are free to use commercially.

### Colour: a four stop green ramp

| Token | Value | Role |
|---|---|---|
| `--g-dark` | `#06291B` | dark green: grounds, headings, the dark card |
| `--g-mid` | `#0C6934` | mid green: the logo green, solid fills, links |
| `--g-light` | `#3FB56F` | light green: small accents, row numbers |
| `--lime` | `#A9EE6E` | lime: buttons, highlights, the lime card, the utility bar |

`--ramp` and `--ramp-soft` run all four in order, and are used on the interior
page heroes. Paper is `--white` and `--cream` (`#F7F7EF`); sections alternate
white, cream, dark and lime so the page has rhythm.

### Icons

**Phosphor Icons** (MIT), self hosted and subset to only the 38 glyphs this site
uses, which takes the three weights from 443 KB down to 18 KB. Duotone carries
the large feature icons (cards, stat tiles, contact blocks), regular the inline
and UI glyphs, fill the stars and social logos.

```html
<i class="ph-duotone ph-security-camera i-lg"></i>   <!-- duotone, large -->
<i class="ph ph-arrow-right i-sm"></i>               <!-- regular, small -->
<i class="ph-fill ph-star i-xs"></i>                 <!-- fill, extra small -->
```

Sizes run `i-xs` 14px through `i-2xl` 44px. To use an icon that is not in the
subset, add its name to the `ICONS` list in `tools/subset_icons.py` and rerun it,
or link the full upstream stylesheet from a CDN while you are working.

### Shape language

Everything is a soft capsule: 28px card radius, fully rounded pills.

- **`.pbtn`** is the pill in pill button, a coloured capsule holding a second
  capsule plus a double chevron. Variants `--light`, `--dark`, `--outline`.
- **`.eyebrow`** is an outlined capsule led by a Phosphor asterisk.
- **`.shead`** puts the section heading left and a supporting sentence, or a
  button, on the right, bottom aligned.
- **`.ncard`** is the signature card: a rounded panel with a bite out of its
  bottom left corner and the CTA sitting in that bite as a detached pill, joined
  by a concave fillet. Colour variants rotate across a row.
- **`.bento`** is the asymmetric image grid used in the About blocks.

### Hero

The homepage hero is sized to `calc(100svh - var(--topbar-h))`, so everything in
it, down to the figures strip, is on screen without scrolling. The headline and
the spacing inside it scale on viewport height as well as width, so it still fits
a short laptop screen. Checked at 1440x900, 1366x768, 1280x720, 1280x640,
1440x1080 and 390x844. Below 560px tall on desktop, and on phones, the hero is
allowed to grow rather than squash.

## Before it goes live

**1. The stock photography is watermarked.** Every file in `assets/img/photos/`
except `residential-electr-services.jpg` is an unlicensed iStock comp, and the
watermark is visible on the page, most obviously in the homepage hero and on
the About and Contact heroes. These must be replaced with licensed images, or
better, with real photographs of Sentinel's own installations and team. Drop
replacements in at the same filenames and the site picks them up with no code
change. Each photo is referenced at two sizes: `name-640.jpg` and `name-1200.jpg`.

**2. The headline numbers need confirming.** The hero strip and the About page
use `24/7`, `3` awards, `5` sectors and `6` systems. All are drawn from the old
site, but if Sentinel has stronger real figures (years trading, sites secured,
cameras under management) those belong here instead.

**3. The contact form has no backend.** It composes a `mailto:` to
`info@sentinel.co.zw` and opens the visitor's email client. That works, but it
loses anyone without a configured mail app. To take submissions properly, point
the `<form>` at a form service (Formspree, Web3Forms, Netlify Forms) or a small
server endpoint, and delete the `data-contact-form` handler at the bottom of
`assets/js/main.js`.

## Also worth a look

- **Social links** in the utility bar and footer point at `facebook.com` and
  `linkedin.com` placeholders. Swap in the real profile URLs.
- **Copy.** Every page was swept for the tells of machine written text. There
  are no em dashes, en dashes or hyphenated compounds anywhere in the visible
  copy. If you edit a page, keep to commas, colons and full stops.
- **The awards** are labelled generically as "Industry award" for 2014, 2015 and
  2016 because the old site never named them. If you have the actual award
  names, put them in `about.html` and `index.html`.
- **The fire detection photo** on `services.html` is the weakest match in the
  set. It shows a guard with a laptop, not fire safety equipment.
- **Projects page.** The old site linked one but it 404s. Three or four real case
  studies would be the single biggest credibility addition to this site.

## Editing pages

The six pages share an identical utility bar, header, footer and CTA band. Two
ways to change them:

- **Edit the HTML directly.** It is plain static HTML with no templating. If you
  change shared chrome, change it in all six files.
- **Or use the generator.** `python tools/build.py` regenerates all six pages
  from the shared shell at the top of that file. It writes plain static HTML.
  The site never needs it to run; it just keeps the duplicated chrome in sync.
  If you have edited the HTML by hand, running it will overwrite your changes.

## Browser support

Modern evergreen browsers. Degrades sensibly: without JavaScript the full page
still renders (reveal animations are gated behind a `js` class), and
`prefers-reduced-motion` disables all motion.

Verified in a headless browser at 1280px and 390px: no console errors, no failed
requests, no horizontal overflow, and no broken internal links or asset paths.
