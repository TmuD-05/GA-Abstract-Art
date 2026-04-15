import sys
import os

# allow imports from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.render import make_fluid_image, save_image, show_image
from src.chromosome import build_chromosome
from src.midi_processor import extract_emotion_features   # adjust name if needed

# 🎵 path to your MIDI file
MIDI_PATH = "/Users/tafadzwa/Genetic Algorithm For Abstract Art/test/A-Whole-New-World-(Theme-From-'Aladdin').mid"

def test_renderer_with_midi():
    print("\n--- Extracting MIDI features ---")
    features = extract_emotion_features(MIDI_PATH)

    print("\n--- MIDI Features ---")
    for k, v in features.items():
        print(f"{k}: {v}")

    print("\n--- Building chromosome ---")
    chromosome = build_chromosome(features)

    print("\n--- Chromosome ---")
    for k, v in chromosome.items():
        print(f"{k}: {v}")

    print("\n--- Generating image ---")
    img = make_fluid_image(300, 300, chromosome)

    assert img is not None
    assert img.shape == (300, 300, 3)

    print("\n--- Saving image ---")
    path = save_image(img)

    print("\n--- Showing image ---")
    show_image(img)

    print("\nDONE ✔")


if __name__ == "__main__":
    test_renderer_with_midi()