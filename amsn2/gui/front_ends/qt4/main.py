from amsn2.gui import base
import sys

try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    from ui_main import Ui_Main
except ImportError, msg:
    print "Could not import all required modules for the Qt 4 GUI."
    print "ImportError: " + str(msg)
    sys.exit()

class aMSNMainWindow(QMainWindow, base.aMSNMainWindow):
    def __init__(self, amsn_core, parent=None):
        QMainWindow.__init__(self, parent)
        self._amsn_core = amsn_core
        self.ui = Ui_Main()
        self.ui.setupUi(self)

    def show(self):
        self.setVisible(True)
        self._amsn_core.mainWindowShown()

    def hide(self):
        self.setVisible(False)

    def set_title(self, title):
        self.setWindowTitle(title)

    def set_view(self, view):
        print "set_view request"