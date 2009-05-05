from views import *

class aMSNStatusManager():
    def __init__(self, core):
        self._core = core
        self._statusview = None
        self._pymsn_profile = None
        self._amsn_profile = core.profile

    def set_profile(self, pymsn_profile):
        self._pymsn_profile = pymsn_profile
        self._statusview = StatusView(self._core, pymsn_profile)
        # TODO: update the contactlist gui from the core

    """ Actions from ourselves """
    def onNickUpdated(self, new_nick):
        # TODO: parsing
        self._pymsn_profile.display_name = new_nick

    def onPMUpdated(self, new_pm):
        # TODO: parsing
        self._pymsn_profile.personal_message = new_pm

    def onDPUpdated(self, new_dp):
        # TODO: manage msn_objects
        pass

    def onPresenceUpdated(self, new_presence):
        for key in self._core.p2s:
            if self._core.p2s[key] == new_presence:
                break
        self._pymsn_profile.presence = key

    """ actions from the core """
    def onCurrentMediaUpdated(self, new_media):
        # TODO: update the contactlist gui from the core
        pass

    # TODO: connect to pymsn event, maybe build a mailbox_manager
    """ Actions from outside """
    def onNewMail(self, info):
        pass


