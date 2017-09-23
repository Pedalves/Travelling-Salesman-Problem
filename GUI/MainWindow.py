from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from threading import Thread

from GeneticAlgorithm.GeneticAlgorithm import GeneticAlgorithm
from GUI.MapView import MapView


class MainWindow(QMainWindow):
    _finishSignal = pyqtSignal(name='finish')
    _pathSignal = pyqtSignal(dict, name='path')

    def __init__(self):
        super(MainWindow, self).__init__()

        self._max_generations = 30

        self.resize(400, 500)
        self.setWindowTitle("Genetic Algorithm")

        self._finishSignal.connect(self._on_finish)
        self._pathSignal.connect(self._on_path_updated)

        self._progress_bar = QProgressBar()
        self._result_text_edit = QTextEdit()

        self._setup_ui()

        self.show()

    @pyqtSlot()
    def _on_finish(self):
        self._progress_bar.setVisible(False)

    @pyqtSlot(dict)
    def _on_path_updated(self, path):
        result = 'Best Path: {}\nGeneration: {}\nCost: {}'.format(path['Path'], path['Generation'], path['Cost'])
        self._result_text_edit.setText(result)
        self._map_view.update_path(path['Path'])

    def _finish(self):
        self._finishSignal.emit()

    def _update_path(self, path):
        self._pathSignal.emit(path)

    def _setup_ui(self):
        window = QWidget(self)

        generations_label = QLabel("Generations: ")
        generations_line_edit = QLineEdit()
        generations_line_edit.setText(str(self._max_generations))

        def on_text_edited(text):
            self._max_generations = int(text)

        generations_line_edit.textEdited.connect(on_text_edited)

        generations_layout = QHBoxLayout()
        generations_layout.addWidget(generations_label)
        generations_layout.addWidget(generations_line_edit)

        start_button = QPushButton('Start')
        start_button.setFixedWidth(50)

        start_button.clicked.connect(self._start_function)

        self._result_text_edit.setReadOnly(True)
        self._result_text_edit.setMaximumSize(400, 50)

        self._map_view = MapView(window)

        self._progress_bar.setTextVisible(False)
        self._progress_bar.setVisible(False)

        main_layout = QVBoxLayout(window)
        main_layout.addLayout(generations_layout)
        main_layout.addWidget(start_button)
        main_layout.addWidget(self._result_text_edit)
        main_layout.addWidget(self._map_view)
        main_layout.addWidget(self._progress_bar)

        window.setLayout(main_layout)

        self.setCentralWidget(window)

    def _start_function(self):
        self._progress_bar.setVisible(True)
        self._progress_bar.setMaximum(0)
        self._progress_bar.setMinimum(0)
        self._progress_bar.setValue(0)

        thr = Thread(target=lambda: GeneticAlgorithm(self._max_generations, callback=self._finish,
                                                     update_path=self._update_path).start())
        thr.start()

