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
import pymsn
from views import *
from profile import *
from contactlist_manager import *
from conversation_manager import *
from oim_manager import *
from theme_manager import *


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
        self._options = options

        self._gui_name = None
        self._gui = None
        self._loop = None
        self._main = None
        self.loadUI(self._options.front_end)

        self._profile_manager = aMSNProfileManager(options)
        self._profile = None
        self._theme_manager = aMSNThemeManager()
        self._contactlist_manager = aMSNContactListManager(self)
        self._oim_manager = aMSNOIMManager(self)
        self._conversation_manager = aMSNConversationManager(self)

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
        # TODO : load the profiles from disk and all settings
        # then show the login window if autoconnect is disabled

        self._main.setTitle("aMSN 2 - Loading")


        splash = self._gui.gui.aMSNSplashScreen(self, self._main)
        image = ImageView()
        image.load("Filename","/path/to/image/here")

        splash.setImage(image)
        splash.setText("Loading...")
        splash.show()

        login = self._gui.gui.aMSNLoginWindow(self, self._main)

        login.setProfiles(self._profile_manager.getAvailableProfileViews())

        splash.hide()
        self._main.setTitle("aMSN 2 - Login")
        login.show()

        menu = self.createMainMenuView()
        self._main.setMenu(menu)

    def getMainWindow(self):
        return self._main

    def signinToAccount(self, login_window, profileview):
        print "Signing in to account %s" % (profileview.email)
        self.profileself.profile
        profile.login = login_window
        profile.client = protocol.Client(self, profile)
        self._profile = profile
        profile.client.connect()

    def connectionStateChanged(self, profile, state):

        status_str = \
        {
            pymsn.event.ClientState.CONNECTING : 'Connecting to server...',
            pymsn.event.ClientState.CONNECTED : 'Connected',
            pymsn.event.ClientState.AUTHENTICATING : 'Authenticating...',
            pymsn.event.ClientState.AUTHENTICATED : 'Password accepted',
            pymsn.event.ClientState.SYNCHRONIZING : 'Please wait while your contact list\nis being downloaded...',
            pymsn.event.ClientState.SYNCHRONIZED : 'Contact list downloaded successfully.\nHappy Chatting'
        }

        if state in status_str:
            profile.login.onConnecting((state + 1)/ 7., status_str[state])
        elif state == pymsn.event.ClientState.OPEN:
            clwin = self._gui.gui.aMSNContactListWindow(self, self._main)
            clwin.profile = profile
            profile.clwin = clwin
            profile.login.hide()
            self._main.setTitle("aMSN 2")
            profile.clwin.show()
            profile.login = None

            self._contactlist_manager.onCLDownloaded(profile.client.address_book)

    def idlerAdd(self, func):
        self._loop.idlerAdd(func)

    def timerAdd(self, delay, func):
        self._loop.timerAdd(delay, func)

    def quit(self):
        self._loop.quit()

    def createMainMenuView(self):
        menu = MenuView()
        quitMenuItem = MenuItemView(MenuItemView.COMMAND, label="Quit", command
                                    = self.quit)
        mainMenu = MenuItemView(MenuItemView.CASCADE_MENU, label="Main")
        mainMenu.addItem(quitMenuItem)

        menu.addItem(mainMenu)

        return menu
