"""
features.py

This module converts raw MIDI data into normalized feature vectors.
It processes values such as tempo, note density, and velocity, and
scales them into a standard range [0,1].

These normalized features represent the emotional characteristics
of the music, such as energy and mood (e.g., calm vs energetic,
sad vs happy).

The output is a feature vector used by the genetic algorithm and
fitness function to guide image generation.
"""