
from imageview import *
from stringview import *

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

