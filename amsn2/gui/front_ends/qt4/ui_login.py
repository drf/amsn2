# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created: Fri Jun 13 12:14:52 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(QtCore.QSize(QtCore.QRect(0,0,313,579).size()).expandedTo(Login.minimumSizeHint()))
        Login.setStyleSheet("#Login {"
        "background-color: qradialgradient(spread:reflect, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(224, 219, 255, 255), stop:1 rgba(255, 255, 255, 255));"
        "}"

        "QLineEdit {"
        "border: 2px solid rgb(180, 180, 180);"
        "border-radius: 10px;"
        "background-color: white;"
        "selection-background-color: darkgray;"
        "padding: 1px 18px 1px 3px;"
        "}"

        "QComboBox {"
        "border: 2px solid rgb(180, 180, 180);"
        "border-radius: 10px;"
        "background-color: white;"
        "selection-background-color: darkgray;"
        "padding: 1px 18px 1px 3px;"
        "min-width: 6em;"
        "}"

        "QComboBox:editable {"
        "background-color: white;"
        "}"

                 "QComboBox:!editable, QComboBox::drop-down:editable {"
                 "     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,"
                 "                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,"
                 "                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);"
                 "}"

                 "QComboBox:!editable:on, QComboBox::drop-down:editable:on {"
                 "    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,"
                 "                                stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,"
                 "                                stop: 0.5 #DDDDDD, stop: 1.0 #E1E1E1);"
                 "}"

                 "QComboBox::drop-down:editable {"
                 "     background: white;"
                 "}"

                 "QComboBox:on {"
                 "    padding-top: 3px;"
                 "    padding-left: 4px;"
                 "}"

                 "QComboBox::drop-down {"
                 "    subcontrol-origin: padding;"
                 "    subcontrol-position: top right;"
                 "    width: 20px;"
                 "    border-left-width: 1px;"
                 "    border-left-color: none;"
                 "    border-left-style: solid;"
                 "    border-top-right-radius: 7px;"
                 "    border-bottom-right-radius: 10px;"
                 "}"

                 "QComboBox::down-arrow {"
                 "    image: url(/usr/lib/kde4/share/icons/oxygen/16x16/actions/arrow-down.png);"
                 "}"

                 "QComboBox::down-arrow:on { "
                 "    top: 1px;"
                 "    left: 1px;"
                 "}"

        "QPushButton {"
        "background: qlineargradient(spread:repeat, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(167, 195, 255, 255), stop:1 rgba(74, 99, 156, 255));"
        "font-weight: bold;"
        "}")

        self.vboxlayout = QtGui.QVBoxLayout(Login)
        self.vboxlayout.setSpacing(2)
        self.vboxlayout.setObjectName("vboxlayout")

        self.checkTestStylesheet = QtGui.QCheckBox(Login)
        self.checkTestStylesheet.setObjectName("checkTestStylesheet")
        self.vboxlayout.addWidget(self.checkTestStylesheet)

        spacerItem = QtGui.QSpacerItem(20,57,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)

        self.pixUser = QtGui.QLabel(Login)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pixUser.sizePolicy().hasHeightForWidth())
        self.pixUser.setSizePolicy(sizePolicy)
        self.pixUser.setMinimumSize(QtCore.QSize(100,100))
        self.pixUser.setStyleSheet("#pixUser {"
        "color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 50));"
        "font-weight: bold;"
        "font-size: 20px;"
        "border: 3px solid gray;"
        "border-radius: 10px;"
        "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(185, 190, 255, 255), stop:1 rgba(255, 255, 255, 255));"
        "}"
        "#pixUser:hover {"
        "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(166, 180, 213, 255), stop:1 rgba(255, 255, 255, 255));"
        "}")
        self.pixUser.setAlignment(QtCore.Qt.AlignCenter)
        self.pixUser.setObjectName("pixUser")
        self.hboxlayout.addWidget(self.pixUser)

        spacerItem2 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem2)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.label = QtGui.QLabel(Login)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.comboAccount = QtGui.QComboBox(Login)
        self.comboAccount.setEditable(True)
        self.comboAccount.setObjectName("comboAccount")
        self.vboxlayout.addWidget(self.comboAccount)

        self.label_2 = QtGui.QLabel(Login)
        self.label_2.setObjectName("label_2")
        self.vboxlayout.addWidget(self.label_2)

        self.linePassword = QtGui.QLineEdit(Login)
        self.linePassword.setEchoMode(QtGui.QLineEdit.Password)
        self.linePassword.setObjectName("linePassword")
        self.vboxlayout.addWidget(self.linePassword)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.label_3 = QtGui.QLabel(Login)
        self.label_3.setObjectName("label_3")
        self.hboxlayout1.addWidget(self.label_3)

        self.comboStatus = QtGui.QComboBox(Login)
        self.comboStatus.setObjectName("comboStatus")
        self.hboxlayout1.addWidget(self.comboStatus)

        spacerItem3 = QtGui.QSpacerItem(108,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem3)
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.checkRememberMe = QtGui.QCheckBox(Login)
        self.checkRememberMe.setChecked(True)
        self.checkRememberMe.setObjectName("checkRememberMe")
        self.vboxlayout.addWidget(self.checkRememberMe)

        self.checkRememberPass = QtGui.QCheckBox(Login)
        self.checkRememberPass.setChecked(True)
        self.checkRememberPass.setObjectName("checkRememberPass")
        self.vboxlayout.addWidget(self.checkRememberPass)

        self.checkSignInAuto = QtGui.QCheckBox(Login)
        self.checkSignInAuto.setObjectName("checkSignInAuto")
        self.vboxlayout.addWidget(self.checkSignInAuto)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setObjectName("hboxlayout2")

        spacerItem4 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem4)

        self.pushSignIn = QtGui.QPushButton(Login)
        self.pushSignIn.setObjectName("pushSignIn")
        self.hboxlayout2.addWidget(self.pushSignIn)

        spacerItem5 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem5)
        self.vboxlayout.addLayout(self.hboxlayout2)

        spacerItem6 = QtGui.QSpacerItem(20,57,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem6)

        self.links = QtGui.QLabel(Login)
        self.links.setObjectName("links")
        self.vboxlayout.addWidget(self.links)

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        Login.setWindowTitle(QtGui.QApplication.translate("Login", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.checkTestStylesheet.setText(QtGui.QApplication.translate("Login", "Test stylesheet", None, QtGui.QApplication.UnicodeUTF8))
        self.pixUser.setText(QtGui.QApplication.translate("Login", "aMSN", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Login", "E-mail address:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Login", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Login", "Status:", None, QtGui.QApplication.UnicodeUTF8))
        self.comboStatus.addItem(QtGui.QApplication.translate("Login", "Online", None, QtGui.QApplication.UnicodeUTF8))
        self.checkRememberMe.setText(QtGui.QApplication.translate("Login", "Remember me", None, QtGui.QApplication.UnicodeUTF8))
        self.checkRememberPass.setText(QtGui.QApplication.translate("Login", "Remember my password", None, QtGui.QApplication.UnicodeUTF8))
        self.checkSignInAuto.setText(QtGui.QApplication.translate("Login", "Sign me in automatically", None, QtGui.QApplication.UnicodeUTF8))
        self.pushSignIn.setText(QtGui.QApplication.translate("Login", "Sign In", None, QtGui.QApplication.UnicodeUTF8))
        self.links.setText(QtGui.QApplication.translate("Login", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"test\"><span style=\" text-decoration: underline;;\">Forgot your password?</span></a></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"test\"><span style=\" text-decoration: underline;\">Service status</span></a></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"test\"><span style=\" text-decoration: underline;\">Get a new account</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

