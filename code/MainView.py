from face import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow
from functools import partial
from Constants import *


class MainView(QMainWindow):
    def __init__(self, controller):
        super(MainView, self).__init__()
        self.controller = controller

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
        self.start_button = self.ui.pushButton_17
        self.step_button = self.ui.pushButton_18
        self.solver_button = self.ui.pushButton_19

        self.hint_label = self.ui.label_5
        self.moves_label = self.ui.label_2
        self.time_label = self.ui.label_4

        self.hint_start_game()
        self.lock_solver()
        self.connect_button(self.ui.pushButton_17, self.controller.new_game_pushed)
        self.connect_cells(self.controller.try_move_cell)

    def connect_cells(self, slot):
        for cell in self.cells:
            cell.clicked.connect(partial(slot, self.cell_ind(cell)))

    def disconnect_cells(self):
        for cell in self.cells:
            cell.disconnect()

    def cell_ind(self, cell):
        return self.cells.index(cell)

    @staticmethod
    def set_cell(button, value):
        button.setText(str(value).replace(str(FIELD_SIZE), ""))
        if value == FIELD_SIZE:
            button.setFlat(True)
        else:
            button.setFlat(False)

    def update_field(self, values):
        for button, value in zip(self.cells, values):
            self.set_cell(button, value)

    def switch_to_reorder(self, space_ind):
        self.disconnect_cells()
        self.connect_cells(self.controller.chose_reorder)
        self.cells[space_ind].setFlat(False)
        self.lock_solver()

    def switch_to_move(self):
        self.disconnect_cells()
        self.connect_cells(self.controller.try_move_cell)

    def swap_text(self, ind1, ind2):
        cell1 = self.cells[ind1]
        cell2 = self.cells[ind2]
        saved = cell1.text()
        cell1.setText(cell2.text())
        cell2.setText(saved)

    def ordered_start(self):
        self.disconnect_button(self.start_button)

    def enable_start(self):
        self.disconnect_button(self.start_button)
        self.connect_button(self.start_button, self.controller.end_reorder)

    def block_start(self):
        self.disconnect_button(self.start_button)

    def finish_reorder(self):
        self.start_button.disconnect()
        self.connect_button(self.start_button, self.controller.new_game_pushed)
        self.switch_to_move()

    def solver_start(self):
        self.solver_button.setText(OFF_SOLVER_BUTTON)

    def solver_end(self):
        self.solver_button.setText(ON_SOLVER_BUTTON)

    def moves_count_update(self, moves_count):
        self.moves_label.setText(str(moves_count))

    def timer_update(self, sec_count):
        self.time_label.setText(f"{sec_count//MIN_TO_SEC:02}:{sec_count%MIN_TO_SEC:02}")

    def connect_buttons(self):
        self.connect_button(self.start_button, self.controller.new_game_pushed)
        self.connect_button(self.step_button, self.controller.step_pushed)
        self.connect_button(self.solver_button, self.controller.switch_solver)

    def disconnect_buttons(self):
        self.disconnect_button(self.start_button)
        self.disconnect_button(self.step_button)
        self.disconnect_button(self.solver_button)

    @staticmethod
    def connect_button(button, slot):
        button.clicked.connect(slot)
        button.setStyleSheet("")

    @staticmethod
    def disconnect_button(button):
        try:
            button.disconnect()  # повертає помилку, якщо жодний сигнал не підключено
            button.setStyleSheet(BLOCKED_STYLESHEET)
        except TypeError:
            pass

    def switch_flat(self, ind):
        cell = self.cells[ind]
        cell.setFlat(not cell.isFlat())

    def victory(self):
        self.cells[-1].setText(FROG)
        self.lock_solver()

    def remove_frog(self, ind):
        self.cells[ind].setText("")

    def begin_game(self):
        self.connect_button(self.step_button, self.controller.step_pushed)
        self.connect_button(self.solver_button, self.controller.switch_solver)

    def lock_solver(self):
        self.disconnect_button(self.step_button)
        self.disconnect_button(self.solver_button)

    def hint_start_game(self):
        self.hint_label.setText(START_GAME_HINT)

    def hint_rebase(self):
        self.hint_label.setText(REBASE_HINT_TEXT)

    def hint_unsolvable(self):
        self.hint_label.setText(UNSOLVABLE_HINT_TEXT)

    def hint_sorted(self):
        self.hint_label.setText(SORTED_HINT_TEXT)

    def hint_ingame(self):
        self.hint_label.setText(INGAME_HINT)

    def hint_solver(self):
        self.hint_label.setText(SOLVER_HINT)
