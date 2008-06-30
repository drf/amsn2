import os.path

class Skin(object):
    def __init__(self, core, path):
        self._path = path
        self._dict = {}
        #TODO : remove, it's just here for test purpose
        self.setKey("buddy_away", "amsn2/themes/default/images/away.png")
        self.setKey("buddy_brb", "amsn2/themes/default/images/away.png")
        self.setKey("buddy_busy", "amsn2/themes/default/images/busy.png")
        self.setKey("buddy_hidden", "amsn2/themes/default/images/offline.png")
        self.setKey("buddy_idle", "amsn2/themes/default/images/away.png")
        self.setKey("buddy_lunch", "amsn2/themes/default/images/away.png")
        self.setKey("buddy_offline", "amsn2/themes/default/images/offline.png")
        self.setKey("buddy_online", "amsn2/themes/default/images/online.png")
        self.setKey("buddy_phone", "amsn2/themes/default/images/busy.png")

         
    def getKey(self, key, default = None):
        try:
            return self._dict[key]
        except KeyError:
            return default
        
    def setKey(self, key, value):
        self._dict[key] = value




class SkinManager(object):
    def __init__(self, core):
        self._core = core
        self.skin = Skin(core, "skins")

    def setSkin(self, name):
        self.skin = Skin(self._core, os.path.join("skins", name))

    def listSkins(self, path):
        pass
