
from imageview import *
from stringview import *

class AccountView:
    def __init__(self, core, email):
        self._core = core
        self.email = email
        self.password = None
        self.nick = StringView()
        self.psm = StringView()
        self.presence = core.Presence.ONLINE
        self.dp = ImageView()

        self.save = False
        self.save_password = False
        self.autologin = False

        self.preferred_ui = None
        self.preferred_backend = 'defaultbackend'

    def __str__(self):
        out = "{ email=" + str(self.email)
        out += " presence=" + self._core.p2s[self.presence]
        out += " save=" + str(self.save) + " save_password=" + str(self.save_password)
        out += " autologin=" + str(self.autologin) + " preferred_ui=" + str(self.preferred_ui)
        out += " preferred_backend=" + self.preferred_backend + " }"
        return out
