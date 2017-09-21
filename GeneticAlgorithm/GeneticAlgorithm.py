from .Individual import Individual
import sys
import random


class GeneticAlgorithm:
    def __init__(self, max_generations, min_individuals=30, max_individuals=70):
        self._max_generations = max_generations

        self._max_individuals = max_individuals
        self._min_individuals = min_individuals

        self._curr_generation = 0

        self._best_individual = {
            'Path': [],
            'Generation': 0,
            'Cost': sys.maxsize
        }

        self._individuals = [Individual.generate_random_individual() for _ in range(min_individuals)]
        self._sort()

        self._update_best_individual()

    def _sort(self):
        self._individuals.sort(key=lambda i: i.fit(), reverse=False)

    def _update_best_individual(self):
        if self._best_individual['Cost'] > self._individuals[0].fit():
            self._best_individual['Path'] = self._individuals[0].get_genes()
            self._best_individual['Generation'] = self._curr_generation
            self._best_individual['Cost'] = self._individuals[0].fit()

    def start(self):
        while self._curr_generation < self._max_generations:
            while len(self._individuals) < self._max_individuals:
                parent1 = random.choice(self._individuals)
                parent2 = random.choice(self._individuals)

                child1, child2 = Individual.crossover(parent1, parent2)

                if random.randint(0, 100) < 30:
                    child1.mutation()

                if random.randint(0, 100) < 30:
                    child2.mutation()

                self._individuals.append(child1)
                self._individuals.append(child2)

            self._individuals += [Individual.generate_random_individual() for _ in range(10)]
            self._sort()

            self._individuals = self._individuals[:self._min_individuals]

            self._curr_generation += 1

            self._update_best_individual()

        print('Best Path: {}\nGeneration: {}\nCost: {}'.format(
            self._best_individual['Path'],  self._best_individual['Generation'], self._best_individual['Cost']))
