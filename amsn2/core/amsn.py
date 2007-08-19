from profile import *
from amsn2.protocol import *

class aMSNCore(object):
    def __init__(self):
        self.profile_manager = aMSNProfileManager()
        self.gui = None


    def setGUI(self, gui):
        self.gui = gui

    def mainWindowShown(self):
        # TODO : load the profiles from disk and all settings
        # and show a splash screen in the main window, until all is loaded
        # then show the login window if autoconnect is disabled
        login = self.gui.createLoginWindow()
        
        use_profile = None
        for prof in self.profile_manager.getAllProfiles():
            if prof.isLocked() is False:
                use_profile = prof
                break
        
        login.switch_to_profile(use_profile)
        login.show_window()

    def addProfile(self, account):
        return self.profile_manager.addProfile(account)

    def signin_to_account(self, login_window, profile):
        print "Signing in to account %s" % (profile.email)
        profile.login = login_window
        profile.client = Client(self, profile)
        profile.client.connect()

    def connection_state_changed(self, profile, state):
        if state == pymsn.event.ClientState.CONNECTING:
            profile.login.onConnecting()
        elif state == pymsn.event.ClientState.CONNECTED:
            profile.login.onConnected()
        elif state == pymsn.event.ClientState.AUTHENTICATING:
            profile.login.onAuthenticating()
        elif state == pymsn.event.ClientState.AUTHENTICATED:
            profile.login.onAuthenticated()
        elif state == pymsn.event.ClientState.SYNCHRONIZING:
            profile.login.onSynchronizing()
        elif state == pymsn.event.ClientState.SYNCHRONIZED:
            profile.login.onSynchronized()
        elif state == pymsn.event.ClientState.OPEN:
            cl = self.gui.createContactList(profile)
            profile.cl = cl
            profile.login.hide_window()
            profile.cl.show_window()
            profile.login = None
       
            for group in profile.client.address_book.groups.values():
                contacts = profile.client.address_book.contacts.search_by_groups(group)
                profile.cl.groupAdded(group)
                for c in contacts:
                    profile.cl.contactAdded(group, c)

            

    def idler_add(self, func):
        self.gui.idler_add(func)

    def timer_add(self, delay, func):
        self.gui.timer_add(delay, func)
    
