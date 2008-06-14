import sys
from amsn2.gui import base

try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    from ui_login import Ui_Login
    from styledwidget import StyledWidget
except ImportError, msg:
    print "Could not import all required modules for the Qt 4 GUI."
    print "ImportError: " + str(msg)
    sys.exit()

class LoginThrobber(StyledWidget):
    def __init__(self, parent=None):
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
    def __init__(self, amsn_core, parent=None):
        StyledWidget.__init__(self, parent)
        self._amsn_core = amsn_core
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        self._main_win = self._amsn_core.getMainWindow()
        QObject.connect(self.ui.pushSignIn, SIGNAL("clicked()"), self.signin)
        QObject.connect(self.ui.checkTestStylesheet, SIGNAL("stateChanged(int)"), self.setTestStyle)
        self.switch_to_profile(None)
        # FIXME: Temporary stuff to make "./amsn2.py -f qt4 account password" possible
        #        This makes it quicker to do testing :)
        if len(sys.argv) > 3:
            self.ui.comboAccount.lineEdit().setText(sys.argv[3])
        if len(sys.argv) > 4:
            self.ui.linePassword.setText(sys.argv[4])

    def show(self):
        self._main_win.fadeIn(self)
        self._main_win.setWindowTitle('aMSN 2 - Login')

    def hide(self):
        pass

    def switch_to_profile(self, profile):
        self.current_profile = profile
        if self.current_profile is not None:
            self._username = self.current_profile.username
            self._password = self.current_profile.password

    def signin(self):
        self.loginThrobber = LoginThrobber(self)
        self._main_win.fadeIn(self.loginThrobber)
        self.current_profile.username = str(self.ui.comboAccount.currentText())
        self.current_profile.email = str(self.ui.comboAccount.currentText())
        self.current_profile.password = str(self.ui.linePassword.text())
        self._amsn_core.signinToAccount(self, self.current_profile)

    def onConnecting(self, message):
        self.loginThrobber.status.setText(str(message))