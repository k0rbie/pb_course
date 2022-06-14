from UiMainWindow import UiMainWindow
from PyQt5.QtWidgets import QMainWindow
from functools import partial
from Constants import *


class MainView(QMainWindow):
    def __init__(self, controller):
        super(MainView, self).__init__()
        self.__controller = controller

        self.__ui = UiMainWindow()
        self.__ui.setupUi(self)

        self.__cells = [self.__ui.pushButton,
                        self.__ui.pushButton_2,
                        self.__ui.pushButton_3,
                        self.__ui.pushButton_4,
                        self.__ui.pushButton_5,
                        self.__ui.pushButton_6,
                        self.__ui.pushButton_7,
                        self.__ui.pushButton_8,
                        self.__ui.pushButton_9,
                        self.__ui.pushButton_10,
                        self.__ui.pushButton_11,
                        self.__ui.pushButton_12,
                        self.__ui.pushButton_13,
                        self.__ui.pushButton_14,
                        self.__ui.pushButton_15,
                        self.__ui.pushButton_16,
                        ]
        self.__start_button = self.__ui.pushButton_17
        self.__step_button = self.__ui.pushButton_18
        self.__solver_button = self.__ui.pushButton_19

        self.__hint_label = self.__ui.label_5
        self.__moves_label = self.__ui.label_2
        self.__time_label = self.__ui.label_4

        self.set_hint(START_GAME_HINT)
        self.lock_solver()
        self.__connect_button(self.__ui.pushButton_17, self.__controller.chose_start)
        self.__connect_cells(self.__controller.try_move_cell)

    def __connect_cells(self, slot):   # Підключення сигналів кнопок до методу
        for cell in self.__cells:
            cell.pressed.connect(partial(slot, self.__cells.index(cell)))

    def __disconnect_cells(self):      # Відключення методів від кнопок
        for cell in self.__cells:
            cell.disconnect()

    def update_field(self, values):     # оновлення поля
        for button, value in zip(self.__cells, values):
            button.setText(str(value).replace(str(FIELD_SIZE), ""))

    def switch_to_reorder(self, space_ind):  # Перемикання у режим користувацького задавання поля
        self.__disconnect_cells()
        self.__connect_cells(self.__controller.chose_reorder_cell)
        self.__cells[space_ind].setFlat(False)

    def switch_to_move(self):       # Перемикання у режим переміщення
        self.__disconnect_cells()
        self.__connect_cells(self.__controller.try_move_cell)

    def swap_text(self, ind1, ind2):    # Обмін текстом між кнопками
        cell1 = self.__cells[ind1]
        cell2 = self.__cells[ind2]
        saved = cell1.text()
        cell1.setText(cell2.text())
        cell2.setText(saved)

    def enable_start(self):     # увімкнення можливості почати гру
        self.__connect_button(self.__start_button, self.__controller.end_reorder)

    def block_start(self):  # блокування можливості почати гри
        self.__disconnect_button(self.__start_button)

    def finish_reorder(self):   # вихід із режиму користувацького задавання поля
        self.__connect_button(self.__start_button, self.__controller.chose_start)
        self.switch_to_move()

    def solver_start(self):  # зміна тексту кнопки автоматичного розвʼязування при його увімкненні
        self.__solver_button.setText(OFF_SOLVER_BUTTON)

    def solver_end(self):  # зміна тексту кнопки автоматичного розвʼязування при його вимиканні
        self.__solver_button.setText(ON_SOLVER_BUTTON)

    def moves_count_update(self, moves_count):  # оновлення тексту лічильника кроків
        self.__moves_label.setText(str(moves_count))

    def timer_update(self, sec_count):  # оновлення відображення таймера
        self.__time_label.setText(f"{sec_count // MIN_TO_SEC:02}:{sec_count % MIN_TO_SEC:02}")

    def connect_buttons(self):  # підключення кнопок інтерфейсу
        self.__connect_button(self.__start_button, self.__controller.chose_start)
        self.__connect_button(self.__step_button, self.__controller.make_solution_step)
        self.__connect_button(self.__solver_button, self.__controller.switch_solver)

    def __connect_button(self, button, slot):  # підключення окремої кнопки
        self.__disconnect_button(button)
        button.clicked.connect(slot)
        button.setStyleSheet("")

    @staticmethod
    def __disconnect_button(button):  # відключення кнопки
        try:
            button.disconnect()  # повертає помилку, якщо жодний сигнал не підключено
            button.setStyleSheet(BLOCKED_STYLESHEET)
        except TypeError:
            pass

    def switch_flat(self, ind):  # перемикає стан Flat кнопки
        cell = self.__cells[ind]
        cell.setFlat(not cell.isFlat())

    def set_frog(self):  # змінює текст порожньої клітинки
        self.__cells[-1].setText(FROG)

    def remove_frog(self, ind):  # прибирає текст порожньої клітинки
        self.__cells[ind].setText("")

    def connect_solver(self):  # підключення кнопок розвʼязування
        self.__connect_button(self.__step_button, self.__controller.step_pushed)
        self.__connect_button(self.__solver_button, self.__controller.switch_solver)

    def lock_solver(self):  # підключення кнопок розвʼязування
        self.__disconnect_button(self.__step_button)
        self.__disconnect_button(self.__solver_button)

    def set_hint(self, text):  # зміна тексту напису-підказки
        self.__hint_label.setText(text)
