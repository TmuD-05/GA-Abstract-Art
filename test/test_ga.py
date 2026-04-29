"""
run_ga.py

Main genetic algorithm runner for generating abstract art from MIDI.
Clean output for A/B testing.
"""

import sys
import os
import numpy as np
import cv2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.chromosome import build_chromosome
from src.ga.crossover import crossover
from src.ga.mutation import mutation
from src.midi_processor import extract_emotion_features
from src.render import make_fluid_image, save_image
from src.fitness import calculate_fitness


class GeneticAlgorithm:
    def __init__(self, pop_size=10, generations=10):
        self.pop_size = pop_size
        self.generations = generations
        self.img_size = 180

    def render_population_grid(self, population, generation):
        """Render population as 2x5 grid"""
        grid_rows = 2
        grid_cols = 5
        spacing = 5

        grid_width = (grid_cols * self.img_size) + (spacing * (grid_cols - 1))
        grid_height = (grid_rows * self.img_size) + (spacing * (grid_rows - 1))

        grid_img = np.ones((grid_height, grid_width, 3), dtype=np.uint8) * 255

        print(f"  Rendering generation {generation + 1} grid...")

        for idx, chrom in enumerate(population[:grid_rows * grid_cols]):
            row = idx // grid_cols
            col = idx % grid_cols

            try:
                fluid_img = make_fluid_image(self.img_size, self.img_size, chrom)
                fluid_img_rgb = cv2.cvtColor(fluid_img, cv2.COLOR_BGR2RGB)
            except Exception as e:
                print(f"  Error rendering image {idx}: {e}")
                fluid_img_rgb = np.ones((self.img_size, self.img_size, 3), dtype=np.uint8) * 128

            start_y = row * (self.img_size + spacing)
            start_x = col * (self.img_size + spacing)

            grid_img[start_y:start_y + self.img_size, start_x:start_x + self.img_size] = fluid_img_rgb

            # Add palette label
            palette_id = chrom["palette_id"]
            cv2.putText(grid_img, f"P{palette_id}", (start_x + 5, start_y + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        return grid_img

    def print_population_table(self, scored_population, generation):
        """Print fitness table"""
        print(f"\n--- Generation {generation + 1} Fitness ---")
        print(f"{'Idx':<4} {'Palette':<8} {'Scale':<8} {'Warp':<8} {'Octaves':<8} {'Fitness':<10}")
        print("-" * 54)

        for idx, (chrom, fitness) in enumerate(scored_population):
            marker = "★" if idx == 0 else ""
            print(
                f"{idx:<4} {chrom['palette_id']:<8} {chrom['scale']:<8.1f} {chrom['warp_strength']:<8.1f} {chrom['octaves']:<8} {fitness:<10.4f} {marker}")

    def run(self, midi_path):
        """Run GA"""

        print(f"\nExtracting features from: {midi_path}")
        features = extract_emotion_features(midi_path)
        print(
            f"Energy: {features['energy']:.3f}, Valence: {features['valence']:.3f}, Density: {features['density']:.3f}")

        print(f"\nInitializing population (size={self.pop_size})...")
        population = [build_chromosome(features) for _ in range(self.pop_size)]

        best_overall = None
        best_overall_fitness = -1

        os.makedirs("outputs/generations", exist_ok=True)

        for gen in range(self.generations):
            print(f"\n{'=' * 60}")
            print(f"Generation {gen + 1}/{self.generations}")
            print(f"{'=' * 60}")

            # Score population
            scored_population = [
                (chrom, calculate_fitness(chrom, features))
                for chrom in population
            ]
            scored_population.sort(key=lambda x: x[1], reverse=True)

            best_chromosome, best_fitness = scored_population[0]
            avg_fitness = np.mean([score for _, score in scored_population])

            print(f"Best: {best_fitness:.4f} | Avg: {avg_fitness:.4f}")

            # Print table
            self.print_population_table(scored_population, gen)

            # Track best
            if best_fitness > best_overall_fitness:
                best_overall = best_chromosome
                best_overall_fitness = best_fitness

            # Save grid
            gen_grid = self.render_population_grid(population, gen)
            gen_grid_file = os.path.join("outputs/generations", f"gen_{gen + 1:03d}.png")
            cv2.imwrite(gen_grid_file, cv2.cvtColor(gen_grid, cv2.COLOR_RGB2BGR))

            # Next generation
            next_population = [best_chromosome]  # Elitism

            while len(next_population) < self.pop_size:
                p1_idx = np.random.randint(0, self.pop_size)
                p2_idx = np.random.randint(0, self.pop_size)

                p1, _ = scored_population[p1_idx]
                p2, _ = scored_population[p2_idx]

                child = mutation(crossover(p1, p2))
                next_population.append(child)

            population = next_population

        # Final result
        print(f"\n{'=' * 60}")
        print(f"FINAL RESULT")
        print(f"{'=' * 60}")
        print(f"Best fitness: {best_overall_fitness:.4f}")
        print(f"Best palette: {best_overall['palette_id']}")

        print(f"\nRendering final image...")
        final_img = make_fluid_image(512, 512, best_overall)
        filename = save_image(final_img, folder="outputs/final")
        print(f"Saved: {filename}\n")

        return best_overall, best_overall_fitness


if __name__ == "__main__":
    MIDI_PATH = "/Users/tafadzwa/Genetic Algorithm For Abstract Art/test/Pirates of the Caribbean - He's a Pirate (1).mid"
    POP_SIZE = 10
    GENERATIONS = 10

    ga = GeneticAlgorithm(pop_size=POP_SIZE, generations=GENERATIONS)
    best_chromosome, best_fitness = ga.run(MIDI_PATH)
