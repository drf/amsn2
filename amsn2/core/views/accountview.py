
from imageview import *
from stringview import *
import papyon

class AccountView:
    def __init__(self):
        self.email = None
        self.password = None
        self.nick = StringView()
        self.presence = 'online'
        self.dp = ImageView()

        self.save = False
        self.save_password = False
        self.autologin = False

        self.preferred_ui = None


    def __str__(self):
        out = "{ email=" + str(self.email) + " presence=" + str(self.presence)
        out += " save=" + str(self.save) + " save_password=" + str(self.save_password)
        out += " autologin=" + str(self.autologin) + "}"
        return out
