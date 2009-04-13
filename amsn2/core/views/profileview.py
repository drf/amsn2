from imageview import *
from stringview import *

class ProfileView:
    def __init__(self):
        self.email = Stringview()
        self.password = Stringview()
        self.nick = Stringview()
        self.status = pymsn.Presence.ONLINE
        self.dp = Imageview()
        self.saveprofile = False
        #TODO: preferred UI ?
