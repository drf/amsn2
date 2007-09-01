from amsn2.gui import *
from amsn2.core import *

WIDTH = 400
HEIGHT = 600
MIN_WIDTH = 100
MIN_HEIGHT = 150

TITLE = "aMSN 2"
WM_NAME = "aMSN2"
WM_CLASS = "main"

class aMSNGUI_Cocoa(aMSNGUI):
    def __init__(self, amsn_core):     
        self._amsn_core = amsn_core
        self._amsn_core.setGUI(self)

    def createLoginWindow(self):
        print "Creating login window"
        self._login = aMSNLoginWindow_Cocoa(self._amsn_core)
        return self._login

    def createContactList(self, profile):
        print "Creating CL"
        cl = aMSNContactList_Cocoa(self._amsn_core)
        return cl

    def launch(self):
        import gobject
        import signal

        mainloop = gobject.MainLoop(is_running=True)

        print "Main window.. launching"
        self.idler_add(self.__on_show)

        def quit():
            mainloop.quit()

        def sigterm_cb():
            gobject.idle_add(mainloop.quit)

        signal.signal(signal.SIGTERM, sigterm_cb)


        while mainloop.is_running():
            try:
                print "Running main loop"
                mainloop.run()
            except KeyboardInterrupt:
               print "Interrupted"
               mainloop.quit()

    def idler_add(self, func):
        import gobject
        gobject.idle_add(func)

    def timer_add(self, delay, func):
        import gobject
        gobject.timeout_add(delay, func)

    def __on_show(self):
        print "Showing main window"
        self._amsn_core.mainWindowShown()
       

class aMSNLoginWindow_Cocoa(aMSNLoginWindow):
    def __init__(self, amsn_core):
        self._amsn_core = amsn_core
        self._amsn_gui = self._amsn_core.gui

        # We start with no profile set up, we let the Core set our starting profile
        self.switch_to_profile(None)

    def show_window(self):
        print "Login screen : Asked to show window"
    
    def hide_window(self):
        print "Login screen : Asked to hide window"

    def switch_to_profile(self, profile):
        self.current_profile = profile
        if self.current_profile is not None:
            print "Login screen : switched to profile %s" % self.current_profile.email
            self.signin()


    def signin(self):
        print "Signing in"
        self._amsn_core.signin_to_account(self, self.current_profile)

    def onConnecting(self):
        print "Connecting"

    def onConnected(self):
        print "Connected"

    def onAuthenticating(self):
        print "Authenticating"

    def onAuthenticated(self):
        print "Authenticated"

    def onSynchronizing(self):
        print "Please wait while your contact list is being downloaded..."

    def onSynchronized(self):
        print "Contact list downloaded successfully"


class aMSNContactList_Cocoa(object):
    def __init__(self, amsn_core):
        self._amsn_core = amsn_core
        self._amsn_gui = self._amsn_core.gui

    def show_window(self):
        print "Contact list : asked to show window"

    def hide_window(self):
        print "Contact list : asked to hide window"

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
        print "Adding contact %s to group %s in CL" % (str(contact.display_name), str(group.id))
    
    def contactRemoved(self, group, contact):
        pass

    def contactRenamed(self, contact):
        pass

    def groupRenamed(self, group):
        pass

    def groupAdded(self, group):
        print "Adding group %s to CL" % str(group.id)

    def groupRemoved(self, group):
        pass

    def configure(self, option, value):
        pass

    def cget(self, option, value):
        pass
