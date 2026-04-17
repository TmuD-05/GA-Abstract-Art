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






Higher fitness scores indicate a better match between music and image.
"""

def check_fitness(chromosome, target):
# get the features from chromosome
  energy, density, valence = get_features(chromosome)

# calculate the difference between scores from chromosome and target value(based on midi file), taking absolute value and subtracting
# from 1 so that higher the difference between chromosome and target , lower the fitness of the chromosome
  e_score = 1- abs(energy - target["energy"])
  d_score = 1- abs(density - target["density"])
  v_score = 1- abs(valence - target["valence"])

  avg = (e_score, d_score, v_score) / 3
  
# using exponential in fitness to check if fitness increases and reaches closer to target faster 
  fitness = avg**2
  return fitness
