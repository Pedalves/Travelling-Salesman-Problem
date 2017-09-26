import numpy as np
import random


class Individual:
    """
    Classe responsavel pelos individuos do algoritimo genetico
    """

    # Matriz com as distancias entre os nos do grafo
    weight_matrix = np.array

    # Total de cromossomos dos individuos ex: [1, 2, 5] -> total de 3 cromossomos
    dimension = 0

    def __init__(self, genes):
        """
        Construtor da classe
        :param genes: Genes do individuo
        """
        self._genes = genes

    def get_genes(self):
        """
        Metodo para retorno dos genes do individuo
        :return: Retorna os genes do individuo
        """
        return self._genes

    def fit(self):
        """
        Metodo de calculo da distancia total percorrida pelo individuo
        :return:
        """

        fitness = 0

        for i in range(Individual.dimension):
            fitness += Individual.weight_matrix[self._genes[i - 1]][self._genes[i]]

        return fitness

    def mutation(self):
        """
        Mutacao baseada na troca de posicao de dois cromossomos
        :return:
        """
        g1 = random.randint(0, Individual.dimension-1)
        g2 = random.randint(0, Individual.dimension-1)
        self._genes[g1], self._genes[g2] = self._genes[g2], self._genes[g1]

    @classmethod
    def crossover(cls, parent1, parent2):
        """
        Metodo de classe responsavel pelo crossover baseado em ciclos
        :param parent1: Pai 1
        :param parent2: Pai 2
        :return: 2 filhos originados apartir dos pais
        """
        parent1_genes = parent1.get_genes()
        parent2_genes = parent2.get_genes()

        child1_genes = parent1.get_genes().copy()
        child2_genes = parent2.get_genes().copy()

        # Lista para conferir se todos os cromossomos dos pais foram percorridos
        ch1 = [False for _ in range(Individual.dimension)]

        count = 0

        # Enquanto existir cromossomos a serem percorrido procura novos ciclos
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
        """
        Metodo de classe responsavel por gerar individuos aleatorios
        :return: Indiviuo aleatorio gerado
        """

        genes = [x for x in range(Individual.dimension)]

        random.shuffle(genes)

        return Individual(genes)

