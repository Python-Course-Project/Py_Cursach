from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

from loging import Ui_Loging
from sign_up import Ui_Sign_up
from men_wn import Ui_Dialog
from main_wnd import Ui_wnd
from enter_f import Ui_filename
# from cat_m import Ui_Categ
from open_men import Ui_Open
from another_sv import Ui_Save
from ano_f import Ui_Ano
from enter_u import Ui_User
from dshare_u import Ui_Dshare
from cat_men import Ui_Catm
from cat_file import Ui_CatF
from new_cat import Ui_NewC
from new_catf import Ui_NewCF
import requests
import json
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
        self.username1 = self.u_line.text()
        password1 = self.p_line.text()
        if len(self.username1) == 0:
            show_m('Warning', 'Empty Username')
        if len(password1) == 0:
            show_m('Warning', 'Empty Password')
        if len(password1) > 0 and len(self.username1) > 0:
            param_req = {'password': password1, 'username': self.username1}
            response = requests.post('https://nameless-sands-73623.herokuapp.com/api/v1/auth_token/token/login',
                                     data=param_req)
            if response.status_code == 400:
                namer = json.loads(response.text)
                show_m('Warning', 'Bad Data')
            if response.status_code == 200:
                X = dict(response.json())
                self.token = X["auth_token"]
                # print(response)

                self.u_line.setText("")
                self.p_line.setText("")
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
        self.username = self.lineEdit.text()
        self.password = self.lineEdit_2.text()
        self.conf_password = self.lineEdit_3.text()
        if len(self.username) == 0:
            show_m('Warning', 'Empty Username')
        if len(self.password) == 0:
            show_m('Warning', 'Empty Password')
        if self.password != self.conf_password:
            show_m('Warning', 'Different Passwords')
        if len(self.username) > 0 and (self.password == self.conf_password):
            param_req = {'username': self.username, 'password': self.password}
            response = requests.post('https://nameless-sands-73623.herokuapp.com/api/v1/auth/users/', data=param_req)
            if response.status_code == 201:
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

    def op_bt(self, w1, w2, token):
        rcreator = requests.get("https://nameless-sands-73623.herokuapp.com/api/v1/note/all/as_creator/",
                                headers={"Authorization": "Token " + str(token)})
        reditor = requests.get("https://nameless-sands-73623.herokuapp.com/api/v1/note/all/as_editor/",
                               headers={"Authorization": "Token " + str(token)})
        # print(r.text)
        self.x = json.loads(rcreator.text) + json.loads(reditor.text)
        for e in self.x:
            w2.listfiles.addItem(e["note_title"])
        change_w(w1, w2)

    def log_bt(self, w1, w2, token):
        r = requests.post("https://nameless-sands-73623.herokuapp.com/api/v1/auth_token/token/logout",
                          headers={"Authorization": "Token " + str(token)})
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
        self.texting.clear()
        change_w(w1, w2)


class File_e(QtWidgets.QDialog, Ui_filename):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

    def gt_bt(self, w1, w2, textc, token):

        self.filenam = self.file_t.text()
        print(self.filenam)
        param_req = {"note_title": self.filenam, "note_text": textc}
        response = requests.post('https://nameless-sands-73623.herokuapp.com/api/v1/note/create/', data=param_req,
                                 headers={"Authorization": "Token " + str(token)})
        print(response.text)
        print(response.status_code)
        if response.status_code == 201:
            change_w(w1, w2)
        else:
            show_m('Warning', 'Filename with this name exist')


class Anoth(QtWidgets.QDialog, Ui_Save):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

    def sav_bt(self, w1, w2, filenam, edit, id, token, w3):
        self.txt = self.another_s.toPlainText()
        if edit == False:
            w2.lineEdit.setText(filenam)
            change_w(w1, w2)
            self.another_s.clear()
        else:
            param_req = {"note_text": self.txt}
            url = "https://nameless-sands-73623.herokuapp.com/api/v1/note/detail/" + str(id) + "/editor"
            r = requests.put(url, data=param_req, headers={"Authorization": "Token " + str(token)})
            change_w(w1, w3)
            self.another_s.clear()


class Open_f(QtWidgets.QDialog, Ui_Open):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

    def ret_bt(self, w1, w2):
        w1.listfiles.clear()
        change_w(w1, w2)

    def del_btn(self, x, token, username):
        if len(self.listfiles) == 0:
            show_m('Warning', 'You have no items')
        if not self.listfiles.currentItem().isSelected():
            show_m('Warning', 'Select Item Please')
        if self.listfiles.currentItem().isSelected():
            param = self.listfiles.currentItem().text()
            request = requests.get("https://nameless-sands-73623.herokuapp.com/api/v1/auth/users/",
                                   headers={"Authorization": "Token " + str(token)})
            name = json.loads(request.text)
            editor = False
            for n in name:
                if username == n["username"]:
                    ids = n["id"]
            for e in x:
                if param == e["note_title"]:
                    edit = e["editor"]
                    if len(edit) > 0:
                        for a in edit:
                            if ids == a:
                                editor = True
                        if editor == False:
                            url = "https://nameless-sands-73623.herokuapp.com/api/v1/note/detail/" + str(
                                e["id"]) + "/creator"
                            r = requests.delete(url, headers={"Authorization": "Token " + str(token)})
                            print(r.status_code)
                            self.listfiles.currentItem().setHidden(True)
                        else:
                            show_m('Warning', 'You cant delete this note')
                    else:
                        url = "https://nameless-sands-73623.herokuapp.com/api/v1/note/detail/" + str(
                            e["id"]) + "/creator"
                        r = requests.delete(url, headers={"Authorization": "Token " + str(token)})
                        print(r.status_code)
                        self.listfiles.currentItem().setHidden(True)

    def opn(self, w1, w2, x, token, username):
        if len(self.listfiles) == 0:
            show_m('Warning', 'You have no items')
        if not self.listfiles.currentItem().isSelected():
            show_m('Warning', 'Select Item Please')
        if self.listfiles.currentItem().isSelected():
            self.yaedit = False
            self.filen = self.listfiles.currentItem().text()
            print(self.filen)
            request = requests.get("https://nameless-sands-73623.herokuapp.com/api/v1/auth/users/",
                                   headers={"Authorization": "Token " + str(token)})
            name = json.loads(request.text)
            # for n in name:
            ids = name[0]["id"]
            print(ids)
            for e in x:
                if self.filen == e["note_title"]:
                    self.edito = e["editor"]
                    if e["user"] == ids:
                        url = "https://nameless-sands-73623.herokuapp.com/api/v1/note/detail/" + str(
                            e["id"]) + "/creator"
                        self.idz = e["id"]
                        r = requests.get(url, headers={"Authorization": "Token " + str(token)})
                        X = dict(r.json())
                        print(X["note_text"])
                        check = X["note_text"]
                        w2.another_s.append(check)
                        change_w(w1, w2)
                        self.listfiles.clear()
                    elif len(self.edito) > 0:
                        for a in self.edito:
                            if ids == a:
                                url = "https://nameless-sands-73623.herokuapp.com/api/v1/note/detail/" + str(
                                    e["id"]) + "/editor"
                                self.idz = e["id"]
                                self.yaedit = True
                                r = requests.get(url, headers={"Authorization": "Token " + str(token)})
                                X = dict(r.json())
                                print(X["note_text"])
                                check = X["note_text"]
                                w2.another_s.append(check)
                                change_w(w1, w2)
                                self.listfiles.clear()

    def share_bt(self, w1, w2, token, username, x):
        if len(self.listfiles) == 0:
            show_m('Warning', 'You have no items')
        if self.listfiles.currentItem().isSelected():
            self.filen = self.listfiles.currentItem().text()
            request = requests.get("https://nameless-sands-73623.herokuapp.com/api/v1/auth/users/",
                                   headers={"Authorization": "Token " + str(token)})
            name = json.loads(request.text)
            editor = False
            for n in name:
                if username == n["username"]:
                    ids = n["id"]
            for e in x:
                if self.filen == e["note_title"]:
                    edit = e["editor"]
                    if len(edit) > 0:
                        for a in edit:
                            if ids == a:
                                editor = True
                        if editor == True:
                            show_m('Warning', 'You cant share  this note')
                        else:
                            self.listfiles.clear()
                            change_w(w1, w2)

                    else:
                        self.listfiles.clear()
                        change_w(w1, w2)
        else:
            show_m('Warning', 'Select Item Please')

    def dshare_bt(self, w1, w2, token, username, x):
        if len(self.listfiles) == 0:
            show_m('Warning', 'You have no items')
        if self.listfiles.currentItem().isSelected():
            self.filen = self.listfiles.currentItem().text()
            request = requests.get("https://nameless-sands-73623.herokuapp.com/api/v1/auth/users/",
                                   headers={"Authorization": "Token " + str(token)})
            name = json.loads(request.text)
            editor = False
            r = requests.get("https://nameless-sands-73623.herokuapp.com/api/v1/users/all/",
                             headers={"Authorization": "Token " + str(token)})

            spisok = json.loads(r.text)
            for n in name:
                if username == n["username"]:
                    ids = n["id"]
            for e in x:
                if self.filen == e["note_title"]:
                    edit = e["editor"]
                    if len(edit) > 0:
                        for a in edit:
                            if ids == a:
                                editor = True
                            for q in spisok:
                                if a == q["id"]:
                                    w2.dlistWidget.addItem(q["username"])
                        if editor == True:
                            show_m('Warning', 'You cant share  this note')
                        else:
                            self.listfiles.clear()
                            change_w(w1, w2)

                    else:
                        self.listfiles.clear()
                        change_w(w1, w2)
        else:
            show_m('Warning', 'Select Item Please')

    def categ_bt(self, w1, w2, token):
        r = requests.get("https://nameless-sands-73623.herokuapp.com/api/v1/category/all/",
                         headers={"Authorization": "Token " + str(token)})
        categ = json.loads(r.text)
        for e in categ:
            w2.clistWidget.addItem(e["note_category"])
        self.listfiles.clear()
        change_w(w1, w2)


class Anof(QtWidgets.QDialog, Ui_Ano):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

    def gt_bn(self, w1, w2, token, id, txt, filenam):
        if self.lineEdit.text() == filenam:
            url = "https://nameless-sands-73623.herokuapp.com/api/v1/note/detail/" + str(id) + "/creator"
            param = requests.get(url, headers={"Authorization": "Token " + str(token)})
            name = json.loads(param.text)
            name["note_text"] = txt
            r = requests.put(url, data=name, headers={"Authorization": "Token " + str(token)})
            change_w(w1, w2)

        else:
            name = self.lineEdit.text()
            url = "https://nameless-sands-73623.herokuapp.com/api/v1/note/detail/" + str(id) + "/creator"
            param = requests.get(url, headers={"Authorization": "Token " + str(token)})
            namer = json.loads(param.text)
            namer["note_text"] = txt
            namer["note_title"] = name
            r = requests.put(url, data=namer, headers={"Authorization": "Token " + str(token)})
            change_w(w1, w2)


class Usern(QtWidgets.QDialog, Ui_User):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

    def user_bt(self, w1, w2, token, filenam, x, w3):
        text = self.userline.text()
        if len(text) == 0:
            show_m('Warning', 'Empty Username')
        request = requests.get("https://nameless-sands-73623.herokuapp.com/api/v1/users/all/",
                               headers={"Authorization": "Token " + str(token)})
        self.name = json.loads(request.text)
        for n in self.name:
            if text == n["username"]:
                ids = n["id"]

        for e in x:
            if filenam == e["note_title"]:
                id = e["id"]
                url = "https://nameless-sands-73623.herokuapp.com/api/v1/note/detail/" + str(id) + "/creator"
                param = requests.get(url, headers={"Authorization": "Token " + str(token)})
                namer = json.loads(param.text)
                namer["editor"].append(ids)
                r = requests.patch(url, data=namer,
                                   headers={"Authorization": "Token " + str(token)})
                print(r.status_code)
                self.userline.setText("")
                # w3.op_bt(w1, w2, token)
                change_w(w1, w3)


class Dshar(QtWidgets.QDialog, Ui_Dshare):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

    def duser_bt(self, w1, w2, token, filenam, x, w3):
        text = self.duserline.text()
        if len(text) == 0:
            show_m('Warning', 'Empty Username')
        request = requests.get("https://nameless-sands-73623.herokuapp.com/api/v1/users/all/",
                               headers={"Authorization": "Token " + str(token)})
        self.name = json.loads(request.text)
        for n in self.name:
            if text == n["username"]:
                ids = n["id"]
        editor = False
        for e in x:
            if filenam == e["note_title"]:
                id = e["id"]
                url = "https://nameless-sands-73623.herokuapp.com/api/v1/note/detail/" + str(id) + "/creator"
                param = requests.get(url, headers={"Authorization": "Token " + str(token)})
                namer = json.loads(param.text)
                for a in namer["editor"]:
                    if a == ids:
                        editor = True
                if editor:
                    namer["editor"].remove(ids)
                    r = requests.patch(url, data=namer,
                                       headers={"Authorization": "Token " + str(token)})
                    print(r.status_code)
                    self.duserline.setText("")
                    # w3.op_bt(w1, w2, token)
                    change_w(w1, w3)
                else:
                    show_m('Warning', 'This note hasnt this name')


class Acat(QtWidgets.QDialog, Ui_Catm):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

    def mainmen_bt(self, w1, w2):
        self.clistWidget.clear()
        change_w(w1, w2)

    def categ_op(self, w1, w2, token,w3):
        catn = self.clistWidget.currentItem().text()
        r = requests.get("https://nameless-sands-73623.herokuapp.com/api/v1/category/all/",
                         headers={"Authorization": "Token " + str(token)})
        categ = json.loads(r.text)
        note = []
        for e in categ:
            if catn == e["note_category"]:
                self.c_id = e["id"]
                note = e["my_note"]
        if len(note) > 0:
            for n in note:
                w2.cflistWidget.addItem(e)
                change_w(w1, w2)
                self.clistWidget.clear()
        else:
            show_m('Warning','Nothing to open')
            change_w(w1,w3)
            self.clistWidget.clear()

    def newcat(self,w1,w2):
        change_w(w1, w2)
        self.clistWidget.clear()

class CatF(QtWidgets.QDialog, Ui_CatF):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

class NewCat(QtWidgets.QDialog, Ui_NewC):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

    def newc_bt(self,w1,w2,token):
        self.catn = self.nclineEdit.text()
        r = requests.get("https://nameless-sands-73623.herokuapp.com/api/v1/category/all/",
                         headers={"Authorization": "Token " + str(token)})
        categ = json.loads(r.text)
        exist = False
        for e in categ:
            if self.catn == e["note_category"]:
                exist = True
        if exist == True:
            show_m('Warning', 'Category exist')
        else:
            rу = requests.get("https://nameless-sands-73623.herokuapp.com/api/v1/note/all/as_creator/",
                              headers={"Authorization": "Token " + str(token)})
            notes = json.loads(rу.text)
            for x in notes:
                w2.listWidget.addItem(x["note_title"])
            change_w(w1,w2)
            self.nclineEdit.setText("")


class NewCatF(QtWidgets.QDialog, Ui_NewCF):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = Loging_F()
    sign = Sign_F()
    men = Men_c()
    note_p = Note_p()
    filen = File_e()
    op = Open_f()
    ano = Anoth()
    anf = Anof()
    usernam = Usern()
    dshare = Dshar()
    allcateg = Acat()
    catf = CatF()
    newc = NewCat()
    newcf = NewCatF()
    # try1 = Cat_e()
    main.Login_b.clicked.connect(lambda: main.loginCheck(main, men))
    main.sign_b.clicked.connect(lambda: main.sign_btn(main, sign))
    sign.c_password.clicked.connect(lambda: sign.confirm_z(sign, main))
    men.pushButton.clicked.connect(lambda: men.cre_btn(men, note_p))
    note_p.pushButton.clicked.connect(lambda: note_p.ret_b(note_p, men))
    note_p.sv_btn.clicked.connect(lambda: note_p.sv(note_p, filen))
    filen.got_bt.clicked.connect(lambda: filen.gt_bt(filen, men, note_p.textc, main.token))
    men.pushButton_2.clicked.connect(lambda: men.op_bt(men, op, main.token))
    op.dButton.clicked.connect(lambda: op.del_btn(men.x, main.token, main.username1))
    op.rButton.clicked.connect(lambda: op.ret_bt(op, men))
    op.oButton.clicked.connect(lambda: op.opn(op, ano, men.x, main.token, main.username1))
    ano.ansv_btn.clicked.connect(lambda: ano.sav_bt(ano, anf, op.filen, op.yaedit, op.idz, main.token, men))
    anf.got_bt.clicked.connect(lambda: anf.gt_bn(anf, men, main.token, op.idz, ano.txt, op.filen))
    op.sButton.clicked.connect(lambda: op.share_bt(op, usernam, main.token, main.username1, men.x))
    usernam.user_btn.clicked.connect(lambda: usernam.user_bt(usernam, op, main.token, op.filen, men.x, men))
    op.deButton.clicked.connect(lambda: op.dshare_bt(op, dshare, main.token, main.username1, men.x))
    dshare.user_dbtn.clicked.connect(lambda: dshare.duser_bt(dshare, op, main.token, op.filen, men.x, men))
    men.pushButton_l.clicked.connect(lambda: men.log_bt(men, main, main.token))
    op.cButton.clicked.connect(lambda: op.categ_bt(op, allcateg, main.token))
    allcateg.cmpushButton.clicked.connect(lambda: allcateg.mainmen_bt(allcateg, men))
    allcateg.copushButton.clicked.connect(lambda: allcateg.categ_op(allcateg, catf, main.token,men))
    allcateg.cnpushButton.clicked.connect(lambda  : allcateg.newcat(allcateg,newc))
    newc.ncpushButton.clicked.connect(lambda : newc.newc_bt(newc,newcf,main.token))
    main.show()
    sys.exit(app.exec_())

#Todo доделать категории посмотреть баг, доделать открытие существующих категорий, доделать создание новой категории
# Todo отловить ошибку 400 и 400 вооот
