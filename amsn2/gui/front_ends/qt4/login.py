# -*- coding: utf-8 -*-
from amsn2.gui import base
from amsn2.core.views import AccountView, ImageView

from PyQt4.QtCore import *
from PyQt4.QtGui import *
try:
    from ui_login import Ui_Login
except ImportError, e:
    print " WARNING: To use the QT4 you need to run the generateFiles.sh, check the README"
    raise e
from styledwidget import StyledWidget


class LoginThrobber(StyledWidget):
    def __init__(self, parent):
        StyledWidget.__init__(self, parent)
        # Throbber
        self.plsWait = QLabel(self)
        self.plsWait.setText("<strong>Please wait...</strong>")
        self.plsWait.setAlignment(Qt.AlignCenter)
        self.status = QLabel(self)
        self.status.setText("")
        self.status.setAlignment(Qt.AlignCenter)
        self.throbber = QLabel(self)
        self.movie = QMovie(self)
        self.movie.setFileName("amsn2/gui/front_ends/qt4/throbber.gif")
        self.movie.start()
        self.throbber.setMovie(self.movie)
        # Layout, for horizontal centering
        self.hLayout = QHBoxLayout()
        self.hLayout.addStretch()
        self.hLayout.addWidget(self.throbber)
        self.hLayout.addStretch()
        # Layout, for vertical centering
        self.vLayout = QVBoxLayout()
        self.vLayout.addStretch()
        self.vLayout.addLayout(self.hLayout)
        self.vLayout.addWidget(self.plsWait)
        self.vLayout.addWidget(self.status)
        self.vLayout.addStretch()
        # Top level layout
        self.setLayout(self.vLayout)
        # Apply StyleSheet
        self.setStyleSheet("background: white;")

class aMSNLoginWindow(StyledWidget, base.aMSNLoginWindow):
    def __init__(self, amsn_core, parent):
        StyledWidget.__init__(self, parent)
        self._amsn_core = amsn_core
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        self._parent = parent
        QObject.connect(self.ui.pushSignIn, SIGNAL("clicked()"), self.signin)
        QObject.connect(self.ui.styleDesktop, SIGNAL("clicked()"), self.setTestStyle)
        QObject.connect(self.ui.styleRounded, SIGNAL("clicked()"), self.setTestStyle)
        QObject.connect(self.ui.styleWLM, SIGNAL("clicked()"), self.setTestStyle)
        QObject.connect(self.ui.checkRememberMe, SIGNAL("toggled(bool)"), self.__on_toggled_cb)
        QObject.connect(self.ui.checkRememberPass, SIGNAL("toggled(bool)"), self.__on_toggled_cb)
        QObject.connect(self.ui.checkSignInAuto, SIGNAL("toggled(bool)"), self.__on_toggled_cb)
        self.setTestStyle()

        # status list
        self.status_values = {}
        self.status_dict = {}
        status_n = 0
        for key in self._amsn_core.p2s:
            name = self._amsn_core.p2s[key]
            if (name == 'offline'): continue
            self.status_values[name] = status_n
            self.status_dict[str.capitalize(name)] = name
            status_n = status_n +1
            self.ui.comboStatus.addItem(str.capitalize(name))

    def setTestStyle(self):
        styleData = QFile()
        if self.ui.styleDesktop.isChecked() == True:
            styleData.setFileName("amsn2/gui/front_ends/qt4/style0.qss")
        elif self.ui.styleWLM.isChecked() == True:
            styleData.setFileName("amsn2/gui/front_ends/qt4/style1.qss")
        elif self.ui.styleRounded.isChecked() == True:
            styleData.setFileName("amsn2/gui/front_ends/qt4/style2.qss")
        if styleData.open(QIODevice.ReadOnly|QIODevice.Text):
            styleReader = QTextStream(styleData)
            self.setStyleSheet(styleReader.readAll())

    def show(self):
        self._parent.fadeIn(self)

    def hide(self):
        pass

    def setAccounts(self, accountviews):
        self._account_views = accountviews

        for accv in self._account_views:
            self.ui.comboAccount.addItem(accv.email)

        if len(accountviews)>0 :
            # first in the list, default
            self.__switch_to_account(self._account_views[0].email)

            if self._account_views[0].autologin:
                self.signin()


    def __switch_to_account(self, email):

        accv = self.getAccountViewFromEmail(email)

        if accv is None:
            accv = AccountView()
            accv.email = email

        self.ui.comboAccount.setItemText(0, accv.email)

        if accv.password:
            self.ui.linePassword.clear()
            self.ui.linePassword.insert(accv.password)

        self.ui.checkRememberMe.setChecked(accv.save)
        self.ui.checkRememberPass.setChecked(accv.save_password)
        self.ui.checkSignInAuto.setChecked(accv.autologin)

    def signin(self):
        self.loginThrobber = LoginThrobber(self)
        self._parent.fadeIn(self.loginThrobber)

        email = self.ui.comboAccount.currentText()
        accv = self.getAccountViewFromEmail(str(email))

        if accv is None:
            accv = AccountView()
            accv.email = str(email)

        accv.password = self.ui.linePassword.text().toLatin1().data()
        accv.presence = self.status_dict[str(self.ui.comboStatus.currentText())]

        accv.save = self.ui.checkRememberMe.isChecked()
        accv.save_password = self.ui.checkRememberPass.isChecked()
        accv.autologin = self.ui.checkSignInAuto.isChecked()

        self._amsn_core.signinToAccount(self, accv)

    def onConnecting(self, progress, message):
        self.loginThrobber.status.setText(str(message))

    def __on_toggled_cb(self, bool):
        email = str(self.ui.comboAccount.currentText())
        accv = self.getAccountViewFromEmail(email)

        if accv is None:
            accv = AccountView()
            accv.email = email
            accv.save = False
            accv.save_password = False
            accv.autologin = False

        sender = self.sender().objectName()
        #just like wlm :)
        if sender == "checkRememberMe":
            if bool == True:
                accv.save = True
            else:
                if self.ui.checkRememberPass.isChecked():
                    self.ui.checkRememberPass.setChecked(False)
                if self.ui.checkSignInAuto.isChecked():
                    self.ui.checkSignInAuto.setChecked(False)
        elif sender == "checkRememberPass":
            if bool == True:
                accv.save_password = True
                if self.ui.checkRememberMe.isChecked() == False:
                    self.ui.checkRememberMe.setChecked(True)
            else:
                if self.ui.checkSignInAuto.isChecked():
                    self.ui.checkSignInAuto.setChecked(False)
        elif sender == "checkSignInAuto":
            if bool == True:
                accv.autologin = True
                if self.ui.checkRememberMe.isChecked() == False:
                    self.ui.checkRememberMe.setChecked(True)
                if self.ui.checkRememberPass.isChecked() == False:
                    self.ui.checkRememberPass.setChecked(True)