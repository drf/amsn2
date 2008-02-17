
import os
from objc import *
from Foundation import *
from AppKit import *

view = None
def getView():
    global view
    return view

# This is a view that we can load into the main window.
class aMSNCocoaLoggingInView(NSView):
    statusText =        IBOutlet('statusText')          # Text field with status text.
    progressIndicator = IBOutlet('progressIndicator')   # Spinner.
    
    def awakeFromNib(self):
        global view
        view = self
        self.progressIndicator.startAnimation_(self)
    
    def setStatus(self, newText):
        self.statusText.setStringValue_(newText)

NSBundle.loadNibNamed_owner_('aMSNCocoaLoggingInView', NSApplication.sharedApplication())
