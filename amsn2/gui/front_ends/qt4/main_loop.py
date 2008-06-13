from amsn2.gui import base
import sys

try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    import gobject
except ImportError, msg:
    print "Could not import all required modules for the Qt 4 GUI."
    print "ImportError: " + str(msg)
    sys.exit()

class aMSNMainLoop(base.aMSNMainLoop):
    def __init__(self, amsn_core):
        import os
        os.putenv("QT_NO_GLIB", "1")
        self.app = QApplication(sys.argv)

    def run(self):
        
        self.gmainloop = gobject.MainLoop()
        self.gcontext = self.gmainloop.get_context()
        self.idletimer = QTimer(QApplication.instance())
        QObject.connect(self.idletimer, SIGNAL('timeout()'), self.on_idle)
        self.idletimer.start(100)
        self.app.exec_()

    def __del__(self):
        self.gmainloop.quit()

    def on_idle(self):
        iter = 0
        while iter < 10 and self.gcontext.pending():
            self.gcontext.iteration()
            iter += 1

    def idler_add(self, func):
        print "idler_add req"
        pass

    def timer_add(self, delay, func):
        print "timer_add req"
        pass

    def quit(self):
        pass
