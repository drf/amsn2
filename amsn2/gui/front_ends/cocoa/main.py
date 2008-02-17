
from nibs import CocoaMainWindow, CocoaLoginView, CocoaLoggingInView
from amsn2.gui import base

class aMSNMainWindow(base.aMSNMainWindow):
    cocoaWin = None
    loginView = None
    
    def __init__(self, amsn_core):
        self._amsn_core = amsn_core
        
        # Load our window.
        self.cocoaWin = CocoaMainWindow.getMainWindow()
        # Load our views.
        self.loginView = CocoaLoginView.getView()
        self.loggingInView = CocoaLoggingInView.getView()
    
    def setTitle(self, title):
        self.cocoaWin.setTitle_(title)
    
    def show(self):
        self.cocoaWin.makeKeyAndOrderFront_(self.cocoaWin)
        self._amsn_core.idlerAdd(self.__on_show)

    def hide(self):
        self.cocoaWin.orderOut_(self.cocoaWin)
    
    def _loadView(self, view, resize=True):
        prevFrame = self.cocoaWin.frame()
        frame = self.cocoaWin.frameRectForContentRect_(view.frame())
        if resize == True:
            self.cocoaWin.setFrame_display_animate_((prevFrame.origin, frame.size), True, True)
        self.cocoaWin.setContentView_(view)
        self.cocoaWin.orderFront_(self.cocoaWin)
    
    def __on_show(self):
        self._amsn_core.mainWindowShown()
