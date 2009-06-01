
import papyon
import papyon.event

class ProfileEvents(papyon.event.ProfileEventInterface):
    def __init__(self, client, personalinfo_manager):
        self._personalinfo_manager = personalinfo_manager
        papyon.event.ProfileEventInterface.__init__(self, client)

    def on_profile_presence_changed(self):
        self._personalinfo_manager.onPresenceUpdated(self._client.profile.presence)

    def on_profile_display_name_changed(self):
        self._personalinfo_manager.onNickUpdated(self._client.profile.display_name)

    def on_profile_personal_message_changed(self):
        self._personalinfo_manager.onPMUpdated(self._client.profile.personal_message)

    def on_profile_current_media_changed(self):
        self._personalinfo_manager.onCMUpdated(self._client.profile.current_media)

    def on_profile_msn_object_changed(self):
        #TODO: filter objects
        if self._client.profile.msn_object._type is papyon.p2p.MSNObjectType.DISPLAY_PICTURE:
            self._personalinfo_manager.onDPUpdated(self._client.profile.msn_object)
