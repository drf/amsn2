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

class aMSNMainWindow(base.aMSNMainWindow):
    def __init__(self, amsn_core):
        self.ui = Ui_Main()
        self.main_win = QMainWindow()
        self.ui.setupUi(self.main_win)

    def show(self):
        self.main_win.show()

    def set_title(self, title):
        self.main_win.setTitle(title)

    def hide(self):
        self.main_win.hide()

    def __on_show(self):
        self._amsn_core.mainWindowShown()