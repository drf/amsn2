from views import *

class aMSNStatusManager():
    def __init__(self, core):
        self._core = core
        self._statusview = None
        self._pymsn_profile = None

    def set_profile(self, pymsn_profile):
        self._pymsn_profile = pymsn_profile
        self._statusview = StatusView(self._core, pymsn_profile)
        # TODO: update the contactlist gui from the core

    """ Actions from ourselves """
    def onNickUpdated(self, new_nick):
        # TODO: parsing
        self._pymsn_profile.display_name = new_nick

    def onPMUpdated(self, new_pm):
        self._pymsn_profile.personal_message = new_pm

    def onDPUpdated(self, new_dp):
        # TODO: manage msn_objects
        pass

    def onPresenceUpdated(self, new_presence):
        self._pymsn_profile.presence = presence

    """ actions from the core """
    def onCurrentMediaUpdated(self, new_media):
        # TODO: update the contactlist gui from the core
        pass

    # TODO: connect to pymsn signals
    """ Actions from outside """
    def onNewMail(self, info):
        pass

    def onOIM(self, oims):
        pass


# necessary????
class aMSNStatus():
    def __init__(self, core, pymsn_profile):
        # TODO: parse fields for smileys, format, etc
        self.nickname = StringView()
        self.nickname.appendText(pymsn_profile.display_name)
        self.psm = StringView()
        self.psm.appendText(pymsn_profile.personal_message)
        self.current_media  = StringView()
        if pymsn_profile.current_media is not None:
            self.current_media.appendText(pymsn_profile.current_media[0])
            self.current_media.appendText(pymsn_profile.current_media[1])
        # TODO: How do I get the profile image?
        self.image = ImageView()
        #self.image.load(pymsn_profile.msn_object)
        self.presence = core.p2s[pymsn_profile.presence]
        # TODO: get more info, how to manage webcams and mail
        self.webcam = None
        self.mail_unread = None


