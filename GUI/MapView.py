from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import random

from GeneticAlgorithm.Individual import Individual


class MapView(QWidget):
    """
    Classe responsavel pelo grafo desenhado na GUI
    """

    def __init__(self, parent=None):
        super(MapView, self).__init__(parent)

        self.setGeometry(300, 300, 300, 190)

        self._cities = []
        self._path = None

        self._setup_ui()

    def _setup_ui(self):
        self.setGeometry(300, 300, 300, 190)

        self.update_cities()

    def update_cities(self):
        self._cities.clear()
        self._path = None

        size = self.size()
        for _ in range(Individual.dimension):
            x = random.randint(1, size.width() - 1)
            y = random.randint(1, size.height() - 1)

            self._cities.append((x, y))

    def paintEvent(self, e):
        qp = QPainter()

        qp.begin(self)

        qp.setPen(QPen(Qt.red, 5, Qt.SolidLine))
        for i in range(Individual.dimension):
            qp.drawPoint(self._cities[i][0], self._cities[i][1])

        if self._path:
            qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))
            for i in range(len(self._cities)):
                qp.drawLine(self._cities[self._path[i-1]][0], self._cities[self._path[i-1]][1],
                            self._cities[self._path[i]][0], self._cities[self._path[i]][1])

        qp.end()

    def update_path(self, path):
        self._path = path
        self.update()

