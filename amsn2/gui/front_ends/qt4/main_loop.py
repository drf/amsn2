from amsn2.gui import base
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import gobject

class aMSNMainLoop(base.aMSNMainLoop):
    def __init__(self, amsn_core):
        import os
        os.putenv("QT_NO_GLIB", "1") # FIXME: Temporary workaround for segfault
                                     #        caused by GLib Event Loop integration
        self.app = QApplication(sys.argv)
        self.gmainloop = gobject.MainLoop()
        self.gcontext = self.gmainloop.get_context()

    def __del__(self):
        self.gmainloop.quit()

    def run(self):
        self.idletimer = QTimer(QApplication.instance())
        QObject.connect(self.idletimer, SIGNAL('timeout()'), self.on_idle)
        self.idletimer.start(100)
        self.app.exec_()

    def on_idle(self):
        iter = 0
        while iter < 10 and self.gcontext.pending():
            self.gcontext.iteration()
            iter += 1

    def idlerAdd(self, func):
        print "idlerAdd req"
        pass

    def timerAdd(self, delay, func):
        print "timerAdd req"
        pass

    def quit(self):
        pass
