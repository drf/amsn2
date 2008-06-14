import sys

try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except ImportError, msg:
    print "Could not import all required modules for the Qt 4 GUI."
    print "ImportError: " + str(msg)
    sys.exit()

class FadingWidget(QWidget):
    def __init__(self, bgColor, parent=None):
        QWidget.__init__(self, parent)
        self._timeLine = QTimeLine(640) # Not too fast, not too slow...
        self._opacity = 0.0
        self._bgColor = bgColor
        QObject.connect(self._timeLine, SIGNAL("valueChanged(qreal)"), self.__setOpacity)
        QObject.connect(self._timeLine, SIGNAL("finished()"), self.__animCompleted)

    def __animCompleted(self):
        if self._opacity == 0.0:
            self.emit(SIGNAL("fadeInCompleted()"))
        elif self._opacity == 1.0:
            self.emit(SIGNAL("fadeOutCompleted()"))

    def fadeIn(self):
        self._timeLine.setDirection(QTimeLine.Backward)
        if self._timeLine.state() == QTimeLine.NotRunning:
            self._timeLine.start()

    def fadeOut(self):
        self._timeLine.setDirection(QTimeLine.Forward)
        if self._timeLine.state() == QTimeLine.NotRunning:
            self._timeLine.start()

    def __setOpacity(self, newOpacity):
        self._opacity = newOpacity
        self.update()

    def paintEvent(self, event):
        if self._opacity > 0.0:
            p = QPainter()
            p.begin(self)
            p.setBrush(self._bgColor)
            p.setOpacity(self._opacity)
            p.drawRect(self.rect())
            p.end()