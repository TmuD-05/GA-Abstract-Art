"""
    Palettes for colour schemes.
    numbered in order from 1 being the 'saddest' colour palette to n being the 'happiest' colour palette.
    Palettes are defines as lists of BGR tuples, which can be used with OpenCV.

    """


#  SAD PALETTES 1-5 (cool, deep, dark)
# could be used for valence 0.0-0.4

PALETTE_1 = [  # deep navy to soft blue
    (94, 4, 3),
    (182, 119, 0),
    (216, 180, 0),
    (239, 224, 144),
    (248, 240, 202),
]

PALETTE_2 = [  # dark purple to lavender
    (80, 10, 40),
    (120, 30, 80),
    (160, 60, 120),
    (200, 120, 170),
    (230, 180, 210),
]

PALETTE_3 = [  # deep blue to teal
    (80, 20, 10),
    (140, 60, 10),
    (180, 120, 20),
    (200, 180, 40),
    (220, 210, 100),
]

PALETTE_4 = [  # dark indigo to soft purple
    (70, 5, 30),
    (110, 20, 70),
    (150, 50, 110),
    (190, 100, 150),
    (220, 160, 190),
]

PALETTE_5 = [  # midnight blue to steel blue
    (60, 10, 10),
    (100, 30, 20),
    (140, 70, 30),
    (180, 120, 60),
    (210, 170, 100),
]

#  NEUTRAL PALETTES 6-10 - kind of mid range, for songs where its hard to tell with the midi features whether more sad or more happy
# could be used for valence 0.4-0.6

PALETTE_6 = [  # deep teal to seafoam
    (60, 40, 10),
    (110, 80, 10),
    (160, 130, 20),
    (200, 180, 60),
    (220, 210, 120),
]

PALETTE_7 = [  # blue-green to mint
    (100, 80, 20),
    (150, 130, 30),
    (190, 170, 60),
    (210, 200, 100),
    (230, 220, 160),
]

PALETTE_8 = [  # slate blue to periwinkle
    (100, 60, 60),
    (150, 100, 100),
    (190, 140, 140),
    (220, 180, 180),
    (240, 210, 210),
]

PALETTE_9 = [  # muted violet to dusty rose
    (90, 40, 70),
    (130, 70, 110),
    (170, 110, 150),
    (210, 160, 190),
    (235, 200, 220),
]

PALETTE_10 = [  # forest green to sage
    (40, 70, 20),
    (70, 110, 30),
    (100, 150, 60),
    (140, 190, 100),
    (180, 220, 150),
]

#  HAPPY PALETTES 11-15 (warm, bright)
# could be used for valence 0.6-1.0

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

PALETTE_14 = [  # terracotta to sand
    (40, 60, 160),
    (60, 100, 200),
    (90, 140, 220),
    (130, 180, 240),
    (180, 215, 250),
]

PALETTE_15 = [  # dusty rose to champagne
    (100, 80, 180),
    (130, 110, 210),
    (160, 150, 230),
    (200, 190, 245),
    (225, 215, 255),
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
}