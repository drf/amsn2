
import pymsn
import pymsn.event
from client import *
from contact import *
from invite import *

class Client(pymsn.Client):
    def __init__(self, amsn_core, profile):
        self._amsn_profile = profile
        self._amsn_core = amsn_core
        server = (self._amsn_profile.getConfigKey("ns_server", "messenger.hotmail.com"), 
                  self._amsn_profile.getConfigKey("ns_port", 1863))
        pymsn.Client.__init__(self, server)

        self._client_events_handler = ClientEvents(self, self._amsn_core)
        self._contact_events_handler = ContactEvents(self, self._amsn_core._contact_manager)
        self._invite_events_handles = InviteEvents(self, self._amsn_core)

    def connect(self):
        self.login(self._amsn_profile.email, self._amsn_profile.password)
        
    def changeNick(self, nick):
        self.profile.display_name = nick.toString()
        
    def changeMessage(self, message):
        self.profile.personal_message = message.toString()

