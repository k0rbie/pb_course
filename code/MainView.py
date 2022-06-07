from face import Ui_MainWindow
from StartDialogCtrl import StartDialogCtrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from functools import partial
from Constants import *
import MainController


class MainView(QMainWindow):
    def __init__(self):
        super(MainView, self).__init__()
        self.controller = MainController.MainController(self)
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

        self.connect_buttons()
        self.connect_cells()

    def connect_cells(self):
        for cell in self.cells:
            cell.clicked.connect(partial(self.cell_move_pushed, self.cell_ind(cell)))

    def cell_ind(self, cell):
        return self.cells.index(cell)

    def update_field(self, values):
        for button, value in zip(self.cells, values):
            button.setText(str(value))
            button.setFlat(False)
        self.cells[self.field.space].setText("")
        self.cells[self.field.space].setFlat(True)

    def swap_text(self, ind1, ind2):
        cell1 = self.cells[ind1]
        cell2 = self.cells[ind2]
        saved = cell1.text()
        cell1.setText(cell2.text())
        cell2.setText(saved)

    def switch_to_reorder(self):
        for cell in self.cells:
            cell.clicked.disconnect()
            cell.clicked.connect(partial(self.controller.chose_reorder, self.cell_ind(cell)))
            cell.setFlat(False)
        self.disconnect_buttons()
        self.enable_start()

    def switch_to_move(self):
        for cell in self.cells:
            cell.clicked.disconnect()
            cell.clicked.connect(partial(self.cell_move_pushed, cell))

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

    def disconnect_buttons(self):
        self.ui.pushButton_17.clicked.disconnect()
        self.ui.pushButton_18.clicked.disconnect()
        self.ui.pushButton_19.clicked.disconnect()

    def new_game_pushed(self):
        self.reset_game()
        self.start_dialog.exec()

    def connect_start_dialog(self):
        self.start_dialog.ui.pushButton.clicked.connect(self.random_reorder)
        self.start_dialog.ui.pushButton_2.clicked.connect(self.user_reorder)

    def cell_move_pushed(self, cell):
        self.controller.try_move_cell(self.cell_ind(cell))
