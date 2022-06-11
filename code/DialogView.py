from UiStartDialog import UiStartDialog
from UiEndDialog import UiEndDialog
from PyQt5.QtWidgets import QDialog


class StartDialogView(QDialog):
    def __init__(self, controller):
        super(StartDialogView, self).__init__()
        self.__controller = controller

        self.__ui = UiStartDialog()
        self.__ui.setupUi(self)

        self.__ui.pushButton.clicked.connect(self.close)
        self.__ui.pushButton_2.clicked.connect(self.close)
        self.__ui.pushButton.clicked.connect(self.__controller.random_reorder)
        self.__ui.pushButton_2.clicked.connect(self.__controller.user_reorder)


class EndDialogView(QDialog):
    def __init__(self, controller):
        super(EndDialogView, self).__init__()
        self.__controller = controller

        self.__ui = UiEndDialog()
        self.__ui.setupUi(self)

        self.__ui.pushButton.clicked.connect(self.close)
        self.__ui.pushButton_2.clicked.connect(self.close)
        self.__ui.pushButton.clicked.connect(self.__controller.save_to_file)
