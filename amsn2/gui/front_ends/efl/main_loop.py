
from amsn2.gui import base
import gobject
import ecore
import elementary

class aMSNMainLoop(base.aMSNMainLoop):
    def __init__(self, amsn_core):
        elementary.init()

    def run(self):
        #ecore.main_loop_glib_integrate()
        mainloop = gobject.MainLoop(is_running=True)
        context = mainloop.get_context()

        def glib_context_iterate():
            iters = 0
            while iters < 10 and context.pending():
                context.iteration()
                iters += 1
            return True

        # Every 100ms, call an iteration of the glib main context loop
        # to allow the protocol context loop to work
        ecore.timer_add(0.1, glib_context_iterate)

        #equals elementary.run()
        ecore.main_loop_begin()

    def idlerAdd(self, func):
        ecore.idler_add(func)

    def timerAdd(self, delay, func):
        ecore.timer_add(delay, func)

    def quit(self):
        ecore.main_loop_quit()

