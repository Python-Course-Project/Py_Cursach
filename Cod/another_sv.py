# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'another_sv.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Save(object):
    def setupUi(self, Save):
        Save.setObjectName("Save")
        Save.resize(400, 320)
        self.another_s = QtWidgets.QTextEdit(Save)
        self.another_s.setGeometry(QtCore.QRect(0, 0, 401, 261))
        self.another_s.setObjectName("another_s")
        self.ansv_btn = QtWidgets.QPushButton(Save)
        self.ansv_btn.setGeometry(QtCore.QRect(10, 270, 371, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.ansv_btn.setFont(font)
        self.ansv_btn.setObjectName("ansv_btn")

        self.retranslateUi(Save)
        QtCore.QMetaObject.connectSlotsByName(Save)

    def retranslateUi(self, Save):
        _translate = QtCore.QCoreApplication.translate
        Save.setWindowTitle(_translate("Save", "Dialog"))
        self.ansv_btn.setText(_translate("Save", "Save"))