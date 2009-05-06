
import evas
import ecore
import ecore.evas

import tempfile
import os

from amsn2.core.views import imageview

class Image(evas.SmartObject):
    def __init__(self, skin, canvas, view):
        self._evas = canvas
        evas.SmartObject.__init__(self, self._evas)

        self._skin = skin
        self._imgs = []
        self.propagate_events = True

        self.load(view)

    #######################################################
    #Public method
    def load(self, view):
        for img in self._imgs:
            self.member_del(img)

        self._imgs = []
        i = 0
        for (resource_type, value) in view.imgs:
            self._imgs.append(self._evas.Image())
            self.member_add(self._imgs[-1])
            try:
                loadMethod = getattr(self, "_loadFrom%s" % resource_type)
            except AttributeError, e:
                print "From load in efl/image.py:\n\t(resource_type, value) = (%s, %s)\n\tAttributeError: %s" % (resource_type, value, e)
            else:
                loadMethod(value, -1, view, i)
                i += 1



    def _loadFromFilename(self, filename, pos=0, view=None, i=0):
        try:
            self._imgs[pos].file_set(filename)
        except evas.EvasLoadError, e:
            print "EvasLoadError: %s" % (e,)

    def _loadFromEET(self, (eetfile, key), pos=0, view=None, i=0):
        try:
            self._imgs[pos].file_set(eetfile, key)
        except evas.EvasLoadError, e:
            print "EvasLoadError: %s" % (e,)

    def _loadFromFileObject(self, fileobject, pos=0, view=None, i=0):
        (fno, tf) = tempfile.mkstemp()
        f = os.fdopen(fno, 'w+b')
        f.write(fileobject.read())
        f.close()
        if view is not None:
            view.imgs[i] = ("Filename", tf)
        self._loadFromFilename(tf, pos, view, i)


    def _loadFromTheme(self, resource_name, pos=0, view=None, i=0):
        res = self._skin.getKey(resource_name)
        if res is not None:
            (type, value) = res
            try:
                loadMethod = getattr(self, "_loadFrom%s" % type)
            except AttributeError, e:
                print "From _loadFromSkin in efl/image.py:\n\t(type, value) = (%s, %s)\n\tAttributeError: %s" % (type, value, e)
            else:
                loadMethod(value, pos, view, i)

    def _loadFromNone(self, r, pos=0):
        pass

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


