from Field import Field
from Solver import Solver
import MainView

from Constants import *
from PyQt5 import QtGui  # QtWidgets, QtCore
from solvability import *
from PyQt5.QtCore import QTimer, QTime, Qt


class MainController:
    def __init__(self, view: MainView):
        self.view = view
        self.field = Field()
        self.solver = Solver(self.field)

        self.reorder_cell_ind = None

        self.solution = []
        self.solution_timer = QTimer(self)
        self.solution_timer.timeout.connect(self.make_solution_step)

        self.sec_count = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.time_update)
        self.moves_count = 0

    def try_move_cell(self, index):
        change = index - self.field.space
        if change in (-1, +1, -4, +4):
            self.make_space_swap(change)
            if not self.timer.isActive() or change != self.solution.pop(0):
                self.generate_solution()
            if self.check_if_solved():
                self.end_game()

    def chose_reorder(self, cell_ind):
        if self.reorder_cell_ind is not None:
            start_invar = self.field.invar()
            self.reorder(self.reorder_cell_ind, cell_ind)
            self.reorder_cell_ind.setFlat(False)
            self.reorder_cell_ind = None
            if self.field.invar() != start_invar:
                self.switch_start(not start_invar)
        else:
            cell_ind.setFlat(True)
            self.reorder_cell_ind = cell_ind

    def reorder(self, ind1, ind2):
        self.field.two_elements_swap(ind1, ind2)
        self.view.swap_text(ind1, ind2)

    def switch_start(self, key):
        if key:
            self.view.enable_start()
        else:
            self.view.block_start()

    def random_reorder(self):
        self.gen_valid()
        self.view.update_field(self.field.arr)
        self.start_game()

    def gen_valid(self):
        self.field.shuffle_arr()
        if not self.field.invar():
            new_x = (self.field.space_x + 2) % FIELD_SIDE
            new_y = self.field.space_y
            swap_ind = new_x + FIELD_SIDE * new_y
            self.field.two_elements_swap(swap_ind, self.field.space)

    def user_reorder(self):
        self.view.switch_to_reorder()

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

    def make_space_swap(self, change):
        self.field.space_swap(change)
        space = self.field.space
        self.cells[space-change].setFlat(False)
        self.cells[space-change].setText(self.cells[space].text())
        self.cells[space].setFlat(True)
        self.cells[space].setText("")
        self.moves_update()
