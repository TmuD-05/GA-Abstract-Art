"""
genetic_algorithm.py

This module implements the genetic algorithm used to evolve abstract images.
It generates an initial population of chromosomes (image representations)
and iteratively improves them over multiple generations.

Key operations include:
- Selection (binary tournament)
- Crossover (combining parent chromosomes)
- Mutation (random variation)
- Replacement (maintaining population diversity)

The algorithm uses the fitness function to evaluate how well each
chromosome matches the emotional features of the input music.

The output is the best-performing chromosome representing the final image.
"""