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
assets/video/           hero.mp4, the homepage hero clip
tools/build.py          Optional page generator (see "Editing pages")
tools/subset_icons.py   Rebuilds the Phosphor subset when you need a new glyph
WEB-DESIGN-PRINCIPLES.md  The design rules this build follows
```

## Deployment

| | |
|---|---|
| Live | https://sentinel-security-iwob.onrender.com |
| Repository | https://github.com/Mutombe/sentinel-security-website |
| Host | Render static site, `srv-dalh10u5vjqs73fcccc0` |

Auto deploy is on: every push to `main` republishes. There is no build command
and the publish path is the repository root, because the site is already static.

To point `sentinel.co.zw` at it, add the domain under Settings, Custom Domains
in the Render dashboard, then set the DNS records Render gives you. Render issues
the TLS certificate automatically once DNS resolves.

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

### Colour: the green ramp

The dark end carries most of this site, so it is a real scale rather than one
value. Seven steps whose hue drifts 158 to 147 as they lighten, meeting the
brand green at 146:

| Token | Value | Used for |
|---|---|---|
| `--g-950` | `#03140E` | the footer, the foot of the hero scrim |
| `--g-900` | `#051D14` | dark section grounds, the mobile drawer |
| `--g-850` | `#06291B` | the default dark, and every dark heading |
| `--g-800` | `#093522` | surfaces sitting **on** a dark ground, so they lift |
| `--g-750` | `#0B4328` | those surfaces on hover |
| `--g-700` | `#0C522E` | mid dark accents |
| `--g-650` | `#0C5F31` | the step just below the brand green |
| `--g-mid` | `#0C6934` | the logo green: solid fills, links, icons on light paper |
| `--g-light` | `#3FB56F` | accents **on dark grounds only** |
| `--lime` | `#A9EE6E` | the accent: buttons, highlights, one card in three |

Three rules keep it honest:

**Depth comes from picking a different step, never from washing white over the
same one.** A card on a dark section is `--g-800`, not `rgba(255,255,255,.04)`.
White washes desaturate and the surface goes grey; a lighter green keeps the hue
and still lifts.

**`--g-light` is a dark-ground colour.** It is 6.8:1 on `--g-900` and only 2.6:1
on white, so anything small sitting on light paper uses `--g-mid` instead. The
sector row numbers and the eyebrow asterisks switch between the two.

**Dark surfaces are gradients, not slabs.** Dark sections run `--g-900` to
`--g-850` and back, with one soft pool of brand green in the upper left. The CTA
band runs diagonally `--g-900` to `--g-800` with a small lime glow in the top
right corner. Flat fills read as slabs; a shallow gradient gives the eye
somewhere to rest.

Paper is `--white` and `--cream` (`#F7F7EF`); sections alternate white, cream,
dark and lime so the page has rhythm.

**Contrast.** Every text and background pair on the site is audited in the
browser: computed colours flattened against their real backgrounds, measured
against WCAG AA (4.5:1 body, 3:1 large). Zero failures on all six pages. The
muted text colour `--body-2` is pinned at `#647269` because anything lighter
drops below 4.5:1 on cream.

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

### Corners

Two states only: **square or round**. No angled cuts, no chamfers, nothing in
between, because a third shape makes the system read as inconsistent rather than
deliberate.

| Kind of thing | Corners | Why |
|---|---|---|
| Surfaces: cards, panels, images, tiles, inputs, icon chips | square top, rounded bottom (`--corner-xl` / `-lg` / `-md`) | the flat shoulder lines up with the grid and with its neighbours |
| Anything you can click: buttons, tags, eyebrows, badges | fully round (`--r-pill`) | maximum contrast against the square shoulders |
| Icon buttons, avatars, step numbers | circles | same family as the pills |

The contrast between the flat tops and the fully round interactive elements is
the point: it tells you what is a surface and what is a control without any
other signal. A row of cards reads as one crisp horizontal line across the top
while the feet stay soft.

Every rendered corner on the site is either `0px` or a radius. The full set in
use is `0 0 26 26`, `0 0 20 20`, `0 0 11 11`, `0 0 0 26` and `0 0 26 11` (the
two halves of the notched card), plus `50%` and `999px` for controls.

The flat top edge also gives cards something to do on hover: a 3px rule draws
itself left to right along the shoulder.

### Shape language

Soft capsules for controls, flat shoulders for surfaces. See Corners above.

- **`.pbtn`** is the pill in pill button, a coloured capsule holding a second
  capsule plus a double chevron. Variants `--light`, `--dark`, `--outline`.
- **`.eyebrow`** is an outlined capsule led by a Phosphor asterisk.
- **`.shead`** puts the section heading left and a supporting sentence, or a
  button, on the right, bottom aligned.
- **`.ncard`** is the signature card: a rounded panel with a bite out of its
  bottom left corner and the CTA sitting in that bite as a detached pill, joined
  by a concave fillet. Colour variants rotate across a row.
- **`.bento`** is the asymmetric image grid used in the About blocks.

### Hero video

The homepage hero plays `assets/video/hero.mp4` (768x432, 8s, 394 KB, H.264)
behind the copy. It is graded into the palette rather than dropped in raw:

1. `filter` pulls the saturation down and the contrast up on warm footage
2. a `mix-blend-mode: color` layer replaces the hue while keeping the luminance,
   so golden hour light survives as light but the frame reads brand green
3. a small `screen` radial puts a controlled lime highlight where the sun is
4. a `multiply` vignette, then the usual scrim and drafting grid on top

The frame is panned with `transform: scale(1.32) translateX(-6%)` on desktop so
the centre of the clip sits under the darkest part of the scrim. Portrait crops
hard into the middle of a 16:9 frame, so mobile drops the pan and uses
`object-position` to hold the walking figure in the top third instead.

Loading is deliberate. The markup carries `preload="none"` and no `autoplay`
attribute; `main.js` attaches and plays it only when motion is welcome and the
connection is not metered:

- `prefers-reduced-motion: reduce` removes the video and the CSS shows the
  poster frame instead
- `navigator.connection.saveData`, or a 2G class connection, does the same
- an IntersectionObserver pauses it whenever the hero leaves the screen, and
  `visibilitychange` pauses it in a background tab

To swap the clip, replace `assets/video/hero.mp4` and regenerate
`assets/img/photos/hero-poster.jpg` from a representative frame. The grade is
tuned for warm backlit footage; cooler footage will want the `filter` and
`.hero__tint` opacity adjusted.

### Hero

The homepage hero is sized to `calc(100svh - var(--topbar-h))`, so everything in
it, down to the figures strip, is on screen without scrolling. The headline and
the spacing inside it scale on viewport height as well as width, so it still fits
a short laptop screen. Checked at 1440x900, 1366x768, 1280x720, 1280x640,
1440x1080 and 390x844. Below 560px tall on desktop, and on phones, the hero is
allowed to grow rather than squash.

## The floating WhatsApp button

Bottom right, above the back to top button. Tapping it opens a small panel that
asks which conversation you want before handing you to WhatsApp:

- **Make an enquiry** goes to `wa.me/263773589461` with a message prefilled
- **Join the community** goes to the community invite link

It closes on Escape, on a click outside, and once an option is taken. Tab is
trapped inside the panel while it is open, and the whole rail hides when the
mobile menu is open. Both links are in `tools/build.py` as `WA_ENQUIRY` and
`WA_COMMUNITY`.

The homepage hero reserves 58px of bottom padding on phones so the button never
sits on top of the figures strip.

## Everything goes somewhere

Every surface that reads as a panel is now a link, because on this site a card
shape means "clickable". Cards, process steps, stat tiles, bento photographs,
sector tags, client logos, the credential chips, the award badges and the footer
logo all have destinations. Audited at zero dead ends across all six pages:
no empty `href`, no `href="#"`, and no card, tile or chip without a target.

The sector rows carry ids (`#corporate`, `#banking`, `#government`,
`#manufacturing`, `#construction`) so the "Where we work" tags can point at the
matching row, and the clients strip and recognition section have `#clients` and
`#recognition`.

## Before it goes live

**1. The stock photography and the hero video are watermarked.** Every file in
`assets/img/photos/` except `residential-electr-services.jpg` is an unlicensed
iStock comp, and so is `assets/video/hero.mp4`, which carries a baked in
"iStock by Getty Images" mark across the middle of the frame.

That watermark is the reason the hero video is panned the way it is: the centre
of the clip is parked under the darkest part of the scrim so the mark does not
read. A licensed copy of the same clip would allow a much stronger composition,
with the guard placed in the clear right hand side of the frame rather than
hidden behind the headline. These must be replaced with licensed images, or
better, with real photographs of Sentinel's own installations and team. Drop
replacements in at the same filenames and the site picks them up with no code
change. Each photo is referenced at two sizes: `name-640.jpg` and `name-1200.jpg`.

**2. The headline numbers need confirming.** The hero strip and the About page
use `24/7`, `3` awards, `5` sectors and `6` systems. All are drawn from the old
site, but if Sentinel has stronger real figures (years trading, sites secured,
cameras under management) those belong here instead.

**3. The WhatsApp community link is a placeholder.** `WA_COMMUNITY` in
`tools/build.py` currently points at `https://chat.whatsapp.com/` with no invite
code, which lands on a generic page. Create the community in WhatsApp, copy its
invite link, and paste it in. The enquiry option beside it is already live and
goes to the real number.

**4. The contact form has no backend.** It composes a `mailto:` to
`info@sentinel.co.zw` and opens the visitor's email client. That works, but it
loses anyone without a configured mail app. To take submissions properly, point
the `<form>` at a form service (Formspree, Web3Forms, Netlify Forms) or a small
server endpoint, and delete the `data-contact-form` handler at the bottom of
`assets/js/main.js`.

## Also worth a look

- **Social icons** used to point at the `facebook.com` and `linkedin.com`
  homepages, which are dead ends. They now carry WhatsApp, email and phone,
  which all reach Sentinel. Put Facebook and LinkedIn back once you have the
  real profile URLs: they go in the `topbar()` and `FOOTER` blocks of
  `tools/build.py`.
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
