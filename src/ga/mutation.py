import numpy as np

MUTATION_RATE = 0.2 # 20% chance to mutate each gene

def mutation(chromosome):
    mutated = chromosome.copy()


    if np.random.random() < MUTATION_RATE:
        mutated["scale"] = np.clip(mutated["scale"] * np.random.uniform(0.8, 1.2), 75, 200) # multiples scale value by a random value in between 0.8 and 1.2, so it can either increase or decrease the scale slightly

    if np.random.random() < MUTATION_RATE:
        mutated["warp_strength"] = np.clip(mutated["warp_strength"] * np.random.uniform(0.8, 1.2), 20, 180)

    if np.random.random() < MUTATION_RATE:
        mutated["octaves"] = np.clip(mutated["octaves"] + np.random.choice([-1, 1]), 1, 6)

    if np.random.random() < MUTATION_RATE:
        mutated["persistence"] =  np.clip(mutated["persistence"] + np.random.uniform(-0.1, 0.1), 0.1, 0.9)

    if np.random.random() < MUTATION_RATE:
        mutated["palette_id"] = np.clip(mutated["palette_id"] + np.random.choice([-1, 1]), 1, 15)

    return mutated