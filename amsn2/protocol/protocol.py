
import pymsn
import pymsn.event


class ClientEvents(pymsn.event.ClientEventInterface):
    def __init__(self, client, amsn_core):
        self._amsn_core = amsn_core
        pymsn.event.ClientEventInterface.__init__(self, client)

    def on_client_state_changed(self, state):
        self._amsn_core.connectionStateChanged(self._client._amsn_profile, state)
        
        if state == pymsn.event.ClientState.OPEN:
            self._client.profile.display_name = "aMSN2"
            self._client.profile.presence = pymsn.Presence.ONLINE
            self._client.profile.current_media = ("I listen to", "Nothing")
            self._client.profile.personal_message = "Testing aMSN2!"

    def on_client_error(self, error_type, error):
        print "ERROR :", error_type, " ->", error

class ContactEvents(pymsn.event.ContactEventInterface):

    def __init__(self, client, amsn_core):
        self._amsn_core = amsn_core
        pymsn.event.ContactEventInterface.__init__(self, client)
        
    def on_contact_presence_changed(self, contact):
        self._amsn_core.contactPresenceChanged(self._client._amsn_profile, contact)


class Client(pymsn.Client):
    def __init__(self, amsn_core, profile):
        self._amsn_profile = profile
        self._amsn_core = amsn_core
        server = (self._amsn_profile.getConfigKey("ns_server", "messenger.hotmail.com"), 
                  self._amsn_profile.getConfigKey("ns_port", 1863))
        pymsn.Client.__init__(self, server)

        self._client_events_handler = ClientEvents(self, self._amsn_core)
        self._contact_events_handler = ContactEvents(self, self._amsn_core)

    def connect(self):
        self.login(self._amsn_profile.email, self._amsn_profile.password)

