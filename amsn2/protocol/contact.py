
from amsn2.core.views import *

import pymsn
import pymsn.event

class ContactEvents(pymsn.event.ContactEventInterface):

    def __init__(self, client, contact_manager):
        self._contact_manager = contact_manager
        pymsn.event.ContactEventInterface.__init__(self, client)

    def on_contact_presence_changed(self, contact):
        c = ContactView.getContact(self._contact_manager._core, contact.id, contact)
        self._contact_manager.onContactPresenceChanged(c)

