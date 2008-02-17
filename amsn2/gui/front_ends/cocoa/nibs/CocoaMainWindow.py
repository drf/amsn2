
# http://kickingkittens.com/wiki/doku.php?id=windowlessnibtutorial
# Code not using NibClassBuilder
#https://develop.participatoryculture.org/trac/democracy/changeset/5711/trunk/tv/platform/osx/frontend/VideoDisplay.py?format=diff&new=5711

import os
from objc import *
from Foundation import *
from AppKit import *

mainWin = None
def getMainWindow():
    global mainWin
    return mainWin

class aMSNCocoaMainWindow(NSWindow):
    def saveInstance(self):
        # Keep an instance of the main window.
        global mainWin
        mainWin = self
    
    def awakeFromNib(self):
        # So that we get delegate events as well.
        self.setDelegate_(self)
    
    # We need to override these so we can save an instance of the window when it is inited.
    def initWithContentRect_styleMask_backing_defer_(self, cr, sm, b, d):
        self.saveInstance()
        return super(aMSNCocoaMainWindow, self).\
            initWithContentRect_styleMask_backing_defer_(cr, sm, b, d)
    def initWithContentRect_styleMask_backing_defer_screen_(self, cr, sm, b, d, s):
        self.saveInstance()
        return super(aMSNCocoaMainWindow, self).\
            initWithContentRect_styleMask_backing_defer_screen_(cr, sm, b, d, s)

NSBundle.loadNibNamed_owner_('aMSNCocoaMainWindow', NSApplication.sharedApplication())
