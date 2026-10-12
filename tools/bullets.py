# -*- coding: utf-8 -*-
"""An icon for every line item, chosen for what the line actually says.

A list of capabilities marked with repeated chevrons or repeated squares tells
the reader nothing: the same shape against nine different sentences is noise
with a job title. These lists are the specification of what Sentinel installs,
so each line gets the glyph for the thing itself - a dome camera against the
cameras, a beam sensor against the beams, a boom against the booms.

Two sources, in this order:

  si:   the Sentinel set in icons.py, drawn for this hardware. Preferred,
        because nobody else has a glyph for a man trap or a speed gate.
  ph:   Phosphor, for the generic half of the vocabulary - a lorry, a
        calendar, a graduation cap.

Matching is by the exact line first, then by keyword, longest phrase first so
"access control" is read before "access". The build asserts that every line
resolved: a line that fell through to a default is a line nobody chose an icon
for, and that is the failure this module exists to prevent.

Repeats within one list are avoided; repeats across lists are deliberate. The
same glyph against "Integration with CCTV" on one page and "CCTV surveillance
systems" on another is the site keeping its word for a thing.
"""

# ---------------------------------------------------------------- exact lines
# Keyed on the line as written. Kept in page order so a list can be read down
# the file the way it is read down the page.
LINES = {

    # ---- Circuitron: security systems ----------------------------------
    "CCTV surveillance systems":              "si:cam-dome",
    "Intruder and alarm systems":             "si:alarm-panel",
    "Electric fencing":                       "si:electric-fence",
    "Video intercoms":                        "si:intercom",
    "Security system integration":            "ph:plugs-connected",
    "Monitoring and maintenance":             "si:video-wall",

    # ---- Circuitron: communication -------------------------------------
    "Two way radios":                         "si:radio",
    "Radio communication systems":            "ph:broadcast",
    "Networking equipment":                   "si:network-rack",
    "Wireless communication solutions":       "ph:wifi-high",
    "Structured cabling":                     "si:cabling",
    "Satellite and radio links":              "si:dish",

    # ---- Circuitron: automation ----------------------------------------
    "Automated gate motors":                  "si:gate-motor",
    "Smart locks":                            "ph:lock-key",
    "Smart lighting":                         "ph:lightbulb",
    "Smart switches and sensors":             "si:smart-switch",
    "Home automation":                        "si:smart-home",
    "Smart security solutions":               "ph:shield-check",
    "Integrated building technologies":       "ph:buildings",

    # ---- Circuitron: technology and electronics ------------------------
    "Computers and laptops":                  "ph:laptop",
    "Printers and peripherals":               "ph:printer",
    "Networking hardware":                    "si:network-rack",
    "Power and backup solutions":             "si:inverter",
    "Electronic equipment":                   "ph:cpu",
    "Technology accessories":                 "ph:usb",

    # ---- CircuitStore ---------------------------------------------------
    "Online and physical retail":             "si:storefront",
    "Product discovery and ordering":         "si:cart",
    "Payment and delivery":                   "ph:truck",
    "After sales support":                    "ph:headset",

    # ---- EcoCircuit -----------------------------------------------------
    "Collection and decommissioning":         "ph:package",
    "Sorting and refurbishment":              "ph:funnel",
    "Material recovery":                      "ph:scales",
    "Responsible recycling":                  "ph:recycle",

    # ---- Renewable energy ----------------------------------------------
    "Load audit and yield modelling":         "ph:chart-line-up",
    "Array, inverter and storage sizing":     "si:solar",
    "Structural mounting and cabling":        "si:cabling",
    "Commissioning and training":             "ph:graduation-cap",
    "Scheduled cleaning and checks":          "ph:calendar-check",
    "Performance monitoring":                 "ph:gauge",
    "Inverter and battery health checks":     "ph:battery-charging",
    "Fault response and spares":              "ph:wrench",

    # ---- Guarding: manned ----------------------------------------------
    "Round the clock guarding":               "si:guard",
    "Access and egress control":              "si:access-reader",
    "Residential and estate posts":           "ph:house-line",
    "Commercial and industrial sites":        "ph:factory",
    "Incident response":                      "si:siren",
    "Supervision and site visits":            "ph:clipboard-text",

    # ---- Guarding: events ----------------------------------------------
    "Access control and screening":           "ph:scan-smiley",
    "Crowd management":                       "ph:users-three",
    "VIP protection":                         "si:guard",
    "Emergency response":                     "si:patrol",
    "Radio coordinated teams":                "si:radio",

    # ---- Guarding: alarm monitoring and response ------------------------
    "24 hour alarm monitoring":               "si:control-room",
    "Rapid armed response":                   "ph:lightning",
    "Real time breach detection":             "si:motion-sensor",
    "Patrol vehicles":                        "si:patrol",
    "Escalation to the control room":         "ph:phone-call",

    # ---- Guarding: dog units -------------------------------------------
    "Patrol dog teams":                       "si:k9",
    "Site and yard patrols":                  "si:perimeter",
    "Night deployments":                      "ph:moon-stars",
    "Handler training":                       "ph:graduation-cap",
    "Support to static posts":                "ph:handshake",

    # ---- Guarding: perimeter -------------------------------------------
    "Layered perimeter design":               "si:perimeter",
    "Integration with CCTV":                  "si:cam-bullet",
    "Integration with intruder detection":    "si:motion-sensor",
    "Integration with access control":        "si:access-reader",
    "Delay and response planning":            "ph:clock-countdown",

    # ---- Guarding: investigations ---------------------------------------
    "Incident investigation":                 "si:investigate",
    "Loss and shrinkage enquiries":           "ph:trend-down",
    "Security audits":                        "ph:clipboard-text",
    "Policy implementation":                  "ph:file-text",
    "Staff vetting support":                  "ph:identification-badge",

    # ---- Services: residential ------------------------------------------
    "Intruder alarm on call day and night":   "si:alarm-panel",
    "CCTV you can check from your phone":     "ph:device-mobile-camera",
    "Electric gate motors":                   "si:gate-motor",
    "Driveway lighting":                      "ph:lightbulb",

    # ---- Services: commercial -------------------------------------------
    "Security design and installation":       "ph:compass-tool",
    "Biometric and card access control":      "si:biometric",
    "Turnstiles and boom gates":              "si:turnstile",
    "Systems talking to each other":          "ph:plugs-connected",

    # ---- Services: industrial -------------------------------------------
    "Video management systems":               "si:video-wall",
    "Number plate readers":                   "ph:scan",
    "Gate automation and parking":            "si:boom-gate",
    "Health monitoring on devices":           "ph:pulse",

    # ---- Services: cameras ----------------------------------------------
    "IP and analogue cameras":                "si:cam-bullet",
    "Remote viewing from anywhere":           "ph:device-mobile-camera",
    "Recording and playback":                 "si:nvr",
    "Camera upgrades on an existing cable run": "si:cabling",
    "Optics that work after dark":            "ph:moon-stars",

    # ---- Services: intruder detection ------------------------------------
    "Motion sensors and perimeter beams":     "si:motion-sensor",
    "Door and window contacts":               "si:door-contact",
    "Panic and duress buttons":               "si:panic-button",
    "Zones you can arm separately":           "si:alarm-panel",
    "Battery backup through an outage":       "ph:battery-charging",

    # ---- Services: access control ----------------------------------------
    "Biometric, card and PIN readers":        "si:biometric",
    "Door controllers and interlocks":        "si:access-reader",
    "Man traps for cash areas and strongrooms": "ph:vault",
    "Visitor management and temporary codes": "ph:identification-badge",
    "Time and attendance integration":        "ph:clock",

    # ---- Services: gates and barriers ------------------------------------
    "Automatic gates and gate motors":        "si:gate-motor",
    "Boom gates and road blockers":           "si:boom-gate",
    "Turnstiles and pedestrian lanes":        "si:turnstile",
    "Safety sensors and remote access":       "si:motion-sensor",
    "Number plate driven entry":              "ph:scan",

    # ---- Services: intercoms ----------------------------------------------
    "Audio and video door stations":          "si:intercom",
    "Residential and estate intercoms":       "ph:house-line",
    "Commercial entry systems":               "ph:buildings",
    "Visitor identification":                 "ph:scan-smiley",
    "Wired to the access control system":     "si:cabling",

    # ---- Services: fire ----------------------------------------------------
    "Addressable and conventional panels":    "si:alarm-panel",
    "Smoke, heat and flame detection":        "si:fire-detect",
    "Sounders and evacuation systems":        "si:siren",
    "Electric fencing and perimeter beams":   "si:electric-fence",
    "Testing and certification on a schedule": "ph:calendar-check",
}


# ------------------------------------------------------------------ keywords
# The safety net, for copy written after this table. Longest phrase first, so
# "access control" wins over "access" and "gate motor" over "gate".
KEYWORDS = [
    ("number plate",      "ph:scan"),
    ("access control",    "si:access-reader"),
    ("electric fenc",     "si:electric-fence"),
    ("gate motor",        "si:gate-motor"),
    ("boom gate",         "si:boom-gate"),
    ("control room",      "si:control-room"),
    ("home automation",   "si:smart-home"),
    ("smart switch",      "si:smart-switch"),
    ("structured cabl",   "si:cabling"),
    ("dog",               "si:k9"),
    ("turnstile",         "si:turnstile"),
    ("intercom",          "si:intercom"),
    ("biometric",         "si:biometric"),
    ("perimeter",         "si:perimeter"),
    ("patrol",            "si:patrol"),
    ("investigat",        "si:investigate"),
    ("recycl",            "ph:recycle"),
    ("solar",             "si:solar"),
    ("inverter",          "si:inverter"),
    ("batter",            "ph:battery-charging"),
    ("network",           "si:network-rack"),
    ("cabl",              "si:cabling"),
    ("satellite",         "si:dish"),
    ("radio",             "si:radio"),
    ("camera",            "si:cam-bullet"),
    ("cctv",              "si:cam-dome"),
    ("alarm",             "si:alarm-panel"),
    ("fire",              "si:fire-detect"),
    ("smoke",             "si:fire-detect"),
    ("siren",             "si:siren"),
    ("panic",             "si:panic-button"),
    ("sensor",            "si:motion-sensor"),
    ("beam",              "si:motion-sensor"),
    ("guard",             "si:guard"),
    ("retail",            "si:storefront"),
    ("recorder",          "si:nvr"),
    ("training",          "ph:graduation-cap"),
    ("schedule",          "ph:calendar-check"),
    ("monitor",           "ph:gauge"),
    ("support",           "ph:headset"),
    ("deliver",           "ph:truck"),
]

# Phosphor glyphs this table reaches for. subset_icons.py reads this, so a
# glyph named here is a glyph in the font, and the two cannot drift apart.
PHOSPHOR = sorted({v.split(":", 1)[1] for v in
                   list(LINES.values()) + [k[1] for k in KEYWORDS]
                   if v.startswith("ph:")})

# Likewise the Sentinel glyphs, so a typo in a name is caught at build time
# rather than showing as an empty square on the page.
SENTINEL = sorted({v.split(":", 1)[1] for v in
                   list(LINES.values()) + [k[1] for k in KEYWORDS]
                   if v.startswith("si:")})

# Longest phrase first, once, rather than on every lookup.
_BY_LENGTH = sorted(KEYWORDS, key=lambda p: -len(p[0]))

_MISSED = []


def pick(text):
    """The icon for a line, as 'si:name' or 'ph:name', or None."""
    t = " ".join(text.split())
    if t in LINES:
        return LINES[t]
    low = t.lower()
    for phrase, which in _BY_LENGTH:
        if phrase in low:
            return which
    _MISSED.append(t)
    return None


def missed():
    """Lines that found no icon. The build refuses to ship a non-empty list."""
    return list(_MISSED)
