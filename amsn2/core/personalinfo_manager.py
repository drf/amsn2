from views import *

class aMSNPersonalInfoManager():
    PERSONALINFO_UPDATED = 0
    _events_cbs = [[]]

    def __init__(self, core):
        self._core = core
        self._personalinfoview = None
        self._papyon_profile = None

    def set_profile(self, papyon_profile):
        self._papyon_profile = papyon_profile
        self._personalinfoview = PersonalInfoView(self._core, papyon_profile)
        self.emit(self.PERSONALINFO_UPDATED, self._personalinfoview)

    def emit(self, event, *args):
        """ emit the event """
        for cb in self._events_cbs[event]:
            #TODO: try except
            cb(*args)

    def register(self, event, callback, type='ro'):
        """ register a callback for an event """
        #TODO: try except
        if type is 'ro':
            self._events_cbs[event].append(callback)
        elif type is 'rw':
            bck_cbs = self._events_cbs[event]
            self._events_cbs[event] = [callback]
            self._events_cbs[event].extend(bck_cbs)

    def unregister(self, event, callback):
        """ unregister a callback for an event """
        #TODO: try except
        self._events_cbs[event].remove(callback)




    """ Actions from ourselves """
    def _onNickUpdated(self, new_nick):
        # TODO: parsing
        self._papyon_profile.display_name = new_nick.toString()
        self.emit(self.PERSONALINFO_UPDATED, self._personalinfoview)
 
    def _onPMUpdated(self, new_pm):
        # TODO: parsing
        self._papyon_profile.personal_message = new_pm.toString()
        self.emit(self.PERSONALINFO_UPDATED, self._personalinfoview)
 
    def _onDPUpdated(self, new_dp):
        # TODO: manage msn_objects
        self.emit(self.PERSONALINFO_UPDATED, self._personalinfoview)
 
    def _onPresenceUpdated(self, new_presence):
        for key in self._core.p2s:
            if self._core.p2s[key] == new_presence:
                break
        self._papyon_profile.presence = key
        self.emit(self.PERSONALINFO_UPDATED, self._personalinfoview)
 
    """ actions from the core """
    def _onCMUpdated(self, new_media):
        self._papyon_profile.current_media = new_media
        self.emit(self.PERSONALINFO_UPDATED, self._personalinfoview)

    # TODO: connect to papyon event, maybe build a mailbox_manager
    """ Actions from outside """
    def _onNewMail(self, info):
        self.emit(self.PERSONALINFO_UPDATED, self._personalinfoview)






