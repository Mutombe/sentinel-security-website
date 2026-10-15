# -*- coding: utf-8 -*-
"""Subject boxes: the part of each photograph that must never be cut or
covered.

A fixed crop looks right at one width and wrong at the next. A face sits
mid frame on the desktop, then slides under the headline or off the edge on a
phone. So each photograph declares its subject instead, as four percentages of
the image (left, top, right, bottom), and the page moves the crop to keep that
rectangle whole at whatever size it is asked for.

Percentages rather than pixels, so the box stays true however the file is
resized.

How these were drawn, per the rules:

  Faces          the face, not the person. Eyes to chin. Hair and shoulders
                 can be cropped; a forehead under a headline cannot.
  Objects        the readable part only, so the screen rather than the hands
                 holding it.
  Tight          a smaller box leaves the engine more room to move.
  Textures       a photograph with no subject gets no box and is framed by
                 CSS alone.

Each was read off a ten percent grid laid over the file.
"""

# name -> (left, top, right, bottom), percentages of the image
FOCUS = {
    # ---- faces -----------------------------------------------------------
    "control-room-monitoring": (46, 16, 61, 43),   # operator's face
    "k9-handler-standing":     (29, 3, 43, 23),    # handler's face
    "officer-on-duty":         (26, 9, 39, 33),    # front officer's face
    "officer-radio":           (30, 7, 42, 27),    # her face
    "officers-team":           (39, 11, 67, 41),   # both faces, side by side
    "officers-warehouse":      (44, 4, 54, 23),    # lead officer's face
    "security-officers":       (30, 7, 61, 35),    # both faces
    "vehicle-checkpoint":      (54, 11, 69, 33),   # her face
    "technician-panel":        (63, 17, 76, 46),   # her face
    "tech-smart":              (46, 19, 60, 45),   # her face
    "tile-night":              (45, 21, 63, 56),   # his face
    "sys-access":              (46, 17, 93, 43),   # the panel and her face

    # ---- the phone photography, shown at the shape it was shot at --------
    # A 3:4 frame of a 3:4 original crops nothing, so these boxes never bind
    # today. They are drawn anyway: the slot outlives the layout, and the
    # first time one of these is asked for in a wide frame the engine should
    # already know what in it must survive.
    "team-office":             (12, 36, 78, 46),   # the four faces
    "team-pair":               (27, 31, 53, 45),   # both faces
    "team-site":               (26, 29, 75, 41),   # both faces
    "install-cabling":         (26, 27, 78, 47),   # the cabinet and his hands
    "install-camera":          (61, 4, 85, 20),    # the camera head
    "sign-wall":               (28, 28, 77, 57),   # the sign face
    "sign-entrance":           (18, 28, 73, 40),   # both faces

    # ---- objects: the readable part --------------------------------------
    "access-terminal":         (44, 14, 71, 61),   # the terminal screen
    "tile-access":             (41, 21, 71, 63),   # the device screen
    "sys-alarms":              (3, 19, 35, 77),    # the alarm panel
    # Was (41, 13, 87, 77): 64 percent of the image tall, which cannot fit
    # a page hero only 535px deep. Tightened to the camera head.
    "sys-cctv":                (47, 21, 85, 63),   # the camera head
    "sys-fire":                (17, 14, 51, 56),   # the beacons
    "sys-gates":               (41, 43, 77, 81),   # the gate motor
    "sys-intercom":            (29, 17, 47, 79),   # the intercom
    "tech-network":            (31, 11, 79, 79),   # the patch panel
    "tech-retail":             (17, 21, 63, 73),   # the devices on the bench
    "power-solar":             (9, 29, 71, 73),    # the array face
    "response-night":          (43, 35, 63, 59),   # the headlights

    # ---- no subject ------------------------------------------------------
    # circuitron-bench and tech-ewaste are textures: cables and mixed scrap.
    # Nothing in them must survive a crop, so they are framed by CSS alone.
}


def box(name):
    """The subject box for a photograph, or None if it has no subject."""
    return FOCUS.get(name)


def attr(name):
    """The box as a data-focus attribute, or an empty string."""
    b = FOCUS.get(name)
    return ' data-focus="%d %d %d %d"' % b if b else ""
