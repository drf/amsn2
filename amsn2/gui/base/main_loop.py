
class aMSNMainLoop(object):
    """ This Interface represents the main loop abstraction of the application.
    Everythin related to the main loop will be delegates here """
    def __init__(self, amsn_core):
        """
        @type amsn_core: aMSNCore
        """

        raise NotImplementedError

    def run(self):
        """ This will run the the main loop"""
        raise NotImplementedError

    def idlerAdd(self, func):
        """
        This will add an idler function into the main loop's idler

        @type func: function
        """
        raise NotImplementedError

    def timerAdd(self, delay, func):
        """
        This will add a timer into the main loop which will call a function

        @type delay:
        @type func: function
        """
        raise NotImplementedError

    def quit(self):
        """ This will be called when the core wants to exit """
        raise NotImplementedError

