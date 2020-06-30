from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

from loging import Ui_Loging
from sign_up import Ui_Sign_up
from men_wn import Ui_Dialog
from main_wnd import Ui_wnd
from enter_f import Ui_filename
# from cat_m import Ui_Categ
import requests
import sys


# функция которое создает всплывающее окошко с предупреждением
def show_m(title, message):
    msBox = QtWidgets.QMessageBox()
    msBox.setIcon(QtWidgets.QMessageBox.Warning)
    msBox.setWindowTitle(title)
    msBox.setText(message)
    msBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msBox.exec_()


# функция меняющая ui
def change_w(w1, w2):
    w1.close()
    w2.show()


# классы импортированные ui с которыми происходит работа
class Loging_F(QtWidgets.QDialog, Ui_Loging):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

    def loginCheck(self, w1, w2):
        username1 = self.u_line.text()
        password1 = self.p_line.text()
        # param_req = {'username':'password'}
        # response = requests.get('',data=param_req)
        # if response:
        if len(username1) == 0:
            show_m('Warning', 'Empty Username')
        if len(password1) == 0:
            show_m('Warning', 'Empty Password')
        if len(password1) > 0 and len(username1) > 0:
            # self.windowz = QtWidgets.QDialog()
            # self.ui = Ui_wnd()
            # self.ui.setupUi(self.windowz)
            # self.windowz.show()
            change_w(w1, w2)

    def sign_btn(self, w1, w2):
        self.u_line.setText("")
        self.p_line.setText("")
        change_w(w1, w2)


class Sign_F(QtWidgets.QDialog, Ui_Sign_up):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

    def confirm_z(self, w1, w2):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        conf_password = self.lineEdit_3.text()
        if len(username) == 0:
            show_m('Warning', 'Empty Username')
        if len(password) == 0:
            show_m('Warning', 'Empty Password')
        if password != conf_password:
            show_m('Warning', 'Different Passwords')
        if len(password) > 0 and 0 < len(username) == len(conf_password):
            self.lineEdit.setText("")
            self.lineEdit_2.setText("")
            self.lineEdit_3.setText("")
            change_w(w1, w2)


class Men_c(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

    def cre_btn(self, w1, w2):
        change_w(w1, w2)


class Note_p(QtWidgets.QDialog, Ui_wnd):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

    def ret_b(self, w1, w2):
        self.texting.clear()
        change_w(w1, w2)

    def sv(self, w1, w2):
        self.textc = self.texting.toPlainText()
        print(self.textc)
        change_w(w1, w2)


class File_e(QtWidgets.QDialog, Ui_filename):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

    def gt_bt(self, w1, w2, textc):
        self.filenam = self.file_t.text()
        print(self.filenam)
        param_req = {"filename": self.filenam, "text": [textc]}
        response = requests.get("url", data=param_req)
        if response:
            change_w(w1, w2)
        else:
            show_m('Warning', 'Filename with this name exist')


# class Cat_e(QtWidgets.QDialog, Ui_Categ):
#     def __init__(self, parent=None):
#         QtWidgets.QDialog.__init__(self, parent)
#         self.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = Loging_F()
    sign = Sign_F()
    men = Men_c()
    note_p = Note_p()
    filen = File_e()
    # try1 = Cat_e()
    main.Login_b.clicked.connect(lambda: main.loginCheck(main, men))
    main.sign_b.clicked.connect(lambda: main.sign_btn(main, sign))
    sign.c_password.clicked.connect(lambda: sign.confirm_z(sign, main))
    men.pushButton.clicked.connect(lambda: men.cre_btn(men, note_p))
    note_p.pushButton.clicked.connect(lambda: note_p.ret_b(note_p, men))
    note_p.sv_btn.clicked.connect(lambda: note_p.sv(note_p, filen))
    filen.got_bt.clicked.connect(lambda: filen.gt_bt(filen, men, note_p.textc))
    main.show()
    sys.exit(app.exec_())
