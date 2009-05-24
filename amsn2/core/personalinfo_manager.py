from views import *

class aMSNPersonalInfoManager:
    def __init__(self, core):
        self._core = core
        self._em = core._event_manager
        self._personalinfoview = PersonalInfoView(self)
        self._papyon_profile = None

    def set_profile_connected(self, amsn_profile):
        self._papyon_profile = amsn_profile.client.profile
        #print '%s' % self._papyon_profile._profile

        # set login presence and update the gui
        self._personalinfoview.presence = amsn_profile.presence

    """ Actions from ourselves """
    def _onNickChanged(self, new_nick):
        # TODO: parsing
        self._papyon_profile.display_name = new_nick.toString()

    def _onPSMChanged(self, new_psm):
        # TODO: parsing
        self._papyon_profile.personal_message = new_psm.toString()

    def _onPresenceChanged(self, new_presence):
        # TODO: manage custom presence
        for key in self._core.p2s:
            if self._core.p2s[key] == new_presence:
                break
        self._papyon_profile.presence = key

    def _onDPChangeRequest(self):
        # TODO: tell the core to invoke a file chooser and change DP
        pass

    def _onDPChanged(self, new_dp):
        # TODO: manage msn_objects
        self._papyon_profile.msn_object = new_dp

    def _onPresenceDPChanged(self, new_presence, new_dp):
        # TODO: manage msn_objects
        self._papyon_profile.presence_msn_object = presence, new_dp

    def _onPSMCMChanged(self, new_psm, new_media):
        self._papyon_profile.personal_message_current_media = new_psm, new_media

    """ Actions from the core """
    def _onCMChanged(self, new_media):
        self._papyon_profile.current_media = new_media

    """ Notifications from the server """
    def onNickUpdated(self, nick):
        # TODO: parse fields for smileys, format, etc
        self._personalinfoview._nickname.reset()
        self._personalinfoview._nickname.appendText(nick)
        self._em.emit(self._em.events.PERSONALINFO_UPDATED, self._personalinfoview)

    def onPSMUpdated(self, psm):
        # TODO: parse fields for smileys, format, etc
        self._personalinfoview._psm.reset()
        self._personalinfoview._psm.appendText(psm)
        self._em.emit(self._em.events.PERSONALINFO_UPDATED, self._personalinfoview)

    def onDPUpdated(self, dp):
        self._personalinfoview._image.reset()
        self._personalinfoview._image.load(dp)
        self._em.emit(self._em.events.PERSONALINFO_UPDATED, self._personalinfoview)

    def onPresenceUpdated(self, presence):
        self._personalinfoview._presence = self._core.p2s[presence]
        self._em.emit(self._em.events.PERSONALINFO_UPDATED, self._personalinfoview)

    def onCMUpdated(self, cm):
        self._personalinfoview._current_media.reset()
        #TODO: insert separators
        self._personalinfoview._current_media.apprndText(cm[0])
        self._personalinfoview._current_media.apprndText(cm[1])
        self._em.emit(self._em.events.PERSONALINFO_UPDATED, self._personalinfoview)

    # TODO: connect to papyon event, maybe build a mailbox_manager
    """ Actions from outside """
    def _onNewMail(self, info):
        self._em.emit(self._em.events.PERSONALINFO_UPDATED, self._personalinfoview)






