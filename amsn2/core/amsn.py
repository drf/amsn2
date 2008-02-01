
import profile
from amsn2 import gui
from amsn2 import protocol
import pymsn

class aMSNCore(object):
    def __init__(self, options):
        """
        Create a new aMSN Core. It takes an options class as argument
        which has a variable for each option the core is supposed to received.
        This is easier done using optparse.
        The options supported are :
           options.account = the account's username to use
           options.password = the account's password to use
           options.front_end = the front end's name to use
           options.debug = whether or not to enable debug output
        """
        self._profile_manager = profile.aMSNProfileManager()
        self._options = options
        self._gui_name = self._options.front_end
        self._gui = gui.GUIManager(self, self._gui_name)
        self._loop = self._gui.getMainLoop();
        self._main = self._gui.getMainWindow();

        if self._options.debug:
            import logging
            logging.basicConfig(level=logging.DEBUG)

    def run(self):
        self._main.show();
        self._loop.run();
        

    def mainWindowShown(self):
        # TODO : load the profiles from disk and all settings
        # and show a splash screen in the main window, until all is loaded
        # then show the login window if autoconnect is disabled
        login = self._gui.getLoginWindow()
        
        profile = None
        if self._options.account is not None:
            if self._profile_manager.profileExists(self._options.account):
                profile = self._profile_manager.getProfile(self._options.account)
            else:
                profile = self._profile_manager.addProfile(self._options.account)
                profile.save = False
            if self._options.password is not None:
                profile.password = self._options.password

        else:
            for prof in self._profile_manager.getAllProfiles():
                if prof.isLocked() is False:
                    profile = prof
                    break

        if profile is None:
            profile = self._profile_manager.addProfile("")
            profile.password = ""
            
        login.switch_to_profile(profile)
        login.show()

    def getMainWindow(self):
        return self._main
            

    def addProfile(self, account):
        return self._profile_manager.addProfile(account)

    def signinToAccount(self, login_window, profile):
        print "Signing in to account %s" % (profile.email)
        profile.login = login_window
        profile.client = protocol.Client(self, profile)
        profile.client.connect()

    def connectionStateChanged(self, profile, state):
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
            cl = self._gui.getContactList()
            cl.profile = profile
            profile.cl = cl
            profile.login.hide()
            profile.cl.show()
            profile.login = None

            for group in profile.client.address_book.groups:
                contacts = profile.client.address_book.contacts.search_by_groups(group)
                profile.cl.groupAdded(group)
                for c in contacts:
                    profile.cl.contactAdded(group, c)

            class NoGroup(object):
                def __init__(self):
                    self.id = 0
                    self.name = "No Group"
            nogroup = None
            contacts = profile.client.address_book.contacts
            for c in contacts:
                if len(c.groups) == 0:
                    if nogroup is None:
                        nogroup = NoGroup()
                        profile.cl.groupAdded(nogroup)
                        
                    profile.cl.contactAdded(nogroup, c)
                    

    def contactPresenceChanged(self, profile, contact):
        profile.cl.contactStateChange(contact)


    def idlerAdd(self, func):
        self._loop.idler_add(func)

    def timerAdd(self, delay, func):
        self._loop.timer_add(delay, func)

    def quit(self):
        self._loop.quit()
