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

import pymsn
import pymsn.event

class OIMEvents(pymsn.event.OfflineMessagesEventInterface):
    def __init__(self, client, oim_manager):
        self._oim_manager = oim_manager
        pymsn.event.OfflineMessagesEventInterface.__init__(self, client)
        
    def on_oim_state_changed(self, state):
        pass

    def on_oim_messages_received(self, messages):
        pass

    def on_oim_messages_fetched(self, messages):
        pass

    def on_oim_messages_deleted(self):
        pass

    def on_oim_message_sent(self, recipient, message):
        pass