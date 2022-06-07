import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow

from MainView import MainView
import timeit


def main():
    app = QApplication(sys.argv)
    ctrl = MainView()
    ctrl.show()
    app.exec()


if __name__ == '__main__':
    main()
