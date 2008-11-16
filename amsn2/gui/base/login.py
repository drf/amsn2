
class aMSNLoginWindow(object):
    """ This interface will represent the login window of the UI"""
    def __init__(self, amsn_core, parent):
        """Initialize the interface. You should store the reference to the core in here """
        raise NotImplementedError

    def show(self):
        """ Draw the login window """
        raise NotImplementedError
    
    def hide(self):
        """ Hide the login window """
        raise NotImplementedError

    def switch_to_profile(self, profile):
        """ This method will be called when the core needs the login window to switch to a different profile """
        raise NotImplementedError

    def signin(self):
        """ This method will be called when the core needs the login window to start the signin process """
        raise NotImplementedError

    def onConnecting(self, progress, message):
        """ This method will be called to notify the UI that we are connecting.
        @progress: the current progress (as float) of the connexion (to be
        exploited as a progress bar, for example)
        @message: the message to show while loging in """
        raise NotImplementedError


