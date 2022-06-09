# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'end_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(505, 222)
        Dialog.setMinimumSize(QtCore.QSize(505, 222))
        Dialog.setMaximumSize(QtCore.QSize(505, 222))
        Dialog.setStyleSheet("QLabel{font:600 16pt \"FreeMono\" bold;\n"
"                    color: white}\n"
"QDialog{background-color: gray}\n"
"QPushButton{font:600 15pt \"FreeMono\" bold; color: white; background-color: gray}\n"
"")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(30, 130, 201, 61))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 10, 471, 91))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(270, 130, 201, 61))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Збереження"))
        self.pushButton.setText(_translate("Dialog", "Так"))
        self.label.setText(_translate("Dialog", "Вітаю, ви розвʼязали пазл!\n"
"Зберегти результат у файл?"))
        self.pushButton_2.setText(_translate("Dialog", "Ні"))

