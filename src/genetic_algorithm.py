"""
genetic_algorithm.py

Runs the genetic algorithm to evolve the best chromosome over many generations.
Each generation uses tournament selection, crossover, and mutation to improve the population.
Elitism keeps the best chromosome from each generation.
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

    best = group[0]
    best_fitness = calculate_fitness(best, target_features)

    for ind in group[1:]:
        fitness = calculate_fitness(ind, target_features)

        if fitness > best_fitness:
            best = ind
            best_fitness = fitness
    return best

def select_parent(population, target_features):
    if random.random() < 0.3:
        return random.choice(population)
    else:
        return tournament_selection(population, target_features, k=2)

def find_best(population, target_features):
    def fitness_func(ind):
        return calculate_fitness(ind, target_features)

    return max(population, key=fitness_func)
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
            p1 = select_parent(population, target_features)
            p2 = select_parent(population, target_features)
            child = crossover(p1, p2)
            child = mutation(child)
            new_population.append(child)

        new_best = find_best(new_population, target_features)
        if calculate_fitness(new_best, target_features) > calculate_fitness(best_ever, target_features):
            best_ever = new_best

        population = new_population


        print(
            f"Generation {generation + 1}/{generations} - Best fitness: {calculate_fitness(best_ever, target_features):.4f}")

    return best_ever