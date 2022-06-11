from UiStartDialog import UiStartDialog as Ui_Start_Dialog
from UiEndDialog import UiEndDialog as Ui_End_Dialog
from PyQt5.QtWidgets import QDialog


class StartDialogView(QDialog):
    def __init__(self, controller):
        super(StartDialogView, self).__init__()
        self.controller = controller

        self.ui = Ui_Start_Dialog()
        self.ui.setupUi(self)

        self.connect_buttons()

    def connect_buttons(self):
        self.ui.pushButton.clicked.connect(self.close)
        self.ui.pushButton_2.clicked.connect(self.close)
        self.ui.pushButton.clicked.connect(self.controller.random_reorder)
        self.ui.pushButton_2.clicked.connect(self.controller.user_reorder)


class EndDialogView(QDialog):
    def __init__(self, controller):
        super(EndDialogView, self).__init__()
        self.controller = controller

        self.ui = Ui_End_Dialog()
        self.ui.setupUi(self)

        self.connect_buttons()

    def connect_buttons(self):
        self.ui.pushButton.clicked.connect(self.close)
        self.ui.pushButton_2.clicked.connect(self.close)
        self.ui.pushButton.clicked.connect(self.controller.save_to_file)
