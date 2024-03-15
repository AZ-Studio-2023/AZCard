# -*- coding: utf-8 -*-
import hashlib
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLineEdit

# 程序设置
api = "http://example.com/"  # 后端地址，务必按照这样的格式填写（网址结尾加"/"）

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(656, 423)
        self.SubtitleLabel_3 = SubtitleLabel(Dialog)
        self.SubtitleLabel_3.setGeometry(QtCore.QRect(220, 230, 119, 28))
        self.SubtitleLabel_3.setObjectName("SubtitleLabel_3")
        self.SubtitleLabel_2 = SubtitleLabel(Dialog)
        self.SubtitleLabel_2.setGeometry(QtCore.QRect(240, 180, 119, 28))
        self.SubtitleLabel_2.setObjectName("SubtitleLabel_2")
        self.SubtitleLabel = SubtitleLabel(Dialog)
        self.SubtitleLabel.setGeometry(QtCore.QRect(220, 130, 119, 28))
        self.SubtitleLabel.setObjectName("SubtitleLabel")
        self.LineEdit_3 = LineEdit(Dialog)
        self.LineEdit_3.setGeometry(QtCore.QRect(320, 230, 128, 33))
        self.LineEdit_3.setInputMask("")
        self.LineEdit_3.setText("")
        self.LineEdit_3.setObjectName("LineEdit_3")
        self.LineEdit_2 = LineEdit(Dialog)
        self.LineEdit_2.setGeometry(QtCore.QRect(320, 180, 128, 33))
        self.LineEdit_2.setInputMask("")
        self.LineEdit_2.setText("")
        self.LineEdit_2.setObjectName("LineEdit_2")
        self.LineEdit = LineEdit(Dialog)
        self.LineEdit.setGeometry(QtCore.QRect(320, 130, 128, 33))
        self.LineEdit.setObjectName("LineEdit")
        self.TitleLabel = TitleLabel(Dialog)
        self.TitleLabel.setGeometry(QtCore.QRect(300, 50, 123, 38))
        self.TitleLabel.setObjectName("TitleLabel")
        self.CaptionLabel = CaptionLabel(Dialog)
        self.CaptionLabel.setGeometry(QtCore.QRect(90, 280, 501, 20))
        self.CaptionLabel.setText("")
        self.CaptionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.CaptionLabel.setProperty("lightColor", QtGui.QColor(255, 0, 0))
        self.CaptionLabel.setObjectName("CaptionLabel")
        self.PushButton = PushButton(Dialog)
        self.PushButton.setGeometry(QtCore.QRect(270, 310, 102, 32))
        self.PushButton.setObjectName("PushButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "AZ卡密获取系统 - 注册"))
        Dialog.setWindowIcon(QIcon("icon.ico"))
        self.SubtitleLabel_3.setText(_translate("Dialog", "激活码："))
        self.SubtitleLabel_2.setText(_translate("Dialog", "密码："))
        self.SubtitleLabel.setText(_translate("Dialog", "用户名："))
        self.LineEdit_3.setPlaceholderText(_translate("Dialog", "请输入激活码"))
        self.LineEdit_2.setPlaceholderText(_translate("Dialog", "请输入密码"))
        self.LineEdit_2.setEchoMode(QLineEdit.Password)
        self.LineEdit.setPlaceholderText(_translate("Dialog", "请输入用户名"))
        self.TitleLabel.setText(_translate("Dialog", "注册"))
        self.PushButton.setText(_translate("Dialog", "注册"))
        self.PushButton.clicked.connect(self.reg)

    def reg(self):
        pwd = hashlib.md5(self.LineEdit_2.text().encode())
        pwd_md5 = pwd.hexdigest()
        req = requests.get(
            "{}reg?name={}&password={}&key={}".format(api, self.LineEdit.text(), pwd_md5,
                                                                     self.LineEdit_3.text())).json()
        if req["code"] == 200:
            self.CaptionLabel.setText("注册成功")
        else:
            self.CaptionLabel.setText("激活码错误或已被使用")


from qfluentwidgets import CaptionLabel, LineEdit, PushButton, SubtitleLabel, TitleLabel

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
