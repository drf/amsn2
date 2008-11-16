
from amsn2.gui import base
import gobject

class aMSNMainLoop(base.aMSNMainLoop):

    def run(self):
        self._mainloop = gobject.MainLoop(is_running=True)

        while self._mainloop.is_running():
            try:
                self._mainloop.run()
            except KeyboardInterrupt:
                self.quit()

        
    def idler_add(self, func):
        gobject.idle_add(func)

    def timer_add(self, delay, func):
        gobject.timeout_add(delay, func)

    def quit(self):
        self._mainloop.quit()
        
