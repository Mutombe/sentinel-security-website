# -*- coding: utf-8 -*-
"""Emits the Sentinel site as plain static HTML from one shared shell.

Run:  python tools/build.py
It writes the six pages in the project root. The site never needs this to run;
it just keeps the duplicated header, footer and CTA band in sync.
"""
import io, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)

NAV = [
    ("index.html", "Home"),
    ("about.html", "About"),
    ("services.html", "Services"),
    ("renewable-energy.html", "Renewable Energy"),
    ("contact.html", "Contact"),
]

# ----------------------------------------------------------------- icons
def icon(name, size="i-md", style="ph", cls=""):
    """A Phosphor glyph. style is 'ph', 'ph-duotone' or 'ph-fill'."""
    return '<i class="%s ph-%s %s%s" aria-hidden="true"></i>' % (
        style, name, size, (" " + cls) if cls else "")

def duo(name, size="i-2xl"):
    return icon(name, size, "ph-duotone")

CHEV = '<span class="pbtn__chev">%s</span>' % icon("caret-double-right", "i-sm")
CHEV_SM = icon("caret-double-right", "i-xs")
ARROW = icon("arrow-right", "i-sm")
STAR = icon("star", "i-xs", "ph-fill")


def pbtn(label, href, variant="", attrs=""):
    cls = "pbtn" + ((" " + variant) if variant else "")
    return '<a class="%s" href="%s"%s><span class="pbtn__label">%s</span>%s</a>' % (
        cls, href, attrs, label, CHEV)


def eyebrow(text, variant=""):
    cls = "eyebrow" + ((" " + variant) if variant else "")
    return '<p class="%s">%s<span>%s</span></p>' % (cls, icon("asterisk", "i-xs"), text)


def shead(kicker, title, aside="", cta="", variant="", kv=""):
    right = ('<div class="shead__cta">%s</div>' % cta) if cta else (
        ('<div class="shead__aside">%s</div>' % aside) if aside else "")
    cls = "shead" + ((" " + variant) if variant else "")
    return """      <div class="%s" data-reveal>
        <div>
          %s
          <h2 class="h-2 shead__title">%s</h2>
        </div>
        %s
      </div>
""" % (cls, eyebrow(kicker, kv), title, right)


def ncard(variant, ico, title, text, bullets, href, cta="Explore more"):
    lis = ""
    if bullets:
        lis = ('<ul class="card__list" style="margin-top:1.25rem">'
               + "".join("<li>%s</li>" % b for b in bullets) + "</ul>")
    return """        <article class="ncard ncard--%s" data-reveal>
          <div class="ncard__main">
            <span class="ncard__icon">%s</span>
            <h3 class="h-3">%s</h3>
            <p>%s</p>
            %s
          </div>
          <div class="ncard__foot">
            <a class="ncard__cta" href="%s">%s %s</a>
            <span class="ncard__fill" aria-hidden="true"></span>
          </div>
        </article>
""" % (variant, duo(ico), title, text, lis, href, cta, CHEV_SM)


# ----------------------------------------------------------------- shell
def head(title, desc, canonical):
    return """<!DOCTYPE html>
<html lang="en-ZW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%s</title>
<meta name="description" content="%s">
<meta name="theme-color" content="#06291B">
<link rel="canonical" href="https://www.sentinel.co.zw/%s">

<meta property="og:type" content="website">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:image" content="assets/img/brand/flier-2.jpg">
<meta property="og:locale" content="en_ZW">

<link rel="icon" type="image/png" sizes="32x32" href="assets/img/brand/favicon-32.png">
<link rel="apple-touch-icon" href="assets/img/brand/favicon-180.png">

<link rel="preload" href="assets/fonts/manrope-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/manrope-800.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/icons/phosphor.css">
<link rel="stylesheet" href="assets/css/style.css">
<script>document.documentElement.classList.add('js');</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
""" % (title, desc, canonical, title, desc)


def topbar():
    return """
<!-- ===== Utility bar ===== -->
<div class="topbar">
  <div class="container topbar__inner">
    <ul class="topbar__list">
      <li>%s <span>Zimbabwe&rsquo;s trusted electronic security company</span></li>
      <li>%s <a href="mailto:info@sentinel.co.zw">info@sentinel.co.zw</a></li>
      <li>%s <a href="tel:+263773589461" class="num">+263 773 589 461</a></li>
    </ul>
    <div class="topbar__social">
      <span class="script">towards a #secure_world</span>
      <a href="https://www.facebook.com/" aria-label="Facebook" rel="noopener">%s</a>
      <a href="https://www.linkedin.com/" aria-label="LinkedIn" rel="noopener">%s</a>
      <a href="https://wa.me/263773589461" aria-label="WhatsApp" rel="noopener">%s</a>
    </div>
  </div>
</div>
""" % (icon("check-circle", "i-xs"), icon("envelope-simple", "i-xs"), icon("phone-call", "i-xs"),
       icon("facebook-logo", "i-sm", "ph-fill"), icon("linkedin-logo", "i-sm", "ph-fill"),
       icon("whatsapp-logo", "i-sm", "ph-fill"))


def header(active):
    items = "\n".join(
        '        <li><a class="nav__link" href="%s"%s>%s</a></li>'
        % (h, ' aria-current="page"' if h == active else "", l) for h, l in NAV)
    drawer = "\n".join(
        '    <a href="%s">%s <span class="num">%02d</span></a>' % (h, l, i + 1)
        for i, (h, l) in enumerate(NAV))
    return """
<!-- ===== Header ===== -->
<header class="header">
  <div class="container header__inner">
    <a class="brand" href="index.html" aria-label="Sentinel Security Technology, home">
      <img class="brand__light" src="assets/img/brand/sentinel-logo-white.png" alt="Sentinel Security Technology" width="300" height="104">
      <img class="brand__dark" src="assets/img/brand/sentinel-logo.png" alt="" width="300" height="104" aria-hidden="true">
    </a>

    <nav class="nav" aria-label="Primary">
      <ul class="nav__list">
%s
      </ul>
    </nav>

    <div class="header__cta">%s</div>

    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="drawer" aria-label="Open menu">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>

<div class="drawer" id="drawer">
  <nav class="drawer__list" aria-label="Mobile">
%s
  </nav>
  <div class="drawer__foot">
    <a href="tel:+263773589461" class="num">+263 773 589 461</a>
    <a href="mailto:info@sentinel.co.zw">info@sentinel.co.zw</a>
    <p>38 Northampton Crescent, Eastlea, Harare</p>
    %s
  </div>
</div>

<main id="main">
""" % (items, pbtn("Book a site survey", "contact.html"), drawer,
       pbtn("Book a site survey", "contact.html", "pbtn--block"))


CTA = """
  <!-- ===== CTA ===== -->
  <section class="section section--tight">
    <div class="container">
      <div class="cta" data-reveal>
        <div class="cta__inner">
          <div>
            %s
            <h2 class="h-2">Book a free site survey</h2>
            <p>We walk your property, write up where you are exposed, and price the fix. No charge.</p>
          </div>
          <div class="cta__actions">
            %s
            %s
          </div>
        </div>
      </div>
    </div>
  </section>
""" % (eyebrow("Next step", "eyebrow--dark"),
       pbtn("Book a site survey", "contact.html", "pbtn--light"),
       pbtn("+263 773 589 461", "tel:+263773589461", "pbtn--outline"))


FOOTER = """
</main>

<!-- ===== Footer ===== -->
<footer class="footer">
  <div class="container">
    <div class="footer__top">
      <div class="footer__brand">
        <img src="assets/img/brand/sentinel-logo-white.png" alt="Sentinel Security Technology" width="300" height="104" loading="lazy">
        <p class="script footer__tagline">towards a #secure_world</p>
        <p>Security specialists who protect and secure your assets through digital solutions. Harare, Zimbabwe.</p>
        <div class="socials">
          <a href="https://www.facebook.com/" aria-label="Sentinel on Facebook" rel="noopener">%s</a>
          <a href="https://www.linkedin.com/" aria-label="Sentinel on LinkedIn" rel="noopener">%s</a>
          <a href="https://wa.me/263773589461" aria-label="Sentinel on WhatsApp" rel="noopener">%s</a>
        </div>
      </div>

      <div>
        <h4>Company</h4>
        <ul class="footer__links">
          <li><a href="index.html">Home</a></li>
          <li><a href="about.html">About us</a></li>
          <li><a href="services.html">Services</a></li>
          <li><a href="renewable-energy.html">Renewable energy</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>

      <div>
        <h4>Services</h4>
        <ul class="footer__links">
          <li><a href="services.html#cctv">CCTV surveillance</a></li>
          <li><a href="services.html#alarms">Intruder alarms</a></li>
          <li><a href="services.html#access">Access control</a></li>
          <li><a href="services.html#fire">Fire detection</a></li>
          <li><a href="services.html#man-traps">Man traps</a></li>
          <li><a href="services.html#physical">Physical access control</a></li>
        </ul>
      </div>

      <div>
        <h4>Get in touch</h4>
        <ul class="footer__contact">
          <li>%s<span>38 Northampton Crescent,<br>Eastlea, Harare, Zimbabwe</span></li>
          <li>%s<span class="num">
              <a href="tel:+263773589461">+263 773 589 461</a>
              <a href="tel:+263772568361">+263 772 568 361</a>
              <a href="tel:+263242006157">+263 24 200 6157</a>
            </span></li>
          <li>%s<a href="mailto:info@sentinel.co.zw">info@sentinel.co.zw</a></li>
        </ul>
      </div>
    </div>

    <div class="footer__bottom">
      <p style="margin:0">&copy; <span data-year class="num">2026</span> Sentinel Security Technology</p>
      <nav aria-label="Legal">
        <a href="privacy.html">Privacy policy</a>
        <a href="contact.html">Contact</a>
      </nav>
    </div>
  </div>
</footer>

<button class="to-top" type="button" aria-label="Back to top">%s</button>

<script src="assets/js/main.js" defer></script>
</body>
</html>
""" % (icon("facebook-logo", "i-sm", "ph-fill"), icon("linkedin-logo", "i-sm", "ph-fill"),
       icon("whatsapp-logo", "i-sm", "ph-fill"),
       icon("map-pin", "i-sm"), icon("phone-call", "i-sm"), icon("envelope-simple", "i-sm"),
       icon("arrow-up", "i-md"))


def phero(label, title, lead, photo=None, alt=""):
    if photo:
        media = """    <div class="phero__media">
      <img src="assets/img/photos/%s-1200.jpg"
           srcset="assets/img/photos/%s-640.jpg 640w, assets/img/photos/%s-1200.jpg 1200w"
           sizes="70vw" alt="%s" width="1200" height="600" fetchpriority="high">
    </div>
    <div class="phero__scrim"></div>
""" % (photo, photo, photo, alt)
        cls = "phero"
    else:
        media, cls = "", "phero phero--plain"
    return """
  <section class="%s">
%s    <div class="container">
      <nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Home</a> <i class="sep">/</i> <span>%s</span></nav>
      <h1 class="h-1">%s</h1>
      <p class="lead">%s</p>
    </div>
  </section>
""" % (cls, media, label, title, lead)


def write(name, title, desc, body, cta=True):
    html = head(title, desc, name) + topbar() + header(name) + body + (CTA if cta else "") + FOOTER
    with io.open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("wrote", name, len(html))


CLIENTS = """
  <!-- ===== Clients ===== -->
  <section class="clients section--white" aria-label="Clients">
    <div class="container">
      <p class="clients__label">Trusted across Zimbabwe</p>
      <div class="marquee">
        <div class="marquee__track">
          <div class="marquee__group">
            <img src="assets/img/clients/ecobank.png" alt="Ecobank" loading="lazy">
            <img src="assets/img/clients/green-fuel.png" alt="Green Fuel" loading="lazy">
            <img src="assets/img/clients/probrands.png" alt="ProBrands" loading="lazy">
            <img src="assets/img/clients/cottco.png" alt="Cottco Holdings Limited" loading="lazy">
          </div>
          <div class="marquee__group" aria-hidden="true">
            <img src="assets/img/clients/ecobank.png" alt="" loading="lazy">
            <img src="assets/img/clients/green-fuel.png" alt="" loading="lazy">
            <img src="assets/img/clients/probrands.png" alt="" loading="lazy">
            <img src="assets/img/clients/cottco.png" alt="" loading="lazy">
          </div>
        </div>
      </div>
    </div>
  </section>
"""

STEPS = [
    ("01", "Survey", "We walk the site with you and write up where you are exposed. This costs you nothing, whether or not you go ahead with us."),
    ("02", "Specify", "You get the camera positions, cable routes, power requirements and coverage in writing, with a price against each line."),
    ("03", "Install", "Our own technicians do the work, commission the system and train whoever will be using it every day."),
    ("04", "Maintain", "Servicing on a schedule, health checks on the equipment, and a number you can call at any hour."),
]

def steps_block():
    out = '      <div class="steps">\n'
    for n, t, p in STEPS:
        out += ('        <div class="step" data-reveal><span class="step__n num">%s</span>'
                '<h3>%s</h3><p>%s</p></div>\n' % (n, t, p))
    return out + "      </div>\n"


# ================================================================= HOME
home = """
  <!-- ===== Hero ===== -->
  <section class="hero">
    <div class="hero__media" aria-hidden="true">
      <video class="hero__video" data-hero-video
             poster="assets/img/photos/hero-poster.jpg"
             muted loop playsinline preload="none"
             width="768" height="432">
        <source src="assets/video/hero.mp4" type="video/mp4">
      </video>
    </div>
    <div class="hero__tint" aria-hidden="true"></div>
    <div class="hero__glow" aria-hidden="true"></div>
    <div class="hero__grid" aria-hidden="true"></div>
    <div class="hero__scrim"></div>

    <div class="container">
      <div class="hero__content">
        <span class="hero__badge">
          <span class="stars">%s%s%s</span>
          Award winning in <b class="num">2014, 2015 and 2016</b>
        </span>

        <h1 class="h-hero">Your <span class="accent-lime">security</span><br>is our business</h1>

        <p class="hero__lead">
          We design, install and maintain electronic security across Zimbabwe, from one
          camera at a front gate to a control room watching a whole estate.
        </p>

        <div class="hero__actions">
          %s
          <dl class="hero__call">
            <a class="rbtn" href="tel:+263773589461" aria-label="Call Sentinel">%s</a>
            <div><dt>Call us</dt><dd class="num">+263 773 589 461</dd></div>
          </dl>
        </div>

        <dl class="hero__facts">
          <div class="hero__fact"><dt class="num">24/7</dt><dd>Support</dd></div>
          <div class="hero__fact"><dt class="num">3</dt><dd>Awards</dd></div>
          <div class="hero__fact"><dt class="num">5</dt><dd>Sectors</dd></div>
          <div class="hero__fact"><dt class="num">6</dt><dd>Systems</dd></div>
        </dl>
      </div>
    </div>
  </section>
""" % (STAR, STAR, STAR, pbtn("Book a free site survey", "contact.html"),
       icon("phone-call", "i-md")) + CLIENTS + """
  <!-- ===== Approach ===== -->
  <section class="section section--cream ruled">
    <div class="container">
""" + shead("Our approach",
            "Residential, commercial and industrial",
            "Every job starts with a site survey and ends with a maintenance plan, whether "
            "it is three cameras on a house or a factory perimeter.") + """
      <div class="grid g-3">
""" + ncard("white", "house-line", "Residential",
            "Alarms, cameras, gate motors and lighting for the house and the wall around it.",
            ["Intruder alarm on call day and night", "CCTV you can check from your phone",
             "Electric gate motors", "Driveway lighting"],
            "services.html#residential") + ncard("lime", "buildings", "Commercial",
            "Offices, shops and shared buildings where staff and visitors move through all day.",
            ["Security design and installation", "Biometric and card access control",
             "Turnstiles and boom gates", "Systems talking to each other"],
            "services.html#commercial") + ncard("dark", "factory", "Industrial",
            "Plant, yard and logistics sites that need cameras, plate readers and gate control working as one.",
            ["Video management systems", "Number plate readers",
             "Gate automation and parking", "Health monitoring on devices"],
            "services.html#industrial") + """      </div>
    </div>
  </section>

  <!-- ===== Who we are ===== -->
  <section class="section section--white">
    <div class="container split">
      <div class="bento" data-reveal>
        <img class="bento__hero" src="assets/img/photos/guards-briefing-1200.jpg"
             srcset="assets/img/photos/guards-briefing-640.jpg 640w, assets/img/photos/guards-briefing-1200.jpg 1200w"
             sizes="(max-width:980px) 100vw, 45vw"
             alt="A Sentinel team briefing before going out to site" width="1200" height="600" loading="lazy">
        <div class="bento__stat">
          %s
          <strong class="num">24/7</strong>
          <span>Someone on the phone<br>at any hour</span>
        </div>
        <img class="bento__tile" src="assets/img/photos/access-control-desk-640.jpg"
             alt="Access control at a reception desk" width="640" height="640" loading="lazy">
      </div>

      <div data-reveal>
        %s
        <h2 class="h-2">We take care of all your security needs</h2>
        <p class="lead">
          An accredited Zimbabwean firm covering electronic security, control room
          operation and physical access control.
        </p>
        <p>
          Our own technicians design, install and commission every system, then stay on to
          maintain it. You call us, not four contractors.
        </p>

        <div class="byline">
          %s
          <div class="byline__person">
            <span class="byline__avatar">%s</span>
            <span>
              <strong>Accredited and insured</strong>
              <span>Based in Harare, working countrywide</span>
            </span>
          </div>
        </div>

        <div class="grid g-2" style="margin-top:2.25rem">
          <div class="ministat">
            <div class="ministat__stars">%s%s%s%s%s</div>
            <div class="ministat__num num">3</div>
            <p class="ministat__label">Best Service Award<br><span class="muted num" style="font-weight:500">2014, 2015 and 2016</span></p>
          </div>
          <div class="ministat">
            <h3>Where we work</h3>
            <div class="tags">
              <span>Corporate</span><span>Banking</span><span>Government</span>
              <span>Manufacturing</span><span>Construction</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ===== Services ===== -->
  <section class="section section--cream" id="services">
    <div class="container">
""" % (duo("check-circle", "i-xl"), eyebrow("Who we are"),
       pbtn("More about us", "about.html"),
       duo("shield-check", "i-md"), STAR, STAR, STAR, STAR, STAR) + shead(
    "Our services",
    "The systems we install and look after",
    cta=pbtn("See all services", "services.html", "pbtn--dark")) + """
      <div class="grid g-3">
"""

SERVICES = [
 ("cctv", "security-camera", "CCTV surveillance",
  "Cameras placed around your actual blind spots, sightlines and lighting, not a standard layout.",
  ["IP and HD analogue systems", "Remote viewing on phone or desktop", "Number plate recognition"]),
 ("alarms", "bell-ringing", "Intruder alarms",
  "Built to put someone off before they get in, and to record what happened if they do.",
  ["Perimeter beams and indoor sensors", "Panic buttons", "Linked to armed response"]),
 ("access", "fingerprint", "Access control",
  "Controlling who opens which door, from one reception to a group of sites.",
  ["Fingerprint, card and PIN readers", "Time and attendance reports", "Visitor passes"]),
 ("fire", "fire-extinguisher", "Fire detection",
  "Fire sensors and alarms that give people time to get out and limit what you lose.",
  ["Addressable and conventional panels", "Smoke, heat and flame sensors", "Sounders and evacuation"]),
 ("man-traps", "door-open", "Man traps",
  "Interlocking doors for banking halls, strongrooms and server rooms.",
  ["Cash handling areas", "Strongroom and server entry", "Stops tailgating"]),
 ("physical", "barricade", "Physical access control",
  "Vehicle and pedestrian control, including high security and anti terror equipment.",
  ["Boom gates and gate motors", "Turnstiles and walkways", "Parking control"]),
]

for anchor, ico, title, text, bullets in SERVICES:
    home += """        <article class="card card--hoverdark" data-reveal>
          <span class="card__icon">%s</span>
          <h3 class="h-4">%s</h3>
          <p>%s</p>
          <ul class="card__list">%s</ul>
          <a class="plink" href="services.html#%s">Read more %s</a>
        </article>
""" % (duo(ico, "i-lg"), title, text, "".join("<li>%s</li>" % b for b in bullets), anchor, ARROW)

home += """      </div>
    </div>
  </section>

  <!-- ===== Process ===== -->
  <section class="section section--dark ruled">
    <div class="container">
""" + shead("How we work", "From the first call to the handover",
            "The same four stages on every job. You see the specification and the price "
            "before any work starts.",
            kv="eyebrow--dark") + steps_block() + """    </div>
  </section>

  <!-- ===== Sectors ===== -->
  <section class="section section--white">
    <div class="container">
""" + shead("Who we work for", "Where our systems run every day",
            "Banks, factories, government departments, building sites and homes. Most of "
            "our work sits in the five below.") + """
      <div class="rows">
"""

SECTORS = [
 ("Corporate offices", "Reception access control, visitor passes, cover on boardrooms and server rooms, cameras across every floor."),
 ("Banking and financial services", "Man traps, strongroom interlocks, cameras over cash handling, and recordings kept long enough to satisfy an audit."),
 ("Government", "High security and anti terror access equipment, controlled perimeters and control room operation."),
 ("Manufacturing and industry", "Plate readers on weighbridges and gates, cameras over the yard, time and attendance across shifts."),
 ("Construction", "Cameras up quickly on a new site, cover on plant and materials, and access control that moves as the build moves."),
]
for i, (t, p) in enumerate(SECTORS, 1):
    home += """        <a class="row" href="contact.html" data-reveal>
          <span class="row__n num">%02d</span>
          <span class="row__body"><h3>%s</h3><p>%s</p></span>
          <span class="row__go" aria-hidden="true">%s</span>
        </a>
""" % (i, t, p, ARROW)

home += """      </div>
    </div>
  </section>

  <!-- ===== Solar ===== -->
  <section class="section section--lime ruled">
    <div class="container split">
      <div data-reveal>
        %s
        <h2 class="h-2">Solar PV for homes, businesses and power plants</h2>
        <p class="script script--lg">keeping the cameras on when the grid is off</p>
        <p class="lead" style="color:var(--ink-2)">
          One of the leading solar PV companies in Zimbabwe. We handle the build, then the
          maintenance that keeps the panels producing.
        </p>
        <div style="margin-top:2rem">%s</div>
      </div>
      <div class="grid g-2" data-reveal>
        <div class="ministat" style="background:var(--g-dark);color:var(--on-dark-soft)">
          <span class="card__icon" style="background:rgba(255,255,255,.1);color:var(--lime)">%s</span>
          <h3 style="color:#fff">Durability</h3>
          <p style="color:var(--on-dark-soft);font-size:.93rem;margin:0">Built for dust, heat, storms and the load an actual Zimbabwean site puts on them.</p>
        </div>
        <div class="ministat" style="background:var(--white)">
          <span class="card__icon">%s</span>
          <h3>Reliability</h3>
          <p style="font-size:.93rem;margin:0">Panels that perform without compromise, backed by a service schedule.</p>
        </div>
        <div class="ministat" style="background:var(--white)">
          <span class="card__icon">%s</span>
          <h3>Output</h3>
          <p style="font-size:.93rem;margin:0">More energy over the life of the system, so the saving stays predictable.</p>
        </div>
        <div class="ministat" style="background:var(--g-mid);color:rgba(255,255,255,.78)">
          <span class="card__icon" style="background:rgba(255,255,255,.14);color:#fff">%s</span>
          <h3 style="color:#fff">Maintenance</h3>
          <p style="color:rgba(255,255,255,.78);font-size:.93rem;margin:0">Cleaning, string checks and battery health on a fixed schedule.</p>
        </div>
      </div>
    </div>
  </section>
""" % (eyebrow("Renewable energy", "eyebrow--lime"),
       pbtn("Look at solar", "renewable-energy.html", "pbtn--dark"),
       duo("shield-check", "i-lg"), duo("sun", "i-lg"), duo("lightning", "i-lg"), duo("wrench", "i-lg"))

write("index.html",
      "Sentinel Security Technology | Electronic Security in Zimbabwe",
      "CCTV, intruder alarms, access control, fire detection and physical access control across Zimbabwe. Based in Harare, support at any hour, award winning in 2014, 2015 and 2016.",
      home)


# ================================================================= ABOUT
about = phero("About", "We take care of all your security needs",
  "An accredited Zimbabwean firm covering electronic security, control room operation "
  "and physical access control.",
  "foot-patrol-street", "A Sentinel officer on foot patrol") + """
  <section class="section section--white">
    <div class="container split">
      <div class="bento" data-reveal>
        <img class="bento__hero" src="assets/img/photos/guards-briefing-1200.jpg"
             srcset="assets/img/photos/guards-briefing-640.jpg 640w, assets/img/photos/guards-briefing-1200.jpg 1200w"
             sizes="(max-width:980px) 100vw, 45vw"
             alt="Sentinel team briefing" width="1200" height="600" loading="lazy">
        <img class="bento__tile" src="assets/img/photos/operator-night-shift-640.jpg"
             alt="Control room operator on night shift" width="640" height="640" loading="lazy">
        <div class="bento__stat">
          %s
          <strong class="num">5</strong>
          <span>Sectors we work in<br>every week</span>
        </div>
      </div>

      <div data-reveal>
        %s
        <h2 class="h-2">What Sentinel does</h2>
        <p class="lead">
          We work for organisations that cannot afford a gap in cover: offices, banks,
          government departments, factories and building sites.
        </p>
        <p>
          That is why banks and manufacturers hand us the parts of a building they cannot
          afford to get wrong. Six things done properly, not twenty done badly.
        </p>
        <div class="tags" style="margin-top:1.75rem">
          <span>Accredited Zimbabwean firm</span><span>Based in Harare</span>
          <span>Working countrywide</span><span>Support at any hour</span>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--cream">
    <div class="container">
""" % (duo("scan-smiley", "i-xl"), eyebrow("Who we are")) + shead(
  "What drives us", "Mission, vision and values",
  "Three statements we are happy to be held to.") + """
      <div class="grid g-3">
""" + ncard("white", "target", "Mission",
            "To keep pace with the technology and stay ahead of our competitors. What we "
            "install today should still hold up in five years.",
            [], "contact.html", "Talk to us") \
    + ncard("lime", "compass", "Vision",
            "We are committed to providing the highest quality of security services to individuals "
            "and business in Zimbabwe.", [], "services.html", "Our services") \
    + ncard("dark", "shield-check", "Values",
            "We set our standards by what clients expect, then try to beat it. Not by "
            "whatever is easiest to deliver.", [], "contact.html", "Work with us") + """      </div>
    </div>
  </section>

  <section class="section section--white">
    <div class="container">
""" + shead("Why clients stay", "Six things we will not cut corners on",
            "Not selling points. The standard every job is held to.") + """
      <div class="grid g-3">
"""

WHY = [
 ("clock-countdown", "We turn up when we said",
  "Our people arrive at the time we gave you, in uniform, with the right parts on the vehicle. A missed appointment is a failure like any other."),
 ("graduation-cap", "Training does not stop",
  "Threats change and so does the equipment. Our technicians keep training on what we install, rather than learning it once."),
 ("tag", "Prices you can pick apart",
  "We quote the system your risk calls for, line by line, so you can question any of it. No lump sums."),
 ("magnifying-glass", "Independent auditing",
  "We assess and audit security risk, including systems we did not install. If yours is good enough, we will say so."),
 ("headset", "Someone answers at 2am",
  "A system nobody can fix overnight protects nothing. Our support runs the same hours your risk does."),
 ("handshake", "One company, start to finish",
  "Design, supply, installation and maintenance all sit with us, so there is nobody to point at."),
]
for ico, t, p in WHY:
    about += """        <article class="card card--hoverdark" data-reveal>
          <span class="card__icon">%s</span>
          <h3 class="h-4">%s</h3>
          <p>%s</p>
        </article>
""" % (duo(ico, "i-lg"), t, p)

about += """      </div>
    </div>
  </section>

  <section class="section section--dark">
    <div class="container">
""" + shead("Recognition", "Best Service Award, three years running",
            "Named Best Service Award in 2014, in 2015 and again in 2016.", kv="eyebrow--dark") + """
      <div class="grid g-3">
        <div class="card card--dark" data-reveal>
          <img class="award-mark" src="assets/img/brand/award-2014-white.png" alt="" aria-hidden="true"
               width="120" height="118" loading="lazy">
          <h3 class="h-4 num">2014</h3><p>Best Service Award</p>
        </div>
        <div class="card card--dark" data-reveal>
          <img class="award-mark" src="assets/img/brand/award-2015-white.png" alt="" aria-hidden="true"
               width="120" height="118" loading="lazy">
          <h3 class="h-4 num">2015</h3><p>Best Service Award</p>
        </div>
        <div class="card card--dark" data-reveal>
          <img class="award-mark" src="assets/img/brand/award-2016-white.png" alt="" aria-hidden="true"
               width="120" height="118" loading="lazy">
          <h3 class="h-4 num">2016</h3><p>Best Service Award</p>
        </div>
      </div>
    </div>
  </section>
""" + CLIENTS

write("about.html",
      "About Us | Sentinel Security Technology",
      "An accredited Zimbabwean security firm supplying electronic security, control room operations and physical access control to corporate, banking, government, manufacturing and construction clients.",
      about)


# ================================================================= SERVICES
def detail(anchor, kicker, title, lead, bullets, photo, alt, flip):
    lis = "".join("<li>%s</li>" % b for b in bullets)
    media = """        <div data-reveal>
          <img src="assets/img/photos/%s-1200.jpg"
               srcset="assets/img/photos/%s-640.jpg 640w, assets/img/photos/%s-1200.jpg 1200w"
               sizes="(max-width:980px) 100vw, 45vw"
               style="border-radius:var(--r-card);aspect-ratio:4/3;object-fit:cover;width:100%%"
               alt="%s" width="1200" height="900" loading="lazy">
        </div>
""" % (photo, photo, photo, alt)
    text = """        <div data-reveal>
          %s
          <h2 class="h-2" style="font-size:clamp(1.6rem,2.8vw,2.3rem)">%s</h2>
          <p class="lead">%s</p>
          <ul class="card__list" style="margin-top:1.4rem">%s</ul>
          <div style="margin-top:2rem">%s</div>
        </div>
""" % (eyebrow(kicker), title, lead, lis, pbtn("Ask for a quotation", "contact.html"))
    inner = (media + text) if flip else (text + media)
    return """      <div class="split" id="%s" style="scroll-margin-top:calc(var(--header-h) + 28px);padding-block:clamp(2.5rem,5vw,4rem)">
%s      </div>
""" % (anchor, inner)


services = phero("Services", "Everything we install and maintain",
  "Residential, commercial and industrial. The same team designs it, installs it and services it, "
  "so there is one number to call when something needs attention.",
  "access-control-desk", "Access control at a reception desk") + """
  <section class="section section--cream">
    <div class="container">
""" + shead("Where we work", "Three kinds of site, one standard of work",
            "The scope of a job changes with the site. How carefully we specify it does not.") + """
      <div class="grid g-3">
""" + ncard("white", "house-line", "Residential",
            "Alarms, cameras, gate motors and lighting for the house and the wall around it.",
            ["Intruder alarm on call day and night", "CCTV you can check from your phone",
             "Electric gate motors", "Driveway lighting"],
            "contact.html", "Get a price") + ncard("lime", "buildings", "Commercial",
            "Offices, shops and shared buildings where staff and visitors move through all day.",
            ["Security design and installation", "Biometric and card access control",
             "Turnstiles and boom gates", "Systems talking to each other"],
            "contact.html", "Get a price") + ncard("dark", "factory", "Industrial",
            "Plant, yard and logistics sites needing cameras, plate readers and gate control as one system.",
            ["Video management systems", "Number plate readers",
             "Gate automation and parking", "Health monitoring on devices"],
            "contact.html", "Get a price") + """      </div>
    </div>
  </section>

  <section class="section section--white">
    <div class="container">
"""
services = services.replace('<article class="ncard ncard--white"', '<article class="ncard ncard--white" id="residential"', 1)
services = services.replace('<article class="ncard ncard--lime"', '<article class="ncard ncard--lime" id="commercial"', 1)
services = services.replace('<article class="ncard ncard--dark"', '<article class="ncard ncard--dark" id="industrial"', 1)

services += shead("In detail", "Six systems we specialise in",
                  "Each one is something we staff for, train for and keep stock for.")

DETAILS = [
 ("cctv", "Surveillance", "CCTV surveillance",
  "Camera systems for homes and businesses, laid out around your actual blind spots, sightlines "
  "and lighting rather than a standard drawing.",
  ["IP and HD analogue cameras", "Video management and remote viewing",
   "Number plate recognition", "Optics that work after dark",
   "Recording kept as long as your policy says"],
  "control-room-monitoring", "Operators watching a CCTV wall"),
 ("alarms", "Detection", "Intruder alarms",
  "Systems meant to put someone off before they get in, and to record an incident already under way "
  "so you have something to act on afterwards.",
  ["Perimeter beams and motion sensors", "Panic and duress buttons",
   "Linked to armed response", "Zones you can arm separately",
   "Battery backup through an outage"],
  "operator-night-shift", "Alarm monitoring on night shift"),
 ("access", "Identity", "Access control",
  "Door control for a small business upward, making a building both safer and easier to move "
  "around, from one reception door to a group of sites.",
  ["Fingerprint, card and PIN readers", "Time and attendance reporting",
   "Visitor passes and temporary codes", "Alerts on forced or held doors",
   "One place to manage several sites"],
  "access-control-desk", "Access control at a reception desk"),
 ("fire", "Life safety", "Fire detection",
  "Fire sensors and alarms that buy people time to get out and keep the damage down.",
  ["Addressable and conventional panels", "Smoke, heat and flame detection",
   "Sounders and evacuation systems", "Doors that release for exit",
   "Testing and certification on a schedule"],
  "guard-reception-radio", "Reception security and life safety monitoring"),
 ("man-traps", "High security", "Man traps",
  "Interlocking doors for the parts of a building that hold real value. Every installation starts "
  "with a site assessment so the trap suits the traffic going through it.",
  ["Banking halls and cash areas", "Server rooms and strongrooms",
   "Interlocks that stop tailgating", "Single occupancy sensing",
   "Override and fire mode release"],
  "guards-briefing", "Security team briefing"),
 ("physical", "Perimeter", "Physical access control",
  "Vehicle and pedestrian equipment, including high security and anti terror products for "
  "perimeters that face real exposure.",
  ["Boom gates and gate automation", "Turnstiles and pedestrian lanes", "Parking control systems",
   "Road blockers and bollards", "Number plate driven access"],
  "k9-vehicle-search", "Vehicle checkpoint search"),
]
for i, d in enumerate(DETAILS):
    services += detail(*d, flip=(i % 2 == 1))

services += """    </div>
  </section>

  <section class="section section--dark ruled">
    <div class="container">
""" + shead("How we work", "From the first call to the handover",
            "Four stages, the same on every job whatever the scale.", kv="eyebrow--dark") + steps_block() + """    </div>
  </section>

  <section class="section section--cream">
    <div class="container container--narrow">
""" + shead("Questions", "Things people ask us first", "", variant="shead--center") + """
      <div class="accordion" data-reveal>
"""

FAQ = [
 ("Do you charge for the site survey?",
  "No. The survey and the risk assessment are free anywhere we work in Zimbabwe, and you keep the written specification either way."),
 ("Can you work on a system another company installed?",
  "Yes. We audit, repair, extend and take over maintenance on existing systems. If yours is sound we will say so, rather than sell you a new one."),
 ("Do you cover sites outside Harare?",
  "We are based in Eastlea, Harare, and work countrywide. Tell us where the site is and we will confirm travel and response times up front."),
 ("What happens when the power goes out?",
  "Every system we design has battery backup sized to your risk. For long outages we add solar through our renewable energy division."),
 ("Can I view my cameras remotely?",
  "Yes, securely, on a phone or a desktop. Permissions are set per user, so staff only see the cameras they are supposed to."),
]
for i, (q, a) in enumerate(FAQ, 1):
    services += """        <div class="acc__item">
          <h3 style="margin:0">
            <button class="acc__btn" type="button" aria-expanded="false" aria-controls="faq%d">
              %s<span class="acc__icon" aria-hidden="true"></span>
            </button>
          </h3>
          <div class="acc__panel" id="faq%d" data-open="false"><div><p>%s</p></div></div>
        </div>
""" % (i, q, i, a)

services += """      </div>
    </div>
  </section>
"""

write("services.html",
      "Services: CCTV, Alarms, Access Control and Fire Detection | Sentinel Security Technology",
      "CCTV, intruder alarms, access control, fire detection, man traps and physical access control for homes, offices and industrial sites across Zimbabwe.",
      services)


# ================================================================= SOLAR
solar = phero("Renewable Energy", "Solar PV for homes, businesses and power plants",
  "One of the leading solar PV companies in Zimbabwe. We handle the engineering, "
  "procurement and construction, then the maintenance that keeps it producing.") + """
  <section class="section section--white">
    <div class="container split">
      <div data-reveal>
        %s
        <h2 class="h-2">Panels that keep your bill down and your site running</h2>
        <p class="script script--lg">towards a #secure_world</p>
        <p class="lead">
          Cutting a bill and surviving an outage are the same job. We size, supply and
          maintain systems that carry the loads you actually run.
        </p>
        <p>
          That covers the whole life of the system, from design and procurement through to
          the servicing that holds output to the business case.
        </p>
        <div style="margin-top:2rem">%s</div>
      </div>
      <div data-reveal>
        <img src="assets/img/photos/residential-electr-services.jpg"
             style="border-radius:var(--r-card);aspect-ratio:4/3;object-fit:cover;width:100%%"
             alt="An electrical distribution board being commissioned" width="600" height="450" loading="lazy">
      </div>
    </div>
  </section>

  <section class="section section--cream">
    <div class="container">
""" % (eyebrow("Solar PV"), pbtn("Ask for a solar assessment", "contact.html")) + shead(
  "Why Sentinel solar", "Three things a system gets judged on",
  "Once the installers have gone, this is what you are left with.") + """
      <div class="grid g-3">
""" + ncard("white", "shield-check", "Durability",
            "Built for real conditions: dust, heat, storms and the load profile of an "
            "actual Zimbabwean site.",
            [], "contact.html", "Talk to us") \
    + ncard("lime", "sun", "Reliability",
            "Panels that perform without compromise, backed by a service schedule rather "
            "than a handshake.",
            [], "contact.html", "Talk to us") \
    + ncard("dark", "lightning", "Output",
            "More energy over the life of the system, so the saving you were promised holds "
            "up.",
            [], "contact.html", "Talk to us") + """      </div>
    </div>
  </section>

  <section class="section section--dark">
    <div class="container">
""" + shead("What we deliver", "Building it, then keeping it producing",
            "One contract for the build. One for everything after it.", kv="eyebrow--dark") + """
      <div class="grid g-2">
        <article class="card card--dark" data-reveal>
          <span class="card__icon">%s</span>
          <h3 class="h-3">Solar PV EPC</h3>
          <p>Everything under one contract: yield modelling, electrical design, installation, grid or hybrid integration, then commissioning.</p>
          <ul class="card__list">
            <li>Load audit and yield modelling</li>
            <li>Array, inverter and storage sizing</li>
            <li>Structural mounting and cabling</li>
            <li>Commissioning and training</li>
          </ul>
        </article>
        <article class="card card--dark" data-reveal>
          <span class="card__icon">%s</span>
          <h3 class="h-3">Operations and maintenance</h3>
          <p>The part most installers skip. Panels get dirty, strings drift and batteries age, so servicing is what keeps output up.</p>
          <ul class="card__list">
            <li>Scheduled cleaning and checks</li>
            <li>Performance monitoring</li>
            <li>Inverter and battery health checks</li>
            <li>Fault response and spares</li>
          </ul>
        </article>
      </div>
    </div>
  </section>

  <section class="section section--white">
    <div class="container">
""" % (duo("solar-panel", "i-lg"), duo("wrench", "i-lg")) + shead(
  "Who we power", "Three markets, the same engineering") + """
      <div class="rows">
"""
for i, (t, p) in enumerate([
  ("Homes", "Bring the bill down and ride out load shedding without a generator, with the alarm, gate motor and cameras still live."),
  ("Businesses", "Offices, shops, warehousing and light industry. Lower running costs, and trading hours that survive a grid interruption."),
  ("Power plants", "Utility scale Solar PV as a full EPC package, with a maintenance contract that holds performance to the model."),
], 1):
    solar += """        <a class="row" href="contact.html" data-reveal>
          <span class="row__n num">%02d</span>
          <span class="row__body"><h3>%s</h3><p>%s</p></span>
          <span class="row__go" aria-hidden="true">%s</span>
        </a>
""" % (i, t, p, ARROW)

solar += """      </div>
    </div>
  </section>

  <section class="section section--cream">
    <div class="container">
""" + shead("Renewable energy division", "Talk to the solar team directly") + """
      <div class="grid g-2">
        <div class="office" data-reveal>
          <h3>Sunway City</h3>
          <p>870 Marula Road, Sunway City, Harare</p>
          <a href="tel:+263783248006" class="num">+263 783 248 006</a>
          <a href="tel:+263242006157" class="num">+263 24 200 6157</a>
          <a href="mailto:info@sentinel.co.zw">info@sentinel.co.zw</a>
        </div>
        <div class="office" data-reveal>
          <h3>Head office, Eastlea</h3>
          <p>38 Northampton Crescent, Eastlea, Harare</p>
          <a href="tel:+263773589461" class="num">+263 773 589 461</a>
          <a href="tel:+263772568361" class="num">+263 772 568 361</a>
          <a href="mailto:info@sentinel.co.zw">info@sentinel.co.zw</a>
        </div>
      </div>
    </div>
  </section>
"""

write("renewable-energy.html",
      "Renewable Energy: Solar PV in Zimbabwe | Sentinel Security Technology",
      "Solar PV engineering, procurement and construction, plus operations and maintenance, for homes, businesses and power plants in Zimbabwe.",
      solar)


# ================================================================= CONTACT
contact = phero("Contact", "Tell us about your site",
  "A free survey and risk assessment, anywhere in Zimbabwe. Send the details and our "
  "technical team will come back to you.",
  "dispatch-tablet", "A technician checking a site on a tablet") + """
  <section class="section section--white">
    <div class="container contact-grid">
      <div data-reveal>
        %s
        <h2 class="h-2" style="font-size:clamp(1.7rem,2.8vw,2.3rem)">Head office</h2>

        <div class="cinfo">
          <span class="cinfo__icon">%s</span>
          <div><h3>Address</h3><p>38 Northampton Crescent,<br>Eastlea, Harare, Zimbabwe</p></div>
        </div>
        <div class="cinfo">
          <span class="cinfo__icon">%s</span>
          <div><h3>Telephone</h3>
            <a href="tel:+263773589461" class="num">+263 773 589 461</a>
            <a href="tel:+263772568361" class="num">+263 772 568 361</a>
            <a href="tel:+263242006157" class="num">+263 24 200 6157</a>
          </div>
        </div>
        <div class="cinfo">
          <span class="cinfo__icon">%s</span>
          <div><h3>Email</h3><a href="mailto:info@sentinel.co.zw">info@sentinel.co.zw</a></div>
        </div>
        <div class="cinfo">
          <span class="cinfo__icon">%s</span>
          <div><h3>Hours</h3><p class="num">Monday to Friday, 08:00 to 17:00<br><span class="accent">Support runs at any hour</span></p></div>
        </div>

        <div style="margin-top:2rem">%s</div>
      </div>

      <div class="formcard" data-reveal>
        <h2 class="h-3">Ask for a site survey</h2>
        <p class="muted" style="margin-bottom:1.75rem">Free, and no obligation.</p>

        <form data-contact-form novalidate>
          <div class="form-grid">
            <div class="field"><label for="name">Your name</label>
              <input id="name" name="name" type="text" autocomplete="name" placeholder="Tendai Moyo" required></div>
            <div class="field"><label for="company">Company</label>
              <input id="company" name="company" type="text" autocomplete="organization" placeholder="Optional"></div>
            <div class="field"><label for="email">Email</label>
              <input id="email" name="email" type="email" autocomplete="email" placeholder="you@company.co.zw" required></div>
            <div class="field"><label for="phone">Phone</label>
              <input id="phone" name="phone" type="tel" autocomplete="tel" placeholder="+263 77 000 0000"></div>
            <div class="field"><label for="service">What do you need?</label>
              <select id="service" name="service">
                <option>CCTV surveillance</option><option>Intruder alarms</option>
                <option>Access control</option><option>Fire detection</option>
                <option>Man traps</option><option>Physical access control</option>
                <option>Solar and renewable energy</option><option>Security risk assessment</option>
                <option>Something else</option>
              </select></div>
            <div class="field"><label for="location">Site location</label>
              <input id="location" name="location" type="text" placeholder="Harare, Bulawayo, elsewhere"></div>
            <div class="field field--full"><label for="message">Tell us about the site</label>
              <textarea id="message" name="message" placeholder="Size of the property, what is already installed, and what worries you."></textarea></div>
          </div>

          <button class="pbtn pbtn--block" type="submit" style="margin-top:1.5rem">
            <span class="pbtn__label">Send enquiry</span>%s
          </button>
          <p class="form-note">This opens your email app with the details filled in. Prefer to talk? Call <a href="tel:+263773589461" class="num">+263 773 589 461</a>.</p>
          <p class="form-status" role="status"></p>
        </form>
      </div>
    </div>
  </section>

  <section class="section section--tight section--cream">
    <div class="container">
""" % (eyebrow("Get in touch"),
       duo("map-pin", "i-md"), duo("phone-call", "i-md"),
       duo("envelope-simple", "i-md"), duo("clock", "i-md"),
       pbtn("Message us on WhatsApp", "https://wa.me/263773589461", attrs=' rel="noopener"'),
       CHEV) + shead("Our locations", "Two addresses in Harare") + """
      <div class="grid g-2">
        <div class="office" data-reveal>
          <h3>Head office, Eastlea</h3>
          <p>38 Northampton Crescent, Eastlea, Harare</p>
          <a href="tel:+263242006157" class="num">+263 24 200 6157</a>
          <a href="mailto:info@sentinel.co.zw">info@sentinel.co.zw</a>
        </div>
        <div class="office" data-reveal>
          <h3>Renewable energy, Sunway City</h3>
          <p>870 Marula Road, Sunway City, Harare</p>
          <a href="tel:+263783248006" class="num">+263 783 248 006</a>
          <a href="mailto:info@sentinel.co.zw">info@sentinel.co.zw</a>
        </div>
      </div>
    </div>
  </section>

  <section class="map-wrap" aria-label="Map of our head office">
    <div class="map-wrap__fallback" aria-hidden="true">
      <strong>38 Northampton Crescent, Eastlea</strong>
      <span>Harare, Zimbabwe</span>
      <a href="https://www.google.com/maps/search/?api=1&amp;query=38+Northampton+Crescent%2C+Eastlea%2C+Harare%2C+Zimbabwe" rel="noopener">Open in Google Maps</a>
    </div>
    <iframe class="map-embed"
      src="https://www.google.com/maps?q=38%20Northampton%20Crescent%2C%20Eastlea%2C%20Harare%2C%20Zimbabwe&output=embed"
      title="Map showing 38 Northampton Crescent, Eastlea, Harare"
      loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
  </section>
"""

write("contact.html",
      "Contact: Book a Free Site Survey | Sentinel Security Technology",
      "Contact Sentinel Security Technology in Harare, Zimbabwe. Free site survey and security risk assessment. Call +263 773 589 461 or email info@sentinel.co.zw.",
      contact, cta=False)


# ================================================================= PRIVACY
privacy = phero("Privacy policy", "Privacy policy",
  "How Sentinel Security Technology handles the information you share with us.") + """
  <section class="section section--white">
    <div class="container container--narrow prose">
      <p><em>Last updated: September 2026.</em></p>

      <h2>Who we are</h2>
      <p>Sentinel Security Technology is a security solutions provider registered in Zimbabwe, with
      its head office at 38 Northampton Crescent, Eastlea, Harare. If you have a question about this
      policy, write to us at <a href="mailto:info@sentinel.co.zw">info@sentinel.co.zw</a>.</p>

      <h2>What we collect</h2>
      <ul>
        <li>The contact details you send through our enquiry form: name, company, email, telephone number and site location.</li>
        <li>The content of your enquiry, including anything you tell us about the site you want secured.</li>
        <li>Basic technical information your browser sends when you visit this website, such as page requests and approximate location.</li>
      </ul>

      <h2>How we use it</h2>
      <ul>
        <li>To answer your enquiry and arrange a site survey.</li>
        <li>To prepare a specification and a quotation.</li>
        <li>To provide support and maintenance if you become a client.</li>
        <li>To meet our legal and contractual obligations.</li>
      </ul>

      <h2>Information about your premises</h2>
      <p>Anything you tell us about your premises, your existing security arrangements or your
      vulnerabilities is treated as confidential. Access is limited to the members of our team who
      need it to deliver your project, and we do not pass it to third parties except where the law
      requires it.</p>

      <h2>Sharing</h2>
      <p>We do not sell your information. We share it only with suppliers and subcontractors working
      on your project, and only as far as they need it to do the work.</p>

      <h2>Retention</h2>
      <p>Enquiry records are kept for as long as we need them to respond and to meet legal
      obligations. Project and maintenance records are kept for the life of the contract and a
      reasonable period afterwards.</p>

      <h2>Your choices</h2>
      <p>You can ask us to correct or delete what we hold about you, or to stop contacting you, by
      writing to <a href="mailto:info@sentinel.co.zw">info@sentinel.co.zw</a>.</p>

      <h2>Cookies and third party content</h2>
      <p>This website loads an embedded Google map on the contact page. Google may set cookies or
      receive your IP address under its own privacy terms. Fonts and icons are served from this site
      rather than from a third party.</p>

      <h2>Changes</h2>
      <p>We may update this policy from time to time. The date at the top of the page shows when it
      was last revised.</p>
    </div>
  </section>
"""

write("privacy.html",
      "Privacy Policy | Sentinel Security Technology",
      "How Sentinel Security Technology collects, uses and protects the information you share with us.",
      privacy, cta=False)

print("done")
