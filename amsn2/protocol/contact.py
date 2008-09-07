
import pymsn
import pymsn.event

class ContactEvents(pymsn.event.ContactEventInterface):

    def __init__(self, client, amsn_core):
        self._amsn_core = amsn_core
        pymsn.event.ContactEventInterface.__init__(self, client)
        
    def on_contact_presence_changed(self, contact):
        self._amsn_core._contact_manager.onContactPresenceChanged(contact)

