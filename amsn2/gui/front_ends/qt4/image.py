from amsn2.gui import base

from PyQt4.QtCore import *
from PyQt4.QtGui import *
    
class Image(QPixmap, base.Image):
    def __init__(self, amsn_core, window):
        QPixmap.__init__(self)
        self._core = amsn_core
        self._window = window

    def loadFromFile(self, filename):
        self.load(filename)

    def loadFromResource(self, resource_name):
        raise NotImplementedError
