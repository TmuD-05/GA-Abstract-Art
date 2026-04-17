import random

def crossover(parent1, parent2):
    """
    Combines two parent chromosomes to create a child chromosome.
    Uses uniform crossover, where each gene is randomly selected from one of the parents.
    """
    child = {}
    for gene in parent1:
        if gene in ["seed_x", "seed_y"]:  # If we want to keep the same seed per generation for consistency
            child[gene] = parent1[gene]

        else:
            child[gene] = random.choice([parent1[gene], parent2[gene]]) # randomly select gene from either parent, would this be considered mutation? or is it just crossover?
    #         then here we essentially picking from one parent to make the child the seed then is this crossover ? what is a crossover
    return child


