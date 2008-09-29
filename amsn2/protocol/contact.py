
import pymsn
import pymsn.event

class ContactEvents(pymsn.event.ContactEventInterface):

    def __init__(self, client, contact_manager):
        self._contact_manager = contact_manager
        pymsn.event.ContactEventInterface.__init__(self, client)
        
    def on_contact_presence_changed(self, contact):
        self._contact_manager.onContactPresenceChanged(contact)

