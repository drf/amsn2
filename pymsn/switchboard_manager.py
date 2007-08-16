# -*- coding: utf-8 -*-
#
# pymsn - a python client library for Msn
#
# Copyright (C) 2005-2007 Ali Sabil <ali.sabil@gmail.com>
# Copyright (C) 2007 Johann Prieur <johann.prieur@gmail.com>
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

"""Switchboard Manager
The switchboard manager is responsible for managing all the switchboards in
use, it simplifies the complexity of the switchboard crack."""

import logging
import gobject

import pymsn.msnp as msnp
from pymsn.transport import ServerType

__all__ = ['SwitchboardManager']

logger = logging.getLogger('protocol:switchboard_manager')

class SwitchboardClient(object):
    def __init__(self, client, contacts):
        self._client = client
        self._switchboard_manager = self._client._switchboard_manager
        self._switchboard = None
        self._switchboard_requested = False

        self._invite_queue = list(contacts)
        self._message_queue = []

        self.participants = set()

        if len(self._invite_queue) > 0:
            self._switchboard_manager.request_switchboard(self)
            self._switchboard_requested = True

    @staticmethod
    def _can_handle_message(message, switchboard_client=None):
        return False

    def _send_message(self,
            content_type, body, headers={}, ack=msnp.MessageAcknowledgement.HALF):
        if self._switchboard is None or \
                self._switchboard.state != msnp.ProtocolState.OPEN:
            self.__request_switchboard()
            self._message_queue.append((content_type, body, headers, ack))
        elif self._switchboard.inviting:
            self._message_queue.append((content_type, body, headers, ack))
        else:
            self.__send_message(content_type, body, headers, ack)

    def _invite_user(self, contact):
        if self._switchboard is None or \
                self._switchboard.state != msnp.ProtocolState.OPEN:
            self.__request_switchboard()
            self._invite_queue.append(contact)
        else:
            self._switchboard.invite_user(contact)

    def _leave(self):
        if self._switchboard is not None and \
                self._switchboard.state != msnp.ProtocolState.CLOSED:
            self._switchboard.leave()
        self._switchboard_manager.close_handler(self)
    
    # callbacks
    def _on_message_received(self, message):
        pass

    def _on_message_sent(self, message):
        pass

    def _on_contact_joined(self, contact):
        pass

    def _on_contact_left(self, contact):
        pass

    def _on_error(self, switchboard, error_type, error):
        pass

    # private
    def _on_switchboard_update(self, switchboard):
        del self._switchboard
        self._switchboard = switchboard
        self._switchboard_requested = False
        self.participants = set(self._switchboard.participants.values())
        if len(self._invite_queue) > 0:
            self.__process_invite_queue()
        else:
            self.__process_message_queue()
        self._switchboard.connect("notify::inviting",
                lambda sb, pspec: self.__on_user_inviting())
        self._switchboard.connect("user-joined",
                lambda sb, contact: self.__on_user_joined(contact))
        self._switchboard.connect("user-left",
                lambda sb, contact: self.__on_user_left(contact))
        self._switchboard.connect("user-invitation-failed",
                lambda sb, contact: self.__on_user_invitation_failed(contact))
    
    def __on_user_inviting(self):
        if not self._switchboard.inviting:
            self.__process_message_queue()

    def __on_user_joined(self, contact):
        self.participants.add(contact)
        if contact in self._invite_queue:
            self._invite_queue.remove(contact)
        self._on_contact_joined(contact)

    def __on_user_left(self, contact):
        if len(self.participants) > 1:
            self.participants.remove(contact)
            self._on_contact_left(contact)

    def __on_user_invitation_failed(self, contact):
        if contact in self._invite_queue:
            self._invite_queue.remove(contact)
    
    # Helper functions
    def __send_message(self, content_type, body, headers, ack):
        trd_id = self._switchboard._transport.transaction_id
        message = msnp.OutgoingMessage(trd_id, ack)
        message.content_type = content_type
        message.body = body
        for key, value in headers.iteritems():
            message.headers[key] = value
        self._switchboard.send_message(message)

    def __request_switchboard(self):
        if not self._switchboard_requested:
            logger.info("requesting new switchboard")
            self._switchboard_manager.request_switchboard(self)
            # store the current contacts, to get them reinvited
            # automagically :p
            self._invite_queue.extend(self.participants) 
            self._switchboard_requested = True

    def __process_invite_queue(self):
        for contact in self._invite_queue:
            self._switchboard.invite_user(contact)

    def __process_message_queue(self):
        for message_params in self._message_queue:
            self.__send_message(*message_params)
        self._message_queue = []


class SwitchboardManager(gobject.GObject):
    """Switchboard management
        
        @undocumented: do_get_property, do_set_property
        @group Handlers: _handle_*, _default_handler, _error_handler"""
    __gsignals__ = {
            "handler-created": (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                (object, object))
            }

    def __init__(self, client):
        """Initializer

            @param client: the main Client instance"""
        gobject.GObject.__init__(self)
        self._client = client
        self._handlers_instance = set()
        self._handlers_class = set()
        self._switchboards = {}
        self._pending_switchboards = {}
        self._client._protocol.connect("switchboard-invitation-received",
                self.__ns_switchboard_invite)

    def register_handler_class(self, handler_class):
        self._handlers_class.add(handler_class)

    def request_switchboard(self, handler):
        #FIXME: check if a usable switchboard is already available 
        #contacts = set(contacts)
        #for switchboard in self._switchboards:
        #    if set(switchboard.participants.values()) == contacts:

        self._client._protocol.\
                request_switchboard(self.__ns_request_response, handler)

    def close_handler(self, handler):
        self._handlers_instance.remove(handler)

    def __ns_request_response(self, session, handler):
        sb = self.__build_switchboard(session)
        self._pending_switchboards[sb] = handler

    def __ns_switchboard_invite(self, protocol, session, inviter):
        self.__build_switchboard(session)

    def __build_switchboard(self, session):
        server, session_id, key = session
        transport_class = self._client._transport_class
        transport = transport_class(server, ServerType.SWITCHBOARD,
                self._client._proxies)
        sb = msnp.SwitchboardProtocol(self._client, transport,
                session_id, key, self._client._proxies)
        sb.connect("notify::state", self.__sb_state_change)
        sb.connect("message-received", self.__sb_message_received)
        transport.establish_connection()
        return sb

    def __sb_state_change(self, switchboard, param_spec):
        state = switchboard.state
        if state == msnp.ProtocolState.OPEN:
            self._switchboards[switchboard] = set()
            try:
                handler = self._pending_switchboards[switchboard]
                self._switchboards[switchboard].add(handler)
                del self._pending_switchboards[switchboard]
                handler._on_switchboard_update(switchboard)
                self._handlers_instance.add(handler)
            except:
                pass
        elif state == msnp.ProtocolState.CLOSED:
            if switchboard not in self._switchboards:
                return
            del self._switchboards[switchboard]

    def __sb_message_received(self, switchboard, message):
        switchboard_participants = set(switchboard.participants.values())

        for handler in self._handlers_instance:
            handler_switchboard = handler._switchboard
            if handler_switchboard != switchboard:
                if handler_switchboard is not None and \
                        handler_switchboard.state != msnp.ProtocolState.CLOSED:
                    continue
                if handler.participants == switchboard_participants:
                    handler._on_switchboard_update(switchboard)
            if handler._can_handle_message(message, handler):
                handler._on_message_received(message)

        for handler_class in self._handlers_class:
            if not handler_class._can_handle_message(message):
                continue

            skip = False
            for handler in self._handlers_instance:
                if isinstance(handler, handler_class) and \
                        handler._switchboard == switchboard:
                    skip = True
                    break
            if skip:
                continue
            
            handler = handler_class(self._client, ())
            handler._on_switchboard_update(switchboard)
            self.emit("handler-created", handler_class, handler)
            self._handlers_instance.add(handler)
            handler._on_message_received(message)

