
import papyon
import papyon.event

class ContactEvents(papyon.event.ContactEventInterface):

    def __init__(self, client, contact_manager):
        self._contact_manager = contact_manager
        papyon.event.ContactEventInterface.__init__(self, client)
        
    def on_contact_presence_changed(self, contact):
        self._contact_manager.onContactPresenceChanged(contact)

