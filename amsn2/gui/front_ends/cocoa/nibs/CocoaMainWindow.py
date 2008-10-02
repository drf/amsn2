
# NB. This is a NIBless utility class. It may be extended in the future..

# http://kickingkittens.com/wiki/doku.php?id=windowlessnibtutorial
# Code not using NibClassBuilder
#https://develop.participatoryculture.org/trac/democracy/changeset/5711/trunk/tv/platform/osx/frontend/VideoDisplay.py?format=diff&new=5711

import os
from objc import *
from Foundation import *
from AppKit import *

class aMSNCocoaMainWindow(NSWindow):
    def init(self):
        super(aMSNCocoaMainWindow, self).init()
        self.setDelegate_(self)
        return self

