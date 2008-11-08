import gobject

class Skin(object):
    def __init__(self, core, path):
        self._path = path
        pass

    def getKey(self, key, default):
        pass

    def setKey(self, key, value):
        pass



class SkinManager(object):
    def __init__(self, core):
        self._core = core
        self.skin = Skin(core, "skins")

    def setSkin(self, name):
        self.skin = Skin(self._core, os.path.join("skins", name))

    def listSkins(self, path):
        pass

