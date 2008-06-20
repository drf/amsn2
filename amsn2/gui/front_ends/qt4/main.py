from amsn2.gui import base

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from fadingwidget import FadingWidget

class aMSNMainWindow(QMainWindow, base.aMSNMainWindow):
    def __init__(self, amsn_core, parent=None):
        QMainWindow.__init__(self, parent)
        self._amsn_core = amsn_core
        self.centralWidget = QWidget(self)
        self.stackedLayout = QStackedLayout()
        #self.stackedLayout.setStackingMode(QStackedLayout.StackAll)
        self.centralWidget.setLayout(self.stackedLayout)
        self.setCentralWidget(self.centralWidget)
        self.opaqLayer = FadingWidget(Qt.white, self)
        self.stackedLayout.addWidget(self.opaqLayer)
        QObject.connect(self.opaqLayer, SIGNAL("fadeInCompleted()"), self.__activateNewWidget)
        QObject.connect(self.opaqLayer, SIGNAL("fadeOutCompleted()"), self.__fadeIn)
        self.resize(230, 550)

    def fadeIn(self, widget):
        widget.setAutoFillBackground(True)
        self.stackedLayout.addWidget(widget)
        self.stackedLayout.setCurrentWidget(self.opaqLayer)
        # Is there another widget in here?
        if self.stackedLayout.count() > 2:
            self.opaqLayer.fadeOut() # Fade out current active widget
        else:
            self.__fadeIn()

    def __fadeIn(self):
        # Delete old widget(s)
        while self.stackedLayout.count() > 2:
            widget = self.stackedLayout.widget(1)
            self.stackedLayout.removeWidget(widget)
            widget.deleteLater()
        self.opaqLayer.fadeIn()

    def __activateNewWidget(self):
        self.stackedLayout.setCurrentIndex(self.stackedLayout.count()-1)

    def show(self):
        self.setVisible(True)
        self._amsn_core.mainWindowShown()

    def hide(self):
        self.setVisible(False)

    def set_title(self, title):
        self.setWindowTitle(title)

    def set_view(self, view):
        print "set_view request"
