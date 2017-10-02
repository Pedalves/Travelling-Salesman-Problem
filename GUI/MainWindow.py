from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from threading import Thread
import numpy as np
import time

from GeneticAlgorithm.GeneticAlgorithm import GeneticAlgorithm
from GeneticAlgorithm.Individual import Individual
from GUI.MapView import MapView


class MainWindow(QMainWindow):
    """
    Classe responsavel que GUI
    """

    _finishSignal = pyqtSignal(name='finish')
    _pathSignal = pyqtSignal(dict, name='path')

    _defaultTSPPath = 'resources/gr17.tsp'
    _defaultSOLPath = 'solutions/gr17py.sol'

    def __init__(self):
        super(MainWindow, self).__init__()

        self._max_generations = 100

        self.resize(400, 500)
        self.setWindowTitle("Genetic Algorithm")

        self._finishSignal.connect(self._on_finish)
        self._pathSignal.connect(self._on_path_updated)

        self._progress_bar = QProgressBar()
        self._result_text_edit = QTextEdit()
        self._file_button = QPushButton('...')
        self._start_button = QPushButton('Start')

        self._map_view = MapView()

        self._change_file(self._defaultTSPPath)

        self._setup_ui()

        self.show()

    @pyqtSlot()
    def _on_finish(self):
        self._result_text_edit.append('Time: {}'.format(time.time()-self._time_start))
        self._progress_bar.setVisible(False)
        self._file_button.setEnabled(True)
        self._start_button.setEnabled(True)

        try:
            with open(self._solution_line_edit.text(), 'w') as f:
                f.write(str(self._result['Cost']))
                path = '\n'
                for city in self._result['Path']:
                    path += str(city) + ' '
                f.write(path)

                f.close()
        except:
            pass

    @pyqtSlot(dict)
    def _on_path_updated(self, path):
        result = 'Best Path: {}\nGeneration: {}\nCost: {}'.format(path['Path'], path['Generation'], path['Cost'])
        self._result_text_edit.setText(result)
        self._map_view.update_path(path['Path'])

        self._result = path

    def _finish(self):
        self._finishSignal.emit()

    def _update_path(self, path):
        self._pathSignal.emit(path)

    def _setup_ui(self):
        window = QWidget(self)

        file_label = QLabel('File: ')
        file_line_edit = QLineEdit()
        file_line_edit.setReadOnly(True)
        file_line_edit.setText(self._defaultTSPPath)

        self._file_button.setFixedWidth(50)

        def on_file_pressed():
            try:
                result = QFileDialog.getOpenFileName(None, 'Select TSP file', filter='*.tsp')

                if len(result[0]) > 0:
                    file_line_edit.setText(result[0])
                    self._change_file(file_line_edit.text())
            except:
                pass

        self._file_button.pressed.connect(on_file_pressed)

        file_layout = QHBoxLayout()
        file_layout.addWidget(file_label)
        file_layout.addWidget(file_line_edit)
        file_layout.addWidget(self._file_button)

        solution_label = QLabel('Save: ')
        self._solution_line_edit = QLineEdit()
        self._solution_line_edit.setReadOnly(True)
        self._solution_line_edit.setText(self._defaultSOLPath)

        solution_button = QPushButton('...')
        solution_button.setFixedWidth(50)

        def on_solution_pressed():
            try:
                result = QFileDialog.getOpenFileName(None, 'Select SOL file', filter='*.sol')

                if len(result[0]) > 0:
                    self._solution_line_edit.setText(result[0])
            except:
                pass

        solution_button.pressed.connect(on_solution_pressed)

        solution_layout = QHBoxLayout()
        solution_layout.addWidget(solution_label)
        solution_layout.addWidget(self._solution_line_edit)
        solution_layout.addWidget(solution_button)

        generations_label = QLabel("Generations: ")
        generations_line_edit = QLineEdit()
        generations_line_edit.setText(str(self._max_generations))

        def on_text_edited(text):
            try:
                self._max_generations = int(text)
            except:
                self._max_generations = 0

        generations_line_edit.textEdited.connect(on_text_edited)

        self._start_button.setFixedWidth(50)

        self._start_button.clicked.connect(self._start_function)

        generations_layout = QHBoxLayout()
        generations_layout.addWidget(generations_label)
        generations_layout.addWidget(generations_line_edit)
        generations_layout.addWidget(self._start_button)

        self._result_text_edit.setReadOnly(True)
        self._result_text_edit.setMaximumHeight(100)

        self._progress_bar.setTextVisible(False)
        self._progress_bar.setVisible(False)

        main_layout = QVBoxLayout(window)
        main_layout.addLayout(file_layout)
        main_layout.addLayout(solution_layout)
        main_layout.addLayout(generations_layout)
        main_layout.addWidget(self._result_text_edit)
        main_layout.addWidget(self._map_view)
        main_layout.addWidget(self._progress_bar)

        window.setLayout(main_layout)

        self.setCentralWidget(window)

    def _start_function(self):
        """
        Metodo responsavel por iniciar o algoritimo genetico em outra thread e iniciar a contagem de tempo
        :return:
        """
        self._file_button.setEnabled(False)
        self._start_button.setEnabled(False)

        self._progress_bar.setVisible(True)
        self._progress_bar.setMaximum(0)
        self._progress_bar.setMinimum(0)
        self._progress_bar.setValue(0)

        self._time_start = time.time()

        thr = Thread(target=lambda: GeneticAlgorithm(self._max_generations, callback=self._finish,
                                                     update_path=self._update_path).start())
        thr.start()

    def _change_file(self, tsp_file):
        """
        Metodo responsavel pela leitura do arquivo TSP
        :param tsp_file: Arquivo que sera lido
        :return:
        """
        lower_tri = ''

        is_lower = True

        with open(tsp_file) as f:
            line = ''
            while 'EOF' not in line:
                line = f.readline()
                if 'DIMENSION' in line:
                    Individual.dimension = int(line.split('DIMENSION: ')[1])
                if 'EDGE_WEIGHT_FORMAT' in line:
                    if 'UPPER_DIAG_ROW' in line:
                        is_lower = False
                elif 'EDGE_WEIGHT_SECTION' in line:
                    line = f.readline()
                    while 'EOF' not in line:
                        lower_tri += line[:-1] + ' '
                        line = f.readline()

        Individual.weight_matrix = np.zeros((Individual.dimension, Individual.dimension))

        lower_tri = [int(x) for x in list(filter(None, lower_tri.split(" ")))]
        count = 0

        if is_lower:
            for i in range(Individual.dimension, 0, -1):
                for j in range(0, Individual.dimension - i + 1):
                    Individual.weight_matrix[Individual.dimension - i][j] = lower_tri[count]
                    Individual.weight_matrix[j][Individual.dimension - i] = lower_tri[count]
                    count += 1

        else:
            for i in range(0, Individual.dimension):
                for j in range(i, Individual.dimension):
                    Individual.weight_matrix[i][j] = lower_tri[count]
                    Individual.weight_matrix[j][i] = lower_tri[count]
                    count += 1

        self._map_view.update_cities()
