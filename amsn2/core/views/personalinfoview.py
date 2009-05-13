from stringview import *
from imageview import *

def rw_property(f):
    return property(**f())

class PersonalInfoView(object):
    def __init__(self, core, papyon_profile):
        # TODO: parse fields for smileys, format, etc
        self._nickname = StringView()
        self._nickname.appendText(papyon_profile.display_name)
        self._psm = StringView()
        self._psm.appendText(papyon_profile.personal_message)
        self._current_media  = StringView()
        if papyon_profile.current_media is not None:
            self._current_media.appendText(papyon_profile.current_media[0])
            self._current_media.appendText(papyon_profile.current_media[1])
        # TODO: How do I get the profile image?
        self._image = ImageView()
        #self.image.load(papyon_profile.msn_object)
        self._presence = core.p2s[papyon_profile.presence]
        self._personalinfo_manager = core._personalinfo_manager

        # TODO: get more info, how to manage webcams and mail
        self._webcam = None
        self._mail_unread = None

    @rw_property
    def nick():
        def fget(self):
            return self._nickname
        def fset(self, nick):
            self._nickname = nick
            self._personalinfo_manager._onNickUpdated(nick)
        return locals()

    @rw_property
    def psm():
        def fget(self):
            return self._psm
        def fset(self, psm):
            self._psm = psm
            self._personalinfo_manager._onPMUpdated(psm)
        return locals()

    @rw_property
    def dp():
        def fget(self):
            return self._image
        def fset(self, imagev):
            self._image = imagev
            self._personalinfo_manager._onDPUpdated(imagev)
        return locals()

    @rw_property
    def current_media():
        def fget(self):
            return self._current_media
        def fset(self, artist, song):
            # TODO: separators
            self._current_media.appendText(artist)
            self._current_media.appendText(song)
            self._personalinfo_manager._onCMUpdated((artist, song))
        return locals()

    @rw_property
    def presence():
        def fget(self):
            return self._presence
        def fset(self, p):
            self._presence = p
            self._personalinfo_manager._onPresenceUpdated(p)
        return locals()

