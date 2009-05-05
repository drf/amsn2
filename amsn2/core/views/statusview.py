from stringview import *
from imageview import *

class StatusView(object):
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

        # callbacks
        def update_nick_cb(nickv):
            core._status_manager.onNickUpdated(nickv)
        self.update_nick = update_nick_cb
        def update_presence_cb(presencev):
            core._status_manager.onPresenceUpdated(presencev)
        self.update_presence = update_presence_cb
        def update_pm_cb(pmv):
            core._status_manager.onPMUpdated(pmv)
        self.update_pm = update_pm_cb
        def update_dp_cb(dpv):
            core._status_manager.onDPUpdated(dpv)
        self.update_dp = update_dp_cb
        # TODO: get more info, how to manage webcams and mail
        self.webcam = None
        self.mail_unread = None
        

