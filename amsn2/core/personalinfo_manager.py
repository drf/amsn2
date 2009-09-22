from views import *

class aMSNPersonalInfoManager:
    def __init__(self, core):
        """
        @type core: aMSNCore
        """

        self._core = core
        self._backend_manager = core._backend_manager
        self._em = core._event_manager
        self._personalinfoview = PersonalInfoView(self)
        self._papyon_profile = None

    def setAccount(self, amsn_account):
        self._papyon_profile = amsn_account.client.profile

        # set nickname at login
        # could be overriden by the one set in the saved account
        # TODO: add setting display picture
        strv = StringView()
        nick = str(amsn_account.view.nick)
        if nick and nick != amsn_account.view.email:
            strv.appendText(nick)
        else:
            strv.appendText(self._papyon_profile.display_name)
        self._personalinfoview.nick = strv

        # TODO: The psm doesn't seem to get fetched from server. Papyon issue?
        strv = StringView()
        psm = str(amsn_account.view.psm)
        if psm:
            strv.appendText(psm)
        self._personalinfoview.psm = strv

        # set login presence, from this moment the client appears to the others
        self._personalinfoview.presence = amsn_account.view.presence

    """ Actions from ourselves """
    def _onNickChanged(self, new_nick):
        # TODO: parsing
        self._papyon_profile.display_name = str(new_nick)

    def _onPSMChanged(self, new_psm):
        # TODO: parsing
        self._papyon_profile.personal_message = str(new_psm)

    def _onPresenceChanged(self, new_presence):
        # TODO: manage custom presence
        for key in self._core.p2s:
            if self._core.p2s[key] == new_presence:
                break
        self._papyon_profile.presence = key

    def _onDPChanged(self, dp_msnobj):
        self._papyon_profile.msn_object = dp_msnobj

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

    def onDPUpdated(self, dp_msnobj):
        self._personalinfoview._image.reset()
        path = self._backend_manager.getFileLocationDP(self._papyon_profile.account,
                                                       self._papyon_profile.id,
                                                       dp_msnobj._data_sha)
        self._personalinfoview._image.load('Filename', path)
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






