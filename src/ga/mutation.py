import numpy as np

MUTATION_RATE = {
   "scale": 0.15,
   "warp_strength": 0.15,
   "palette_id": 0.1,
   "octaves": 0.2,
   "persistence": 0.05,
}

"""
    Randomly changes chromosome traits so the GA can explore new artistic styles. 

    This function uses two different methods for mutation:
    1. Small 'nudges' for decimal-based numbers (Scale, Warp, Persistence) to 
       fine-tune the artistic details.
    2. Fixed 'jumps' for whole numbers (Palette, Octaves) to try out 
       different categories.

    Finally, it uses clipping to make sure the values never go out of bounds, 
    which prevents the image generator from crashing or producing errors.
    """
def mutation(chromosome):
    mutated = chromosome.copy()

    if np.random.random() < MUTATION_RATE["scale"]:
        mutated["scale"] += np.random.uniform(-15, 15)
        mutated["scale"] = np.clip(mutated["scale"], 75, 200)

    if np.random.random() < MUTATION_RATE["warp_strength"]:
        mutated["warp_strength"] += np.random.uniform(-10, 10)
        mutated["warp_strength"] = np.clip(mutated["warp_strength"], 20, 140)

    if np.random.random() < MUTATION_RATE["octaves"]:
        mutated["octaves"] = np.clip(mutated["octaves"] + np.random.choice([-1, 1]), 1, 6)

    if np.random.random() < MUTATION_RATE["persistence"]:
        mutated["persistence"] += np.random.uniform(-0.05, 0.05)
        mutated["persistence"] = np.clip(mutated["persistence"], 0.3, 0.8)

    if np.random.random() < MUTATION_RATE["palette_id"]:
        mutated["palette_id"] += np.random.choice([-2, -1, 1, 2])
        mutated["palette_id"] = np.clip(mutated["palette_id"], 1, 25)

    return mutated