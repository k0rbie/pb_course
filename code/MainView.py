from face import Ui_MainWindow
from DialogView import StartDialogView
from PyQt5.QtWidgets import QMainWindow
from functools import partial
from Constants import *
import MainController


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
        self.lock_solver()
        self.connect_button(self.ui.pushButton_17, self.controller.new_game_pushed)
        self.connect_cells()

    def connect_cells(self):
        for cell in self.cells:
            cell.clicked.connect(partial(self.cell_move_pushed, cell))

    def cell_ind(self, cell):
        return self.cells.index(cell)

    def set_cell(self, button, value):
        button.setText(str(value).replace(str(FIELD_SIZE), ""))
        if value == FIELD_SIZE:
            button.setFlat(True)
        else:
            button.setFlat(False)

    def update_field(self, values):
        for button, value in zip(self.cells, values):
            self.set_cell(button, value)

    def switch_to_reorder(self):
        for cell in self.cells:
            cell.disconnect()
            cell.clicked.connect(partial(self.controller.chose_reorder, self.cell_ind(cell)))
            cell.setFlat(False)
        self.lock_solver()

    def switch_to_move(self):
        for cell in self.cells:
            cell.disconnect()
            cell.clicked.connect(partial(self.cell_move_pushed, cell))

    def swap_text(self, ind1, ind2):
        cell1 = self.cells[ind1]
        cell2 = self.cells[ind2]
        saved = cell1.text()
        cell1.setText(cell2.text())
        cell2.setText(saved)

    def ordered_start(self):
        self.disconnect_button(self.ui.pushButton_17)
        self.ui.pushButton_17.setText("Змініть\nрозташування")

    def enable_start(self):
        self.disconnect_button(self.ui.pushButton_17)
        self.connect_button(self.ui.pushButton_17, self.controller.end_reorder)
        self.ui.pushButton_17.setText("Розпочати")

    def block_start(self):
        self.disconnect_button(self.ui.pushButton_17)
        self.ui.pushButton_17.setText("Немає\nрозвʼязку")

    def finish_reorder(self):
        self.ui.pushButton_17.disconnect()
        self.connect_button(self.ui.pushButton_17, self.controller.new_game_pushed)
        self.ui.pushButton_17.setText("Нова гра")
        self.switch_to_move()

    def solver_start(self):
        self.ui.pushButton_19.setText("Зупинити")

    def solver_end(self):
        self.ui.pushButton_19.setText("Автоматичне\nрозвʼязування")

    def timer_update(self, sec_count):
        self.ui.label_4.setText(f"{sec_count//MIN_TO_SEC:02}:{sec_count%MIN_TO_SEC:02}")

    def moves_count_update(self, moves_count):
        self.ui.label_2.setText(str(moves_count))

    def connect_buttons(self):
        self.connect_button(self.ui.pushButton_17, self.controller.new_game_pushed)
        self.connect_button(self.ui.pushButton_18, self.controller.step_pushed)
        self.connect_button(self.ui.pushButton_19, self.controller.switch_solver)

    def disconnect_buttons(self):
        self.disconnect_button(self.ui.pushButton_17)
        self.disconnect_button(self.ui.pushButton_18)
        self.disconnect_button(self.ui.pushButton_19)

    def connect_button(self, button, slot):
        button.clicked.connect(slot)
        button.setStyleSheet("")

    def disconnect_button(self, button):
        try:
            button.disconnect()
            button.setStyleSheet("color: rgb(119, 118, 123); background-color: rgb(192, 191, 188);")
        except TypeError:  # повертає помилку, якщо жодний сигнал не підключено
            pass

    def cell_move_pushed(self, cell):
        self.controller.try_move_cell(self.cell_ind(cell))

    def switch_flat(self, ind):
        cell = self.cells[ind]
        cell.setFlat(not cell.isFlat())

    def victory(self):
        self.cells[-1].setText("🐸")
        self.lock_solver()

    def remove_frog(self, ind):
        self.cells[ind].setText("")

    def unlock_solver(self):
        self.connect_button(self.ui.pushButton_18, self.controller.step_pushed)
        self.connect_button(self.ui.pushButton_19, self.controller.switch_solver)

    def lock_solver(self):
        self.disconnect_button(self.ui.pushButton_18)
        self.disconnect_button(self.ui.pushButton_19)
