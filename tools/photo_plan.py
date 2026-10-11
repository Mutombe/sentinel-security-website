# -*- coding: utf-8 -*-
"""What every photograph on the site has to show, and where it goes.

`want` is the brief: what must be in the frame for the picture to be honest in
that slot. `queries` are what to ask Unsplash. `sizes` are the exact pixel
dimensions the markup declares, so nothing is ever scaled or letterboxed.

HERO is 1200x608, a page hero is 1200x600, a detail block is 1200x900 and a
bento tile is square.
"""

HERO = [(640, 324), (1200, 608)]
PHERO = [(640, 320), (1200, 600)]
DETAIL = [(640, 480), (1200, 900)]
TILE = [(640, 640)]
WIDE = [(640, 427), (1200, 800)]

SLOTS = [
    # ------------------------------------------------- the home page hero
    {
        "id": "hero-control-room",
        "file": "control-room-monitoring",
        "use": "Home hero, slide 1",
        "want": "A security control room from behind an operator: a wall of camera "
                "feeds, low light, screens the brightest thing in the frame.",
        "queries": ["security control room monitors", "cctv control room operator",
                    "surveillance monitoring room", "security operations centre"],
        "sizes": HERO, "crop": "entropy",
    },
    {
        "id": "hero-officers",
        "file": "security-officers",
        "use": "Home hero slide 2, bento, guarding page hero",
        "want": "Uniformed security officers, outdoors or at a post, working rather "
                "than posed. Dark uniform reads best against the scrim.",
        "queries": ["security guard uniform", "security officer building entrance",
                    "security personnel patrol", "security staff night"],
        "sizes": HERO, "crop": "faces",
    },
    {
        "id": "hero-technician",
        "file": "technician-panel",
        "use": "Home hero slide 3, contact page hero",
        "want": "A technician on site with a device: installing or commissioning "
                "something, hands visible, not a stock person smiling at a laptop.",
        "queries": ["technician installing security camera", "engineer tablet site",
                    "cctv installation technician", "electrician commissioning panel"],
        "sizes": HERO, "crop": "entropy",
    },
    {
        "id": "phero-systems",
        "file": "access-terminal",
        "use": "Security systems page hero, bento tile",
        "want": "An access control point: a reader beside a door, a turnstile or a "
                "reception barrier. Equipment in the frame, not just a lobby.",
        "queries": ["access control card reader door", "office turnstile entrance",
                    "keycard reader wall", "building entrance security barrier"],
        "sizes": PHERO, "crop": "entropy",
    },
    {
        "id": "phero-about",
        "file": "officer-on-duty",
        "use": "About page hero",
        "want": "An officer walking a perimeter or a street, seen from behind or in "
                "profile, with the property in shot.",
        "queries": ["security guard walking patrol", "security officer perimeter walk",
                    "guard patrolling street", "security patrol back view"],
        "sizes": PHERO, "crop": "entropy",
    },
    {
        "id": "phero-circuitron",
        "file": "circuitron-bench",
        "use": "Circuitron page hero",
        "want": "Technology work: a bench with electronics, a network rack being "
                "patched, or circuit boards being handled.",
        "queries": ["network rack patch cables", "electronics repair bench",
                    "server room technician", "circuit board repair hands"],
        "sizes": PHERO, "crop": "entropy",
    },

    # -------------------------------------------- the six security systems
    {
        "id": "sys-cctv",
        "file": "sys-cctv",
        "use": "services.html #cctv",
        "want": "A real CCTV camera on a building or a pole, close enough to see it "
                "is a camera. Dome or bullet, outdoors.",
        "queries": ["cctv camera building wall", "surveillance camera outdoor",
                    "security camera mounted pole", "dome camera ceiling"],
        "sizes": DETAIL, "crop": "entropy",
    },
    {
        "id": "sys-alarms",
        "file": "sys-alarms",
        "use": "services.html #alarms",
        "want": "An alarm keypad or control panel on a wall, or a motion sensor in a "
                "corner. The hardware, not an abstract.",
        "queries": ["alarm keypad wall", "home security alarm panel",
                    "burglar alarm control panel", "motion sensor wall corner"],
        "sizes": DETAIL, "crop": "entropy",
    },
    {
        "id": "sys-access",
        "file": "sys-access",
        "use": "services.html #access",
        "want": "A reader being used: a hand presenting a card or a finger on a "
                "biometric scanner at a door.",
        "queries": ["fingerprint scanner door access", "hand access card reader",
                    "biometric reader office door", "keycard access hand"],
        "sizes": DETAIL, "crop": "entropy",
    },
    {
        "id": "sys-gates",
        "file": "sys-gates",
        "use": "services.html #gates",
        "want": "An automatic gate or a boom barrier at a vehicle entrance, "
                "preferably mid travel.",
        "queries": ["automatic gate entrance driveway", "boom barrier car park",
                    "sliding gate motor", "vehicle barrier entrance security"],
        "sizes": DETAIL, "crop": "entropy",
    },
    {
        "id": "sys-intercom",
        "file": "sys-intercom",
        "use": "services.html #intercoms",
        "want": "A video door station or intercom panel at a gate or a front door, "
                "with the button and camera visible.",
        "queries": ["video intercom door station", "video doorbell entrance",
                    "intercom panel gate", "door entry phone panel"],
        "sizes": DETAIL, "crop": "entropy",
    },
    {
        "id": "sys-fire",
        "file": "sys-fire",
        "use": "services.html #fire",
        "want": "A smoke detector on a ceiling, a fire alarm call point, or a "
                "detection panel. Clearly life safety equipment.",
        "queries": ["smoke detector ceiling", "fire alarm call point wall",
                    "fire detection panel", "sprinkler smoke alarm ceiling"],
        "sizes": DETAIL, "crop": "entropy",
    },

    # ------------------------------------------- square crops for the bento
    {
        "id": "tile-access",
        "file": "tile-access",
        "use": "Home page bento, square tile",
        "want": "The same access terminal, cropped square.",
        "queries": ["access control card reader door"],
        "sizes": TILE, "crop": "entropy",
    },
    {
        "id": "tile-night",
        "file": "tile-night",
        "use": "About page bento, square tile",
        "want": "The same night monitoring desk, cropped square.",
        "queries": ["night shift control room"],
        "sizes": TILE, "crop": "entropy",
    },

    # ------------------------------------------------- guarding operations
    {
        "id": "ops-k9",
        "file": "k9-handler-standing",
        "use": "Guarding page, dog units",
        "want": "A working dog with a handler, on lead, outdoors. A German shepherd "
                "or malinois in a working context rather than a pet portrait.",
        "queries": ["police dog handler", "german shepherd working dog handler",
                    "security dog patrol", "k9 unit dog lead"],
        "sizes": WIDE, "crop": "entropy",
    },
    {
        "id": "ops-patrol",
        "file": "response-night",
        "use": "Guarding page, response",
        "want": "A marked response vehicle, or officers arriving at a site. Movement, "
                "night or dusk preferred.",
        "queries": ["security patrol vehicle night", "security response car",
                    "patrol car headlights night", "security van site"],
        "sizes": WIDE, "crop": "entropy",
    },
    {
        "id": "ops-radio",
        "file": "officer-radio",
        "use": "Guarding page, events and reception",
        "want": "A two way radio in use, or an officer at a reception or event "
                "checkpoint with a radio on the shoulder.",
        "queries": ["security guard two way radio", "walkie talkie security hand",
                    "event security staff radio", "reception security desk"],
        "sizes": WIDE, "crop": "entropy",
    },
    {
        "id": "ops-checkpoint",
        "file": "vehicle-checkpoint",
        "use": "Guarding page, perimeter and vehicle control",
        "want": "A vehicle checkpoint: a car at a gate being checked, or a guard at "
                "a boom with a clipboard.",
        "queries": ["vehicle checkpoint security guard", "car entrance gate guard",
                    "security checkpoint barrier car", "guard inspecting vehicle"],
        "sizes": WIDE, "crop": "entropy",
    },

    # ------------------------------------------------ circuitron and power
    {
        "id": "tech-network",
        "file": "tech-network",
        "use": "Circuitron, communications and connectivity",
        "want": "A network rack or a patch panel with cabling, or a radio mast. "
                "Infrastructure, clearly.",
        "queries": ["network patch panel cables", "server rack data centre",
                    "structured cabling rack", "radio antenna mast tower"],
        "sizes": WIDE, "crop": "entropy",
    },
    {
        "id": "tech-smart",
        "file": "tech-smart",
        "use": "Circuitron, automation and smart technology",
        "want": "A smart home control: a wall panel, a phone controlling a light or "
                "a lock, inside a real room.",
        "queries": ["smart home control panel wall", "smart home app phone lights",
                    "smart lock door phone", "home automation touch panel"],
        "sizes": WIDE, "crop": "entropy",
    },
    {
        "id": "tech-retail",
        "file": "tech-retail",
        "use": "Circuitron, CircuitStore",
        "want": "An electronics or technology shop interior: shelves of devices, a "
                "counter, a customer being served.",
        "queries": ["electronics store shelves", "computer shop interior",
                    "technology store counter", "electronics retail display"],
        "sizes": WIDE, "crop": "entropy",
    },
    {
        "id": "tech-ewaste",
        "file": "tech-ewaste",
        "use": "Circuitron, EcoCircuit",
        "want": "Electronic waste being handled: stacked boards, stripped cable, "
                "sorted components. Recovery rather than a landfill.",
        "queries": ["electronic waste circuit boards", "e waste recycling computers",
                    "old electronics sorting recycling", "copper cable recycling scrap"],
        "sizes": WIDE, "crop": "entropy",
    },
    {
        "id": "power-solar",
        "file": "power-solar",
        "use": "Renewable energy page",
        "want": "A solar array on a roof or a ground mount, in daylight, with the "
                "panels filling most of the frame.",
        "queries": ["solar panels roof installation", "solar array sunlight",
                    "photovoltaic panels building", "solar installation technician"],
        "sizes": WIDE, "crop": "entropy",
    },
]

# The chosen Unsplash photo id per slot. Fill from the contact sheet, then run
# `python tools/photos.py fetch`.
CHOICES = {
    "hero-control-room": "TtMKq3lJm-U",
    "hero-officers": "YQ9aFeawqeo",
    "hero-technician": "GXLPLG3_Vf4",
    "phero-systems": "CqSpoJs2ehg",
    "phero-about": "WyoErwOE0Oc",
    "phero-circuitron": "PSpf_XgOM5w",
    "sys-cctv": "zBTYRFCeaS0",
    "sys-alarms": "9jBbdyp7cMw",
    "sys-access": "IhG7G2LpUEo",
    "sys-gates": "OEr69DGHRA0",
    "sys-intercom": "rekjaWhHAWk",
    "sys-fire": "Ea4OPjLDt5k",
    "ops-k9": "5q7G1zwQvtY",
    "ops-patrol": "pVH9fA_GBMw",
    "ops-radio": "mae4VNOFVQ8",
    "ops-checkpoint": "WKAC7w5Iv7M",
    "tech-network": "ohBcGYJ8brQ",
    "tech-smart": "NohN3BIkAZM",
    "tech-retail": "bKDOZ7neVl4",
    "tech-ewaste": "A7NNW7pjHOk",
    "power-solar": "eNzotIHdUsY",
    "tile-access": "CqSpoJs2ehg",
    "tile-night": "F9kaWPCi8t0"
}
