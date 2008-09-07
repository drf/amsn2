
import profile
from amsn2 import gui
from amsn2 import protocol
import pymsn
from views import *
    
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
        self._loop = self._gui.gui.aMSNMainLoop(self)
        self._main = self._gui.gui.aMSNMainWindow(self)
        self._skin_manager = self._gui.gui.SkinManager(self)

        self.p2s = {pymsn.Presence.ONLINE:"online",
                    pymsn.Presence.BUSY:"busy",
                    pymsn.Presence.IDLE:"idle",
                    pymsn.Presence.AWAY:"away",
                    pymsn.Presence.BE_RIGHT_BACK:"brb",
                    pymsn.Presence.ON_THE_PHONE:"phone",
                    pymsn.Presence.OUT_TO_LUNCH:"lunch",
                    pymsn.Presence.INVISIBLE:"hidden",
                    pymsn.Presence.OFFLINE:"offline"}

        if self._options.debug:
            import logging
            logging.basicConfig(level=logging.DEBUG)

    def run(self):
        self._main.show();
        self._loop.run();
        

    def mainWindowShown(self):
        # TODO : load the profiles from disk and all settings
        # then show the login window if autoconnect is disabled
        
        self._main.setTitle("aMSN 2 - Loading")
        
        splash = self._gui.gui.aMSNSplashScreen(self, self._main)
        image = self._gui.gui.Image(self, self._main)
        image.load("File","/path/to/image/here")
        
        splash.setImage(image)
        splash.setText("Loading...")
        splash.show()
        
        login = self._gui.gui.aMSNLoginWindow(self, self._main)
        
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
        
        splash.hide()
        self._main.setTitle("aMSN 2 - Login")
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
            profile.login.onConnecting("Connecting to server...")
        elif state == pymsn.event.ClientState.CONNECTED:
            profile.login.onConnecting("Connected...")
        elif state == pymsn.event.ClientState.AUTHENTICATING:
            profile.login.onConnecting("Authenticating...")
        elif state == pymsn.event.ClientState.AUTHENTICATED:
            profile.login.onConnecting("Password accepted...")
        elif state == pymsn.event.ClientState.SYNCHRONIZING:
            profile.login.onConnecting("Please wait while your contact list\nis being downloaded...")
        elif state == pymsn.event.ClientState.SYNCHRONIZED:
            profile.login.onConnecting("Contact list downloaded successfully\nHappy Chatting")
        elif state == pymsn.event.ClientState.OPEN:
            clwin = self._gui.gui.aMSNContactListWindow(self, self._main)
            clwin.profile = profile
            profile.clwin = clwin
            profile.login.hide()
            self._main.setTitle("aMSN 2")
            profile.clwin.show()
            profile.login = None

            for group in profile.client.address_book.groups:
                contacts = profile.client.address_book.contacts.search_by_groups(group)
                groupV = self.buildGroup(group, 0, len(contacts))
                groupV.contacts = []
                
                for contact in contacts:
                    contactV = self.buildContact(contact)
                    groupV.contacts.append(contactV)
                                
                profile.clwin._clwidget.groupAdded(groupV)

            groupV = self.buildGroup(None, 0, 0)
            groupV.contacts = []
                
            contacts = profile.client.address_book.contacts.search_by_memberships(pymsn.Membership.FORWARD)
            for contact in contacts:
                if len(contact.groups) == 0:
                    contactV = self.buildContact(contact)
                    groupV.contacts.append(contactV)
                                
            if len(groupV.contacts) > 0:
                groupV = self.buildGroup(None, 0, len(groupV.contacts))
                profile.clwin._clwidget.groupAdded(groupV)


    def buildGroup(self, group, active, total):
        groupV = GroupView.getGroup(group.id if group else 0)
        groupV.icon = None # TODO : expanded/collapsed icon
        groupV.name = StringView() # TODO : default color from skin/settings
        groupV.name.appendText(group.name if group else "No Group") # TODO : parse or translation
        groupV.name.appendText("(" + str(active) + "/" + str(total) + ")")
        
        return groupV
    
    def buildContact(self, contact):
        contactV = ContactView.getContact(contact.id)
        contactV.icon = self._gui.gui.Image(self, self._main)
        contactV.icon.load("Skin","buddy_" + self.p2s[contact.presence])
        contactV.dp = self._gui.gui.Image(self, self._main)
        contactV.dp.load("Skin","default_dp")
        contactV.name = StringView() # TODO : default colors
        contactV.name.openTag("nickname")
        contactV.name.appendText(contact.display_name) # TODO parse
        contactV.name.closeTag("nickname")
        contactV.name.appendText(" ")
        contactV.name.openTag("status")
        contactV.name.appendText("(")
        contactV.name.appendText(self.p2s[contact.presence])
        contactV.name.appendText(")")
        contactV.name.closeTag("status")
        contactV.name.appendText(" ")
        contactV.name.openTag("psm")
        contactV.name.setItalic()
        contactV.name.appendText(contact.personal_message)
        contactV.name.unsetItalic()
        contactV.name.closeTag("psm")
        
        return contactV
        
    def contactPresenceChanged(self, profile, contact):
        c = self.buildContact(contact)
        profile.clwin._clwidget.contactUpdated(c)


    def idlerAdd(self, func):
        self._loop.idler_add(func)

    def timerAdd(self, delay, func):
        self._loop.timer_add(delay, func)

    def quit(self):
        self._loop.quit()
