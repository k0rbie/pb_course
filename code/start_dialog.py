# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'start_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(505, 222)
        Dialog.setStyleSheet("QLabel{font:600 16pt \"FreeMono\" bold;\n"
"                    color: white}\n"
"QDialog{background-color: gray}\n"
"QPushButton{font:600 15pt \"FreeMono\" bold; color: white; background-color: gray}")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 10, 471, 91))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(30, 130, 201, 61))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(270, 130, 201, 61))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Задати поле"))
        self.label.setText(_translate("Dialog", "Оберіть спосіб задавання\n"
"стартового розташування"))
        self.pushButton.setText(_translate("Dialog", "Випадково"))
        self.pushButton_2.setText(_translate("Dialog", "Вручну"))

