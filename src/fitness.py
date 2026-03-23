"""
fitness.py

This module evaluates how well a generated image matches the emotional
characteristics of the input music.

It assigns a fitness score to each chromosome based on:
1. Spatial energy: measures visual complexity relative to music energy
2. Colour-mood alignment: compares image colors to expected emotional tones

The combined fitness score is used by the genetic algorithm to guide
the evolution process toward better image representations.

Higher fitness scores indicate a better match between music and image.
"""