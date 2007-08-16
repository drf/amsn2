# -*- coding: utf-8 -*-
#
# pymsn - a python client library for Msn
#
# Copyright (C) 2005-2006 Ali Sabil <ali.sabil@gmail.com>
# Copyright (C) 2006  Ole André Vadla Ravnås <oleavr@gmail.com>
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

"""Client
This module contains classes that clients should use in order to make use
of the library."""

from transport import *
from event import ClientState, ClientErrorType

import profile
import msnp
import pymsn.service.SingleSignOn as SSO
import pymsn.service.AddressBook as AB
import pymsn.service.OfflineIM as OIM

from switchboard_manager import SwitchboardManager
from conversation import Conversation
from pymsn.event import EventsDispatcher

import logging

__all__ = ['Client']

logger = logging.getLogger('client')

class Client(EventsDispatcher):
    """This class provides way to connect to the notification server as well
    as methods to manage the contact list, and the personnal settings.

    Basically you should inherit from this class and implement the callbacks
    in order to build a client.

    @group Connection: login, logout"""

    def __init__(self, server, proxies={}, transport_class=DirectConnection):
        """Initializer

            @param server: the Notification server to connect to.
            @type server: tuple(host, port)

            @param proxies: proxies that we can use to connect
            @type proxies: {type: string => L{gnet.proxy.ProxyInfos}}"""
        EventsDispatcher.__init__(self)

        self.__state = ClientState.CLOSED
        self._proxies = proxies
        self._transport_class = transport_class
        self._proxies = proxies
        self._transport = transport_class(server, ServerType.NOTIFICATION,
                self._proxies)

        self._protocol = msnp.NotificationProtocol(self, self._transport,
                self._proxies)

        self._switchboard_manager = SwitchboardManager(self)
        self._switchboard_manager.register_handler_class(Conversation)

        self._sso = None
        self.profile = None
        self.address_book = None

        self.oim_box = None
        self.__setup_callbacks()

    def __setup_callbacks(self):
        self._transport.connect("connection-success", self._on_connect_success)
        self._transport.connect("connection-failure", self._on_connect_failure)
        self._transport.connect("connection-lost", self._on_disconnected)

        self._protocol.connect("notify::state",
                self._on_protocol_state_changed)

        self._switchboard_manager.connect("handler-created",
                self._on_switchboard_handler_created)

    def __setup_addressbook_callbacks(self):
        def connect_signal(name):
            self.address_book.connect(name, self._on_addressbook_event, name)

        connect_signal("new-pending-contact")

        connect_signal("messenger-contact-added")
        connect_signal("contact-deleted")

        connect_signal("contact-blocked")
        connect_signal("contact-unblocked")

        connect_signal("group-added")
        connect_signal("group-deleted")
        connect_signal("group-renamed")
        connect_signal("group-contact-added")
        connect_signal("group-contact-deleted")

    def __setup_oim_box_callbacks(self):
        self.oim_box.connect("notify::state", 
                             self._on_oim_box_state_changed)

        def connect_signal(name):
            self.oim_box.connect(name, self._on_oim_box_event, name)

        connect_signal("messages-fetched")
        connect_signal("message-sent")
        connect_signal("messages-deleted")

    def _get_state(self):
        return self.__state
    def _set_state(self, state):
        self.__state = state
        self._dispatch("on_client_state_changed", state)
    state = property(_get_state)
    _state = property(_get_state, _set_state)

    ### public methods & properties
    def login(self, account, password):
        """Login to the server.

            @param account: the account to use for authentication.
            @type account: string

            @param password: the password needed to authenticate to the account
            """
        assert(self._state == ClientState.CLOSED, "Login already in progress")
        self.profile = profile.User((account, password), self._protocol)
        self._transport.establish_connection()
        self._state = ClientState.CONNECTING

    def logout(self):
        """Logout from the server."""
        if self.__state == ClientState.CLOSED: # FIXME: we need something better
            return
        self._protocol.signoff()
        self.__state = ClientState.CLOSED

    # - - Transport
    def _on_connect_success(self, transp):
        self._sso = SSO.SingleSignOn(self.profile.account, 
                                     self.profile.password,
                                     self._proxies)
        self.address_book = AB.AddressBook(self._sso, self._proxies)
        self.__setup_addressbook_callbacks()
        self.oim_box = OIM.OfflineMessagesBox(self._sso, self._proxies)
        self.__setup_oim_box_callbacks()

        self._state = ClientState.CONNECTED

    def _on_connect_failure(self, transp, reason):
        self._dispatch("on_client_error", ClientErrorType.NETWORK, reason)
        self._state = ClientState.CLOSED

    def _on_disconnected(self, transp, reason):
        self._dispatch("on_client_error", ClientErrorType.NETWORK, reason)
        self._state = ClientState.CLOSED

    # - - Notification Protocol
    def _on_protocol_state_changed(self, proto, param):
        state = proto.state
        if state == msnp.ProtocolState.AUTHENTICATING:
            self._state = ClientState.AUTHENTICATING
        elif state == msnp.ProtocolState.AUTHENTICATED:
            self._state = ClientState.AUTHENTICATED
        elif state == msnp.ProtocolState.SYNCHRONIZING:
            self._state = ClientState.SYNCHRONIZING
        elif state == msnp.ProtocolState.SYNCHRONIZED:
            self._state = ClientState.SYNCHRONIZED
        elif state == msnp.ProtocolState.OPEN:
            self._state = ClientState.OPEN
            im_contacts = [contact for contact in self.address_book.contacts \
                    if contact.attributes['im_contact']]
            for contact in im_contacts:
                self._connect_contact_signals(contact)

    # - - Contact
    def _connect_contact_signals(self, contact):
        contact.connect("notify::presence",
                self._on_contact_property_changed)
        contact.connect("notify::display-name",
                self._on_contact_property_changed)
        contact.connect("notify::personal-message",
                self._on_contact_property_changed)
        contact.connect("notify::current-media",
                self._on_contact_property_changed)
        #contact.connect("notify::display-picture",
        #        self._on_contact_property_changed)
        contact.connect("notify::client-capabilities",
                self._on_contact_property_changed)

    def _on_contact_property_changed(self, contact, pspec):
        method_name = "on_contact_%s_changed" % pspec.name.replace("-", "_")
        self._dispatch(method_name, contact)

    # - - Switchboard Manager
    def _on_switchboard_handler_created(self, sb_mgr, handler_class, handler):
        if handler_class is Conversation:
            if self._dispatch("on_invite_conversation", handler) == 0:
                logger.warning("No event handler attached for conversations")
        else:
            logger.warning("Unknown Switchboard Handler class %s" % handler_class)

    # - - Address book
    def _on_addressbook_event(self, address_book, *args):
        event_name = args[-1]
        event_args = args[:-1]
        if event_name == "messenger-contact-added":
            self._connect_contact_signals(event_args[0])
        method_name = "on_addressbook_%s" % event_name.replace("-", "_")
        self._dispatch(method_name, *event_args)
            
    def _on_addressbook_error(self, address_book, error_code):
        self._dispatch("on_client_error", ClientErrorType.ADDRESSBOOK, error_code)

    # - - Offline messages
    def _on_oim_box_state_changed(self, oim_box, pspec):
        state = oim_box.state
        if state == OIM.constants.OfflineMessagesBoxState.SYNCHRONIZED:
            oim_box.fetch_messages()

    def _on_oim_box_event(self, oim_box, *args):
        method_name = "on_oim_box_%s" % args[-1].replace("-", "_")
        self._dispatch(method_name, args[:-1])
