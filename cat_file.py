# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cat_file.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CatF(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(558, 312)
        self.cflistWidget = QtWidgets.QListWidget(Dialog)
        self.cflistWidget.setGeometry(QtCore.QRect(10, 10, 541, 241))
        self.cflistWidget.setObjectName("cflistWidget")
        self.cfpushButton = QtWidgets.QPushButton(Dialog)
        self.cfpushButton.setGeometry(QtCore.QRect(10, 260, 541, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.cfpushButton.setFont(font)
        self.cfpushButton.setObjectName("cfpushButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.cfpushButton.setText(_translate("Dialog", "Main Menu"))
