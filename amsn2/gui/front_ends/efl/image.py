
import evas
import ecore
import ecore.evas

from amsn2.gui import base

class Image(evas.SmartObject, base.Image):
    def __init__(self, amsn_core, window):
        self._amsn_core = amsn_core
        self._amsn_gui = self._amsn_core.getMainWindow()
        self._evas = self._amsn_gui._evas
        evas.SmartObject.__init__(self, self._evas)

        
        self._skin = self._amsn_core._skin_manager.skin
        self._imgs = []



    #######################################################
    #Public methods
    def load(self, resource_type, value):
        self._imgs = [ self._evas.Image() ]
        try:
            loadMethod = getattr(self, "_loadFrom%s" % resource_type)
        except AttributeError, e:
            print "From load in efl/image.py:\n\t(resource_type, value) = (%s, %s)\n\tAttributeError: %s" % (resource_type, value, e)
        else:
            loadMethod(value)
        
    def append(self, resource_type, value):
        self._imgs.append(self._evas.Image())
        try:
            loadMethod = getattr(self, "_loadFrom%s" % resource_type)
        except AttributeError, e:
            print "From append in efl/image.py:\n\t(resource_type, value) = (%s, %s)\n\tAttributeError: %s" % (resource_type, value, e)
        else:
            loadMethod(value, pos=-1)

    def prepend(self, resource_type, value):
        self._imgs.insert(0, self._evas.Image())
        try:
            loadMethod = getattr(self, "_loadFrom%s" % resource_type)
        except AttributeError, e:
            print "From prepend in efl/image.py:\n\t(resource_type, value) = (%s, %s)\n\tAttributeError: %s" % (resource_type, value, e)
        else:
            loadMethod(value, pos=0)



    def _loadFromFile(self, filename, pos=0):
        try:
            self._imgs[pos].file_set(filename)
        except evas.EvasLoadError, e:
            print "EvasLoadError: %s" % (e,)

    def _loadFromEET(self, (eetfile, key), pos=0):
        try:
            self._imgs[pos].file_set(eetfile, key)
        except evas.EvasLoadError, e:
            print "EvasLoadError: %s" % (e,)

    def _loadFromSkin(self, resource_name, pos=0):
        res = self._skin.getKey(resource_name)
        if res is not None:
            (type, value) = res
            try:
                loadMethod = getattr(self, "_loadFrom%s" % type)
            except AttributeError, e:
                print "From _loadFromSkin in efl/image.py:\n\t(type, value) = (%s, %s)\n\tAttributeError: %s" % (type, value, e)
            else:
                loadMethod(value, pos)



    #######################################################
    # Need to overwritre some evas.SmartObject methods:

    def show(self):
        for img in self._imgs:
            img.show()

    def hide(self):
        for img in self._imgs:
            img.hide()

    def resize(self, w, h):
        for img in self._imgs:
            img.size_set(w, h)
            img.fill_set(0,0,w,h)

    def clip_set(self, obj):
        for img in self._imgs:
            img.clip_set(obj)

    def clip_unset(self):
        for img in self._imgs:
            img.clip_unset()

    def move(self, x, y):
        for img in self._imgs:
            img.move(x ,y)


