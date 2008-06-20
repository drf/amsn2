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
    
class Image(QPixmap, base.Image):
    def __init__(self, amsn_core, window):
        QPixmap.__init__(self)
        self._core = amsn_core
        self._window = window

    def loadFromFile(self, filename):
        self.load(filename)

    def loadFromResource(self, resource_name):
        raise NotImplementedError