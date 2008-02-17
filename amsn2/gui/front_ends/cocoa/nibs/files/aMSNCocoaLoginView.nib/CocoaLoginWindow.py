
from amsn2.gui.front_ends.cocoa import main_loop

import os
from objc import *
from Foundation import *
from AppKit import *

#import 

#NibClassBuilder.extractClasses('aMSNCocoaMainWindow')

# NibClassBuilder.AutoBaseClass doesn't work for some reason...
class aMSNCocoaMainWindow(NSWindow):
    def test_(self):
        pass

    def awakeFromNib_(self):
	    print 'hello world'

NSBundle.loadNibNamed_owner_('aMSNCocoaMainWindow.nib', currentBundle())
