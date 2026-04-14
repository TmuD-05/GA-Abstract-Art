"""
chromosome.py

This module defines the data structures used to represent an image
in the genetic algorithm.

Each chromosome consists of a collection of shapes, where each shape
has attributes such as position, size, color, and opacity.

This module does not implement any algorithmic logic; it only defines
how image data is structured and stored.

These structures are used by the genetic algorithm, renderer, and
fitness function.
"""

import numpy as np
from palettes import PALETTES

def pick_palette(valence):
    if valence < 0.4:
        low, high = 1, 5

    elif valence < 0.6:
        low, high = 6, 10

    else:
        low, high = 11, 15

    return np.random.randint(low, high + 1)

def pick_scale(energy):
    # energy 0.0 = range 150-200, larger shapes, less going on
    # energy 1.0 = range 75-100, smaller, tighter shapes, more chaotic
    # total range should be 75 - 200
    start = int(200 - energy * 125)
    end = int(300 - energy * 220)

    return np.random.uniform(start, end)

def pick_octaves(density):
    # high density = high octaves, low density = low octaves
    # density 0.0 = 1-2 (simple, smooth)
    # density 1.0 = 5-6 (more complex, chaotic)

    start = max(1, round(density * 5))
    end = min(6, round(1 + density * 5))

    if start == end:
        return start

    return np.random.randint(start, end + 1)

def pick_warp_strength(energy):
    # high energy = more warp, more distortion
    # low energy = less warp, smoother, calmer
    # energy 0.0 = 20-50
    # energy 1.0 = 150-180
    start = 20 + energy * 130
    end = 50 + energy * 130

    return np.random.uniform(start, end)

def build_chromosome(features: dict) -> dict:

    energy = features['energy']
    valence = features['valence']
    density = features['density']

    chromosome = {
        "palette_id": pick_palette(valence),
        "scale": pick_scale(energy),
        "octaves": pick_octaves(density),
        "persistence": np.random.uniform(0.3, 0.8), #could possibly get rid of this, i personally think it does nothing
        "warp_strength": pick_warp_strength(energy),

        #these values we have to decide if we want to keep the same ones per generation or give each chromosome a diff one
        #all the seed does is ensure we dont have the exact same 'flow pattern' each time, so each seed value has a different 'flow pattern'
        "seed_x": np.random.uniform(0, 10000),
        "seed_y": np.random.uniform(0, 10000),

    }

    return chromosome