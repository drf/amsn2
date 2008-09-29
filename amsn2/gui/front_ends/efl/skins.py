import os.path

class Skin(object):
    def __init__(self, core, path):
        self._path = path
        self._dict = {}
        #TODO : remove, it's just here for test purpose
        #TODO : explain a bit :D
        self.setKey("buddy_away", ("File", "amsn2/themes/default/images/away.png"))
        self.setKey("buddy_brb", ("File", "amsn2/themes/default/images/away.png"))

        # Just to show you can use an image from the edj file
        self.setKey("buddy_busy", ("EET", ("amsn2/themes/default.edj", "images/0")))

        self.setKey("buddy_hidden", ("File", "amsn2/themes/default/images/offline.png"))
        self.setKey("buddy_idle", ("File", "amsn2/themes/default/images/away.png"))
        self.setKey("buddy_lunch", ("File", "amsn2/themes/default/images/away.png"))
        self.setKey("buddy_offline", ("File", "amsn2/themes/default/images/offline.png"))
        self.setKey("buddy_online", ("File", "amsn2/themes/default/images/online.png"))
        self.setKey("buddy_phone", ("File", "amsn2/themes/default/images/busy.png"))

        self.setKey("default_dp", ("File", "amsn2/themes/default/images/contact_list/nopic.png"))

        self.setKey("emblem_busy", ("File", "amsn2/themes/default/images/contact_list/busy_emblem.png"))

         
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
