from .Individual import Individual
import sys
import random


class GeneticAlgorithm:
    """
    Classe responsavel pela execucao do algoritimo genetico
    """

    def __init__(self, max_generations, min_individuals=30, max_individuals=70, callback=None, update_path=None):
        """
        Construtor da classe
        :param max_generations: Quantidade de geracao que serao criadas ao longo da execucao do algoritimo
        :param min_individuals: Quantidade minima de individuos por geracao
        :param max_individuals: Quantidade maxima de individuos por geracao
        :param callback: Callback de sinalizar termino do algoritimo
        :param update_path: Callback para atualizar o valo do melhor individuo
        """

        self._max_generations = max_generations

        self._max_individuals = max_individuals
        self._min_individuals = min_individuals

        self._callback = callback
        self._update_path = update_path

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
        """
        Ordena os individuos por custo de forma crescente
        :return:
        """

        self._individuals.sort(key=lambda i: i.fit(), reverse=False)

    def _update_best_individual(self):
        """
        Atualiza o valor do melhor individuo encontrado pelo algoritimo, quanto menor o custo melhor e o resultado
        :return:
        """

        if self._best_individual['Cost'] > self._individuals[0].fit():
            self._best_individual['Path'] = self._individuals[0].get_genes()
            self._best_individual['Generation'] = self._curr_generation
            self._best_individual['Cost'] = self._individuals[0].fit()

            #executa callback para atualizar o valor de melhor individuo na GUI
            if self._update_path:
                self._update_path(self._best_individual)

    def start(self):
        """
        Metodo responsavel por executar o algoritimo genetico
        :return:
        """

        while self._curr_generation < self._max_generations:

            # Loop para crossover e mutacao, varia entre o valor minimo e o maximo de individuos de uma geracao
            while len(self._individuals) < self._max_individuals:

                # Escolhe os pais de maneira aleatoria
                parent1 = random.choice(self._individuals)
                parent2 = random.choice(self._individuals)

                child1, child2 = Individual.crossover(parent1, parent2)

                # Mutacao com probabilidade variando de 70% a 10%, a probabilidade diminui com o passar das geracoes
                if random.randint(0, 100) > 30 + \
                        (self._curr_generation * 0.5) if (self._curr_generation * 0.5) < 60 else 60:
                    child1.mutation()

                if random.randint(0, 100) > 30 + \
                        (self._curr_generation * 0.5) if (self._curr_generation * 0.5) < 60 else 60:
                    child2.mutation()

                self._individuals.append(child1)
                self._individuals.append(child2)

            # Adiciona 10 novos individuos aleatorios a populacao
            self._individuals += [Individual.generate_random_individual() for _ in range(10)]

            # Ordena de acordo com o menor custo do caminho
            self._sort()

            # Seleciona os 'min_individuals' melhores individuos da geracao corrente para a nova geracao
            self._individuals = self._individuals[:self._min_individuals]

            self._curr_generation += 1

            # Atualiza o melhor indiviudo encontrado
            self._update_best_individual()

        # executa callback para sinalizar para a GUI o fim da execucao do algoritimo,
        # caso nao exista uma gui o valor e printado
        if self._callback:
            self._callback()
        else:
            print('Best Path: {}\nGeneration: {}\nCost: {}'.format(
                self._best_individual['Path'],  self._best_individual['Generation'], self._best_individual['Cost']))
