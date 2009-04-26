from imageview import *
from stringview import *
import pymsn

class ProfileView:
    def __init__(self):
        self.email = StringView()
        self.password = StringView()
        self.nick = StringView()
        self.status = pymsn.Presence.ONLINE
        self.dp = ImageView()
        self.saveprofile = False
        #TODO: preferred UI ?
