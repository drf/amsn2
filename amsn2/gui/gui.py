
class aMSNGUI(object):
    """ This Interface represents the main window of the application. Everythin will be done from here """
    def __init__(self, amsn_core):
        pass

    def launch(self):
        """ This launches the the main window, creates it, etc.. and takes care of launching the main loop """
        pass

    def createLoginWindow(self):
        """ Should create an aMSNLoginWindow object and return it """
        pass

    def createContactList(self, profile):
        """ Should create an aMSNContactList object for the specified profile and return it """
        pass

    def idler_add(self, func):
        """ This is a helper function that delegates idler handling to the GUI so it could use its own main loop """
        pass

    def timer_add(self, delay, func):
        """ This is a helper function that delegates timers handling to the GUI so it could use its own main loop """
        pass

class aMSNLoginWindow(object):
    def __init__(self, amsn_core):
        pass

    def show_window(self):
        pass
    
    def hide_window(self):
        pass

    def switch_to_profile(self, profile):
        pass

    def signin(self):
        pass

    def onConnecting(self):
        pass

    def onConnected(self):
        pass

    def onAuthenticating(self):
        pass

    def onAuthenticated(self):
        pass

    def onSynchronizing(self):
        pass

    def onSynchronized(self):
        pass


class aMSNContactList(object):
    def __init__(self, amsn_gui, profile):
        pass

    def show_window(self):
        pass

    def hide_window(self):
        pass

    def contactStateChange(self, contact):
        pass

    def contactNickChange(self, contact):
        pass
        
    def contactPSMChange(self, contact):
        pass
    
    def contactAlarmChange(self, contact):
        pass

    def contactDisplayPictureChange(self, contact):
        pass

    def contactSpaceChange(self, contact):
        pass
    
    def contactSpaceFetched(self, contact):
        pass

    def contactBlocked(self, contact):
        pass

    def contactUnblocked(self, contact):
        pass

    def contactMoved(self, from_group, to_group, contact):
        pass

    def contactAdded(self, group, contact):
        pass
    
    def contactRemoved(self, group, contact):
        pass

    def contactRenamed(self, contact):
        pass

    def groupRenamed(self, group):
        pass

    def groupAdded(self, group):
        pass

    def groupRemoved(self, group):
        pass

    def configure(self, option, value):
        pass

    def cget(self, option, value):
        pass

