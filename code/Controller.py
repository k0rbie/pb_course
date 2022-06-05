import sys
import time

from Field import Field
from Solver import Solver
from face import Ui_MainWindow
from random import shuffle
from PyQt5 import QtGui  # QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer, QTime, Qt
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
        self.solution = []
        self.solution_timer = QTimer(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.time_update)
        self.ui.pushButton_17.clicked.connect(self.new_game_pushed)
        self.ui.pushButton_18.clicked.connect(self.step_pushed)
        self.ui.pushButton_19.clicked.connect(self.solve_pushed)

    def new_game_pushed(self):
        self.gen_valid()
        self.update_field()
        self.time_start()

    def time_start(self):
        self.timer.start(1000)
        self.ui.label_4.setText("0")

    def time_update(self):
        self.ui.label_4.setText(str(int(self.ui.label_4.text())+1))

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

    def step_pushed(self):
        for i in range(1, 11):
            self.ui.label_4.setText(str(i))
            time.sleep(0.5)

    def solve_pushed(self):
        self.solver = Solver(self.field)
        self.solution = self.solver.solve()
        self.solution_timer.timeout.connect(self.show_solution_step)
        self.solution_timer.start(500)
        # for move in solution:
        #     self.field.space_swap(move)
        #     self.show_swap(self.field.space - move, move)
        # self.update_field()

    def show_solution_step(self):
        if len(self.solution):
            move = self.solution.pop(0)
            # self.show_swap(self.field.space - move, move)
            self.update_field()
        else:
            self.solution_timer.stop()

    def update_field(self):
        for button, value in zip(self.cells, self.field.arr):
            if value == 16:
                button.setText("  ")
                button.setFlat(True)
            else:
                button.setText(str(value))
                button.setFlat(False)
        # time.sleep(0.5)

    def show_swap(self, space, change):
        temp = self.cells[space].text()
        self.cells[space].setText(self.cells[space+change].text())
        self.cells[space+change].setText(temp)
        self.cells[space+change].setFlat(True)
        self.cells[space].setFlat(False)
