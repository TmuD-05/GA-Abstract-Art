from src.palettes import PALETTES
import cv2
import numpy as np
import os


def render_palette_swatch(palette_id, palette, warp_strength=100):
    """Render a palette swatch with warp effect"""
    from src.render import make_fluid_image

    # Create a simple chromosome with the palette
    chromosome = {
        "palette_id": palette_id,
        "scale": 100,
        "octaves": 4,
        "persistence": 0.5,
        "warp_strength": warp_strength,  # High warp
        "seed_x": np.random.uniform(0, 1000),
        "seed_y": np.random.uniform(0, 10000),
    }

    # Render image
    img = make_fluid_image(200, 200, chromosome)
    return img


print("Rendering all palettes with high warp...")
os.makedirs("outputs/palette_swatches", exist_ok=True)

for palette_id in sorted(PALETTES.keys()):
    print(f"  Rendering palette {palette_id}...")
    img = render_palette_swatch(palette_id, PALETTES[palette_id], warp_strength=120)

    filename = f"outputs/palette_swatches/palette_{palette_id:02d}.png"
    cv2.imwrite(filename, img)

print("\n✓ All palettes saved to outputs/palette_swatches/")