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
        self.__field = Field()

        self.__solver = None
        self.__initial_field = None
        self.__reorder_cell_ind = None

        self.__solution_is_valid = False
        self.__solution = []
        self.__solution_timer = QTimer()
        self.__solution_timer.timeout.connect(self.__make_solution_step)

        self.__moves_count = 0
        self.__sec_count = 0
        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__time_update)

        app = QApplication(sys.argv)
        self.__view = MainView(self)
        self.__start_dialog = StartDialogView(self)
        self.__end_dialog = EndDialogView(self)
        self.__view.show()
        app.exec()

    def try_move_cell(self, index):
        if self.__field.next_to_space(index):
            change = index - self.__field.space_ind
            self.__make_space_swap(change)
            if self.__timer.isActive():
                if self.__solution_is_valid and change != self.__solution.pop(0):
                    self.__solution_is_valid = False
                if self.__field.is_sorted():
                    self.__end_game()
                    self.__win_game()

    def random_reorder(self):
        self.__view.switch_flat(self.__field.space_ind)
        self.__field.shuffle_arr()
        if not self.__field.invar():
            new_x = (self.__field.space_x + 2) % FIELD_SIDE
            new_y = self.__field.space_y
            swap_ind = new_x + FIELD_SIDE * new_y
            self.__field.two_elements_swap(swap_ind, self.__field.space_ind)
        self.__view.update_field(self.__field.arr)
        self.__view.switch_flat(self.__field.space_ind)
        self.__start_game()

    def user_reorder(self):
        self.__view.switch_to_reorder(self.__field.space_ind)
        self.__update_rebase_view()

    def chose_reorder_cell(self, cell_ind):
        if self.__reorder_cell_ind is not None:
            self.__field.two_elements_swap(cell_ind, self.__reorder_cell_ind)
            self.__view.swap_text(cell_ind, self.__reorder_cell_ind)
            self.__view.switch_flat(self.__reorder_cell_ind)
            self.__reorder_cell_ind = None
            self.__update_rebase_view()
        else:
            self.__view.switch_flat(cell_ind)
            self.__reorder_cell_ind = cell_ind

    def __update_rebase_view(self):
        if self.__field.is_sorted():
            self.__view.block_start()
            self.__view.set_hint(SORTED_HINT_TEXT)
        elif self.__field.invar():
            self.__view.enable_start()
            self.__view.set_hint(REBASE_HINT_TEXT)
        else:
            self.__view.block_start()
            self.__view.set_hint(UNSOLVABLE_HINT_TEXT)

    def end_reorder(self):
        self.__view.switch_flat(self.__field.space_ind)
        self.__view.finish_reorder()
        self.__start_game()

    def __start_game(self):
        self.__view.connect_solver()
        self.__view.set_hint(INGAME_HINT)
        self.__initial_field = self.__field.matrix_view()
        self.__timer.start(SEC_TO_MS)

    def __end_game(self):
        self.__turn_off_solver()
        self.__view.set_hint(START_GAME_HINT)
        self.__timer.stop()
        self.__view.lock_solver()

    def __win_game(self):
        self.__view.set_frog()
        self.__end_dialog.exec()

    def chose_start(self):
        if self.__timer.isActive():
            self.__end_game()
        else:
            self.__view.remove_frog(self.__field.space_ind)
        self.__moves_count = -1
        self.__moves_update()
        self.__sec_count = -1
        self.__time_update()
        self.__start_dialog.exec()

    def save_to_file(self):
        with open("results.txt", "a") as f:
            f.write(f"Час закінчення гри:   {strftime('%d.%m.%Y %H:%M:%S', localtime(time()))}\n")
            f.write(f"Кількість переміщень: {self.__moves_count}\n")
            f.write(f"Витрачений час:       {self.__sec_count} сек.\n")
            f.write(f"Початковий стан поля: \n{self.__initial_field}\n")

    def __time_update(self):
        self.__sec_count += 1
        self.__view.timer_update(self.__sec_count)

    def __moves_update(self):
        self.__moves_count += 1
        self.__view.moves_count_update(self.__moves_count)

    def __turn_off_solver(self):
        self.__solution_timer.stop()
        self.__view.solver_end()
        if self.__timer.isActive():
            self.__view.set_hint(INGAME_HINT)
        else:
            self.__view.set_hint(START_GAME_HINT)

    def __turn_on_solver(self):
        self.__validate_solution()
        self.__solution_timer.start(SOLVE_INTERVAL)
        self.__view.solver_start()
        self.__view.set_hint(SOLVER_HINT)

    def switch_solver(self):
        if self.__solution_timer.isActive():
            self.__turn_off_solver()
        else:
            self.__turn_on_solver()

    def __generate_solution(self):
        self.__solver = Solver(deepcopy(self.__field))
        self.__solution = self.__solver.solve()

    def __validate_solution(self):
        if not self.__solution_is_valid:
            self.__generate_solution()
            self.__solution_is_valid = True

    def step_pushed(self):
        self.__validate_solution()
        self.__make_solution_step()

    def __make_solution_step(self):
        self.__make_space_swap(self.__solution.pop(0))
        if not self.__solution:
            self.__end_game()
            self.__win_game()

    def __make_space_swap(self, change):
        self.__field.space_swap(change)
        space = self.__field.space_ind
        self.__view.swap_text(space, space - change)
        self.__view.switch_flat(space)
        self.__view.switch_flat(space - change)
        self.__moves_update()
