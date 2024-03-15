import json
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLineEdit
import main_q
import register_q
import hashlib

# 程序设置
api = "http://example.com/"  # 后端地址，务必按照这样的格式填写（网址结尾加"/"）

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(653, 423)
        self.PushButton = PushButton(Form)
        self.PushButton.setGeometry(QtCore.QRect(280, 280, 102, 32))
        self.PushButton.setObjectName("PushButton")
        self.PushButton_2 = PushButton(Form)
        self.PushButton_2.setGeometry(QtCore.QRect(280, 320, 102, 32))
        self.PushButton_2.setObjectName("PushButton_2")
        self.LineEdit = LineEdit(Form)
        self.LineEdit.setGeometry(QtCore.QRect(320, 140, 128, 33))
        self.LineEdit.setObjectName("LineEdit")
        self.LineEdit_2 = LineEdit(Form)
        self.LineEdit_2.setGeometry(QtCore.QRect(320, 190, 128, 33))
        self.LineEdit_2.setInputMask("")
        self.LineEdit_2.setText("")
        self.LineEdit_2.setObjectName("LineEdit_2")
        self.SubtitleLabel = SubtitleLabel(Form)
        self.SubtitleLabel.setGeometry(QtCore.QRect(220, 140, 119, 28))
        self.SubtitleLabel.setObjectName("SubtitleLabel")
        self.SubtitleLabel_2 = SubtitleLabel(Form)
        self.SubtitleLabel_2.setGeometry(QtCore.QRect(240, 190, 119, 28))
        self.SubtitleLabel_2.setObjectName("SubtitleLabel_2")
        self.TitleLabel = TitleLabel(Form)
        self.TitleLabel.setGeometry(QtCore.QRect(300, 60, 123, 38))
        self.TitleLabel.setObjectName("TitleLabel")
        self.CaptionLabel = CaptionLabel(Form)
        self.CaptionLabel.setGeometry(QtCore.QRect(150, 240, 381, 20))
        self.CaptionLabel.setText("")
        self.CaptionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.CaptionLabel.setProperty("lightColor", QtGui.QColor(255, 0, 0))
        self.CaptionLabel.setObjectName("CaptionLabel")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "AZ卡密获取系统 - 登录"))
        Form.setWindowIcon(QIcon("icon.ico"))
        self.PushButton.setText(_translate("Form", "登录"))
        self.PushButton.clicked.connect(self.login)
        self.PushButton_2.setText(_translate("Form", "注册账号"))
        self.PushButton_2.clicked.connect(self.open_reg)
        self.LineEdit.setPlaceholderText(_translate("Form", "请输入用户名"))
        self.LineEdit_2.setPlaceholderText(_translate("Form", "请输入密码"))
        self.LineEdit_2.setEchoMode(QLineEdit.Password)
        self.SubtitleLabel.setText(_translate("Form", "用户名："))
        self.SubtitleLabel_2.setText(_translate("Form", "密码："))
        self.TitleLabel.setText(_translate("Form", "登录"))

    def login(self):
        pwd = hashlib.md5(self.LineEdit_2.text().encode())
        pwd_md5 = pwd.hexdigest()
        req = requests.get(
            "{}login?name={}&password={}".format(api, self.LineEdit.text(), pwd_md5)).json()
        if req["code"] == 200:
            u = open("account.json", "w")
            u.write(json.dumps({"username": self.LineEdit.text()}))
            u.close()
            Form.close()
            self.open_main()
        else:
            self.CaptionLabel.setText("账号或密码错误")

    def open_main(self):
        main_d = main_q.QtWidgets.QDialog()
        ui = main_q.Ui_Dialog()
        ui.setupUi(main_d)
        main_d.show()
        main_d.exec_()

    def open_reg(self):
        reg = register_q.QtWidgets.QDialog()
        ui_r = register_q.Ui_Dialog()
        ui_r.setupUi(reg)
        reg.show()
        reg.exec_()


from qfluentwidgets import CaptionLabel, LineEdit, PushButton, SubtitleLabel, TitleLabel

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
