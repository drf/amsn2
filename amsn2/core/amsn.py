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
import papyon
from views import *
from account_manager import *
from contactlist_manager import *
from conversation_manager import *
from oim_manager import *
from theme_manager import *
from personalinfo_manager import *
from event_manager import *

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
        self._event_manager = aMSNEventManager(self)
        self._options = options

        self._gui_name = None
        self._gui = None
        self._loop = None
        self._main = None
        self.loadUI(self._options.front_end)

        self._backend_manager = aMSNBackendManager()
        self._account_manager = aMSNAccountManager(self, options)
        self._account = None
        self._theme_manager = aMSNThemeManager()
        self._contactlist_manager = aMSNContactListManager(self)
        self._oim_manager = aMSNOIMManager(self)
        self._conversation_manager = aMSNConversationManager(self)
        self._personalinfo_manager = aMSNPersonalInfoManager(self)

        self.p2s = {papyon.Presence.ONLINE:"online",
                    papyon.Presence.BUSY:"busy",
                    papyon.Presence.IDLE:"idle",
                    papyon.Presence.AWAY:"away",
                    papyon.Presence.BE_RIGHT_BACK:"brb",
                    papyon.Presence.ON_THE_PHONE:"phone",
                    papyon.Presence.OUT_TO_LUNCH:"lunch",
                    papyon.Presence.INVISIBLE:"hidden",
                    papyon.Presence.OFFLINE:"offline"}

        import logging
        if self._options.debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.WARNING)

    def run(self):
        self._main.show();
        self._loop.run();

    def loadUI(self, ui_name):
        self._gui_name = ui_name
        self._gui = gui.GUIManager(self, self._gui_name)
        self._loop = self._gui.gui.aMSNMainLoop(self)
        self._main = self._gui.gui.aMSNMainWindow(self)
        self._skin_manager = self._gui.gui.SkinManager(self)

    def switchToUI(self, ui_name):
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
        print "Signing in to account %s" % (accountview.email)
        self._account = self._account_manager.signinToAccount(accountview)
        self._account.login = login_window
        self._account.client = protocol.Client(self, self._account)
        self._account.client.connect(accountview.email, accountview.password)

    def connectionStateChanged(self, account, state):

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
        self._loop.idlerAdd(func)

    def timerAdd(self, delay, func):
        self._loop.timerAdd(delay, func)

    def quit(self):
        if self._account is not None:
            self._account.signOut()
        self._loop.quit()

    def createMainMenuView(self):
        menu = MenuView()
        quitMenuItem = MenuItemView(MenuItemView.COMMAND, label="Quit", command
                                    = self.quit)
        mainMenu = MenuItemView(MenuItemView.CASCADE_MENU, label="Main")
        mainMenu.addItem(quitMenuItem)

        menu.addItem(mainMenu)

        return menu
