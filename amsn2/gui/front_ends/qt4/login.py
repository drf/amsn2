import sys

try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    from ui_login import Ui_Login
except ImportError, msg:
    print "Could not import all required modules for the Qt 4 GUI."
    print "ImportError: " + str(msg)
    sys.exit()

class aMSNLoginWindow(QWidget, object):
    def __init__(self, amsn_core, parent=None):
        QWidget.__init__(self, parent)
        print "login.py, __init__"
        self._amsn_core = amsn_core
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        self.setStyleSheet("")
        self._main_win = self._amsn_core.getMainWindow()
        QObject.connect(self.ui.pushSignIn, SIGNAL("clicked()"), self.signin)
        self.switch_to_profile(None)

    def show(self):
        print "login.py, show"
        self._main_win.setCentralWidget(self)
        self._main_win.setWindowTitle('aMSN 2 - Login')

    def hide(self):
        pass

    def switch_to_profile(self, profile):
        self.current_profile = profile
        if self.current_profile is not None:
            self._username = self.current_profile.username
            self._password = self.current_profile.password

    def signin(self):
        print "login.py, signin"
        self.current_profile.username = str(self.ui.comboAccount.currentText())
        self.current_profile.email = str(self.ui.comboAccount.currentText())
        self.current_profile.password = str(self.ui.linePassword.text())
        self._amsn_core.signinToAccount(self, self.current_profile)

    def onConnecting(self, message):
        #self.status.set_text(message)
        print "login.py, onConnecting: " + str(message)