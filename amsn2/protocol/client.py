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

import papyon
import papyon.event
from events.client import *
from events.contact import *
from events.invite import *
from events.oim import *
from events.addressbook import *

class Client(papyon.Client):
    def __init__(self, amsn_core, profile):
        self._amsn_profile = profile
        self._amsn_core = amsn_core
        server = (self._amsn_profile.getConfigKey("ns_server", "messenger.hotmail.com"),
                  self._amsn_profile.getConfigKey("ns_port", 1863))
        papyon.Client.__init__(self, server)

        self._client_events_handler = ClientEvents(self, self._amsn_core)
        self._contact_events_handler = ContactEvents(self, self._amsn_core._contactlist_manager)
        self._invite_events_handler = InviteEvents(self, self._amsn_core)
        self._oim_events_handler = OIMEvents(self, self._amsn_core._oim_manager)
        self._addressbook_events_handler = AddressBookEvents(self, self._amsn_core)

    def connect(self):
        self.login(self._amsn_profile.email, self._amsn_profile.password)

    def changeNick(self, nick):
        self.profile.display_name = nick.toString()

    def changeMessage(self, message):
        self.profile.personal_message = message.toString()
