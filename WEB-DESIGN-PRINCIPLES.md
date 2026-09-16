# Vibe coding: web design principles

Working notes on building interfaces that look designed rather than assembled.
Written from the Sentinel build, but none of it is specific to that project.

The through line: **taste is a series of decisions you can name.** Every time
something looks right, there is a reason, and the reason can be written down as
a rule. What follows is that list.

---

## 0. The loop

> Build it. Look at it. Fix what you see. Repeat.

Most of the quality in a build comes from actually looking at the thing, at real
sizes, in a real browser, and being honest about what you see. Reading your own
CSS and imagining the result is not looking.

Run a local server and render the page headlessly after every meaningful change.
Screenshot it. Crop into the component you just touched and look at it at 3x.
Half the bugs in this build were invisible in the code and obvious in a crop: a
heading inheriting the wrong colour and vanishing on a dark hero, a card's corner
radii mirrored, a fillet positioned on the wrong axis, a logo stretched by an
HTML `width` attribute the CSS did not override.

Three cheap signals catch most failures before a screenshot is even needed:

- console errors
- failed network requests
- `document.documentElement.scrollWidth > clientWidth` (horizontal overflow)

Automate those three. Look at pixels for everything else.

---

## 1. Steal the grammar, not the pixels

When you are given a reference, do not copy it. **Decompose it.** Go component by
component and write down what each one is actually doing:

- What is the section header pattern? (title left, supporting line right, bottom aligned)
- What shape is a button? (capsule holding a second capsule, plus a chevron)
- What is the signature move? (a bite cut out of the card's bottom left corner,
  with the CTA sitting in it as a detached pill)
- How do colours rotate across a row? (white, accent, dark)
- What is the paper? (not white: a warm off white)

That list is the grammar. You can then write entirely different content, in a
different palette, and it will still feel like it belongs to the same family.
Copying pixels gives you a knockoff. Copying grammar gives you a design system.

Sample the reference's actual colour values with a script rather than eyeballing
them. You will be wrong about hex codes every time.

---

## 2. Tokens before components

Every value that appears twice is a token. Write the token block first, then
build components that only ever reference tokens.

```css
:root {
  --g-dark: #06291B;  --g-mid: #0C6934;  --g-light: #3FB56F;  --lime: #A9EE6E;
  --cream: #F7F7EF;   --line: #E4E6DA;
  --r-card: 28px;     --r-pill: 999px;   --notch: 18px;
  --section-y: clamp(4.5rem, 8vw, 7.5rem);
  --ease: cubic-bezier(.22, .61, .36, 1);
}
```

The test: **can you rebrand the entire site by editing the token block?** If yes,
your components are clean. If you have to hunt for hardcoded hexes, they are not.

Tokens also make the responsive pass trivial. Shrinking `--r-card`, `--notch`,
`--gutter` and `--section-y` inside one media query rescales the whole system at
once, without touching a single component rule.

---

## 3. Build a ramp, not a palette

A palette is a bag of colours. A **ramp** is an ordered progression, and ordered
progressions are what make interfaces feel considered.

Four steps is usually enough:

| Step | Role |
|---|---|
| dark | grounds, headings, the dark card, the footer |
| mid | the brand colour: solid fills, links, icons |
| light | small accents, numbers, hover states |
| accent | the pop: primary buttons, one card in three, the utility bar |

Derive the dark and light steps from the brand hue rather than picking new
colours, so the ramp reads as one family. Let the accent drift in hue at the
bright end (a forest green ramp that ends in a yellow green lime) because that is
what gives it energy.

Then **alternate section grounds** down the page: white, off white, dark, accent.
A page with one background colour reads flat no matter how good the components
are. Rhythm is created by the grounds, not the content.

One more rule: an accent that appears everywhere stops being an accent. If the
lime is on every card, nothing pops. Use it on roughly one element in five.

---

## 4. Assign type roles, not typefaces

Do not think "which fonts". Think "which jobs":

1. **Body, headings and numbers.** One workhorse family with real weights (400
   to 800) and proper lining and tabular figures. This does 95 percent of the
   work. A well drawn grotesque at 800 makes a better display face than a
   dedicated display face you half like.
2. **A symbolic accent.** One face used four or five times on the whole site, for
   a tagline or a signature phrase. Never for anything functional.

Assigning roles first stops you accumulating five families that all do the same
job.

**Verify the accent face before you commit to it.** Display and script fonts
routinely have missing or decorative glyphs. The first script in this build had
swash ornaments in its digit slots, so "24/7" rendered as squiggles. Render a
specimen with numbers, punctuation and the actual strings you intend to set,
and look at it.

Also, for scripts specifically: **upright reads as considered, oblique reads as
stock.** A steeply slanted brush script drags the whole composition forward and
cheapens it. An upright connected script sits level with the grid and looks like
a signature.

Give numbers their own class:

```css
.num { font-variant-numeric: tabular-nums lining-nums; letter-spacing: -.03em; }
```

Figures set with proportional oldstyle numerals in a stat block look broken, and
almost nobody can say why.

---

## 5. Pick one signature component

Every design that reads as "designed" has a move you could describe to somebody
over the phone. One shape that repeats and that nothing else on the web does
quite the same way.

In this build it is a card whose bottom left corner is bitten out, with the call
to action sitting in the bite as a detached pill, joined by a concave fillet.

The point is not that specific shape. The point is **having one**, and then using
it enough that it becomes the site's fingerprint. Three tiers on the homepage,
three on the services page, three values on the about page: same component,
different content, and the site coheres.

Build it properly. A concave corner is not `border-radius`; it is a small square
of the card colour with a quarter disc masked out of it:

```css
.fill::before {
  content: "";
  position: absolute; left: calc(-1 * var(--notch)); top: 0;
  width: var(--notch); height: var(--notch);
  background: var(--c);
  mask: radial-gradient(circle var(--notch) at 0 100%, transparent 98%, #000 100%);
}
```

Fifteen lines of CSS, fully responsive, no images. Signature moves are usually
cheaper than they look. What they cost is the half hour of working out the
geometry on paper first.

---

## 6. Texture is the difference between clean and premium

A flat coloured rectangle is clean. A flat coloured rectangle with a drafting
grid at four percent opacity is expensive.

Draw patterns as background layers, not DOM and not images:

```css
--pat-grid: linear-gradient(rgba(255,255,255,.045) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,.045) 1px, transparent 1px);

.section--dark {
  background-color: var(--g-dark);
  background-image: var(--pat-grid);
  background-size: 34px 34px;
}
```

Costs nothing, scales perfectly, themes with a token.

Rules for texture:

- **Keep it at the threshold of visibility.** 4 to 10 percent opacity. If a
  visitor notices the pattern, it is too strong. They should notice that the
  surface has depth.
- **Vary it by surface, not randomly.** Grid on dark grounds, dots on light
  grounds, diagonal hatch on accent tiles. One pattern per surface type, used
  consistently.
- **Mask patterns where they meet photography** so there is no hard seam.
- **Let the pattern carry brand meaning where it can.** A security and systems
  installer gets a drafting grid because its own marketing already used
  blueprints. A bakery would get something else.

Column rules (hairlines dropped down the container at the column boundaries) are
the same idea applied to layout: they suggest the page is set on a drawing sheet.
Fade them out at the top and bottom with a mask so they do not terminate hard,
and drop them entirely on mobile where there are no columns to rule.

---

## 7. Composition rules that carry most of the weight

**The split section header.** Title on the left at large size, one supporting
sentence on the right, both aligned to the same baseline at the bottom. This one
pattern makes a page look art directed. Swap the right side for a button when the
section has an obvious next step.

**Bento over uniform grids.** One wide image, then a square tile and a stat card
beneath it, is more interesting than three equal cards, and takes the same time
to build.

**Full bleed photography, contained text.** Let the image run to the viewport
edge and keep the copy inside the container. Fade the photo into a flat ground
with a horizontal gradient rather than cutting it with a hard edge.

**Make the fade wider than you think.** If the image starts at 38 percent and the
scrim reaches full opacity at 30 percent, you get a visible vertical seam. Push
the image wider so its edge sits inside the opaque part of the gradient.

**Do not tint photography with the brand colour.** It is the fastest way to make
a site look like a template. Scrim only as far as the text needs for contrast,
then let the photo be its own colour.

---

## 8. Above the fold is a real constraint

If you have a hero, the whole hero should be on screen. A visitor should not have
to scroll to discover there was a second half to it.

```css
.hero {
  height: calc(100svh - var(--topbar-h));
  min-height: 520px;
  max-height: 1040px;
}
```

Use `svh`, not `vh`, or mobile browser chrome will cut the bottom off.

Then make the contents scale on **height as well as width**, because a 1366x768
laptop is a short viewport, not a narrow one:

```css
.h-hero { font-size: clamp(2.05rem, min(6.1vw, 7.4vh), 4.7rem); }
```

`min(vw, vh)` is the whole trick: the type takes whichever dimension is more
constrained. Apply it to the internal gaps too.

Then verify at real sizes: 1440x900, 1366x768, 1280x720, 1280x640, 1440x1080,
390x844. Assert that the last element in the hero has `bottom <= innerHeight`.

Give it an escape hatch. Below roughly 560px of height, let the hero grow and
scroll rather than crushing the type.

---

## 9. Measure the copy, do not eyeball it

This is the most underrated discipline in the list.

**A line that is one line on desktop and two on mobile breaks the layout.** A
card title that wraps, a bullet that spills, a label that folds: each one costs
you the rhythm that everything else was built to create.

So measure it. Instrument the page, count the rendered lines of every text
element at desktop width and at 390px, and diff the two:

```js
const cs = getComputedStyle(el);
const inner = el.getBoundingClientRect().height
            - parseFloat(cs.paddingTop) - parseFloat(cs.paddingBottom);
const lines = Math.max(1, Math.round(inner / parseFloat(cs.lineHeight)));
```

Report two lists:

1. one line on desktop, two or more on mobile (fix every one)
2. five or more lines on mobile (shorten until there are none)

Then rewrite the copy to fit. Not the CSS: the copy. Working budgets that held up
across this build:

| Element | Budget |
|---|---|
| Eyebrow, label, tag | 20 characters |
| Card bullet | 34 characters |
| Card title | 26 characters |
| Button label | 22 characters |
| Card body paragraph | 110 characters |
| Section supporting line | 130 characters |
| Lead paragraph | 150 characters |
| Body paragraph | 165 characters |

Headings are the exception. A large heading wrapping to two or three lines on a
phone is correct typography, not a defect. The rule is about small text.

Writing to a character budget also improves the writing. "Number plate
recognition on gates and weighbridges" becomes "Number plate recognition" and
loses nothing. Constraints edit better than good intentions do.

---

## 10. Write copy that does not read as generated

Interfaces are judged on their words as much as their spacing, and generated
prose has a smell. The tells, in rough order of how much damage they do:

- **The em dash.** Nothing marks machine written text faster in 2026. Use commas,
  colons, full stops and brackets. Ban the character outright and grep for it.
- **The fragment pair heading.** "Four steps. No surprises." "Six disciplines.
  One accountable partner." Instantly recognisable, instantly hollow. Write a
  plain declarative heading instead: "From the first call to the handover".
- **Hollow superlatives.** seamless, robust, leverage, elevate, unlock, bespoke,
  cutting edge, comprehensive, tailored, holistic. Grep for the whole list.
- **"Not just X, but Y."** And its relatives: "It's not about X, it's about Y."
- **Three item parallel lists** used as a rhetorical flourish rather than because
  there happen to be three things.
- **Stating the obvious as insight.** "Security is important for businesses."

Replace all of it with specifics. "A system nobody can fix overnight protects
nothing" beats "we offer comprehensive round the clock support", and it is
shorter, which the line budget will thank you for.

Verify mechanically. Grep the built HTML for dash characters, for the
superlative list, for "not just". The count should be zero, and you should be
able to prove it rather than believe it.

---

## 11. Mobile is a different design, not a narrower one

Collapsing every grid to one column is the default, and the default is bad. It
makes the page enormously tall and uniformly flat.

Decide per component what the phone version actually is:

- **Tiles stay two up.** Stat cards, image tiles, footer link columns. They are
  small and square; they do not need full width.
- **Prose goes one up.** Anything with a paragraph in it.
- **Process steps become a list.** Four stacked boxes with a circled number on
  top of each is four screens of scrolling. The same content as a two column
  grid, number beside the text, is a quarter of the height and reads better.
- **The utility bar keeps the useful item.** On desktop it holds a tagline, an
  email and a phone number. On a phone it should hold the phone number, because
  that is the one somebody will tap. Hiding "all but the first" is the lazy
  version and usually keeps the wrong one.
- **Buttons go full width and centre their label**, but do not become slabs:
  keep the pill radius and the internal padding proportional.
- **Inputs use 16px minimum font size** or iOS zooms the viewport on focus.

Shrink the system tokens in the same media query (`--gutter`, `--section-y`,
`--r-card`, `--notch`, `--cell`) so the whole design scales together instead of
desktop proportions sitting awkwardly on a small screen.

And add a very narrow breakpoint (around 380px) to unwind the two up decisions
that stop working on the smallest phones.

---

## 12. Own your assets

- **Self host fonts.** No third party request, no layout shift, no privacy
  footnote in the policy. `font-display: swap`, and preload the two faces that
  appear above the fold.
- **Subset icon fonts.** Three Phosphor weights are 443KB. The 38 glyphs this
  site actually uses are 18KB. Parse the upstream stylesheet for the codepoints
  you reference, subset with fontTools, emit a stylesheet with only those rules.
  Twenty lines of script, a 96 percent saving, and it is repeatable.
- **Prefer an icon set with weights.** Duotone for large feature icons, regular
  for inline and UI, filled for stars and logos. One family, three registers, and
  the interface gains hierarchy for free.
- **Read the licence.** Personal use fonts are common in downloaded bundles and
  are not usable on a company site. Watermarked stock comps are not usable
  anywhere. Flag both loudly rather than shipping them quietly, and prefer an
  SIL OFL equivalent where one exists, because it solves the problem instead of
  deferring it.
- **Generate brand variants from the source asset.** A white logo for dark
  grounds, a cropped mark for the favicon and watermarks, white versions of dark
  graphics that would otherwise disappear on a dark section. Script it so it is
  reproducible.

---

## 13. Degrade honestly

- **Never gate content behind JavaScript.** Scroll reveal animations are the
  usual culprit: if the hidden state lives in the base stylesheet, a JS failure
  leaves a blank page. Gate the hidden state behind a class that JS adds:
  `.js [data-reveal] { opacity: 0 }`. No JS, no hiding.
- **Intersection observers drop entries during fast scrolls.** A flick or the End
  key can carry an element past the viewport between two callbacks, and it stays
  invisible for good. Add a cheap sweep on scroll that reveals anything already
  above the fold.
- **`prefers-reduced-motion` turns off everything**, including background
  animation and smooth scrolling, not just the obvious transitions.
- **`overflow-x: clip` rather than `hidden`** on the root: it clips without
  creating a scroll container, so `position: sticky` keeps working.
- **Give every embed a fallback.** A third party map that fails to load should
  leave a styled panel with the address and a link, not a white void.

---

## 14. Motion

Restraint. One easing curve as a token, used everywhere:
`cubic-bezier(.22, .61, .36, 1)`.

- Reveals: 700ms, 24px of travel, and stagger siblings by 85ms so a row
  cascades instead of snapping.
- Hovers: 300 to 400ms. Lift a card 6px, never more.
- Never animate `width`, `height`, `top` or `left`. Transform and opacity only.
- If a hover state cannot be reached on a touch device, make sure the component
  still communicates everything it needs to without it.

---

## 15. The checklist

Before calling anything done, prove these rather than assume them:

- [ ] Zero console errors, zero failed requests, on every page
- [ ] `scrollWidth === clientWidth` at 1280 and at 390
- [ ] Every internal link and asset path resolves (walk the built HTML)
- [ ] Every CSS `url()` resolves
- [ ] The hero fits one screen at six real viewport sizes
- [ ] No text is one line on desktop and two on mobile, except headings
- [ ] No paragraph exceeds four lines at 390px
- [ ] Zero em dashes, zero hollow superlatives in the built HTML
- [ ] Images are not stretched: rendered aspect ratio equals natural ratio
- [ ] The page renders fully with JavaScript disabled
- [ ] Mobile navigation opens, locks scroll and closes
- [ ] Every font and icon file is licensed for the use

The last one is not a design point, but it is the one that will actually stop a
launch.

---

## 16. Anti-patterns

| Do not | Do |
|---|---|
| Copy a reference's pixels | Copy its grammar |
| Pick colours | Build a ramp |
| Pick fonts | Assign roles |
| One background colour down the page | Alternate grounds |
| Flat surfaces everywhere | Texture at 5 percent opacity |
| Brand tint over photography | Scrim only for contrast |
| Collapse everything to one column | Decide per component |
| Fit the CSS to the copy | Fit the copy to the budget |
| Em dashes | Commas and full stops |
| Ship the full icon font | Subset it |
| Assume it renders | Open it and look |

---

## The short version

Decompose the reference into rules. Put every value in a token. Order your
colours into a ramp and alternate the grounds. Give each typeface one job and
check its glyphs. Invent one shape nobody else has and repeat it. Add texture
just below the threshold of visibility. Size the hero to the screen, including
its height. Measure the copy and cut it to fit rather than letting it break the
layout. Write like a person. Own and subset your assets. Degrade without
JavaScript.

Then open it in a browser and look at it, because that is the only step that
actually tells you the truth.
