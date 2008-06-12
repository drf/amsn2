
import objc
from Foundation import *
from AppKit import *
import sys
from amsn2.gui import base
import gobject

class aMSNMainLoop(base.aMSNMainLoop):
    nsapp = None
    def __init__(self, amsn_core):
        pass

    def run(self):
        self._mainloop = gobject.MainLoop(is_running=True)
        self._context = self._mainloop.get_context()
        
        self._app = aMSNCocoaNSApplication.sharedApplication()
        self._app.finishLaunching()
        
        def glib_context_iterate():
            iters = 0
            while iters < 10 and self._context.pending():
                self._context.iteration()
            return True
        
        while True:
            try:
                # This hangs for at most 100ms, or until an event is fired.
                # More events == less hang.
                self._app.processEvents(100)
                glib_context_iterate()
            except KeyboardInterrupt:
                self.quit()

        
    def idler_add(self, func):
        gobject.idle_add(func)

    def timer_add(self, delay, func):
        gobject.timeout_add(delay, func)

    def quit(self):
        self._mainloop.quit()
        sys.exit()
        
class aMSNCocoaNSApplication(NSApplication):
    def __init__(self):
        self.setDelegate(self)
    
    # Override run so that it doesn't hang. We'll process events ourself thanks! 
    def run(self):
        return Null
    
    # Looks at the events stack and processes the topmost.
    # return:   True    - An event was processed.
    #           False   - No events in queue.    
    def processEvents(self, timeout=100):
        # Get the next event from the queue.
        if timeout < 0:
            eventTimeout = NSDate.distantPast()
        elif timeout == 0:
            eventTimeout = NSDate.distantFuture()
        else:
            eventTimeout = NSDate.dateWithTimeIntervalSinceNow_(float(timeout/1000.0))
    
        # NSAnyEventMask = 0xffffffff - http://osdir.com/ml/python.pyobjc.devel/2003-10/msg00130.html
        event = self.nextEventMatchingMask_untilDate_inMode_dequeue_( \
            0xffffffff, \
            eventTimeout, \
            NSDefaultRunLoopMode , \
            True)
        
        # Process event if we have one. (python None == cocoa nil)
        if event != None:
            self.sendEvent_(event)
            return True
        
        return False

# We call this so that the if someone calls NSApplication.sharedApplication again, they get an aMSNCocoaNSApplication instance rather than a new NSApplication.
aMSNCocoaNSApplication.sharedApplication()
