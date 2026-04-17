import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.chromosome import build_chromosome
from src.ga.crossover import crossover
from src.ga.selection import selection
from src.ga.mutation import mutation
from src.midi_processor import extract_emotion_features
from src.render import make_fluid_image, save_image
from src.fitness import calculate_fitness


POP_SIZE = 10
GENERATIONS = 10

def run_ga(midi_path):
    features = extract_emotion_features(midi_path)

    population = [build_chromosome(features) for _ in range(POP_SIZE)]

    best_overall = None
    best_overall_fitness = -1

    for gen in range(GENERATIONS):
        print(f"\n=== Generation {gen} ===")

        scored_population = [
            (chrom, calculate_fitness(chrom, features))
            for chrom in population
        ]

        scored_population.sort(key=lambda x: x[1], reverse=True)

        best_chromosome, best_fitness = scored_population[0]
        print(f"Best fitness: {best_fitness:.4f}")

        if best_fitness > best_overall_fitness:
            best_overall = best_chromosome
            best_overall_fitness = best_fitness

        # Save generation best (optional)
        img = make_fluid_image(200, 200, best_chromosome)
        save_image(img)

        # Selection
        selected = selection(scored_population)

        # Reproduction
        next_population = []
        for i in range(0, POP_SIZE, 2):
            parent1 = selected[i]
            parent2 = selected[i + 1]

            child1 = mutation(crossover(parent1, parent2))
            child2 = mutation(crossover(parent2, parent1))

            next_population.extend([child1, child2])

        population = next_population

    print("\n=== FINAL BEST ===")
    print(f"Best overall fitness: {best_overall_fitness:.4f}")

    final_img = make_fluid_image(300, 300, best_overall)
    save_image(final_img, folder="outputs/final")

    return best_overall

if __name__ == "__main__":
    MIDI_PATH = "/Users/tafadzwa/Genetic Algorithm For Abstract Art/test/Pirates of the Caribbean - He's a Pirate (1).mid"
    run_ga(MIDI_PATH)