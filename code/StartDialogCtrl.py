from start_dialog import Ui_Dialog as Ui_Start_Dialog
from PyQt5.QtWidgets import QDialog


class StartDialogCtrl(QDialog):
    def __init__(self):
        super(StartDialogCtrl, self).__init__()
        self.ui = Ui_Start_Dialog()
        self.ui.setupUi(self)
        self.custom_value = 0
        self.ui.pushButton.clicked.connect(self.close)
        self.ui.pushButton_2.clicked.connect(self.close)
