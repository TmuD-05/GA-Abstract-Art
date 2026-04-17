FITNESS_WEIGHTS = {
    'palette': 0.35,
    'scale': 0.25,
    'warp': 0.25,
    'octave': 0.15
}
def calculate_fitness(chromosome, target_features):
    # scale

    tgt_energy = target_features["energy"]

    scale_start =  200 - tgt_energy * 125
    scale_end =  300 + tgt_energy * 220

    ideal_s =  (scale_start + scale_end) /2

    dev_s = abs(ideal_s - chromosome["scale"])

    max_error_s = max( abs(ideal_s - scale_start), abs(ideal_s - scale_end) )

    scale_score = max(0,1 - dev_s /max_error_s)

    # palette
    if(target_features['valence'] < 0.5):

        ideal_p = 1 + (target_features['valence'] * 8)

        dev_p = abs(ideal_p - chromosome["palette_id"])

        max_error_p = max(abs(ideal_p - 1),abs(ideal_p - 5))

        palette_score = max(0,1 - dev_p / max_error_p)

    else:
        ideal_p = 6 + (18 * (target_features['valence'] - 0.5))

        dev_p = abs(ideal_p - chromosome["palette_id"])

        max_error_p = max(abs(ideal_p - 6),abs(ideal_p - 15))

        palette_score = max(0, 1 - dev_p / max_error_p)


    # octave
    ideal_o = 1 + (target_features['density'] * 5)
    dev_o = abs(ideal_o - chromosome["octaves"])
    max_error_o = max(abs(ideal_o - 1), abs(ideal_o - 6))
    octave_score = max(0,1 - dev_o / max_error_o)

    # warp

    warp_start = 20 + target_features['energy'] * 130
    warp_end =  50 + target_features['energy'] * 130

    ideal_w = (warp_start + warp_end) / 2

    dev_w = abs(ideal_w - chromosome["warp_strength"])

    max_error_w = max(abs(ideal_w - warp_start), abs(ideal_w - warp_end))

    warp_score = max(0,1 - dev_w / max_error_w)

    fitness_score = (
            palette_score * FITNESS_WEIGHTS['palette'] +
            scale_score * FITNESS_WEIGHTS['scale'] +
            warp_score * FITNESS_WEIGHTS['warp'] +
            octave_score * FITNESS_WEIGHTS['octave']
    )
    return fitness_score






