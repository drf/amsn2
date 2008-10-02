
from nibs import CocoaMainWindow
from amsn2.gui import base

class aMSNMainWindow(base.aMSNMainWindow):
    cocoaWin = None
    
    def __init__(self, amsn_core):
        self._amsn_core = amsn_core
        
        # Load our window.
        self.cocoaWin = CocoaMainWindow.aMSNCocoaMainWindow.alloc().init()
    
    def setMenu(self, menu_view):
        pass
    
    def setTitle(self, title):
        self.cocoaWin.setTitle_(title)
    
    def show(self):
        self.cocoaWin.makeKeyAndOrderFront_(self.cocoaWin)
        self._amsn_core.idlerAdd(self.__on_show)

    def hide(self):
        self.cocoaWin.orderOut_(self.cocoaWin)
    
    def _loadView(self, view, resize=False):
        prevFrame = self.cocoaWin.frame()
        frame = self.cocoaWin.frameRectForContentRect_(view.frame())
        self.cocoaWin.setFrame_display_animate_((prevFrame.origin, frame.size), True, bool(resize))
        self.cocoaWin.setContentView_(view)
        self.cocoaWin.orderFront_(self.cocoaWin)
    
    def __on_show(self):
        self._amsn_core.mainWindowShown()
