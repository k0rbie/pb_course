import sys
from Field import Field
from Solver import Solver
from face import Ui_MainWindow
from random import shuffle
from PyQt5 import QtGui  # QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from solvability import *


class Controller(QMainWindow):
    def __init__(self, side):
        super(Controller, self).__init__()
        self.field = Field(side)
        self.solver = Solver(self.field)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.cells = [self.ui.pushButton,
                      self.ui.pushButton_2,
                      self.ui.pushButton_3,
                      self.ui.pushButton_4,
                      self.ui.pushButton_5,
                      self.ui.pushButton_6,
                      self.ui.pushButton_7,
                      self.ui.pushButton_8,
                      self.ui.pushButton_9,
                      self.ui.pushButton_10,
                      self.ui.pushButton_11,
                      self.ui.pushButton_12,
                      self.ui.pushButton_13,
                      self.ui.pushButton_14,
                      self.ui.pushButton_15,
                      self.ui.pushButton_16,
                      ]
        self.ui.pushButton_17.clicked.connect(self.new_game_pushed)

    def new_game_pushed(self):
        self.gen_valid()
        self.display()

    def gen_valid(self):
        self.shuffle_arr()
        if not self.field.invar():
            new_x = (self.field.space_x + 2) % self.field.side
            new_y = self.field.space_y
            swap_ind = new_x + self.field.side * new_y
            self.field.arr[swap_ind], self.field.arr[self.field.space] =\
                self.field.arr[self.field.space], self.field.arr[swap_ind]
            self.field.space = swap_ind
            self.field.update_space_coords()
            self.field.invar()

    def shuffle_arr(self):
        shuffle(self.field.arr)
        self.field.find_space()

    def display(self):
        for button, value in zip(self.cells, self.field.arr):
            if value == 16:
                button.setText("  ")
                button.setFlat(True)
            else:
                button.setText(str(value))
                button.setFlat(False)

    def swap(self, space, change):
        temp = self.cells[space].text()
        self.cells[space].setText(self.cells[space+change].text())
        self.cells[space+change].setText(temp)
        self.cells[space+change].setFlat(True)
        self.cells[space].setFlat(False)
