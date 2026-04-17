from src.chromosome import build_chromosome
from src.render import make_fluid_image, save_image, show_image


test_features = {
    'energy': 0.85,
    'valence': 0.80,
    'density': 0.72
}

chromosome = build_chromosome(test_features)

print("Chromosome:")
for key, value in chromosome.items():
    print(f"{key}: {value}")

img = make_fluid_image(512, 512, chromosome)
show_image(img)
save_image(img)