
from nibs import CocoaSplashScreenView
from amsn2.gui import base

class aMSNSplashScreen(base.aMSNSplashScreen):
    def __init__(self, amsn_core, parent):
        self.parent = parent
        self.view = CocoaSplashScreenView.getView()

    def show(self):
        self.parent._loadView(self.view)
    
    def hide(self):
        pass
    
    def setText(self, text):
        self.view.setStatus(text)
        
    def setImage(self, image):
        pass

