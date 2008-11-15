
# This is the main comunication module, all comunication to the JS frontend will be issued from here

class Backend(object):
    def __init__(self,In,Out):
        self.listeners = {}
        self._in = open(In, "r+")
        self._out = open(Out,"a")

    def addListener(self,event,listener):
        # The backend sets a listener to an event
        if not self.listeners.has_key(event):
            self.listeners[event] = []
        self.listeners[event].append(listener)

    def checkEvent(self):
        # This function is called to check for events in the file
        try:
            # one event per line, divided by columns divided by tab
            # the first column is the event, the next columns are the arguments
            eventDesc=self._in.readline()
            while len(eventDesc) > 0:
                try:
                    eventDesc = eventDesc.strip().split("\t")
                    eventName = eventDesc.pop(0)
                    realValues = []
                    for value in eventDesc:
                        realValues.append(str(value).decode('string_escape'))
                    if eventName is not "":
                        self.event(eventName,realValues)
                except:
                     # event problem.. probably a badly encoded string
                     break
                eventDesc=self._in.readline()
        except:
            # problem with lines (maybe empty file)
            pass
        # Return true to continue checking events
        return True
        
    def event(self,event,values):
        # The JS client sent a message to the backend 
        # select the function to call depending on the type of event
        if self.listeners[event] is not None:
            for func in self.listeners[event]:
                try:
                    # if the function returns false, then it means it doesnt want to be called again
                    if not func(values):
                        self.listeners[event].remove(func)
                except:
                    pass

    def send(self,event,values):
        # The backend sent a message to the JS client
        # select the JS function to call depending on the type of event
        call = event + "(["
        for value in values:
            call += "'"+str(value).encode('string_escape')+"',"
        call=call.rstrip(",")+"]);"
        try:
           self._out.write(call)
           self._out.flush()
        except:
           pass
