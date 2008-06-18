
import evas
import ecore
import ecore.evas

from amsn2.gui import base

class Image(base.Image):
    def __init__(self, amsn_core, window):
        self._amsn_core = amsn_core
        self._amsn_gui = self._amsn_core.getMainWindow()
        self._evas = self._amsn_gui._evas
        self._img = self._evas.evas.Image()

    def loadFromFile(self, filename):
        try:
            self._img.file_set(filename)
        except evas.EvasLoadError, e:
            print "EvasLoadError: %s" % e
        else:
            print self._img.load_error


    def loadFromResource(self, resource_name):
        raise NotImplementedError


