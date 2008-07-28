
import evas
import ecore
import ecore.evas

from amsn2.gui import base

class Image(evas.SmartObject, base.Image):
    def __init__(self, amsn_core, window):
        self._amsn_core = amsn_core
        self._amsn_gui = self._amsn_core.getMainWindow()
        self._evas = self._amsn_gui._evas
        evas.SmartObject.__init__(self, self._evas.evas)

        
        self._skin = self._amsn_core._skin_manager.skin
        self._imgs = [ self._evas.evas.Image() ]

    def loadFromFile(self, filename):
        print "loading image %s" % filename
        try:
            self._imgs[1:] = []
            self._imgs[0].file_set(filename)
        except evas.EvasLoadError, e:
            print "EvasLoadError: %s" % (e,)
            #TODO : raise ImgLoadError ?

    def loadFromEET(self, (eetfile, key)):
        print "eetfile = %s, key = %s" % (eetfile, key)
        try:
            self._imgs[1:] = []
            self._imgs[0].file_set(eetfile, key)
        except evas.EvasLoadError, e:
            print "EvasLoadError: %s" % (e,)
            #TODO : raise ImgLoadError ?


    def loadFromResource(self, resource_name):
        res = self._skin.getKey(resource_name)
        if res is not None:
            (type, value) = res
            try:
                loadMethod = getattr(self, "loadFrom%s" % type)
            except AttributeError, e:
                print "From loadFromResource in efl/image.py:\n\t(type, value) = (%s, %s)\n\tAttributeError: %s" % (type, value, e)
            else:
                loadMethod(value)

    def addFromFile(self, filename): 
        print "loading image %s" % filename
        try:
            self._imgs.append(self._evas.evas.Image())
            self._imgs[-1].file_set(filename)
        except evas.EvasLoadError, e:
            print "EvasLoadError: %s" % (e,)
            #TODO : raise ImgLoadError ?

    def addFromResource(self, resource_name):
        res = self._skin.getKey(resource_name)
        if res is not None:
            (type, value) = res
            try:
                addMethod = getattr(self, "addFrom%s" % type)
            except AttributeError, e:
                print "From addFromResource in efl/image.py:\n\t(type, value) = (%s, %s)\n\tAttributeError: %s" % (type, value, e)
            else:
                addMethod(value)






    def show(self):
        print "show", self.size
        for img in self._imgs:
            img.show()

    def hide(self):
        print "hide", self.size
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


