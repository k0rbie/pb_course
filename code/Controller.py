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
from functools import partial


class Controller(QMainWindow):
    def __init__(self, side):
        super(Controller, self).__init__()
        self.field = Field(side)
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
        self.solver = Solver(self.field)
        self.solution = []
        self.solution_timer = QTimer(self)
        self.solution_timer.timeout.connect(self.make_solution_step)

        self.sec_count = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.time_update)
        self.moves_count = 0

        self.connect_buttons()

    def connect_buttons(self):
        for cell in self.cells:
            cell.clicked.connect(partial(self.try_to_move, cell))

        self.ui.pushButton_17.clicked.connect(self.new_game_pushed)
        self.ui.pushButton_18.clicked.connect(self.step_pushed)
        self.ui.pushButton_19.clicked.connect(self.solve_pushed)

    def try_to_move(self, cell):
        change = self.cells.index(cell) - self.field.space
        if change in (-1, +1, -4, +4):
            self.make_space_swap(change)
            if not self.timer.isActive() or change != self.solution.pop(0):
                self.generate_solution()
            if self.check_if_solved():
                self.end_game()

    def check_if_solved(self):
        return not len(self.solution)

    def end_game(self):
        self.turn_off_solver()
        if self.timer.isActive():
            self.cells[-1].setText("🐸")
            self.timer.stop()

    def new_game_pushed(self):
        self.gen_valid()
        self.update_field()
        self.generate_solution()
        self.moves_count = -1
        self.moves_update()
        self.timer_start()
        self.turn_off_solver()

    def timer_start(self):
        self.sec_count = -1
        self.timer.start(1000)
        self.time_update()

    def time_update(self):
        self.sec_count += 1
        self.ui.label_4.setText(f"{self.sec_count//60:02}:{self.sec_count%60:02}")

    def moves_update(self):
        self.moves_count += 1
        self.ui.label_2.setText(str(self.moves_count))

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
        self.make_solution_step()

    def solve_pushed(self):
        self.switch_solver()

    def turn_off_solver(self):
        self.solution_timer.stop()
        self.ui.pushButton_19.setText("Автоматичне\nрозвʼязування")

    def turn_on_solver(self):
        self.solution_timer.start(80)
        self.ui.pushButton_19.setText("Зупинити")

    def switch_solver(self):
        if self.solution_timer.isActive():
            self.turn_off_solver()
        elif not self.check_if_solved():
            self.turn_on_solver()

    def generate_solution(self):
        self.solver = Solver(self.field)
        self.solution = self.solver.solve()

    def make_solution_step(self):
        print(self.solution)
        if len(self.solution):
            self.make_space_swap(self.solution.pop(0))
        if self.check_if_solved():
            self.end_game()

    def update_field(self):
        for button, value in zip(self.cells, self.field.arr):
            button.setText(str(value))
            button.setFlat(False)
        self.cells[self.field.space].setText("")
        self.cells[self.field.space].setFlat(True)

    def make_space_swap(self, change):
        self.field.space_swap(change)
        space = self.field.space
        self.cells[space-change].setFlat(False)
        self.cells[space-change].setText(self.cells[space].text())
        self.cells[space].setFlat(True)
        self.cells[space].setText("")
        self.moves_update()
