"""
chromosome.py

This module defines the data structures used to represent an image
in the genetic algorithm.

These structures are used by the genetic algorithm, renderer, and
fitness function.
"""

import numpy as np

def pick_palette(valence, energy):
    if valence < 0.4: #made this 0.4 from 0.5 due to our valence calculation issues
        start, end = 1, 10 # darker, moodier, cooler palettes

    else:
        if energy < 0.7: #need to test smt like edm music and see what is scores for valence
            start, end = 11, 15 # happy but not intense
        else:
            start, end = 16, 21 # neon / intense

    return np.random.randint(start, end + 1)


def pick_scale(energy):
    if energy < 0.3:
        return np.random.uniform(170, 200)
    elif energy < 0.7:
        return np.random.uniform(120, 150)
    else:
        return np.random.uniform(75, 100)


def pick_octaves(density):

    start = max(1, round(density * 5))
    end = min(6, round(1 + density * 5))

    if start == end:
        return start

    return np.random.randint(start, end + 1)


# high energy = more warp, more distortion
# low energy = less warp, smoother, calmer
def pick_warp_strength(energy):
    if energy < 0.3:
        return np.random.uniform(20, 35)
    elif energy < 0.7:
        return np.random.uniform(55, 75)
    else:
        return np.random.uniform(110, 140)

def build_chromosome(features: dict) -> dict:

    energy = features['energy']
    valence = features['valence']
    density = features['density']

    chromosome = {
        "palette_id": pick_palette(valence, energy),
        "scale": pick_scale(energy),
        "octaves": pick_octaves(density),
        "persistence": 0.4 + density * 0.3,
        "warp_strength": pick_warp_strength(energy),

        #these values we have to decide if we want to keep the same ones per generation or give each chromosome a diff one
        #all the seed does is ensure we dont have the exact same 'flow pattern' each time, so each seed value has a different 'flow pattern'
        "seed_x": np.random.uniform(0, 10000),
        "seed_y": np.random.uniform(0, 10000),

    }

    return chromosome