# -*- coding: utf-8 -*-
"""The shape of the Sentinel group, and the content that fills it.

This is the single source of truth for the structure the Operations Director
drew: one parent with three operating companies under it, and divisions under
those. Everything on the site that describes a company reads from here, so the
structure can only be described one way.

Sources: the Sentinel Integrated Technologies brochure, the Sentinel Security
Services company profile (2026) and the Circuitron Systems company profile.
"""

PARENT = {
    "name": "Sentinel",
    "role": "The group",
    "line": "One holding company, three operating businesses, one standard of work.",
    "href": "group.html",
}

COMPANIES = [
    # ------------------------------------------------------ 1. technologies
    {
        "id": "technologies",
        "href": "services.html",
        "name": "Sentinel Integrated Technologies",
        "short": "Integrated Technologies",
        "legal": "Sentinel Integrated Technologies (PVT) Ltd",
        "role": "Electronic security technology",
        "headline": "The systems that watch the site",
        "blurb": "Cameras, alarms, readers, gates and detectors, specified for one "
                 "property and commissioned as one system. Our own technicians do "
                 "the work and stay on to service it.",
        "icon": "cam-dome",
        # Lockups are different shapes, so each carries the height that makes
        # its wordmark sit at the same optical size as the others.
        "logo": "assets/img/brand/sentinel-logo.svg",
        "logo_wh": (1328, 568),
        "logo_white": "assets/img/brand/sentinel-logo-white.svg",
        "logo_small": "assets/img/brand/sentinel-logo-compact.svg",
        "logo_small_white": "assets/img/brand/sentinel-logo-compact-white.svg",
        "logo_h": 50,
        "strap": "towards a #secure world",
        "line": "Designs, installs and maintains the electronic systems that watch a "
                "site: cameras, alarms, access, fire and the gates between them.",
        "lead": "Integrated security for homes, businesses and institutions. We design, "
                "install, integrate and maintain systems that work together rather "
                "than operate in isolation.",
        "chips": ["CCTV", "Alarms", "Access control", "Fire"],
        "divisions": [
            {
                "id": "cctv",
                "icon": "cam-bullet",
                "name": "CCTV and video surveillance",
                "line": "Cameras chosen for the light they will actually face, and a "
                        "recorder sized for the footage you need to keep.",
                "items": ["IP and analogue CCTV systems", "Remote viewing",
                          "Recording and playback", "Camera upgrades",
                          "Video monitoring", "Commercial and residential installations"],
            },
            {
                "id": "alarms",
                "icon": "alarm-panel",
                "name": "Intruder and alarm systems",
                "line": "Detection layered so a breach is caught at the fence, the "
                        "door and the room, not only at the last one.",
                "items": ["Intruder detection", "Alarm systems", "Motion sensors",
                          "Door and window sensors", "Panic buttons", "Alarm integration"],
            },
            {
                "id": "access",
                "icon": "access-reader",
                "name": "Access control",
                "line": "Who may pass, when, and a record of it afterwards. Readers "
                        "that survive dust, heat and a thousand hands a day.",
                "items": ["Biometric access", "Card and proximity systems",
                          "Door controllers", "Mantrap systems", "Visitor management",
                          "Time and attendance integration"],
            },
            {
                "id": "gates",
                "icon": "gate-motor",
                "name": "Gate automation",
                "line": "The gate is the first thing a site is judged on and the first "
                        "thing that fails. We fit motors rated for your traffic.",
                "items": ["Automatic gates", "Gate motors", "Remote access",
                          "Safety sensors", "Intercom integration"],
            },
            {
                "id": "intercoms",
                "icon": "intercom",
                "name": "Video intercoms",
                "line": "See who is at the gate before you open it, from the house, "
                        "the office or a phone anywhere.",
                "items": ["Audio and video communication", "Residential intercoms",
                          "Commercial entry systems", "Visitor identification",
                          "Integration with access control"],
            },
            {
                "id": "fire",
                "icon": "fire-detect",
                "name": "Fire detection and perimeter",
                "line": "Smoke and heat picked up early, and an energised perimeter "
                        "that holds the line while help is on the way.",
                "items": ["Fire detection and alarm", "Electric fencing",
                          "Perimeter protection", "Monitoring", "Technical support",
                          "Security system integration"],
            },
        ],
        "sectors": ["Corporate and commercial", "Residential",
                    "Construction and projects", "Healthcare"],
        "process": ["Assess", "Design", "Install", "Integrate", "Monitor", "Maintain"],
    },

    # --------------------------------------------------------- 2. guarding
    {
        "id": "guarding",
        "href": "security-services.html",
        "name": "Sentinel Security Services",
        "short": "Security Services",
        "legal": "Sentinel Security Services",
        "role": "Security operations",
        "headline": "The people who hold the ground",
        "blurb": "Officers, handlers and response crews, supervised on a schedule "
                 "and answerable to a control room that is staffed at every hour "
                 "of every day.",
        "icon": "guard",
        "logo": "assets/img/brand/sentinel-security-services.svg",
        "logo_wh": (1702, 568),
        "logo_white": "assets/img/brand/sentinel-security-services-white.svg",
        "logo_h": 50,
        "strap": "people, dogs and response",
        "line": "Puts trained officers, handlers and response teams on the ground, "
                "across all ten provinces.",
        "lead": "Security operations since 2016. Officers, dog units and armed "
                "response, backed by a control room that answers at three in the "
                "morning as readily as at three in the afternoon.",
        "chips": ["Guarding", "Dog units", "Response", "Investigations"],
        "divisions": [
            {
                "id": "manned",
                "icon": "guard",
                "name": "Manned guarding",
                "line": "Officers trained past the basics, posted to protect premises, "
                        "assets and the people inside them, around the clock.",
                "items": ["Round the clock guarding", "Access and egress control",
                          "Residential and estate posts", "Commercial and industrial sites",
                          "Incident response", "Supervision and site visits"],
            },
            {
                "id": "events",
                "icon": "radio",
                "name": "Event security",
                "line": "Order and safety at an event of any size, so the thing you "
                        "planned is the thing people remember.",
                "items": ["Access control and screening", "Crowd management",
                          "VIP protection", "Emergency response",
                          "Radio coordinated teams"],
            },
            {
                "id": "response",
                "icon": "patrol",
                "name": "Alarm monitoring and response",
                "line": "Breaches picked up in real time and a response team moving "
                        "before you have finished the call.",
                "items": ["24 hour alarm monitoring", "Rapid armed response",
                          "Real time breach detection", "Patrol vehicles",
                          "Escalation to the control room"],
            },
            {
                "id": "k9",
                "icon": "k9",
                "name": "Dog units",
                "line": "A handler and a trained dog cover ground that cameras cannot, "
                        "and deter what cameras only record.",
                "items": ["Patrol dog teams", "Site and yard patrols",
                          "Night deployments", "Handler training",
                          "Support to static posts"],
            },
            {
                "id": "perimeter",
                "icon": "perimeter",
                "name": "Perimeter protection",
                "line": "Once the first line is breached the whole facility is "
                        "compromised, so we build several lines, not one.",
                "items": ["Layered perimeter design", "Integration with CCTV",
                          "Integration with intruder detection",
                          "Integration with access control", "Delay and response planning"],
            },
            {
                "id": "investigations",
                "icon": "investigate",
                "name": "Investigations",
                "line": "Led by officers who spent careers in the Criminal "
                        "Investigations Department before they came to us.",
                "items": ["Incident investigation", "Loss and shrinkage enquiries",
                          "Security audits", "Policy implementation",
                          "Staff vetting support"],
            },
        ],
        "sectors": ["Corporations", "Private sector", "Residential",
                    "Educational institutions", "Functions and events",
                    "Farms and mining"],
        "process": ["Risk survey", "Deploy", "Supervise", "Report", "Review"],
    },

    # ------------------------------------------------------- 3. circuitron
    {
        "id": "circuitron",
        "href": "circuitron.html",
        "name": "Circuitron Systems",
        "short": "Circuitron Systems",
        "legal": "Circuitron Systems (Private) Limited",
        "role": "Technology and systems",
        "headline": "The technology business, standing on its own",
        "blurb": "Communications, automation, electronics and power, sold and "
                 "supported as products in their own right, with a shop and a "
                 "recycling route attached.",
        "icon": "network-rack",
        "logo": "assets/img/brand/circuitron-logo.png",
        "logo_wh": (531, 169),
        "logo_white": "assets/img/brand/circuitron-logo.png",
        "logo_h": 34,
        "strap": "Secure. Connect. Power.",
        "line": "Carries the technology business on its own: communications, "
                "automation, electronics, retail and electronic waste recovery.",
        "lead": "A Zimbabwean technology and systems company built out of more than a "
                "decade of security work. Engineering security, powering "
                "connectivity, building tomorrow.",
        "chips": ["Communications", "Automation", "Electronics", "Retail"],
        "divisions": [
            {
                "id": "security-systems",
                "icon": "cam-dome",
                "name": "Security systems",
                "line": "The same discipline the group was built on, sold and "
                        "installed as a technology product in its own right.",
                "items": ["CCTV surveillance systems", "Intruder and alarm systems",
                          "Electric fencing", "Video intercoms",
                          "Security system integration", "Monitoring and maintenance"],
            },
            {
                "id": "communications",
                "icon": "radio",
                "name": "Communication and connectivity",
                "line": "Radios that reach across a farm and networks that hold up "
                        "when the power does not.",
                "items": ["Two way radios", "Radio communication systems",
                          "Networking equipment", "Wireless communication solutions",
                          "Structured cabling", "Satellite and radio links"],
            },
            {
                "id": "automation",
                "icon": "smart-home",
                "name": "Automation and smart technology",
                "line": "Buildings that do the obvious things by themselves: lights, "
                        "locks, gates, sensors, all under one app.",
                "items": ["Automated gate motors", "Smart locks", "Smart lighting",
                          "Smart switches and sensors", "Home automation",
                          "Smart security solutions", "Integrated building technologies"],
            },
            {
                "id": "electronics",
                "icon": "inverter",
                "name": "Technology and electronics",
                "line": "Computers, printers, network hardware and the power to keep "
                        "them running through a cut.",
                "items": ["Computers and laptops", "Printers and peripherals",
                          "Networking hardware", "Power and backup solutions",
                          "Electronic equipment", "Technology accessories"],
            },
        ],
        "units": [
            {
                "id": "circuitstore",
                "icon": "cart",
                "name": "CircuitStore",
                "strap": "Connect. Shop. Innovate.",
                "line": "The retail arm. Security kit, electronics, radios, "
                        "networking and computers, online and in store, with the "
                        "support that follows a sale.",
                "items": ["Online and physical retail", "Product discovery and ordering",
                          "Payment and delivery", "After sales support"],
            },
            {
                "id": "ecocircuit",
                "icon": "e-waste",
                "name": "EcoCircuit",
                "strap": "Recover. Refurbish. Recycle.",
                "line": "The sustainability arm. Zimbabwe has little formal route "
                        "for old electronics, so we built one: collect, refurbish "
                        "what can be saved, recover the rest.",
                "items": ["Collection and decommissioning", "Sorting and refurbishment",
                          "Material recovery", "Responsible recycling"],
            },
        ],
        "sectors": ["Households", "Businesses", "Institutions", "Consumer market"],
        "process": ["Understand", "Select", "Integrate", "Support"],
    },
]


def by_id(cid):
    for c in COMPANIES:
        if c["id"] == cid:
            return c
    raise KeyError(cid)


# ------------------------------------------------------------- shared facts
BRANDS = [
    ("Cathexis", "Video management"),
    ("Hikvision", "Cameras and recorders"),
    ("Dahua", "Cameras and recorders"),
    ("Gallagher", "Perimeter and access"),
    ("ZKTeco", "Biometrics and time"),
    ("Suprema", "Biometric readers"),
    ("Centurion", "Gate automation"),
    ("BoomGate Systems", "Vehicle barriers"),
    ("IDS", "Alarm panels"),
    ("Jablotron", "Wireless alarms"),
]

LEADERS = [
    {
        "name": "Sheila Nhambure",
        "role": "Managing Director",
        "icon": "control-room",
        "line": "Fifteen years in customer service, sales and distribution, with a "
                "track record in key account management and territory growth.",
        "quals": ["Executive MBA, Africa University",
                  "BSc Management Information Systems, Midlands State University",
                  "BSc Marketing Communications, IMM",
                  "Reading towards CISSP"],
    },
    {
        "name": "Samuel Nhuta",
        "role": "Operations Director",
        "icon": "investigate",
        "line": "Twenty one years in the Zimbabwe Republic Police, nine of them in "
                "the Criminal Investigations Department's commercial crimes "
                "division, and thirteen in middle management as officer in charge.",
        "quals": ["MSc Peace Leadership and Conflict Management, ZOU",
                  "BSc Political Science, University of Zimbabwe",
                  "Professional Diploma in Risk and Security Management, CIRSM",
                  "Certificates in financial crimes investigation"],
    },
]

CONTACT = {
    "address": "29 Tweed Road, Eastlea, Harare",
    "phones": [("+263 77 358 9461", "+263773589461"),
               ("+263 77 256 8361", "+263772568361"),
               ("+263 24 200 6157", "+263242006157")],
    "email": "info@sentinel.co.zw",
}
