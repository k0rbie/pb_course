import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow

from Controller import Controller
import timeit


def main():
    app = QApplication(sys.argv)
    ctrl = Controller(side)
    ctrl.show()
    app.exec()


if __name__ == '__main__':
    side = 4
    main()
    # print(timeit.timeit(main, number=1))
