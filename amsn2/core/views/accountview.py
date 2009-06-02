
from imageview import *
from stringview import *
import papyon

class AccountView:
    def __init__(self):
        self.email = None
        self.password = None
        self.nick = StringView()
        self.presence = papyon.Presence.ONLINE
        self.dp = ImageView()

        self.save = False

        self.preferred_ui = None
