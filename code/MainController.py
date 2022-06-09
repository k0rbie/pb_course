from Field import Field
from Solver import Solver
from Constants import *

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
from copy import deepcopy

from time import time, localtime, strftime
import sys

from MainView import MainView
from DialogView import StartDialogView, EndDialogView


class MainController:
    def __init__(self):
        self.field = Field()
        self.solver = Solver(deepcopy(self.field))

        self.initial_field = None
        self.reorder_cell_ind = None

        self.solution = []
        self.solution_timer = QTimer()
        self.solution_timer.timeout.connect(self.make_solution_step)

        self.moves_count = 0
        self.sec_count = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.time_update)

        self.start_enabled = False

        app = QApplication(sys.argv)
        self.view = MainView(self)
        self.start_dialog = StartDialogView(self)
        self.end_dialog = EndDialogView(self)
        self.view.show()
        app.exec()

    def try_move_cell(self, index):
        change = index - self.field.space_ind
        if self.field.next_to_space(index):
            self.make_space_swap(change)
            if not self.timer.isActive() or change != self.solution.pop(0):
                self.generate_solution()
            elif not self.solution:
                self.end_game()

    def user_reorder(self):
        self.view.switch_to_reorder()
        self.start_enabled = False
        self.update_rebase_view()

    def chose_reorder(self, cell_ind):
        if self.reorder_cell_ind is not None:
            self.reorder(self.reorder_cell_ind, cell_ind)
            self.view.switch_flat(self.reorder_cell_ind)
            self.reorder_cell_ind = None
            self.update_rebase_view()
        else:
            self.view.switch_flat(cell_ind)
            self.reorder_cell_ind = cell_ind

    def reorder(self, ind1, ind2):
        self.field.two_elements_swap(ind1, ind2)
        self.view.swap_text(ind1, ind2)

    def update_rebase_view(self):
        if self.start_enabled:
            self.view.disable_new_game()
            self.start_enabled = False
        if self.field.is_sorted():
            self.view.ordered_start()
        elif self.field.invar():
            self.view.enable_start()
            self.start_enabled = True
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
            self.field.two_elements_swap(swap_ind, self.field.space_ind)

    def start_game(self):
        self.initial_field = self.field.matrix_view()
        self.view.enable_solver()
        self.generate_solution()
        self.timer_start()

    def reset_game(self):
        if self.timer.isActive():
            self.timer.stop()
            self.solution_timer.stop()
            self.view.disable_solver()
        else:
            self.view.remove_frog(self.field.space_ind)
        self.moves_count = -1
        self.moves_update()
        self.sec_count = -1
        self.time_update()

    def end_game(self):
        self.turn_off_solver()
        if self.timer.isActive():
            self.view.victory()
            self.view.disable_solver()
            self.timer.stop()
            self.end_dialog.exec()
            #

    def save_to_file(self):
        with open("results.txt", "a") as f:
            f.write(f"Час закінчення гри:   {strftime('%d.%m.%Y %H:%M:%S', localtime(time()))}\n")
            f.write(f"Кількість переміщень: {self.moves_count}\n")
            f.write(f"Витрачений час:       {self.sec_count} сек.\n")
            f.write(f"Початковий стан поля: \n{self.initial_field}\n")

    def end_reorder(self):
        self.view.switch_flat(self.field.space_ind)
        self.view.finish_reorder()
        self.start_game()

    def timer_start(self):
        self.timer.start(SEC_TO_MS)

    def time_update(self):
        self.sec_count += 1
        self.view.timer_update(self.sec_count)

    def moves_update(self):
        self.moves_count += 1
        self.view.moves_count_update(self.moves_count)

    def new_game_pushed(self):
        self.reset_game()
        self.start_dialog.exec()

    def step_pushed(self):
        self.make_solution_step()

    def turn_off_solver(self):
        self.solution_timer.stop()
        self.view.solver_end()

    def turn_on_solver(self):
        self.solution_timer.start(SOLVE_INTERVAL)
        self.view.solver_start()

    def switch_solver(self):
        if self.solution_timer.isActive():
            self.turn_off_solver()
        elif self.solution:
            self.turn_on_solver()

    def generate_solution(self):
        self.solver = Solver(deepcopy(self.field))
        self.solution = self.solver.solve()

    def make_solution_step(self):
        self.make_space_swap(self.solution.pop(0))
        if not self.solution:
            self.end_game()

    def make_space_swap(self, change):
        self.field.space_swap(change)
        space = self.field.space_ind
        self.view.swap_text(space, space-change)
        self.view.switch_flat(space)
        self.view.switch_flat(space-change)
        self.moves_update()
