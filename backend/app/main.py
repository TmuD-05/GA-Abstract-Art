"""
main.py

Main entry point for the Genetic Algorithm for Abstract Art.
Orchestrates feature extraction, GA evolution, rendering, and visualization.
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.src.midi_processor import extract_emotion_features
from backend.src.genetic_algorithm import ga_main
from backend.src.render import make_fluid_image, save_image
from backend.src.fitness import calculate_fitness

"""
   Main workflow:
   1. Extract emotional features from MIDI
   2. Run genetic algorithm to evolve best chromosome
   3. Render final image
   4. Save output
   """
app = FastAPI(title="Genetic Algorithm Art Engine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows your React frontend to communicate with this server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="backend/app/static"), name="static")

def main():

    MIDI_PATH = "/Users/tafadzwa/Genetic Algorithm For Abstract Art/test/EDM/Skrillex - Scary Monsters and nice splities (all parts).mid"
    OUTPUT_DIR = "/Users/tafadzwa/Genetic Algorithm For Abstract Art/outputs/final"
    POP_SIZE = 50
    GENERATIONS = 100

    print("=" * 70)
    print("GENETIC ALGORITHM FOR ABSTRACT ART")
    print("=" * 70)


    print(f"\n[1/4] Extracting emotional features from MIDI...")
    try:
        target_features = extract_emotion_features(MIDI_PATH)
        print(f" Features extracted:")
        print(f"  - Energy:  {target_features['energy']:.3f}")
        print(f"  - Valence: {target_features['valence']:.3f}")
        print(f"  - Density: {target_features['density']:.3f}")
    except Exception as e:
        print(f"   Error extracting features: {e}")
        return

    print(f"\n[2/4] Running genetic algorithm...")
    print(f"  Population size: {POP_SIZE}")
    print(f"  Generations: {GENERATIONS}")
    try:
        best_chromosome = ga_main(target_features, pop_size=POP_SIZE, generations=GENERATIONS)
        best_fitness = calculate_fitness(best_chromosome, target_features)
        print(f" GA completed")
        print(f"  - Best fitness: {best_fitness:.4f}")
        print(f"  - Best palette: {best_chromosome['palette_id']}")
        print(f"  - Best scale: {best_chromosome['scale']:.2f}")
    except Exception as e:
        print(f" Error running GA: {e}")
        return

    print(f"\n[3/4] Rendering final image (512x512)...")
    try:
        final_img = make_fluid_image(512, 512, best_chromosome)
        print(f" Image rendered successfully")
    except Exception as e:
        print(f" Error rendering image: {e}")
        return


    print(f"\n[4/4] Saving image...")
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        filename = save_image(final_img, folder=OUTPUT_DIR)
    except Exception as e:
        print(f" Error saving image: {e}")
        return

    print(f"\n{'=' * 70}")
    print("SUMMARY")
    print(f"{'=' * 70}")
    print(f"MIDI:              {os.path.basename(MIDI_PATH)}")
    print(f"Final Fitness:     {best_fitness:.4f}")
    print(f"Best Chromosome:")
    for key, value in best_chromosome.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")
    print(f"\nOutput saved to:   {filename}")
    print(f"{'=' * 70}\n")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8080, reload=True)
    main()