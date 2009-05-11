from views import *

class aMSNStatusManager():
    STATUS_UPDATED = 0
    _events_cbs = [[]]

    def __init__(self, core):
        self._core = core
        self._statusview = None
        self._pymsn_profile = None

    def set_profile(self, pymsn_profile):
        self._pymsn_profile = pymsn_profile
        self._statusview = StatusView(self._core, pymsn_profile)
        self.emit(self.STATUS_UPDATED, self._statusview)

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
        self._pymsn_profile.display_name = new_nick.toString()
        self.emit(self.STATUS_UPDATED, self._statusview)
 
    def _onPMUpdated(self, new_pm):
        # TODO: parsing
        self._pymsn_profile.personal_message = new_pm.toString()
        self.emit(self.STATUS_UPDATED, self._statusview)
 
    def _onDPUpdated(self, new_dp):
        # TODO: manage msn_objects
        self.emit(self.STATUS_UPDATED, self._statusview)
 
    def _onPresenceUpdated(self, new_presence):
        for key in self._core.p2s:
            if self._core.p2s[key] == new_presence:
                break
        self._pymsn_profile.presence = key
        self.emit(self.STATUS_UPDATED, self._statusview)
 
    """ actions from the core """
    def _onCMUpdated(self, new_media):
        self._pymsn_profile.current_media = new_media
        self.emit(self.STATUS_UPDATED, self._statusview)

    # TODO: connect to papyon event, maybe build a mailbox_manager
    """ Actions from outside """
    def _onNewMail(self, info):
        self.emit(self.STATUS_UPDATED, self._statusview)






