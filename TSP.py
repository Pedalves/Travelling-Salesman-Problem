from PyQt5.QtWidgets import QApplication
import sys

from GUI.MainWindow import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    t = MainWindow()
    sys.exit(app.exec_())
