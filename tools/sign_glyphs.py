# -*- coding: utf-8 -*-
"""Solid pictograms for the signs.

The drawn icon set is a screen idiom: a 1.5 stroke on a 24 grid, read at arm's
length. A sign is read at twenty metres, through dust, often at an angle, and
thickening a line icon until it carries that far closes up its detail: the dome
camera becomes a blob and the reader becomes a smudge.

So the signs get their own glyphs, drawn as filled silhouettes on a 100 grid.
Same subjects, different medium. These are the shapes the eye resolves first.
"""

# Each entry is a list of (path_d, fill_rule). Everything is on a 0..100 grid.
GLYPHS = {

# The universal CCTV pictogram: a bullet camera on a wall bracket.
"camera": [
    # body, tilted down to the right
    ("M18 26 L78 44 L72 64 L12 46 Z", "nonzero"),
    # sunshade along the top of the body
    ("M17 22 L79 40 L76 48 L14 30 Z", "nonzero"),
    # lens hood at the front
    ("M76 46 L95 52 L89 72 L70 66 Z", "nonzero"),
    # bracket arm and wall plate
    ("M36 56 L44 58 L40 78 L32 76 Z", "nonzero"),
    ("M20 74 H52 V86 H20 Z", "nonzero"),
    ("M8 70 H18 V90 H8 Z", "nonzero"),
],

# A dog's head in profile, ears up, facing left.
# A paw. Two attempts at a profile dog read as a donkey, and an unconvincing
# animal on a warning sign undermines the warning. The paw is unmistakable at
# any size, and the headline carries the word "guard".
"dog": [
    ("M50 46 C66 46 79 57 79 70 C79 84 66 93 50 93 C34 93 21 84 21 70 C21 57 34 46 50 46 Z", "nonzero"),
    ("M6.86 44.07 a10.00 13.00 -24 1 0 18.27 -8.13 a10.00 13.00 -24 1 0 -18.27 8.13 Z", "nonzero"),
    ("M27.60 25.46 a10.50 14.00 -8 1 0 20.80 -2.92 a10.50 14.00 -8 1 0 -20.80 2.92 Z", "nonzero"),
    ("M51.60 22.54 a10.50 14.00 8 1 0 20.80 2.92 a10.50 14.00 8 1 0 -20.80 -2.92 Z", "nonzero"),
    ("M74.86 35.93 a10.00 13.00 24 1 0 18.27 8.13 a10.00 13.00 24 1 0 -18.27 -8.13 Z", "nonzero"),
],

# A response vehicle with a light bar, seen from the side.
"response": [
    ("M6 56 L18 36 C19 34 21 33 23 33 L72 33 C74 33 76 34 77 36 L92 56 "
     "L94 60 V74 H82 A10 10 0 0 0 62 74 H40 A10 10 0 0 0 20 74 H6 Z", "nonzero"),
    ("M30 22 H62 V32 H30 Z", "nonzero"),         # light bar
    ("M34 12 H46 V22 H34 Z", "nonzero"),
    ("M50 12 H62 V22 H50 Z", "nonzero"),
],
"response_cut": [
    ("M26 38 H48 V54 H14 Z", "nonzero"),         # windows
    ("M54 38 H70 L82 54 H54 Z", "nonzero"),
],
"response_wheels": [
    ("M30 74 a10 10 0 1 1 -20 0 a10 10 0 1 1 20 0 Z", "nonzero"),
    ("M72 74 a10 10 0 1 1 -20 0 a10 10 0 1 1 20 0 Z", "nonzero"),
],

# A door with a reader beside it, and a hand presenting a card.
# A card presented to a reader. A door on its own read as a locker; the card,
# the throw and the panel together read as access control.
"reader": [
    ("M68 12 H92 C94 12 96 14 96 16 V76 C96 78 94 80 92 80 H68 "
     "C66 80 64 78 64 76 V16 C64 14 66 12 68 12 Z", "nonzero"),
    ("M6 48 L44 36 C46 35 48 36 49 38 L56 60 C57 62 56 64 54 65 "
     "L16 77 C14 78 12 77 11 75 L4 53 C3 51 4 49 6 48 Z", "nonzero"),
],
"reader_cut": [
    ("M70 22 H90 V30 H70 Z", "nonzero"),
    ("M70 36 H90 V42 H70 Z", "nonzero"),
    ("M10 55 L42 45 L44 51 L12 61 Z", "nonzero"),
],
"reader_dot": [
    ("M80 62 a6 6 0 1 1 -12 0 a6 6 0 1 1 12 0 Z", "nonzero"),
    ("M57 28 c5 3 8 8 8 14", "nonzero"),
],

# An alarm bell: the pictogram everyone already knows.
"alarm": [
    ("M50 6 C54 6 57 9 57 13 V17 C73 21 84 35 84 52 V66 L92 80 H8 L16 66 "
     "V52 C16 35 27 21 43 17 V13 C43 9 46 6 50 6 Z", "nonzero"),
    ("M38 86 H62 A12 12 0 0 1 38 86 Z", "nonzero"),
],

# ISO W012: a lightning bolt. The statutory electricity pictogram.
"bolt": [
    ("M58 4 L18 56 H44 L36 96 L82 40 H54 Z", "nonzero"),
],
}

# Which parts are knocked out of the solid body rather than added to it.
CUTS = {"response": ["response_cut"], "reader": ["reader_cut"]}
EXTRA = {"response": ["response_wheels"], "reader": ["reader_dot"]}
