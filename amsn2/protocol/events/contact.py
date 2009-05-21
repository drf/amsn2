
import papyon
import papyon.event

class ContactEvents(papyon.event.ContactEventInterface):

    def __init__(self, client, contact_manager):
        self._contact_manager = contact_manager
        papyon.event.ContactEventInterface.__init__(self, client)

    def on_contact_presence_changed(self, contact):
        self._contact_manager.onContactChanged(contact)

    def on_contact_display_name_changed(self, contact):
        self._contact_manager.onContactChanged(contact)

    def on_contact_personal_message_changed(self, contact):
        self._contact_manager.onContactChanged(contact)

    def on_contact_current_media_changed(self, contact):
        self._contact_manager.onContactChanged(contact)

    def on_contact_msn_object_changed(self, contact):
        # TODO: filter DPs
        if contact.msn_object._type is papyon.p2p.MSNObjectType.DISPLAY_PICTURE:
            self._contact_manager.onContactDPChanged(contact)

    def on_contact_memberships_changed(self, contact):
        pass

    def on_contact_infos_changed(self, contact, infos):
        pass

    def on_contact_client_capabilities_changed(self, contact):
        pass

