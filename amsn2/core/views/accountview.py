
from imageview import *
from stringview import *
import papyon

class AccountView:
    def __init__(self):
        self.email = StringView()
        self.password = StringView()
        self.nick = StringView()
        self.status = papyon.Presence.ONLINE
        self.dp = ImageView()
        self.saveprofile = False
        #TODO: preferred UI ?
