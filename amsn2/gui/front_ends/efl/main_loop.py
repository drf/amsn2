
from amsn2.gui import base
import gobject
import ecore

class aMSNMainLoop(base.aMSNMainLoop):
    def __init__(self, amsn_core):
        pass
    
    def run(self):
        mainloop = gobject.MainLoop(is_running=True)
        context = mainloop.get_context()

        def glib_context_iterate():
            iters = 0
            while iters < 10 and context.pending():
                context.iteration()
            return True

        # Every 100ms, call an iteration of the glib main context loop
        # to allow the protocol context loop to work
        ecore.timer_add(0.1, glib_context_iterate)

        ecore.main_loop_begin()
        
    def idler_add(self, func):
        ecore.idler_add(func)

    def timer_add(self, delay, func):
        ecore.timer_add(delay, func)

    def quit(self):
        ecore.main_loop_quit()
        
