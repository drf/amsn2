class aMSNEvents:
    # ContactList events
    CONTACTVIEW_UPDATED = 0
    GROUPVIEW_UPDATED = 1
    CLVIEW_UPDATED = 2
    AMSNCONTACT_UPDATED = 3
    # PersonalInfo events
    PERSONALINFO_UPDATED = 4

class aMSNEventManager:
    def __init__(self, core):
        self._core = core
        self._events_cbs = [ [] for e in dir(aMSNEvents) if e.isupper()]
        self.events = aMSNEvents()

    def emit(self, event, *args):
        """ emit the event """
        for cb in self._events_cbs[event]:
            #TODO: try except
            cb(*args)

    # maybe create a default set of priority, like PLUGIN, CORE...
    def register(self, event, callback, type='ro', priority = 0):
        """ register a callback for an event """
        #TODO: try except
        if type is 'ro':
            self._events_cbs[event].append(callback)
        elif type is 'rw':
            # TODO: insertion depends on priority
            bck_cbs = [].extend(self._events_cbs)
            self._events_cbs[event] = [callback]
            self._events_cbs[event].extend(bck_cbs)

    def unregister(self, event, callback):
        """ unregister a callback for an event """
        #TODO: try except
        self._events_cbs[event].remove(callback)



