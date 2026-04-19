"""
chromosome.py

This module defines the data structures used to represent an image
in the genetic algorithm.

These structures are used by the genetic algorithm, renderer, and
fitness function.
"""

import numpy as np

def pick_palette(valence, energy):
    if valence < 0.4:
        start, end = 1, 10

    else:
        if energy < 0.7:
            start, end = 11, 19
        else:
            start, end = 16, 25

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
        "persistence": np.random.uniform(0.3, 0.8),
        "warp_strength": pick_warp_strength(energy),

        "seed_x": np.random.uniform(0, 1000),
        "seed_y": np.random.uniform(0, 10000),

    }

    return chromosome