
from amsn2.gui import base

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from fadingwidget import FadingWidget
    
class aMSNSplashScreen(QSplashScreen, base.aMSNSplashScreen):

    def __init__(self, amsn_core, parent):
        QSplashScreen.__init__(self, parent)

    def show(self):
        self.setVisible(True)
        qApp.processEvents()
    
    def hide(self):
        self.setVisible(False)
        qApp.processEvents()
    
    def setText(self, text):
        self.showMessage(text)
        qApp.processEvents()
        
    def setImage(self, image):
        self.setPixmap(image)
        qApp.processEvents()
