import sys
import os
import cv2
import numpy as np

# allow imports from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.chromosome import build_chromosome
from src.render import make_fluid_image

from datetime import datetime


POP_SIZE = 10

features = {
    "energy": 0.6,
    "valence": 0.5,
    "density": 1
}

OUTPUT_FOLDER = "outputs/population_test"
filename = os.path.join(
    OUTPUT_FOLDER,
    f"grid_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
)

def show_population_grid(images, cols=5):
    rows = int(np.ceil(len(images) / cols))

    h, w, c = images[0].shape
    grid = np.zeros((rows * h, cols * w, c), dtype=np.uint8)

    for idx, img in enumerate(images):
        r = idx // cols
        c_idx = idx % cols
        grid[r*h:(r+1)*h, c_idx*w:(c_idx+1)*w] = img

    return grid


def test_population():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    population = [build_chromosome(features) for _ in range(POP_SIZE)]

    images = []

    print("\n--- Chromosome Palette IDs ---")
    for i, chrom in enumerate(population):
        print(f"{i}: palette_id = {chrom['palette_id']}")

        img = make_fluid_image(150, 150, chrom)
        images.append(img)


    grid = show_population_grid(images)

    from datetime import datetime
    grid_filename = f"grid_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    grid_path = os.path.join(OUTPUT_FOLDER, grid_filename)


    cv2.imwrite(grid_path, grid)

    # Optional: show it
    cv2.imshow("Population Grid", grid)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(f"\nGrid saved at: {grid_path}")


if __name__ == "__main__":
    test_population()