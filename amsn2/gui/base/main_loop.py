
class aMSNMainLoop(object):
    """ This Interface represents the main loop abstraction of the application.
    Everythin related to the main loop will be delegates here """
    def __init__(self, amsn_core):
        pass

    def run(self):
        """ This will run the the main loop"""
        pass

    def idlerAdd(self, func):
        """ This will add an idler function into the main loop's idler """
        pass

    def timerAdd(self, delay, func):
        """ This will add a timer into the main loop which will call a function"""
        pass

    def quit(self):
        """ This will be called when the core wants to exit """
        pass
    
