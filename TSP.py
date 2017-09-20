from pprint import pprint
import numpy as np


tsp_file = 'resources/gr17.tsp'
dimension = 0

lower_tri = ''

with open(tsp_file) as f:
    line = ''
    while 'EOF' not in line:
        line = f.readline()
        if 'DIMENSION' in line:
            dimension = int(line.split('DIMENSION: ')[1])
        elif 'EDGE_WEIGHT_SECTION' in line:
            line = f.readline()
            while 'EOF' not in line:
                lower_tri += line[:-1]
                line = f.readline()

array = np.zeros((dimension, dimension))

lower_tri = [int(x) for x in list(filter(None, lower_tri.split(" ")))]

count = 0
for i in range(dimension, 0, -1):
    for j in range(0, dimension - i + 1):
        array[dimension - i][j] = lower_tri[count]
        array[j][dimension - i] = lower_tri[count]
        count += 1

pprint(array)
