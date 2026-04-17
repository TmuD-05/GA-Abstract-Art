import random


def crossover(parent1, parent2):
   """
   Combines two parent chromosomes to create a child chromosome.
   Uses uniform crossover, where each gene is randomly selected from one of the parents.
   """
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


