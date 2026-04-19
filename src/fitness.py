"""
Calculate fitness score based on how well chromosome matches target features.

Args:
    chromosome: Dict with palette_id, scale, warp_strength, octaves, etc.
    target_features: Dict with energy, valence, density

Returns:
    fitness_score: 0-1 score (higher is better)
"""

FITNESS_WEIGHTS = {
    'palette': 0.4,
    'scale': 0.2,
    'warp': 0.2,
    'octave': 0.2
}


def calculate_fitness(chromosome, target_features):

    tgt_energy = target_features["energy"]
    tgt_density = target_features["density"]


    scale_start = 200 - tgt_energy * 125
    scale_end = 300 + tgt_energy * 220

    ideal_s = (scale_start + scale_end) / 2
    dev_s = abs(ideal_s - chromosome["scale"])
    max_error_s = max(abs(ideal_s - scale_start), abs(ideal_s - scale_end))

    scale_score = max(0, 1 - dev_s / max_error_s)

    valence = round(target_features['valence'], 1)
    energy = round(target_features['energy'], 1)

    if valence < 0.4:
        start = int(1 + valence * 20)
        end = int(4 + valence * 20)
    else:
        t = (valence - 0.4) / 0.6
        if energy < 0.7:
            start = int(11 + t * 5)
            end = int(14 + t * 5)
        else:
            start = int(16 + t * 6)
            end = int(19 + t * 6)

    ideal_p = (start + end) / 2
    dev_p = abs(ideal_p - chromosome["palette_id"])
    max_error_p = max(abs(ideal_p - start), abs(ideal_p - end))

    palette_score = max(0, 1 - dev_p / max_error_p)


    ideal_o = 1 + (tgt_density * 5)
    dev_o = abs(ideal_o - chromosome["octaves"])
    max_error_o = max(abs(ideal_o - 1), abs(ideal_o - 6))

    octave_score = max(0, 1 - dev_o / max_error_o)


    warp_start = 20 + tgt_energy * 130
    warp_end = 50 + tgt_energy * 130

    ideal_w = (warp_start + warp_end) / 2
    dev_w = abs(ideal_w - chromosome["warp_strength"])
    max_error_w = max(abs(ideal_w - warp_start), abs(ideal_w - warp_end))

    warp_score = max(0, 1 - dev_w / max_error_w)

    fitness_score = (
            palette_score * FITNESS_WEIGHTS['palette'] +
            scale_score * FITNESS_WEIGHTS['scale'] +
            warp_score * FITNESS_WEIGHTS['warp'] +
            octave_score * FITNESS_WEIGHTS['octave']
    )

    return fitness_score