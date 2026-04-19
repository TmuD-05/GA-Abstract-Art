import random

"""
    Creates a new 'child' chromosome by mixing the traits of two parent chromosomes.

    This function uses two strategies to combine genetic information:
    1. For smooth, decimal values (like Seed, Scale, and Warp), it uses 'Blended 
       Crossover.' Instead of just picking one parent, it mixes them together 
       at a random ratio to create a completely new value between the two.
    2. For distinct categories (like Palette or Octaves), it uses 'Uniform 
       Crossover.' It simply flips a coin to choose the exact value from 
       either Parent A or Parent B.

    This ensures that the child inherits the best of both parents while
"""

def crossover(parent1, parent2):

   child = {}
   for gene in parent1:
       if gene in ["seed_x", "seed_y"]:


           alpha = random.random()


           child[gene] = parent1[gene] * alpha + parent2[gene] * (1 - alpha)


       elif gene in ["scale", "warp_strength", "persistence"]:


           alpha = random.random()
           child[gene] = parent1[gene] *alpha + parent2[gene] *(1 - alpha)


       else:
           child[gene] = random.choice([parent1[gene], parent2[gene]])


   return child


