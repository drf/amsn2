import sys
from amsn2.gui import base

try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    from fadingwidget import FadingWidget
except ImportError, msg:
    print "Could not import all required modules for the Qt 4 GUI."
    print "ImportError: " + str(msg)
    sys.exit()
    
class aMSNSplashScreen(QSplashScreen, base.aMSNSplashScreen):

    def __init__(self, amsn_core, parent=None):
        QSplashScreen.__init__(self, parent)

    def show(self):
        self.setVisible(True)
        qApp.processEvents()
    
    def hide(self):
        self.setVisible(False)
        qApp.processEvents()
    
    def showText(self, text):
        self.showMessage(text)
        qApp.processEvents()
        
    def setImage(self, image):
        self.setPixmap(image)
        qApp.processEvents()