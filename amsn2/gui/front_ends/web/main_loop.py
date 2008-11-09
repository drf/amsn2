
from amsn2.gui import base
import gobject

class aMSNMainLoop(base.aMSNMainLoop):
    def __init__(self, amsn_core):
        self._amsn_core = amsn_core
    
    def run(self):
        self._mainloop = gobject.MainLoop(is_running=True)
        while self._mainloop.is_running():
            try:
                self._mainloop.run()
            except KeyboardInterrupt:
                self.quit()

        
    def idlerAdd(self, func):
        gobject.idle_add(func)

    def timerAdd(self, delay, func):
        gobject.timeout_add(delay, func)

    def quit(self):
        self._mainloop.quit()
        
