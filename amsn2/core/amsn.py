# -*- coding: utf-8 -*-
#
# amsn - a python client for the WLM Network
#
# Copyright (C) 2008 Dario Freddi <drf54321@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from amsn2 import gui
from amsn2 import protocol
from amsn2.backend import aMSNBackendManager
from views import *
from account_manager import *
from contactlist_manager import *
from conversation_manager import *
from oim_manager import *
from theme_manager import *
from personalinfo_manager import *
from event_manager import *

import papyon
import logging

# Top-level loggers
papyon_logger = logging.getLogger("papyon")
logger = logging.getLogger("amsn2")

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
        self.p2s = {papyon.Presence.ONLINE:"online",
                    papyon.Presence.BUSY:"busy",
                    papyon.Presence.IDLE:"idle",
                    papyon.Presence.AWAY:"away",
                    papyon.Presence.BE_RIGHT_BACK:"brb",
                    papyon.Presence.ON_THE_PHONE:"phone",
                    papyon.Presence.OUT_TO_LUNCH:"lunch",
                    papyon.Presence.INVISIBLE:"hidden",
                    papyon.Presence.OFFLINE:"offline"}
        self.Presence = papyon.Presence

        self._event_manager = aMSNEventManager(self)
        self._options = options

        self._gui_name = None
        self._gui = None
        self._loop = None
        self._main = None
        self._account = None
        self.loadUI(self._options.front_end)

        self._backend_manager = aMSNBackendManager(self)
        self._account_manager = aMSNAccountManager(self, options)
        self._theme_manager = aMSNThemeManager(self)
        self._contactlist_manager = aMSNContactListManager(self)
        self._oim_manager = aMSNOIMManager(self)
        self._conversation_manager = aMSNConversationManager(self)
        self._personalinfo_manager = aMSNPersonalInfoManager(self)

        # TODO: redirect the logs somewhere, something like ctrl-s ctrl-d for amsn-0.9x
        logging.basicConfig(level=logging.WARNING)

        if self._options.debug_protocol:
            papyon_logger.setLevel(logging.DEBUG)
        else:
            papyon_logger.setLevel(logging.WARNING)

        if self._options.debug_amsn2:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.WARNING)

    def run(self):
        self._main.show()
        self._loop.run()

    def loadUI(self, ui_name):
        """
        @type ui_name: str
        @param ui_name: The name of the User Interface
        """

        self._gui_name = ui_name
        self._gui = gui.GUIManager(self, self._gui_name)
        if not self._gui.gui:
            print "Unable to load UI %s" %(self._gui_name,)
            self.quit()
        self._loop = self._gui.gui.aMSNMainLoop(self)
        self._main = self._gui.gui.aMSNMainWindow(self)
        self._skin_manager = self._gui.gui.SkinManager(self)

    def switchToUI(self, ui_name):
        """
        @type ui_name: str
        @param ui_name: The name of the User Interface
        """

        #TODO: unloadUI + stop loops??? + loadUI + run
        pass

    def mainWindowShown(self):
        # TODO : load the accounts from disk and all settings
        # then show the login window if autoconnect is disabled

        self._main.setTitle("aMSN 2 - Loading")


        splash = self._gui.gui.aMSNSplashScreen(self, self._main)
        image = ImageView()
        image.load("Filename","/path/to/image/here")

        splash.setImage(image)
        splash.setText("Loading...")
        splash.show()

        login = self._gui.gui.aMSNLoginWindow(self, self._main)

        login.setAccounts(self._account_manager.getAvailableAccountViews())

        splash.hide()
        self._main.setTitle("aMSN 2 - Login")
        login.show()

        menu = self.createMainMenuView()
        self._main.setMenu(menu)

    def getMainWindow(self):
        return self._main

    def signinToAccount(self, login_window, accountview):
        """
        @type login_window: aMSNLoginWindow
        @type accountview: AccountView
        """

        print "Signing in to account %s" % (accountview.email)
        self._account = self._account_manager.signinToAccount(accountview)
        self._account.login = login_window
        self._account.client = protocol.Client(self, self._account)
        self._account.client.connect(accountview.email, accountview.password)

    def signOutOfAccount(self):
        self._account.client.logout()
        self._account.signOut()

    def connectionStateChanged(self, account, state):
        """
        @type account: aMSNAccount
        @type state: L{papyon.event.ClientState}
        @param state: New state of the Client.
        """

        status_str = \
        {
            papyon.event.ClientState.CONNECTING : 'Connecting to server...',
            papyon.event.ClientState.CONNECTED : 'Connected',
            papyon.event.ClientState.AUTHENTICATING : 'Authenticating...',
            papyon.event.ClientState.AUTHENTICATED : 'Password accepted',
            papyon.event.ClientState.SYNCHRONIZING : 'Please wait while your contact list\nis being downloaded...',
            papyon.event.ClientState.SYNCHRONIZED : 'Contact list downloaded successfully.\nHappy Chatting'
        }

        if state in status_str:
            account.login.onConnecting((state + 1)/ 7., status_str[state])
        elif state == papyon.event.ClientState.OPEN:
            clwin = self._gui.gui.aMSNContactListWindow(self, self._main)
            clwin.account = account
            account.clwin = clwin
            account.login.hide()
            self._main.setTitle("aMSN 2")
            account.clwin.show()
            account.login = None

            self._personalinfo_manager.setAccount(account)
            self._contactlist_manager.onCLDownloaded(account.client.address_book)

    def idlerAdd(self, func):
        """
        @type func: function
        """

        self._loop.idlerAdd(func)

    def timerAdd(self, delay, func):
        """
        @type delay: int
        @param delay: delay in seconds?
        @type func: function
        """

        self._loop.timerAdd(delay, func)

    def quit(self):
        if self._account:
            self._account.signOut()
        if self._loop:
            self._loop.quit()
        logging.shutdown()
        exit(0)

    # TODO: move to UImanager
    def addContact(self):
        def contactCB(account, invite_msg):
            if account:
                self._contactlist_manager.addContact(account, self._account.view.email,
                                                     invite_msg, [])
        self._gui.gui.aMSNContactInputWindow(('Contact to add: ', 'Invite message: '),
                                             contactCB, ())

    def removeContact(self):
        def contactCB(account):
            if account:
                try:
                    papyon_contact = self._contactlist_manager._papyon_addressbook.\
                                                    contacts.search_by('account', account)[0]
                except IndexError:
                    self._gui.gui.aMSNErrorWindow('You don\'t have the %s contact!', account)
                    return

                self._contactlist_manager.removeContact(papyon_contact.id)

        self._gui.gui.aMSNContactDeleteWindow('Contact to remove: ', contactCB, ())

    def changeDP(self):
        def set_dp(view):
            path = view.imgs[0][1]
            f = open(path)
            dp_obj = papyon.p2p.MSNObject(self._account.client.profile,
                                          os.path.getsize(path),
                                          papyon.p2p.MSNObjectType.DISPLAY_PICTURE,
                                          f.name, f.name, data=f)
            self._account.client.msn_object_store.publish(dp_obj)
            self._personalinfo_manager._personalinfoview.dp = dp_obj

        def open_file():
            def update_dplist(file_path):
                # TODO: fire up a window to choose the dp size and a friendly name
                # TODO: save the new image in a local cache
                dp_view = ImageView('Filename', file_path)
                dpwin.update_dp_list((dp_view, ))
            filters = {'Image files':("*.png", "*.jpeg", "*.jpg", "*.gif", "*.bmp"),
                       'All files':('*.*')}
            directory = os.path.join("amsn2", "themes", "displaypic", "default")
            self._gui.gui.aMSNFileChooserWindow(filters, directory, update_dplist)

        def capture():
            pass

        default_dps = ('dp_amsn', 'dp_female', 'dp_male', 'dp_nopic')
        user_dps = [ImageView('Filename', self._theme_manager.get_dp(dp)[1]) for dp in default_dps]
        dpwin = self._gui.gui.aMSNDPChooserWindow(user_dps,
                                                  (('Capture', capture),
                                                   ('Open file', open_file)),
                                                  set_dp)

    def createMainMenuView(self):
        menu = MenuView()
        quitMenuItem = MenuItemView(MenuItemView.COMMAND, label="Quit",
                                    command = self.quit)
        logOutMenuItem = MenuItemView(MenuItemView.COMMAND, label="Log out", 
                                      command = self.signOutOfAccount)
        mainMenu = MenuItemView(MenuItemView.CASCADE_MENU, label="Main")
        mainMenu.addItem(logOutMenuItem)
        mainMenu.addItem(quitMenuItem)

        addContactItem = MenuItemView(MenuItemView.COMMAND, label="Add Contact",
                                      command=self.addContact)
        removeContact = MenuItemView(MenuItemView.COMMAND, label='Remove contact',
                                     command=self.removeContact)

        contactsMenu = MenuItemView(MenuItemView.CASCADE_MENU, label="Contacts")
        contactsMenu.addItem(addContactItem)
        contactsMenu.addItem(removeContact)

        menu.addItem(mainMenu)
        menu.addItem(contactsMenu)

        return menu

