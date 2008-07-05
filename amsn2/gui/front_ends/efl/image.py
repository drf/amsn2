
import evas
import ecore
import ecore.evas

from amsn2.gui import base

class Image(base.Image):
    def __init__(self, amsn_core, window):
        self._amsn_core = amsn_core
        self._amsn_gui = self._amsn_core.getMainWindow()
        self._evas = self._amsn_gui._evas
        self._skin = self._amsn_core._skin_manager.skin
        self._img = self._evas.evas.Image()

    def loadFromFile(self, filename):
        print "loading image %s" % filename
        try:
            self._img.file_set(filename)
        except evas.EvasLoadError, e:
            print "EvasLoadError: %s" % (e,)
            #TODO : raise ImgLoadError ?

    def loadFromEET(self, (eetfile, key)):
        print "eetfile = %s, key = %s" % (eetfile, key)
        self._img.file_set(eetfile, key)


    def loadFromResource(self, resource_name):
        (type, value) = self._skin.getKey(resource_name)
        try:
            loadMethod = getattr(self, "loadFrom%s" % type)
        except AttributeError, e:
            print "From loadFromResource in efl/image.py:\n\t(type, value) = (%s, %s)\n\tAttributeError: %s" % (type, value, e)
        else:
            loadMethod(value)


