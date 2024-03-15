import base64
import json
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon


def gen_key():
    u = open("account.json", "r")
    data = json.loads(u.read())
    u.close()
    data = data['username']
    encode_data = base64.b64encode(data.encode()).decode("utf-8")
    return encode_data


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(616, 226)
        self.PushButton = PushButton(Dialog)
        self.PushButton.setGeometry(QtCore.QRect(260, 130, 102, 32))
        self.PushButton.setObjectName("PushButton")
        self.CaptionLabel = CaptionLabel(Dialog)
        self.CaptionLabel.setGeometry(QtCore.QRect(20, 190, 581, 16))
        self.CaptionLabel.setText("")
        self.CaptionLabel.setProperty("lightColor", QtGui.QColor(255, 0, 0))
        self.CaptionLabel.setObjectName("CaptionLabel")
        self.LineEdit = LineEdit(Dialog)
        self.LineEdit.setGeometry(QtCore.QRect(40, 70, 541, 33))
        self.LineEdit.setObjectName("LineEdit")
        self.SubtitleLabel = SubtitleLabel(Dialog)
        self.SubtitleLabel.setGeometry(QtCore.QRect(270, 20, 119, 28))
        self.SubtitleLabel.setObjectName("SubtitleLabel")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "AZ小号机Pro"))
        Dialog.setWindowIcon(QIcon("icon.ico"))
        self.PushButton.setText(_translate("Dialog", "获取卡密"))
        self.PushButton.clicked.connect(self.getkey)
        self.LineEdit.setPlaceholderText(_translate("Dialog", "卡密将会在这里被输出，同时保存至小号机目录下"))
        self.SubtitleLabel.setText(_translate("Dialog", "AZ小号机"))
        requ = str(requests.get("https://v1.api.azstudio.net.cn/odd").json()["odd"])
        self.CaptionLabel.setText("库存剩余：{}个卡密".format(requ))

    def getkey(self):
        self.CaptionLabel.setText("")
        key = gen_key()
        req = requests.get("https://v1.api.azstudio.net.cn/get?user_key={}".format(key)).json()
        if req["code"] == 200:
            self.LineEdit.setText(req["msg"])
            u = open("卡密.txt", "a", encoding="utf-8")
            u.write(req["msg"] + "\n")
            u.close()
            self.CaptionLabel.setText("库存剩余：{}个卡密".format(req["odd"]))
        else:
            self.LineEdit.setText(req["msg"])
            self.CaptionLabel.setText(req["msg"])


from qfluentwidgets import CaptionLabel, LineEdit, PushButton, SubtitleLabel

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
