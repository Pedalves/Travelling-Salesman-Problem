import numpy as np
import random


class Individual:
    weight_matrix = np.array
    dimension = 0

    def __init__(self, genes):
        self._genes = genes

    def get_genes(self):
        return self._genes

    def fit(self):
        fitness = 0

        for i in range(Individual.dimension):
            fitness += Individual.weight_matrix[self._genes[i - 1]][self._genes[i]]

        return fitness

    def mutation(self):
        g1 = random.randint(0, Individual.dimension-1)
        g2 = random.randint(0, Individual.dimension-1)
        self._genes[g1], self._genes[g2] = self._genes[g2], self._genes[g1]

    @classmethod
    def crossover(cls, parent1, parent2):
        return parent1, parent2

    @classmethod
    def generate_random_individual(cls):
        genes = [x for x in range(Individual.dimension)]

        random.shuffle(genes)

        return Individual(genes)

