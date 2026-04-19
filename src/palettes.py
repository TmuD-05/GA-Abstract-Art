"""
palettes.py

Defines a set of 25 colour palettes used to render images.
Palettes are ordered from more cool and dark colours to brighter and intense colours.
Each palette is a list of BGR colour tuples for use with OpenCV.
    """

PALETTE_1 = [
    (80, 30, 10),
    (110, 40, 20),
    (140, 50, 35),
    (170, 60, 55),
    (200, 70, 80)
]

PALETTE_2 = [  # deep navy to cold blue
    (20, 5, 5),
    (60, 10, 10),
    (120, 40, 30),
    (180, 80, 60),
    (240, 120, 90)
]

PALETTE_3 = [  # dark blue to dark purple
    (60, 20, 10),
    (80, 25, 40),
    (100, 30, 80),
    (120, 35, 120),
    (140, 40, 160)
]

PALETTE_4 = [  # deep blue to teal
    (50, 10, 10),
    (80, 30, 20),
    (110, 60, 30),
    (140, 100, 50),
    (170, 140, 80)
]

PALETTE_5 = [  # dark indigo to soft purple
    (25, 5, 20),
    (60, 15, 60),
    (100, 40, 100),
    (140, 80, 140),
    (190, 130, 190)
]

PALETTE_6 = [  # midnight blue to medium blue
    (60, 10, 10),
    (100, 30, 20),
    (140, 70, 30),
    (180, 120, 60),
    (210, 170, 100),
]

#  NEUTRAL PALETTES 6-10 - kind of mid range, for songs where its hard to tell with the midi features whether more sad or more happy


PALETTE_7 = [  # deep teal to seafoam
    (60, 40, 10),
    (110, 80, 10),
    (160, 130, 20),
    (200, 180, 60),
    (220, 210, 120),
]

PALETTE_8 = [  # tealish gray
    (60, 70, 40),
    (90, 110, 60),
    (120, 140, 90),
    (160, 170, 130),
    (200, 210, 170)
]

PALETTE_9 = [  # slate blue to periwinkle
    (100, 60, 60),
    (150, 100, 100),
    (190, 140, 140),
    (220, 180, 180),
    (240, 210, 210),
]

#too pastel?
PALETTE_10 = [  # muted violet to dusty rose
    (90, 40, 70),
    (130, 70, 110),
    (170, 110, 150),
    (210, 160, 190),
    (235, 200, 220),
]

"""
PALETTE_10 = [  # forest green to sage
    (40, 70, 20),
    (70, 110, 30),
    (100, 150, 60),
    (140, 190, 100),
    (180, 220, 150),
]
"""

#  HAPPY PALETTES 11-19 (warm, bright)

PALETTE_11 = [  # coral to peach
    (60, 80, 180),
    (80, 120, 220),
    (100, 160, 240),
    (140, 200, 250),
    (180, 230, 255),
]

PALETTE_12 = [  # rose to blush pink
    (80, 40, 140),
    (120, 70, 190),
    (160, 110, 220),
    (200, 160, 240),
    (230, 200, 255),
]

PALETTE_13 = [  # amber to warm gold
    (20, 120, 200),
    (30, 160, 230),
    (50, 200, 245),
    (100, 220, 255),
    (160, 240, 255),
]

PALETTE_14 = [ # red to bright orange
    (0, 0, 255),
    (0, 40, 255),
    (0, 80, 255),
    (0, 120, 255),
    (0, 180, 255)
]


PALETTE_15 = [ # hot pink to orange
    (80, 40, 255),
    (60, 80, 255),
    (40, 120, 255),
    (20, 160, 255),
    (0, 200, 255)
]

PALETTE_16 = [ # orange - blue
   (0, 140, 255),
    (40, 120, 220),
    (80, 100, 180),
    (140, 80, 140),
    (220, 60, 100)
]

PALETTE_17 = [ # pink to purple
    (120, 40, 255),
    (140, 30, 240),
    (160, 20, 220),
    (180, 10, 200),
    (200, 0, 180)
]

PALETTE_18 = [ # blue to yellow-green
    (255, 120, 0),
    (220, 160, 20),
    (180, 200, 40),
    (120, 230, 80),
    (60, 255, 140)
]

PALETTE_19 = [ # teal to yellow
    (180, 140, 60),
    (190, 160, 80),
    (205, 180, 110),
    (220, 200, 140),
    (235, 220, 180),
]


# NEON / INTENSE PALETTES 16-21 (for high energy songs, more warp, more distortion, more intense colours)
PALETTE_20 = [  # neon sky blue to cyan
    (255, 80, 0),
    (255, 120, 20),
    (255, 160, 60),
    (255, 200, 100),
    (255, 240, 160)
]

PALETTE_21 = [  #lime to slight yellow pop
    (80, 255, 60),
    (120, 255, 80),
    (160, 255, 120),
    (200, 255, 160),
    (240, 255, 210),
]

PALETTE_22 = [  # hot pink to magenta
    (180, 60, 255),
    (200, 90, 255),
    (220, 120, 255),
    (240, 160, 255),
    (255, 200, 255),
]

PALETTE_23 = [  # bright aqua to cyan
    (255, 200, 60),
    (255, 220, 90),
    (255, 240, 120),
    (240, 255, 160),
    (210, 255, 200),
]

PALETTE_24 = [  # orange to yellow to white
    (60, 140, 255),
    (90, 180, 255),
    (120, 220, 255),
    (160, 240, 255),
    (220, 255, 255),
]

PALETTE_25 = [  # neon mix (cyan to magenta vibe)
    (255, 80, 200),
    (255, 120, 160),
    (255, 180, 120),
    (240, 240, 100),
    (200, 255, 140),
]

PALETTES = {
    1:  PALETTE_1,
    2:  PALETTE_2,
    3:  PALETTE_3,
    4:  PALETTE_4,
    5:  PALETTE_5,
    6:  PALETTE_6,
    7:  PALETTE_7,
    8:  PALETTE_8,
    9:  PALETTE_9,
    10: PALETTE_10,
    11: PALETTE_11,
    12: PALETTE_12,
    13: PALETTE_13,
    14: PALETTE_14,
    15: PALETTE_15,
    16: PALETTE_16,
    17: PALETTE_17,
    18: PALETTE_18,
    19: PALETTE_19,
    20: PALETTE_20,
    21: PALETTE_21,
    22: PALETTE_22,
    23: PALETTE_23,
    24: PALETTE_24,
    25: PALETTE_25
}