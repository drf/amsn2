from stringview import *
from imageview import *

def rw_property(f):
    return property(**f())

class StatusView(object):
    def __init__(self, core, pymsn_profile):
        # TODO: parse fields for smileys, format, etc
        self._nickname = StringView()
        self._nickname.appendText(pymsn_profile.display_name)
        self._psm = StringView()
        self._psm.appendText(pymsn_profile.personal_message)
        self._current_media  = StringView()
        if pymsn_profile.current_media is not None:
            self._current_media.appendText(pymsn_profile.current_media[0])
            self._current_media.appendText(pymsn_profile.current_media[1])
        # TODO: How do I get the profile image?
        self._image = ImageView()
        #self.image.load(pymsn_profile.msn_object)
        self._presence = core.p2s[pymsn_profile.presence]
        self._status_manager = core._status_manager

        # TODO: get more info, how to manage webcams and mail
        self._webcam = None
        self._mail_unread = None

    @rw_property
    def nick():
        def fget(self):
            return self._nickname
        def fset(self, nick):
            self._nickname = nick
            self._status_manager._onNickUpdated(nick)
        return locals()

    @rw_property
    def psm():
        def fget(self):
            return self._psm
        def fset(self, psm):
            self._psm = psm
            self._status_manager._onPMUpdated(psm)
        return locals()

    @rw_property
    def dp():
        def fget(self):
            return self._image
        def fset(self, imagev):
            self._image = imagev
            self._status_manager._onDPUpdated(imagev)
        return locals()

    @rw_property
    def current_media():
        def fget(self):
            return self._current_media
        def fset(self, artist, song):
            # TODO: separators
            self._current_media.appendText(artist)
            self._current_media.appendText(song)
            self._status_manager._onCMUpdated((artist, song))
        return locals()

    @rw_property
    def presence():
        def fget(self):
            return self._presence
        def fset(self, p):
            self._presence = p
            self._status_manager._onPresenceUpdated(p)
        return locals()

