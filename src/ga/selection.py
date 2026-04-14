import random


def selection(scored_population):
    """
    Selects individuals from the population based on their fitness scores.
    Uses binary tournament selection to choose parents for crossover.
    """
    selected = []
    for _ in range(len(scored_population)):
        # Randomly select two individuals
        ind1 = random.choice(scored_population)
        ind2 = random.choice(scored_population)

        # Compare their fitness scores and select the better one
        if ind1[1] > ind2[1]:  # Assuming higher fitness is better
            selected.append(ind1[0])  # Append the chromosome
        else:
            selected.append(ind2[0])

    return selected