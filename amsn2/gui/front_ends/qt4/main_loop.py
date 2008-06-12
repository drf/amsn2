from amsn2.gui import base
import sys

try:
    from PyQt4.QtGui import *
except ImportError, msg:
    print "Could not import all required modules for the Qt 4 GUI."
    print "ImportError: " + str(msg)
    sys.exit()

class aMSNMainLoop(base.aMSNMainLoop):
    def __init__(self, amsn_core):
        self.loop = QApplication(sys.argv)

    def run(self):
        sys.exit(self.loop.exec_())

    def idler_add(self, func):
        pass

    def timer_add(self, delay, func):
        pass

    def quit(self):
        pass