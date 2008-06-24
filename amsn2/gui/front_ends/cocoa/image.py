
from AppKit import *
from amsn2.gui import base

class Image(base.Image):
    def __init__(self, amsn_core, window):
        self._amsn_core = amsn_core
        self._amsn_gui = self._amsn_core.getMainWindow()
        #self._img = NSImage.alloc().init()

    def loadFromFile(self, filename):
        #self._img.release()
        #self._img = NSImage.alloc().initWithContentsOfFile_(filename)
        pass

    def loadFromResource(self, resource_name):
        raise NotImplementedError


