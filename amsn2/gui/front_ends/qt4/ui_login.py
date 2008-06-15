# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created: Mon Jun 16 00:07:10 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(294,597)
        Login.setStyleSheet("""QWidget {
font-size: 11px;
}

#Login {
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(155, 191, 193), stop:0.253333 rgb(236, 243, 246));
}

QLineEdit {
border: 1px solid rgb(169, 183, 199);
border-radius: 0px;
background-color: white;
selection-background-color: darkgray;
min-height: 20px;
max-height: 20px;
min-width: 225px;
max-width: 225px;
}

QLineEdit:hover {
border: 1px solid rgb(0, 136, 228);
}

QComboBox {
border: 1px solid rgb(169, 183, 199);
border-radius: 0px;
background-color: white;
selection-background-color: darkgray;
min-height: 20px;
max-height: 20px;
}

QComboBox:editable {
background-color: white;
min-width: 225px;
max-width: 225px;
}

QComboBox:!editable {
border: 1px solid rgb(169, 183, 199);
background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(226, 225, 231), stop:1 rgb(255, 255, 255));
}

         QComboBox:!editable:on, QComboBox::drop-down:editable:on {
             background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                         stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,
                                         stop: 0.5 #DDDDDD, stop: 1.0 #E1E1E1);
         }

         QComboBox::drop-down:editable {
              background: white;
         }

         QComboBox:on { 
             padding-top: 3px;
             padding-left: 4px;
         }

         QComboBox::drop-down {
             subcontrol-origin: padding;
             subcontrol-position: top right;
             width: 20px;

             border-left-width: 1px;
             border-left-color: none;
             border-left-style: solid; 
             border-top-right-radius: 7px;
             border-bottom-right-radius: 10px;
         }

         QComboBox::down-arrow {
             image: url(amsn2/gui/front_ends/qt4/msn-down.png);
         }

         QComboBox::down-arrow:on { 
             top: 1px;
             left: 1px;
         }

QComboBox:hover {
border: 1px solid rgb(0, 136, 228);
}

QPushButton {
background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:0.395556 rgba(200, 200, 200, 255));
border: 1px solid gray;
border-radius: 3px;
padding: 2px 16px;
}

QPushButton:hover {
background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(0, 86, 178), stop:0.395556 rgb(0, 136, 228));
border: 1px solid rgb(0, 136, 228);
color: white;
}""")
        self.verticalLayout_7 = QtGui.QVBoxLayout(Login)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        spacerItem = QtGui.QSpacerItem(20,31,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.pixUser = QtGui.QLabel(Login)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pixUser.sizePolicy().hasHeightForWidth())
        self.pixUser.setSizePolicy(sizePolicy)
        self.pixUser.setMinimumSize(QtCore.QSize(131,129))
        self.pixUser.setAlignment(QtCore.Qt.AlignCenter)
        self.pixUser.setObjectName("pixUser")
        self.horizontalLayout_4.addWidget(self.pixUser)
        spacerItem2 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout_7.addLayout(self.horizontalLayout_4)
        spacerItem3 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Fixed)
        self.verticalLayout_7.addItem(spacerItem3)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem4 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem5 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(Login)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.comboAccount = QtGui.QComboBox(Login)
        self.comboAccount.setEditable(True)
        self.comboAccount.setObjectName("comboAccount")
        self.verticalLayout.addWidget(self.comboAccount)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtGui.QLabel(Login)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.linePassword = QtGui.QLineEdit(Login)
        self.linePassword.setEchoMode(QtGui.QLineEdit.Password)
        self.linePassword.setObjectName("linePassword")
        self.verticalLayout_2.addWidget(self.linePassword)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtGui.QLabel(Login)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.comboStatus = QtGui.QComboBox(Login)
        self.comboStatus.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboStatus.setObjectName("comboStatus")
        self.horizontalLayout.addWidget(self.comboStatus)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        spacerItem6 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem6)
        self.verticalLayout_6.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem7 = QtGui.QSpacerItem(28,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem7)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem8 = QtGui.QSpacerItem(13,13,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem8)
        self.checkRememberMe = QtGui.QCheckBox(Login)
        self.checkRememberMe.setChecked(True)
        self.checkRememberMe.setObjectName("checkRememberMe")
        self.verticalLayout_5.addWidget(self.checkRememberMe)
        self.checkRememberPass = QtGui.QCheckBox(Login)
        self.checkRememberPass.setChecked(True)
        self.checkRememberPass.setObjectName("checkRememberPass")
        self.verticalLayout_5.addWidget(self.checkRememberPass)
        self.checkSignInAuto = QtGui.QCheckBox(Login)
        self.checkSignInAuto.setObjectName("checkSignInAuto")
        self.verticalLayout_5.addWidget(self.checkSignInAuto)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem9 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem9)
        self.pushSignIn = QtGui.QPushButton(Login)
        self.pushSignIn.setObjectName("pushSignIn")
        self.horizontalLayout_2.addWidget(self.pushSignIn)
        spacerItem10 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem10)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        spacerItem11 = QtGui.QSpacerItem(13,13,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem11)
        self.links = QtGui.QLabel(Login)
        self.links.setStyleSheet("color: red;")
        self.links.setObjectName("links")
        self.verticalLayout_5.addWidget(self.links)
        self.horizontalLayout_5.addLayout(self.verticalLayout_5)
        spacerItem12 = QtGui.QSpacerItem(28,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem12)
        self.verticalLayout_6.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6.addLayout(self.verticalLayout_6)
        spacerItem13 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem13)
        self.verticalLayout_7.addLayout(self.horizontalLayout_6)
        spacerItem14 = QtGui.QSpacerItem(20,30,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem14)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_4 = QtGui.QLabel(Login)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setWeight(75)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_7.addWidget(self.label_4)
        self.styleDesktop = QtGui.QRadioButton(Login)
        self.styleDesktop.setObjectName("styleDesktop")
        self.horizontalLayout_7.addWidget(self.styleDesktop)
        self.styleRounded = QtGui.QRadioButton(Login)
        self.styleRounded.setObjectName("styleRounded")
        self.horizontalLayout_7.addWidget(self.styleRounded)
        self.styleWLM = QtGui.QRadioButton(Login)
        self.styleWLM.setChecked(True)
        self.styleWLM.setObjectName("styleWLM")
        self.horizontalLayout_7.addWidget(self.styleWLM)
        self.verticalLayout_7.addLayout(self.horizontalLayout_7)

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        Login.setWindowTitle(QtGui.QApplication.translate("Login", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Login", "E-mail address:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Login", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Login", "Sign in as:", None, QtGui.QApplication.UnicodeUTF8))
        self.comboStatus.addItem(QtGui.QApplication.translate("Login", "Online", None, QtGui.QApplication.UnicodeUTF8))
        self.comboStatus.addItem(QtGui.QApplication.translate("Login", "Busy", None, QtGui.QApplication.UnicodeUTF8))
        self.comboStatus.addItem(QtGui.QApplication.translate("Login", "Away", None, QtGui.QApplication.UnicodeUTF8))
        self.comboStatus.addItem(QtGui.QApplication.translate("Login", "Show offline", None, QtGui.QApplication.UnicodeUTF8))
        self.checkRememberMe.setText(QtGui.QApplication.translate("Login", "Remember me", None, QtGui.QApplication.UnicodeUTF8))
        self.checkRememberPass.setText(QtGui.QApplication.translate("Login", "Remember my password", None, QtGui.QApplication.UnicodeUTF8))
        self.checkSignInAuto.setText(QtGui.QApplication.translate("Login", "Sign me in automatically", None, QtGui.QApplication.UnicodeUTF8))
        self.pushSignIn.setText(QtGui.QApplication.translate("Login", "Sign In", None, QtGui.QApplication.UnicodeUTF8))
        self.links.setText(QtGui.QApplication.translate("Login", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\'; font-size:10pt;\"><a href=\"test\"><span style=\"text-decoration: none; color:#0088e4;\">Forgot your password?</span></a></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\'; font-size:10pt; color:#ffffff;\"><a href=\"test\"><span style=\"text-decoration: none; color:#0088e4;\">Service status</span></a></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\'; font-size:10pt; color:#ffffff;\"><a href=\"test\"><span style=\"text-decoration: none; color:#0088e4;\">Get a new account</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Login", "Test style", None, QtGui.QApplication.UnicodeUTF8))
        self.styleDesktop.setText(QtGui.QApplication.translate("Login", "Desktop", None, QtGui.QApplication.UnicodeUTF8))
        self.styleRounded.setText(QtGui.QApplication.translate("Login", "Rounded", None, QtGui.QApplication.UnicodeUTF8))
        self.styleWLM.setText(QtGui.QApplication.translate("Login", "WLM", None, QtGui.QApplication.UnicodeUTF8))

