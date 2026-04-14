from chromosome import build_chromosome
from render import make_fluid_image, save_image, show_image


test_features = {
    'energy': 0.7,
    'valence': 0.3,
    'density': 0.5
}

chromosome = build_chromosome(test_features)

print("Chromosome:")
for key, value in chromosome.items():
    print(f"{key}: {value}")

img = make_fluid_image(512, 512, chromosome)
show_image(img)
save_image(img)