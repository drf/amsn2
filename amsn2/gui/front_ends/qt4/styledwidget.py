import sys

try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    from ui_login import Ui_Login
    from fadingwidget import FadingWidget
except ImportError, msg:
    print "Could not import all required modules for the Qt 4 GUI."
    print "ImportError: " + str(msg)
    sys.exit()

# Styled Widget: QWidget subclass that directly supports Qt StyleSheets
class StyledWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

    # Needed to support StyleSheets on pure subclassed QWidgets
    # See: http://doc.trolltech.com/4.4/stylesheet-reference.html
    def paintEvent(self, event):
        opt = QStyleOption()
        opt.init(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

    # FIXME: This is just temporary!!!! for testing
    def setTestStyle(self, state):
        if state == Qt.Checked:
            self.setStyleSheet("#Login {"
        "background-color: qradialgradient(spread:reflect, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(224, 219, 255, 255), stop:1 rgba(255, 255, 255, 255));"
        "}"

        "QLineEdit {"
        "border: 2px solid rgb(180, 180, 180);"
        "border-radius: 10px;"
        "background-color: white;"
        "selection-background-color: darkgray;"
        "padding: 1px 18px 1px 3px;"
        "}"

        "QComboBox {"
        "border: 2px solid rgb(180, 180, 180);"
        "border-radius: 10px;"
        "background-color: white;"
        "selection-background-color: darkgray;"
        "padding: 1px 18px 1px 3px;"
        "min-width: 6em;"
        "}"

        "QComboBox:editable {"
        "background-color: white;"
        "}"

                 "QComboBox:!editable, QComboBox::drop-down:editable {"
                 "     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,"
                 "                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,"
                 "                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);"
                 "}"

                 "QComboBox:!editable:on, QComboBox::drop-down:editable:on {"
                 "    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,"
                 "                                       #self.status.set_text(message) stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,"
                 "                                stop: 0.5 #DDDDDD, stop: 1.0 #E1E1E1);"
                 "}"

                 "QComboBox::drop-down:editable {"
                 "     background: white;"
                 "}"

                 "QComboBox:on {"
                 "    padding-top: 3px;"
                 "    padding-left: 4px;"
                 "}"

                 "QComboBox::drop-down {"
                 "    subcontrol-origin: padding;"
                 "    subcontrol-position: top right;"
                 "    width: 20px;"
                 "    border-left-width: 1px;"
                 "    border-left-color: none;"
                 "    border-left-style: solid;"
                 "    border-top-right-radius: 7px;"
                 "    border-bottom-right-radius: 10px;"
                 "}"

                 "QComboBox::down-arrow {"
                 "    image: url(/usr/lib/kde4/share/icons/oxygen/16x16/actions/arrow-down.png);"
                 "}"

                 "QComboBox::down-arrow:on { "
                 "    top: 1px;"
                 "    left: 1px;"
                 "}"

        "QPushButton {"
        "background: qlineargradient(spread:repeat, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(167, 195, 255, 255), stop:1 rgba(74, 99, 156, 255));"
        "font-weight: bold;"
        "}")
            self.ui.pixUser.setStyleSheet("#pixUser {"
        "color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 50));"
        "font-weight: bold;"
        "font-size: 20px;"
        "border: 3px solid gray;"
        "border-radius: 10px;"
        "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(185, 190, 255, 255), stop:1 rgba(255, 255, 255, 255));"
        "}"
        "#pixUser:hover {"
        "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(166, 180, 213, 255), stop:1 rgba(255, 255, 255, 255));"
        "}")
        else:
            self.setStyleSheet("")
            self.ui.pixUser.setStyleSheet("")