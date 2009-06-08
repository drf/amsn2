import os.path

class Skin(base.Skin):
    def __init__(self, core, path):
        self._path = path
        self._dict = {}
        #TODO : remove, it's just here for test purpose
        #TODO : explain a bit :D
        self.setKey("buddy_online", ("Filename", "amsn2/themes/default/images/online.png"))
        self.setKey("emblem_online", ("Filename", "amsn2/themes/default/images/contact_list/plain_emblem.png"))

        self.setKey("buddy_away", ("Filename", "amsn2/themes/default/images/away.png"))
        self.setKey("emblem_away", ("Filename", "amsn2/themes/default/images/contact_list/away_emblem.png"))
        self.setKey("buddy_brb", ("Filename", "amsn2/themes/default/images/away.png"))
        self.setKey("emblem_brb", ("Filename", "amsn2/themes/default/images/contact_list/away_emblem.png"))
        self.setKey("buddy_idle", ("Filename", "amsn2/themes/default/images/away.png"))
        self.setKey("emblem_idle", ("Filename", "amsn2/themes/default/images/contact_list/away_emblem.png"))
        self.setKey("buddy_lunch", ("Filename", "amsn2/themes/default/images/away.png"))
        self.setKey("emblem_lunch", ("Filename", "amsn2/themes/default/images/contact_list/away_emblem.png"))

        # Just to show you can use an image from the edj file
        self.setKey("buddy_busy", ("EET", ("amsn2/themes/default.edj", "images/0")))
        self.setKey("emblem_busy", ("Filename", "amsn2/themes/default/images/contact_list/busy_emblem.png"))
        self.setKey("buddy_phone", ("EET", ("amsn2/themes/default.edj", "images/0")))
        self.setKey("emblem_phone", ("Filename", "amsn2/themes/default/images/contact_list/busy_emblem.png"))

        self.setKey("buddy_offline", ("Filename", "amsn2/themes/default/images/offline.png"))
        self.setKey("emblem_offline", ("Filename", "amsn2/themes/default/images/contact_list/offline_emblem.png"))
        self.setKey("buddy_hidden", ("Filename", "amsn2/themes/default/images/offline.png"))
        self.setKey("emblem_hidden", ("Filename", "amsn2/themes/default/images/contact_list/offline_emblem.png"))

        self.setKey("default_dp", ("Filename", "amsn2/themes/default/images/contact_list/nopic.png"))



    def getKey(self, key, default=None):
        try:
            return self._dict[key]
        except KeyError:
            return default

    def setKey(self, key, value):
        self._dict[key] = value




class SkinManager(base.SkinManager):
    def __init__(self, core):
        self._core = core
        self.skin = Skin(core, "skins")

    def setSkin(self, name):
        self.skin = Skin(self._core, os.path.join("skins", name))

    def listSkins(self, path):
        pass
