# -*- coding: utf-8 -*-
#
# Copyright (C) 2007  Ali Sabil <ali.sabil@gmail.com>
# Copyright (C) 2007  Ole André Vadla Ravnås <oleavr@gmail.com>
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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#

from base import BaseEventInterface
import pymsn.gnet
import pymsn.msnp

__all__ = [ "ClientState", "ClientErrorType",
        "NetworkError", "AuthenticationError", "ProtocolError",
        "ClientEventInterface" ]

ClientState = pymsn.msnp.ProtocolState

class ClientState(object):
    CLOSED = 0
    CONNECTING = 1
    CONNECTED = 2
    AUTHENTICATING = 3
    AUTHENTICATED = 4
    SYNCHRONIZING = 5
    SYNCHRONIZED = 6
    OPEN = 7

class ClientErrorType(object):
    NETWORK = 0
    AUTHENTICATION = 1
    PROTOCOL = 2
    ADDRESSBOOK = 3

NetworkError = pymsn.gnet.IoError

class AuthenticationError(object):
    UNKNOWN = 0
    INVALID_USERNAME = 1
    INVALID_PASSWORD = 2
    INVALID_USERNAME_OR_PASSWORD = 3

class ProtocolError(object):
    UNKNOWN = 0

class ClientEventInterface(BaseEventInterface):
    def __init__(self, client):
        BaseEventInterface.__init__(self, client)

    def on_client_state_changed(self, state):
        pass

    def on_client_error(self, type, error):
        pass

