from PyQt5.QtWidgets import QApplication
import sys
import numpy as np

from GeneticAlgorithm.Individual import Individual
from GUI.MainWindow import MainWindow

tsp_file = 'resources/gr17.tsp'

lower_tri = ''

with open(tsp_file) as f:
    line = ''
    while 'EOF' not in line:
        line = f.readline()
        if 'DIMENSION' in line:
            Individual.dimension = int(line.split('DIMENSION: ')[1])
        elif 'EDGE_WEIGHT_SECTION' in line:
            line = f.readline()
            while 'EOF' not in line:
                lower_tri += line[:-1]+' '
                line = f.readline()

Individual.weight_matrix = np.zeros((Individual.dimension, Individual.dimension))

lower_tri = [int(x) for x in list(filter(None, lower_tri.split(" ")))]
count = 0
for i in range(Individual.dimension, 0, -1):
    for j in range(0, Individual.dimension - i + 1):
        Individual.weight_matrix[Individual.dimension - i][j] = lower_tri[count]
        Individual.weight_matrix[j][Individual.dimension - i] = lower_tri[count]
        count += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    t = MainWindow()
    sys.exit(app.exec_())
