from views import *

class aMSNPersonalInfoManager:
    def __init__(self, core):
        self._core = core
        self._em = core._event_manager
        self._personalinfoview = None
        self._papyon_profile = None

    def setAccount(self, amsn_account):
        self._papyon_profile = amsn_account.client.profile
        self._personalinfoview = PersonalInfoView(self._core, self._papyon_profile)

        # set login presence and update the gui
        self._personalinfoview.presence = amsn_account.presence

    """ Actions from ourselves """
    def _onNickUpdated(self, new_nick):
        # TODO: parsing
        self._papyon_profile.display_name = new_nick.toString()
        self._em.emit(self._em.events.PERSONALINFO_UPDATED, self._personalinfoview)

    def _onPMUpdated(self, new_pm):
        # TODO: parsing
        self._papyon_profile.personal_message = new_pm.toString()
        self._em.emit(self._em.events.PERSONALINFO_UPDATED, self._personalinfoview)

    def _onDPUpdated(self, new_dp):
        # TODO: manage msn_objects
        self._em.emit(self._em.events.PERSONALINFO_UPDATED, self._personalinfoview)

    def _onPresenceUpdated(self, new_presence):
        for key in self._core.p2s:
            if self._core.p2s[key] == new_presence:
                break
        self._papyon_profile.presence = key
        self._em.emit(self._em.events.PERSONALINFO_UPDATED, self._personalinfoview)

    """ actions from the core """
    def _onCMUpdated(self, new_media):
        self._papyon_profile.current_media = new_media
        self._em.emit(self._em.events.PERSONALINFO_UPDATED, self._personalinfoview)

    # TODO: connect to papyon event, maybe build a mailbox_manager
    """ Actions from outside """
    def _onNewMail(self, info):
        self._em.emit(self._em.events.PERSONALINFO_UPDATED, self._personalinfoview)






