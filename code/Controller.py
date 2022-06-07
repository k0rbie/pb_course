import sys
import time

from Field import Field
from Solver import Solver
from face import Ui_MainWindow
from StartDialogCtrl import StartDialogCtrl
from random import shuffle
from PyQt5 import QtGui  # QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtCore import QTimer, QTime, Qt
from solvability import *
from functools import partial
from Constants import *


class Controller(QMainWindow):
    def __init__(self):
        super(Controller, self).__init__()
        self.field = Field()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.start_dialog = StartDialogCtrl()
        self.connect_start_dialog()
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
        self.connect_cells()

        self.reorder_cell = None

    def connect_cells(self):
        for cell in self.cells:
            cell.clicked.connect(partial(self.try_to_move, cell))

    def switch_to_reorder(self):
        for cell in self.cells:
            cell.clicked.disconnect()
            cell.clicked.connect(partial(self.chose_reorder, cell))

    def switch_to_move(self):
        for cell in self.cells:
            cell.clicked.disconnect()
            cell.clicked.connect(partial(self.try_to_move, cell))

    def chose_reorder(self, cell):
        if self.reorder_cell:
            start_invar = self.field.invar()
            self.reorder(self.reorder_cell, cell)
            self.reorder_cell.setFlat(False)
            self.reorder_cell = None
            if self.field.invar() != start_invar:
                self.switch_start(not start_invar)
        else:
            cell.setFlat(True)
            self.reorder_cell = cell

    def switch_start(self, key):
        if key:
            self.enable_start()
        else:
            self.block_start()

    def enable_start(self):
        self.ui.pushButton_17.clicked.connect(self.end_reorder)
        self.ui.pushButton_17.setText("Розпочати")

    def block_start(self):
        self.ui.pushButton_17.clicked.disconnect()
        self.ui.pushButton_17.setText("Немає\nрозвʼязку")

    def connect_buttons(self):
        self.ui.pushButton_17.clicked.connect(self.new_game_pushed)
        self.ui.pushButton_18.clicked.connect(self.step_pushed)
        self.ui.pushButton_19.clicked.connect(self.solve_pushed)

    def new_game_pushed(self):
        self.reset_game()
        self.start_dialog.exec()

    def connect_start_dialog(self):
        self.start_dialog.ui.pushButton.clicked.connect(self.random_reorder)
        self.start_dialog.ui.pushButton_2.clicked.connect(self.user_reorder)

    def random_reorder(self):
        self.gen_valid()
        self.update_field()
        self.start_game()

    def user_reorder(self):
        self.switch_to_reorder()
        self.cells[self.field.space].setFlat(False)
        self.ui.pushButton_17.clicked.disconnect()
        self.ui.pushButton_18.clicked.disconnect()
        self.ui.pushButton_19.clicked.disconnect()
        self.enable_start()

    def start_game(self):
        self.generate_solution()
        self.timer_start()

    def reset_game(self):
        self.turn_off_solver()
        self.timer.stop()
        self.moves_count = -1
        self.moves_update()
        self.sec_count = -1
        self.time_update()

    def end_game(self):
        self.turn_off_solver()
        if self.timer.isActive():
            self.cells[-1].setText("🐸")
            self.timer.stop()

    def try_to_move(self, cell):
        change = self.cells.index(cell) - self.field.space
        if change in (-1, +1, -4, +4):
            self.make_space_swap(change)
            if not self.timer.isActive() or change != self.solution.pop(0):
                self.generate_solution()
            if self.check_if_solved():
                self.end_game()

    def check_if_solved(self):
        return not self.solution

    def end_reorder(self):
        self.cells[self.field.space].setFlat(True)
        self.ui.pushButton_17.clicked.disconnect()
        self.connect_buttons()
        self.ui.pushButton_17.setText("Нова гра")
        self.switch_to_move()
        self.start_game()

    def timer_start(self):
        self.timer.start(SEC_TO_MS)

    def time_update(self):
        self.sec_count += 1
        self.ui.label_4.setText(f"{self.sec_count//MIN_TO_SEC:02}:{self.sec_count%MIN_TO_SEC:02}")

    def moves_update(self):
        self.moves_count += 1
        self.ui.label_2.setText(str(self.moves_count))

    def gen_valid(self):
        self.shuffle_arr()
        if not self.field.invar():
            new_x = (self.field.space_x + 2) % FIELD_SIDE
            new_y = self.field.space_y
            swap_ind = new_x + FIELD_SIDE * new_y
            self.field.two_elements_swap(swap_ind, self.field.space)

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
        self.solution_timer.start(SOLVER_INT)
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
        if self.solution:
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

    def reorder(self, cell1, cell2):
        ind1 = self.cells.index(cell1)
        ind2 = self.cells.index(cell2)
        self.field.two_elements_swap(ind1, ind2)
        saved = cell1.text()
        cell1.setText(cell2.text())
        cell2.setText(saved)
