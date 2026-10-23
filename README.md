# Sentinel Integrated Technologies website

A static site for the Sentinel group. No build step required, no dependencies.
Open `index.html` or upload the whole folder to any web host.

```
index.html                 Home (group overview + the structure chart)
group.html                 The group in full: three companies, every capability
services.html              Sentinel Integrated Technologies
                           (anchors: #residential #commercial #industrial
                                     #cctv #alarms #access #gates #intercoms #fire)
security-services.html     Sentinel Security Services
circuitron.html            Circuitron Systems (anchors: #circuitstore #ecocircuit)
signage.html               The sign set, where each one goes, and the spec
about.html                 The group story, leadership, mission and values
renewable-energy.html      Solar PV and backup power
contact.html               Contact + enquiry form + map
privacy.html               Privacy policy
robots.txt, sitemap.xml    SEO
assets/css/style.css       The whole design system (one file, sectioned and commented)
assets/js/main.js          Header, group panel, drawer, reveals, carousel, accordion, form
assets/fonts/              Manrope (body, headings, numbers), Caveat (accents)
assets/icons/phosphor.css  Phosphor, subset to the glyphs in use
assets/icons/sentinel.svg  The drawn icon set, 35 glyphs (see "The icon set")
assets/img/                brand, clients, photos
tools/build.py             Page generator (see "Editing pages")
tools/group.py             The group structure and its content, in one place
tools/icons.py             Source for the drawn icon set
tools/build_icons.py       Builds the sprite, and a proof sheet for checking it
tools/subset_icons.py      Rebuilds the Phosphor subset when you need a new glyph
tools/signs.py             Builds the site signage artwork
tools/sign_glyphs.py       Solid pictograms for the signs
tools/typeset.py           Outlines type, so sign artwork needs no fonts
WEB-DESIGN-PRINCIPLES.md   The design rules this build follows
```

## The group

The site is built around the structure the Operations Director drew: one parent
with three operating companies, and two divisions under one of those.

```
Sentinel
├── Sentinel Integrated Technologies (Private) Limited   services.html
│     CCTV · alarms · access control · gate automation · intercoms · fire
├── Sentinel Security Services                    security-services.html
│     manned security · events · alarm response · dog units · perimeter · investigations
└── Circuitron Systems (Private) Limited          circuitron.html
      security systems · communications · automation · electronics
      ├── CircuitStore    retail and e-commerce
      └── EcoCircuit      electronic waste recovery
```

**`tools/group.py` is the single source of truth.** Every place a company is
described reads from it: the chart on the home page, the panel under the nav,
the group page, each company page, the six capability cards on the home page,
and the footer. Change a capability there and it changes everywhere, and the
anchors cannot drift out of step with the headings.

To add a capability to a company, add a dict to its `divisions` list with an
`id`, an `icon` from the drawn set, a `name`, a one sentence `line` and an
`items` list. Then run `python tools/build.py`.

## The icon set

`assets/icons/sentinel.svg` holds 35 glyphs drawn for this site, because
Phosphor has no word for a dome camera, an electric fence, a gate motor or a
dog unit. They follow the reference sheets the client supplied: a 24 grid, a
1.5 stroke, round caps and joins, open line work, and nothing closer than 2px
to the edge.

Phosphor still covers the generic vocabulary (clock, phone, envelope, shield,
caret). The drawn set covers the hardware and the work.

```
python tools/build_icons.py                       rebuild the sprite
python tools/build_icons.py --sheet proof.html    plus a page showing every
                                                  glyph at 20, 24, 32 and 64px
                                                  on light and dark
```

The sprite is inlined into each page at build time, once, straight after
`<body>`. That is deliberate: `<use href="other-file.svg#id">` does not work
cross file in Chrome or Safari, and the sprite gzips to a few hundred bytes
against markup that repeats.

Use one with `si("cam-dome")` in `tools/build.py`, or in hand written HTML:

```html
<svg class="si i-xl" aria-hidden="true"><use href="#si-cam-dome"/></svg>
```

The size classes (`i-xs` through `i-2xl`) are the same scale Phosphor uses, and
a glyph takes its colour from `color` like any font icon.

**Open the proof sheet before you ship a new glyph.** Several of these were
redrawn two and three times because the first version read as the wrong object
at icon size: the first dome camera read as an eye, the first motion sensor as
a handbag, the first dog as a hand. A PTZ camera was cut altogether because at
24px it was indistinguishable from the dome.

## The hero

Three panels, one per company, over three photographs, picked by a row of
named tabs. Each panel carries that company's own lockup, its own headline, its
own two actions and a photograph of its own work. Everything comes from
`tools/group.py`, so a fourth company would appear in the hero without anyone
remembering to add it.

The headlines are written as one sentence split three ways, which is why they
should be edited together or not at all:

> The systems that **watch** the site &middot; The officers who **hold** the
> ground &middot; The technology that **connects** both

**The tab row is the picker.** Dots say "there are more pictures"; named tabs
say who the three companies are, which is what the hero is now for. The rail
along the top of the active tab doubles as the progress bar, so the dwell is
visible rather than a surprise.

Behaviour: hovering or tabbing into the hero holds it, because reading beats
advancing. Arrow keys move between tabs. Inactive panels are hidden with
`visibility`, which also takes their links out of the tab order, so a keyboard
user never lands on an invisible button. Reduced motion stops the advance, the
drift and the progress sweep, and leaves the tabs working.

Each panel is the same height, so nothing jumps when the slide changes, and the
whole hero fits one screen at 1920, 1440, 1366, 1280, 1024, 834, 390 and 360.

**Contrast on a photograph has to be sampled, not calculated.** `--g-900` under
the copy is not the real background; the picture is. The copy sits on a local
radial wash rather than a heavier global scrim, so the photograph keeps its
openness and only the type area is conditioned. Measured at the glyphs on all
three slides, the worst case is 4.68:1 against a 3:1 requirement for the
headline, and every small text element clears 4.5:1.

## The photography

Three sources, and which is which matters. `assets/img/photos/CREDITS.md` is
generated by `tools/credits.py` and lists every one.

**Sentinel's own.** Seven frames supplied by the client: officers in Sentinel
uniform at Sentinel sites, with Sentinel vehicles and Zimbabwean plates. These
carry the whole people side of the site.

**Sentinel's own, off a phone.** Seven more, sent over WhatsApp in October
2026: staff at the office, a site visit, a technician cabling a cabinet, and
the company's own signs on client walls. They arrive at 810 by 1080, so they
are shown portrait at the size they were taken rather than stretched into a
wide frame, through the `.wall` component on the about, services and signage
pages. Three more came in the same batch and are not used, being second poses
of groups already shown.

**Licensed stock the client supplied.** Seven frames, used only where no
Sentinel photograph exists for the subject: the control room, a reader being
used, a smart panel, a rack, solar, retail equipment.

**Unsplash.** Twelve frames, all hardware and places with nobody in shot.

```
python tools/photos_local.py          crop and resize the client's files
python tools/photos_local.py <slot>   just one
python tools/credits.py               rewrite CREDITS.md
python tools/photos.py ...            the Unsplash pipeline, unchanged
```

`tools/photos_local.py` holds the mapping. Each entry names its source file and
a **focus point**, because cropping a 3:2 photograph to a 2:1 hero from the
centre takes people's heads off. The phone batch is the exception that proves
it: a 3:4 frame of a 3:4 original crops nothing, so the focus point there is
only insurance against a future layout. Sources are large originals and live
outside the repository: set `SENTINEL_PHOTO_SRC` if they are not in the
default folder.

**Context is a correctness requirement here, not a preference.** The first
Unsplash pass put European crowds, a Japanese electronics shop and white hands
on the readers of a Zimbabwean security company whose whole argument is that it
knows these sites. Every photograph with a person in it was replaced. Searches
for guards and dog units also return mostly police and military; none of that
is used either, because a private company showing police livery is claiming
something it is not.

**One thing to decide.** The uniforms, vehicles and buildings in the supplied
photographs read "Sentinel Security Technology", which is the name the group
traded under before this round. The site now says Sentinel Integrated
Technologies, with Sentinel Security Services as the manned security company.
Either
the imagery or the naming needs to move.

The October phone batch adds a second case of the same thing. The signs on
those walls are printed "Sentinel Security Services", which is a real company
in the group and reads correctly, but they carry an address on Northampton
Crescent rather than the 29 Tweed Road the site gives. At the size they are
shown the address is not legible, so nothing contradicts itself on screen.
Still: either those signs are at the old address and should be reprinted, or
the site has the wrong head office.

## The logo

The house lockup is `assets/img/brand/sit-lockup.png`, built by
`tools/sit_lockup.py` from artwork the client supplied in October 2026: a
larger wordmark against the shield than the drawn version carried, and the
entity line spelled out as "(Private) Limited" rather than "(PVT) Ltd".

| file | use |
|---|---|
| `sit-lockup.png` | full lockup: shield, SENTINEL, Integrated Technologies, (Private) Limited |
| `sit-lockup-compact.png` | without the entity line, for the header, the drawer and anything at 52px or under |
| `mark.svg` | the shield alone, and the favicons rendered from it |
| `*-white.png` | the same pair knocked out for dark grounds |
| `circuitron-logo.png` | Circuitron's own mark, trimmed to its artwork |
| `sentinel-logo*.svg` | the drawn lockup these replaced, kept and unreferenced |

**These are raster, and the files they replaced were not.** The supplied art
is a background removal off a white original, so there is no vector to outline
this time. Two things follow. The generator does not treat the PNG as pixels
to copy: in a background removal an edge pixel carries full alpha and a colour
blended toward white, so reading that blend back out recovers a clean one
channel coverage mask, which is then painted `#0C6934` for light grounds and
white for dark. Both files are the same mask, so the green and the knockout
cannot fall out of register. And the compact lockup is a re-layout rather than
a crop: the shield keeps its height and the two remaining lines are re-centred
against it, because cropping the entity line away would shrink the mark with
it.

The art is kept at the 555 x 214 it arrived at and its coverage held to 32
steps. Nothing on the site renders it above 58px, a quarter of that, so the
browser averages the steps away, and the flat runs that survive halve the file:
each of the four is smaller than the SVG it replaces. Resampling it smaller
does the opposite, inventing a distinct alpha per pixel, and a 456px wide
version came out half again bigger than the 555px it was made from.

If a vector original ever turns up, it should replace these. Nothing on the
page needs more resolution than they have, but a logo that cannot be scaled is
a logo with a ceiling, and the drawn files in the same folder are there to fall
back to.

The shield is 589 x 568 with a 41 stroke: an outer hexagon minus an inner one
(even odd), then nine rectangles for the S. It is small enough to read in full
inside `assets/img/brand/mark.svg`, so a colour or weight change is a one line
edit rather than a redraw. Favicons are rendered from it by
`brand_assets.py` in the scratchpad rather than hand cropped.

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
| Symbolic accents | **Caveat** | `assets/fonts/caveat.woff2` |

Caveat is a handwriting face. It carries six short lines on the whole site, so `tools/fetch_accent.py` pulls it from Google Fonts, pins the weight axis at 600 and subsets it to the 31 characters those lines use: 75KB becomes 16KB. Re run that script after changing any accent copy, or a character will be missing and fall back to Manrope.

Caveat's x-height is small against Manrope, so every accent slot carries its own size rather than inheriting the body size.

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

### Hero carousel

Four stills crossfade behind the copy, 6.2s each, with a slow drift on whichever
slide is showing. The bars under the figures strip jump to a slide and reset the
clock.

Only the first slide ships a `src`. The rest carry `data-src` / `data-srcset`
and are attached after `window.load`, so the first frame never competes with the
stylesheet or the fonts. The carousel pauses when the hero scrolls out of view
and in a background tab, and `prefers-reduced-motion` stops the auto advance and
the drift while leaving the bars working.

**Balancing the set.** Stock photographs never match each other. Measured on the
part of the frame the hero actually shows, the candidates ranged from 25 to 159
mean luminance; dropping a bright one into three dark ones made the carousel look
like a slideshow rather than a set. Each slide therefore carries two custom
properties:

```html
<div class="hero__slide" style="--pos:72% 34%;--expo:2.45">
```

`--pos` is its `object-position`, so the subject stays clear of the headline
whatever the crop. `--expo` multiplies the brightness filter. The four were tuned
by rendering them, measuring the mean luminance of the uncovered right side, and
adjusting until the set sat in a 20 point band instead of a 71 point one. Re-run
that measurement if you swap a photograph in.

### Hero overlays

Four layers, each with exactly one job, and all of them deliberately light. The
photograph is barely touched: `saturate(.9) contrast(1.04)` and a brightness
multiplier. The scrim alone earns the legibility.

1. **Unify** (`mix-blend-mode: color`, 24%) replaces hue while leaving luminance
   alone, so four photographs shot by four people read as one set.
2. **Vignette** (`multiply`) pulls the corners down a little.
3. **Grid** at half strength: texture, not decoration.
4. **Scrim**: a long horizontal ramp under the copy that clears completely by
   78%, plus short fades at the head and foot so the hero meets the header and
   the page below without an edge. On phones the copy stacks, so the ramp runs
   down the frame instead of across it.

The right side of the frame is left almost untouched. That restraint is checked
rather than assumed: the hero type is measured against the real pixels behind the
glyphs on every slide, and the headline sits at 10:1 or better against a 3:1
requirement.

### Hero
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

**1. The photography is stock, and should not stay that way.** The watermarked
iStock comps are gone: all 22 photographs now come from Unsplash under its
licence, chosen against a written brief per slot and credited in
`assets/img/photos/CREDITS.md`.

They are still pictures of other people's buildings. The cover of the Sentinel
Security Services profile has a photograph of Sentinel's own officers outside a
Sentinel branded office, and it is better than anything in this set because it
is true. Ask the client for that shoot, or commission one: officers on post, a
technician on a ladder, the control room, a gate install, a dog unit. Drop
replacements in at the same filenames and the site picks them up with no code
change. Each photo is referenced at two sizes, `name-640.jpg` and
`name-1200.jpg`, and `tools/photo_plan.py` records the exact dimensions.

Also outstanding: `python tools/photos.py triggers` has 22 downloads still to
acknowledge to Unsplash, blocked by the demo key's hourly limit.

**2. Sentinel Security Services has no logo of its own.** The supplied artwork
covers Sentinel Integrated Technologies and Circuitron Systems. Where the
manned security company needs a mark, the site uses the Sentinel shield with
company name set beside it in Manrope (`company_logo()` in `tools/build.py`).
That is a deliberate stand in, not a wordmark. Drop a real file into
`assets/img/brand/` and change the company's `logo` value in `tools/group.py`.

The descriptor type in the supplied lockup is a squared condensed grotesque
that has not been identified, so no new wordmark should be set by eye. If the
designer's font is known, say so and the sub brand lockups can be drawn
properly.

**3. The headline numbers need confirming.** The hero strip uses `3` companies,
`10` provinces, `24/7` response and `2016`. The first comes from the structure,
the rest from the Sentinel Security Services profile. If there are stronger
real figures (sites secured, cameras under management, officers deployed) they
belong here instead.

**4. The group's own name.** The Operations Director's diagram labels the parent
simply "Sentinel". The site uses that, with the Sentinel Integrated Technologies
lockup as the house mark because that is the only Sentinel wordmark that exists.
If the holding company trades under a fuller name, change `PARENT["name"]` in
`tools/group.py`.

**5. The brand green.** The supplied logo inks at `#2D6635`. The site's brand
green is `#0C6934`, which the whole palette was built around over earlier
rounds, and the logo files are generated in that colour so nothing on the page
shows two greens. If `#2D6635` is the official value, say so and the ramp can be
rebuilt around it.

**6. Renewable energy sits outside the structure.** `renewable-energy.html`
predates the group diagram, which does not mention solar. It is kept as a group
level capability and cross linked from Circuitron's power section. Tell us which
company owns it and it can be moved under that company properly.

**7. The WhatsApp community link is a placeholder.** `WA_COMMUNITY` in
`tools/build.py` currently points at `https://chat.whatsapp.com/` with no invite
code, which lands on a generic page. Create the community in WhatsApp, copy its
invite link, and paste it in. The enquiry option beside it is already live and
goes to the real number.

**8. The contact form has no backend.** It composes a `mailto:` to
`info@sentinel.co.zw` and opens the visitor's email client. That works, but it
loses anyone without a configured mail app. To take submissions properly, point
the `<form>` at a form service (Formspree, Web3Forms, Netlify Forms) or a small
server endpoint, and delete the `data-contact-form` handler at the bottom of
`assets/js/main.js`.

## Also worth a look

- **Social links.** The real profiles are now in, as `FACEBOOK` and `LINKEDIN`
  near the top of `tools/build.py`: the utility bar and the footer carry the
  logos, and the contact page names them in full under "Follow us". They open
  in a new tab through the shared `OFFSITE` attribute string. If a page moves,
  change the two constants and rebuild; nothing else holds the address. The
  Facebook URL is the numeric `profile.php?id=` form, which is what the page
  itself hands out: if a vanity name is ever claimed, swap it in.
- **Copy.** Every page was swept for the tells of machine written text. There
  are no em dashes, en dashes or hyphenated compounds anywhere in the visible
  copy. If you edit a page, keep to commas, colons and full stops.
- **The awards** are labelled generically as "Industry award" for 2014, 2015 and
  2016 because the old site never named them. If you have the actual award
  names, put them in `about.html` and `index.html`.
- **The photographs do not yet match the new structure.** The library was shot
  for one company and now has to carry three. Manned security has usable frames;
  technology and Circuitron pages are borrowing them. Replacing these is the
  next piece of work.
- **The Circuitron profile names three sub brands,** CircuitStore and
  EcoCircuit, both built here, and refers to a certificate of incorporation
  dated 19 August 2026. Neither sub brand has artwork yet; both are set
  typographically.
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
