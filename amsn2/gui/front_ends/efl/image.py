
import evas
import ecore
import ecore.evas

from amsn2.core.views import imageview

class Image(evas.SmartObject):
    def __init__(self, skin, canvas, view=None):
        self._evas = canvas
        evas.SmartObject.__init__(self, self._evas)

        self._skin = skin
        self._imgs = []
        self.propagate_events = True

        if view is not None:
            self.load(view)
    #######################################################
    #Public methods
    def load(self, view):
        for img in self._imgs:
            self.member_del(img)

        self._imgs = []
        for (resource_type, value) in view.imgs:
            self._imgs.append(self._evas.Image())
            self.member_add(self._imgs[-1])
            try:
                loadMethod = getattr(self, "_loadFrom%s" % resource_type)
            except AttributeError, e:
                print "From load in efl/image.py:\n\t(resource_type, value) = (%s, %s)\n\tAttributeError: %s" % (resource_type, value, e)
            else:
                loadMethod(value, -1)

    def appendView(self, view):
        for (resource_type, value) in view.imgs:
            img = self._evas.Image()
            self.member_add(img)
            self._imgs.append(img)
            try:
                loadMethod = getattr(self, "_loadFrom%s" % resource_type)
            except AttributeError, e:
                print "From append in efl/image.py:\n\t(resource_type, value) = (%s, %s)\n\tAttributeError: %s" % (resource_type, value, e)
            else:
                loadMethod(value, pos=-1)

    def appendImage(self, image):
        for i in image._imgs:
            self._imgs.append(i)
            self.member_add(i)

    def prependView(self, resource_type, value):
        for (resource_type, value) in view.imgs.reverse():
            img = self._evas.Image()
            self.member_add(img)
            self._imgs.insert(0, img)
            try:
                loadMethod = getattr(self, "_loadFrom%s" % resource_type)
            except AttributeError, e:
                print "From prepend in efl/image.py:\n\t(resource_type, value) = (%s, %s)\n\tAttributeError: %s" % (resource_type, value, e)
            else:
                loadMethod(value, pos=0)

    def prependImage(self, image):
        for i in image._imgs.reverse():
            self._imgs.insert(0,i)
            self.member_add(i)


    def _loadFromFilename(self, filename, pos=0):
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


