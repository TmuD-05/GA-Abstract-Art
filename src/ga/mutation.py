import numpy as np


"""
The random.random picks a value between 0.0 and 0.1.
0.2 = 20% chance of mutation. 0.1 = 10% chance of mutation.
The mutation function takes in a chromosome (which is a dictionary of parameters) and randomly mutates some of the parameters based on the defined mutation rate.
Each parameter has a certain chance to be mutated, and if it is chosen for mutation, it is modified by a small random amount within specified bounds. The mutated chromosome is then returned, 
which can be used in the next generation of the genetic algorithm.

"""

def mutation(chromosome):
    mutated = chromosome.copy()


    if np.random.random() < 0.2:
        mutated["scale"] += np.random.uniform(-15, 15) # 15 might be too high for this
        mutated["scale"] = np.clip(mutated["scale"], 75, 200)

    if np.random.random() < 0.2:
        mutated["warp_strength"] += np.random.uniform(-10, 10)
        mutated["warp_strength"] = np.clip(mutated["warp_strength"], 20, 140)

    if np.random.random() < 0.2:
        mutated["octaves"] = np.clip(mutated["octaves"] + np.random.choice([-1, 1]), 1, 6)

    if np.random.random() < 0.1:
        mutated["persistence"] += np.random.uniform(-0.05, 0.05)
        mutated["persistence"] = np.clip(mutated["persistence"], 0.3, 0.8)

    if np.random.random() < 0.1:
        mutated["palette_id"] += np.random.choice([-2, -1, 1, 2])
        mutated["palette_id"] = np.clip(mutated["palette_id"], 1, 21)

    return mutated