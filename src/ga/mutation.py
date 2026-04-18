import numpy as np

MUTATION_RATE = {
   "scale": 0.15,           # Important for composition
   "warp_strength": 0.15,   # Important for flow
   "palette_id": 0.1,       # Already selected well, mutate conservatively
   "octaves": 0.2,          # Moderate importance
   "persistence": 0.05,     # Low impact, rarely mutate
}


def mutation(chromosome):
    mutated = chromosome.copy()

    if np.random.random() < MUTATION_RATE["scale"]:
        mutated["scale"] += np.random.uniform(-15, 15) # 15 might be too high for this
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
        mutated["palette_id"] = np.clip(mutated["palette_id"], 1, 21)

    return mutated