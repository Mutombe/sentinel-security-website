# -*- coding: utf-8 -*-
"""The Sentinel custom icon set.

Drawn on a 24 grid with a 1.5 stroke, round caps and round joins, to the same
discipline as the reference sheets: open line work, no fills except small
accent nodes, every shape inside a 2px margin.

Each entry is (title, body). The body is raw SVG that inherits stroke and fill
from the <symbol>, so a glyph recolours with `color` like any Phosphor icon.
Anything that must be solid says so with fill="currentColor" stroke="none".

Phosphor still covers the generic vocabulary (clock, phone, shield, handshake
and so on). This set exists for the things Phosphor has no word for: the
actual hardware Sentinel installs and the work its officers do.
"""

DOT = '<circle cx="%s" cy="%s" r="%s" fill="currentColor" stroke="none"/>'

ICONS = {

# ---------------------------------------------------------------- cameras
# ---------------------------------------------------------------- cameras
"cam-dome": ("Dome camera", """
  <path d="M2.8 5.4h18.4"/>
  <path d="M12 5.4V3.2"/>
  <rect x="4.8" y="7.6" width="14.4" height="2.6" rx="1.1"/>
  <path d="M6.2 10.2a5.8 5.8 0 0 0 11.6 0"/>
  <circle cx="12" cy="13.4" r="1.8"/>
"""),
"cam-bullet": ("Bullet camera", """
  <path d="M3.5 3.5v17"/>
  <path d="M3.5 11.6h2.4"/>
  <rect x="5.9" y="8.6" width="9.8" height="6" rx="3"/>
  <path d="M15.7 9.8 19.3 8v7.2l-3.6-1.8"/>
  <path d="M8.4 7.4h5"/>
  """ + DOT % (17.4, 11.6, 0.85)),

"nvr": ("Recorder", """
  <rect x="2.5" y="5" width="19" height="5" rx="1.5"/>
  <rect x="2.5" y="13" width="19" height="5" rx="1.5"/>
  """ + DOT % (5.6, 7.5, 0.85) + DOT % (5.6, 15.5, 0.85) + """
  <path d="M9 7.5h9"/>
  <path d="M9 15.5h9"/>
"""),

"video-wall": ("Monitoring wall", """
  <rect x="2.5" y="3.5" width="8.5" height="6.5" rx="1.2"/>
  <rect x="13" y="3.5" width="8.5" height="6.5" rx="1.2"/>
  <rect x="2.5" y="12" width="8.5" height="6.5" rx="1.2"/>
  <rect x="13" y="12" width="8.5" height="6.5" rx="1.2"/>
  <path d="M8.5 21.5h7"/>
  <path d="M12 18.5v3"/>
"""),

"control-room": ("Control room", """
  <rect x="2.6" y="2.5" width="18.8" height="9.6" rx="1.5"/>
  <path d="M5.8 5.4h5.6"/>
  <path d="M5.8 7.4h8.8"/>
  <path d="M5.8 9.4h5.6"/>
  <circle cx="12" cy="15.4" r="2.4"/>
  <path d="M6.2 21.5a5.8 5.8 0 0 1 11.6 0"/>
"""),
# ----------------------------------------------------------------- alarms
"alarm-panel": ("Alarm panel", """
  <rect x="5" y="2.5" width="14" height="19" rx="2"/>
  <rect x="7.5" y="5" width="9" height="3.5" rx="0.8"/>
  """ + DOT % (8.6, 11.8, 1) + DOT % (12, 11.8, 1) + DOT % (15.4, 11.8, 1)
      + DOT % (8.6, 15.2, 1) + DOT % (12, 15.2, 1) + DOT % (15.4, 15.2, 1)
      + DOT % (8.6, 18.6, 1) + DOT % (12, 18.6, 1) + DOT % (15.4, 18.6, 1)),

"motion-sensor": ("Motion sensor", """
  <path d="M5.6 3.8h12.8l-1.5 6.1H7.1z"/>
  <path d="M6.3 6.9h11.4"/>
  <path d="M9.4 12.2a3.4 3.4 0 0 0 5.2 0"/>
  <path d="M7.3 13.9a5.9 5.9 0 0 0 9.4 0"/>
  <path d="M5.2 15.6a8.4 8.4 0 0 0 13.6 0"/>
"""),
"door-contact": ("Door contact", """
  <path d="M3.5 3.5h7v17h-7z"/>
  <path d="M13.5 3.5h7v17h-7z"/>
  <rect x="8.2" y="9" width="2.3" height="6" rx="0.7"/>
  <rect x="13.5" y="9" width="2.3" height="6" rx="0.7"/>
  <path d="M11.3 10.5v3"/>
"""),

"panic-button": ("Panic button", """
  <circle cx="12" cy="12" r="9"/>
  <circle cx="12" cy="12" r="4.2"/>
  <path d="M12 2.2v2.4"/>
  <path d="M12 19.4v2.4"/>
  <path d="M2.2 12h2.4"/>
  <path d="M19.4 12h2.4"/>
  """ + DOT % (12, 12, 1.5)),

"siren": ("Siren", """
  <path d="M7 12.5a5 5 0 0 1 10 0v4H7z"/>
  <path d="M5.5 19.5h13"/>
  <path d="M7 16.5v3"/>
  <path d="M17 16.5v3"/>
  <path d="M12 3.2v3"/>
  <path d="M5.6 5.6 7.7 7.7"/>
  <path d="M18.4 5.6 16.3 7.7"/>
  <path d="M2.8 12h2.2"/>
  <path d="M19 12h2.2"/>
"""),

"fire-detect": ("Fire detection", """
  <circle cx="12" cy="12" r="9"/>
  <circle cx="12" cy="12" r="6.1"/>
  <path d="M12 8.1c1.7 1.6 2.6 2.9 2.6 4.2a2.6 2.6 0 0 1-5.2 0c0-.8.3-1.6 1-2.1.1.6.4 1.1.9 1.3-.3-1.1-.1-2.3.7-3.4z"/>
"""),
# --------------------------------------------------------- access control
"access-reader": ("Access control", """
  <path d="M4 2.5h11v19H4z"/>
  """ + DOT % (12.4, 12, 0.9) + """
  <rect x="17" y="7.5" width="4.5" height="9" rx="1.2"/>
  <path d="M18.2 10h2.1"/>
  <path d="M18.2 12.2h2.1"/>
  """ + DOT % (19.25, 14.5, 0.85)),

"biometric": ("Biometric access", """
  <path d="M12 2.8c-3.4 0-6.2 2.6-6.2 5.8"/>
  <path d="M18.2 8.6c0-3.2-2.8-5.8-6.2-5.8"/>
  <path d="M5.8 13.6V8.6"/>
  <path d="M18.2 8.6v3.1"/>
  <path d="M8.9 8.6a3.1 3.1 0 0 1 6.2 0v6.2"/>
  <path d="M8.9 8.6v8.4"/>
  <path d="M12 8.6v9.9"/>
  <path d="M15.1 17.8a9 9 0 0 1-.6 3"/>
  <path d="M5.9 16.8a9 9 0 0 0 1-3.2"/>
  <path d="M18.1 14.6a12 12 0 0 1-.9 5.4"/>
"""),

"turnstile": ("Speed gate", """
  <path d="M2.5 20.5h19"/>
  <rect x="3" y="8.8" width="4.8" height="11.7" rx="1.3"/>
  <rect x="16.2" y="8.8" width="4.8" height="11.7" rx="1.3"/>
  <path d="M7.8 12h3.1"/>
  <path d="M13.1 12h3.1"/>
  <path d="M12 3.4v5.4"/>
  <path d="M9.6 5.8 12 3.4l2.4 2.4"/>
  """ + DOT % (5.4, 15.6, 0.9) + DOT % (18.6, 15.6, 0.9)),
"intercom": ("Video intercom", """
  <rect x="5.5" y="2.5" width="13" height="19" rx="2"/>
  <rect x="8" y="5" width="8" height="5.5" rx="1"/>
  """ + DOT % (12, 7.75, 1.15) + """
  <path d="M9 13.5h6"/>
  <circle cx="12" cy="17.8" r="2"/>
  """ + DOT % (12, 17.8, 0.8)),

# -------------------------------------------------------------- perimeter
# -------------------------------------------------------------- perimeter
"gate-motor": ("Gate automation", """
  <path d="M2.5 20.5h19"/>
  <path d="M3.5 7.5h13v10h-13z"/>
  <path d="M3.5 11h13"/>
  <path d="M3.5 14h13"/>
  <path d="M7 7.5v10"/>
  <path d="M11 7.5v10"/>
  <rect x="18" y="12.5" width="3.5" height="5" rx="1"/>
  <path d="M19.75 12.5v-2"/>
  """ + DOT % (19.75, 15, 0.85)),

"boom-gate": ("Boom barrier", """
  <path d="M2.5 20.5h19"/>
  <rect x="3" y="11" width="4" height="9.5" rx="1.2"/>
  <path d="M7.5 9 21 5.2"/>
  <path d="M9.9 8.3l.6 2.1"/>
  <path d="M13.5 7.3l.6 2.1"/>
  <path d="M17.1 6.3l.6 2.1"/>
  """ + DOT % (5, 14.5, 0.9)),

"electric-fence": ("Electric fencing", """
  <path d="M4 3.5v17"/>
  <path d="M20 3.5v17"/>
  <path d="M4 6.2h16"/>
  <path d="M4 11h3.8"/>
  <path d="M16.2 11H20"/>
  <path d="M4 15.8h16"/>
  <path d="M4 20h16"/>
  <path d="M13.6 6.6 9.6 12.4h3.4l-2.6 5.8"/>
"""),

"perimeter": ("Perimeter protection", """
  <path d="M12 2.5 3.5 6v6c0 4.4 3.6 7.8 8.5 9.5 4.9-1.7 8.5-5.1 8.5-9.5V6z"/>
  <path d="M12 6.3 7 8.4v3.4c0 2.5 2.1 4.6 5 5.7 2.9-1.1 5-3.2 5-5.7V8.4z"/>
  """ + DOT % (12, 11.6, 1.5)),

# ------------------------------------------------ manned security and ops
"guard": ("Manned security", """
  <path d="M7 6.5h10"/>
  <path d="M8.5 6.5a3.5 3.5 0 0 1 7 0"/>
  <path d="M8.8 8.2a3.4 3.4 0 0 0 6.4 0"/>
  <path d="M12 11.6v2"/>
  <path d="M4.5 21.5v-2.8A5.2 5.2 0 0 1 9.7 13.5h4.6a5.2 5.2 0 0 1 5.2 5.2v2.8"/>
  <path d="M12 13.9v7.6"/>
  """ + DOT % (16.8, 17.5, 0.9)),

"k9": ("K9 unit", """
  <path d="M7.6 6.6 5.2 3.2 4.1 7.6"/>
  <path d="M16.4 6.6 18.8 3.2l1.1 4.4"/>
  <path d="M5.8 11a6.2 6.2 0 0 1 12.4 0v1.6a6.2 6.2 0 0 1-12.4 0z"/>
  """ + DOT % (9.5, 10.2, 1) + DOT % (14.5, 10.2, 1) + """
  <path d="M10.7 14.2h2.6L12 15.9z"/>
  <path d="M12 15.9v1.5"/>
"""),

"patrol": ("Response patrol", """
  <path d="M2.5 16.5v-3l2-4.5h15l2 4.5v3"/>
  <path d="M2.5 16.5h19"/>
  <path d="M6 9V6.5h12V9"/>
  <path d="M9 6.5V4.5h6v2"/>
  <circle cx="7" cy="17.5" r="2.2"/>
  <circle cx="17" cy="17.5" r="2.2"/>
  """ + DOT % (5, 13.2, 0.85) + DOT % (19, 13.2, 0.85)),

"radio": ("Two way radio", """
  <rect x="7" y="6.5" width="10" height="15" rx="2"/>
  <path d="M14.5 6.5V3.2"/>
  <rect x="9.3" y="9" width="5.4" height="3.2" rx="0.8"/>
  """ + DOT % (10, 15, 0.9) + DOT % (12, 15, 0.9) + DOT % (14, 15, 0.9)
      + DOT % (10, 17.6, 0.9) + DOT % (12, 17.6, 0.9) + DOT % (14, 17.6, 0.9) + """
  <path d="M17.6 2.4a5.5 5.5 0 0 1 3.9 3.9"/>
  <path d="M17.2 5.3a2.7 2.7 0 0 1 1.5 1.5"/>
"""),

"investigate": ("Investigations", """
  <path d="M5 2.5h9l4.5 4.5v6"/>
  <path d="M5 2.5v19h5"/>
  <path d="M13.5 2.5V7h5"/>
  <path d="M7.8 7.5h3.4"/>
  <path d="M7.8 11h5.2"/>
  <circle cx="15.4" cy="15.4" r="4"/>
  <path d="M18.4 18.4 21.5 21.5"/>
"""),

# --------------------------------------------- networks, power, utilities
# --------------------------------------------- networks, power, utilities
"network-rack": ("Network rack", """
  <rect x="4" y="2.5" width="16" height="19" rx="1.8"/>
  <rect x="6.5" y="5" width="11" height="3.4" rx="0.8"/>
  <rect x="6.5" y="10.3" width="11" height="3.4" rx="0.8"/>
  <rect x="6.5" y="15.6" width="11" height="3.4" rx="0.8"/>
  """ + DOT % (8.6, 6.7, 0.75) + DOT % (8.6, 12, 0.75) + DOT % (8.6, 17.3, 0.75) + """
  <path d="M11 6.7h4.4"/>
  <path d="M11 12h4.4"/>
  <path d="M11 17.3h4.4"/>
"""),

"cabling": ("Structured cabling", """
  <rect x="4.6" y="2.8" width="14.8" height="5.2" rx="1.4"/>
  <path d="M7.2 5.6v1.2"/>
  <path d="M9.6 5.6v1.2"/>
  <path d="M12 5.6v1.2"/>
  <path d="M14.4 5.6v1.2"/>
  <path d="M16.8 5.6v1.2"/>
  <path d="M12 8v3.4"/>
  <path d="M12 11.4H5.4a1.6 1.6 0 0 0-1.6 1.6v1.9"/>
  <path d="M12 11.4h6.6a1.6 1.6 0 0 1 1.6 1.6v1.9"/>
  <path d="M12 11.4v3.5"/>
  """ + DOT % (3.8, 16.6, 1.6) + DOT % (12, 16.6, 1.6) + DOT % (20.2, 16.6, 1.6) + """
  <path d="M1.8 21.2h4"/>
  <path d="M10 21.2h4"/>
  <path d="M18.2 21.2h4"/>
"""),
"dish": ("Satellite link", """
  <ellipse cx="10.4" cy="8.8" rx="7.6" ry="5.6" transform="rotate(-28 10.4 8.8)"/>
  <path d="M10.4 8.8 16.4 4.2"/>
  <circle cx="17.5" cy="3.4" r="1.5"/>
  <path d="M11.9 13.8 13 20.5"/>
  <path d="M9.4 20.5h7"/>
"""),

"smart-home": ("Smart technology", """
  <path d="M3.5 10.5 12 3.5l8.5 7"/>
  <path d="M5.6 12.4v8.1h12.8v-8.1"/>
  <path d="M9.6 16.5a3.4 3.4 0 0 1 4.8 0"/>
  <path d="M7.3 14.1a6.7 6.7 0 0 1 9.4 0"/>
  """ + DOT % (12, 18.8, 1)),

"smart-switch": ("Smart switch", """
  <rect x="3.5" y="5" width="17" height="14" rx="2"/>
  <rect x="7" y="8" width="10" height="8" rx="1.4"/>
  <path d="M7 12h10"/>
  """ + DOT % (12, 10, 0.9)),
"inverter": ("Backup power", """
  <rect x="2.5" y="5.5" width="19" height="13" rx="2"/>
  <path d="M12 5.5v13"/>
  <path d="M8.6 9.2 6 12.6h3l-1.4 2.9"/>
  <path d="M15 11h4.2"/>
  <path d="M15 14.2h4.2"/>
  <path d="M6 20.5h3"/>
  <path d="M15 20.5h3"/>
"""),

"solar": ("Solar", """
  <path d="M2.8 14.2 5.6 4.2h12.8l2.8 10z"/>
  <path d="M4.2 9.2h15.6"/>
  <path d="M9.4 4.2 8 14.2"/>
  <path d="M14.6 4.2l1.4 10"/>
  <path d="M12 14.2v6.3"/>
  <path d="M8.8 20.5h6.4"/>
"""),

"e-waste": ("Electronic waste", """
  <rect x="9.3" y="9.3" width="5.4" height="5.4" rx="1"/>
  <path d="M9.3 11H7.7"/>
  <path d="M9.3 13H7.7"/>
  <path d="M14.7 11h1.6"/>
  <path d="M14.7 13h1.6"/>
  <path d="M4.6 15a8.2 8.2 0 0 1 2.3-10"/>
  <path d="M6.9 5 6.4 8.1"/>
  <path d="M6.9 5 9.9 5.8"/>
  <path d="M19.4 9a8.2 8.2 0 0 1-2.3 10"/>
  <path d="M17.1 19l.5-3.1"/>
  <path d="M17.1 19 14.1 18.2"/>
"""),

"storefront": ("Retail", """
  <path d="M3.5 9.5V20a1.5 1.5 0 0 0 1.5 1.5h14a1.5 1.5 0 0 0 1.5-1.5V9.5"/>
  <path d="M2.5 9.5 4.3 3.5h15.4l1.8 6"/>
  <path d="M8.8 3.5 8.2 9.5"/>
  <path d="M15.2 3.5l.6 6"/>
  <path d="M2.5 9.5a3 3 0 0 0 5.7 0 3 3 0 0 0 5.6 0 3 3 0 0 0 5.7 0"/>
  <path d="M8.5 21.5v-6h7v6"/>
"""),

"cart": ("Online store", """
  <path d="M2.5 3.5h2.8l2.6 11.4h10l2.1-8.2H6.3"/>
  <circle cx="9.4" cy="19.2" r="1.8"/>
  <circle cx="17.2" cy="19.2" r="1.8"/>
  <path d="M13 8.5v3.6"/>
  <path d="M11.2 10.3h3.6"/>
"""),

# ------------------------------------------------------------------ group
# ------------------------------------------------------------------ group
"group-tree": ("Group structure", """
  <rect x="8.5" y="2.5" width="7" height="5" rx="1.4"/>
  <rect x="2" y="16.5" width="6" height="5" rx="1.4"/>
  <rect x="9" y="16.5" width="6" height="5" rx="1.4"/>
  <rect x="16" y="16.5" width="6" height="5" rx="1.4"/>
  <path d="M12 7.5v4.6"/>
  <path d="M5 16.5v-2.2a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v2.2"/>
  <path d="M12 12.1v4.4"/>
"""),

}
