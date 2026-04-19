"""
genetic_algorithm.py

This module implements the genetic algorithm used to evolve abstract images.
It generates an initial population of chromosomes (image representations)
and iteratively improves them over multiple generations.

Key operations include:
- Selection (tournament)
- Crossover (combining parent chromosomes)
- Mutation (random variation)

The algorithm uses the fitness function to evaluate how well each
chromosome matches the emotional features of the input music.

The output is the best-performing chromosome representing the final image.
"""

from src.chromosome import build_chromosome
import random
from src.fitness import calculate_fitness
from src.ga.crossover import crossover
from src.ga.mutation import mutation

TOURNAMENT_K = 3


def create_population(n, features):

    population = []
    for i in range(n):
        population.append(build_chromosome(features))
    return population


def tournament_selection(population, target_features, k=TOURNAMENT_K):

    group = []
    for i in range(k):
        index = random.randint(0, len(population) - 1)
        group.append(population[index])

    best = max(group, key=lambda ind: calculate_fitness(ind, target_features))
    return best


def find_best(population, target_features):

    return max(population, key=lambda ind: calculate_fitness(ind, target_features))
    """
    Main genetic algorithm loop

    Args:
        target_features: Dict with energy, valence, density
        pop_size: Population size (default 20)
        generations: Number of generations (default 50)

    Returns:
        best_ever: Best chromosome found
    """

def ga_main(target_features, pop_size=20, generations=50):


    population = create_population(pop_size, target_features)

    best_ever = find_best(population, target_features)

    for generation in range(generations):
        new_population = []


        best = find_best(population, target_features)
        new_population.append(best)


        while len(new_population) < pop_size:
            p1 = tournament_selection(population, target_features, TOURNAMENT_K)
            p2 = tournament_selection(population, target_features, TOURNAMENT_K)
            child = crossover(p1, p2)
            child = mutation(child)
            new_population.append(child)


        if random.random() < 0.1 and len(new_population) > 1:
            replace_index = random.randint(1, len(new_population) - 1)
            new_population[replace_index] = build_chromosome(target_features)


        new_best = find_best(new_population, target_features)
        if calculate_fitness(new_best, target_features) > calculate_fitness(best_ever, target_features):
            best_ever = new_best

        population = new_population


        print(
            f"Generation {generation + 1}/{generations} - Best fitness: {calculate_fitness(best_ever, target_features):.4f}")

    return best_ever