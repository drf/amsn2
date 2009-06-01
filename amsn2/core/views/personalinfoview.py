from stringview import *
from imageview import *

def rw_property(f):
    return property(**f())

class PersonalInfoView(object):
    def __init__(self, personalinfo_manager):
        self._personalinfo_manager = personalinfo_manager

        self._nickname = StringView()
        self._psm = StringView()
        self._current_media  = StringView()
        self._image = ImageView()
        self._presence = 'offline'

        # TODO: get more info, how to manage webcams and mail
        self._webcam = None
        self._mail_unread = None

    def onDPChangeRequest(self):
        self._personalinfo_manager._onDPChangeRequest()

    @rw_property
    def nick():
        def fget(self):
            return self._nickname
        def fset(self, nick):
            self._personalinfo_manager._onNickChanged(nick)
        return locals()

    @rw_property
    def psm():
        def fget(self):
            return self._psm
        def fset(self, psm):
            self._personalinfo_manager._onPSMChanged(psm)
        return locals()

    @rw_property
    def dp():
        def fget(self):
            return self._image
        def fset(self, imagev):
            self._personalinfo_manager._onDPChanged(imagev)
        return locals()

    @rw_property
    def current_media():
        def fget(self):
            return self._current_media
        def fset(self, artist, song):
            self._personalinfo_manager._onCMChanged((artist, song))
        return locals()

    @rw_property
    def presence():
        def fget(self):
            return self._presence
        def fset(self, presence):
            self._personalinfo_manager._onPresenceChanged(presence)
        return locals()

    @rw_property
    def psm_current_media():
        def fget(self):
            return (self.psm, self.current_media)
        def fset(self, psm, artist, song):
            self._personalinfo_manager._onPSMCMChanged(psm, (artist, song))
        return locals()

