"""
renderer.py

This module is responsible for converting a chromosome into a visual image.
It uses the Pillow library to draw shapes onto a canvas based on the
parameters stored in the chromosome.

Each shape's position, size, color, and opacity are used to render
an abstract image.

The output is a generated image that visually represents a chromosome,
which can then be evaluated by the fitness function or saved to disk.
"""