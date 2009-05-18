
from objc import *
from Foundation import *
from AppKit import *

view = None
def getView():
    global view
    return view

class aMSNCocoaSplashScreenView(NSView):
    statusText = IBOutlet('statusText')  # Text field with status text.

    def awakeFromNib(self):
        global view
        view = self

    def setStatus(self, text):
        self.statusText.setStringValue_(text)

NSBundle.loadNibNamed_owner_('aMSNCocoaSplashScreenView', NSApplication.sharedApplication())
