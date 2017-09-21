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
        parent1_genes = parent1.get_genes()
        parent2_genes = parent2.get_genes()

        child1_genes = parent1.get_genes().copy()
        child2_genes = parent2.get_genes().copy()

        ch1 = [False for _ in range(Individual.dimension)]

        count = 0
        while False in ch1:
            count += 1

            i = 0
            for i in range(Individual.dimension):
                if not ch1[i]:
                    break
            ini = i

            ch1[i] = True

            child1_genes[i] = parent1_genes[i] if count % 2 == 1 else parent2_genes[i]
            child2_genes[i] = parent1_genes[i] if count % 2 == 0 else parent2_genes[i]

            i = parent1_genes.index(parent2_genes[i])

            while i != ini:
                ch1[i] = True

                child1_genes[i] = parent1_genes[i] if count % 2 == 1 else parent2_genes[i]
                child2_genes[i] = parent1_genes[i] if count % 2 == 0 else parent2_genes[i]

                i = parent1_genes.index(parent2_genes[i])

        child1 = Individual(child1_genes)
        child2 = Individual(child2_genes)

        return child1, child2

    @classmethod
    def generate_random_individual(cls):
        genes = [x for x in range(Individual.dimension)]

        random.shuffle(genes)

        return Individual(genes)

