import random

def crossover(parent1, parent2):
    """
    Combines two parent chromosomes to create a child chromosome.
    Uses uniform crossover, where each gene is randomly selected from one of the parents.
    """
    child = {}
    for key in parent1:
        if key in ["seed_x", "seed_y"]:  # If we want to keep the same seed per generation for consistency
            child[key] = parent1[key]
        else:
            child[key] = random.choice([parent1[key], parent2[key]]) # randomly select gene from either parent, would this be considered mutation? or is it just crossover?
    return child


