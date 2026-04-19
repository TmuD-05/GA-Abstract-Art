import random

"""
    Selects individuals from the population based on their fitness scores.
    Uses binary tournament selection to choose parents for crossover.
"""

def selection(scored_population):
    selected = []
    for _ in range(len(scored_population)):

        ind1 = random.choice(scored_population)
        ind2 = random.choice(scored_population)


        if ind1[1] > ind2[1]:
            selected.append(ind1[0])
        else:
            selected.append(ind2[0])

    return selected