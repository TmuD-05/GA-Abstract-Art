import random

"""
crossover.py

Combines two parent chromosomes to produce a child chromosome.
For seed, scale, and warp, it uses blended crossover to create a new mixed value from both parents.
For palette and octaves, it uses uniform crossover to randomly select the value from either parent.

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


