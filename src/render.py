"""
renderer.py

This module is responsible for converting a chromosome into a visual image.
It uses the Pillow library to draw shapes onto a canvas based on the
parameters stored in the chromosome.

Each shape's position, size, color, and opacity are used to render
an abstract image.

The output is a generated image that visually represents a chromosome,
which can then be evaluated by the fitness function or saved to disk.
"""

import numpy as np
import cv2
import os
from opensimplex import noise2
from datetime import datetime
from palettes import PALETTES

def interpolate_colour(t, palette):
    scaled = t * (len(palette) - 1)
    idx1 = int(scaled)
    idx2 = min(idx1 + 1, len(palette) - 1)
    frac = scaled - idx1
    c1 = np.array(palette[idx1])
    c2 = np.array(palette[idx2])
    return tuple((c1 * (1 - frac) + c2 * frac).astype(int))

def make_fluid_image(width, height, chromosome):
    canvas = np.zeros((height, width, 3), dtype=np.uint8)

    scale = chromosome["scale"]
    warp_strength = chromosome["warp_strength"]
    octaves = chromosome["octaves"]
    palette = PALETTES[chromosome["palette_id"]]
    persistence = chromosome["persistence"] # might just be able to take out
    # flow_angle = chromosome["flow_angle"] # i think this is useless, since our image is static, it just directs the flow a certain way

    # if we want to keep these static for each gen, we would not be pulling from chromosome
    seed_x = chromosome["seed_x"]
    seed_y = chromosome["seed_y"]

    print("Generating image...")

    for y in range(height):
        if y % (height // 10) == 0:
            print(f"Progress:{int(y/height*100)}% ")

        for x in range(width):

            nx, ny = 0.0, 0.0
            amp, freq = 1.0, 1.0
            for _ in range (octaves):
                nx += amp * noise2((x + seed_x) * freq / scale, (y + seed_y) * freq / scale)
                ny += amp * noise2((x + seed_x + 300) * freq / scale, (y + seed_y + 300) * freq / scale)
                amp *= persistence
                freq *= 2.0

            warped_x = x + warp_strength * nx
            warped_y = y + warp_strength * ny

            val, amp, freq = 0.0, 1.0, 1.0
            for _ in range (octaves):
                val += amp * noise2(warped_x * freq / scale, warped_y * freq / scale)
                amp *= persistence
                freq *= 2.0

            t = (val + 1) / 2
            t = max(0.0, min(1.0, t))

            canvas[y, x] = interpolate_colour(t, palette)

    return canvas

# image saving and showing

def save_image(img, folder="outputs"):
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%d_%H%M%S")
    filename = os.path.join(folder, f"fluid_{timestamp}.png")
    cv2.imwrite(filename, img)
    print(f"Image saved as {filename}")
    return filename

def show_image(img, window_name="Fluid Image"): # we can find a diff name for the window
    cv2.imshow(window_name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

