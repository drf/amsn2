# -*- coding: utf-8 -*-
#
# pymsn - a python client library for Msn
#
# Copyright (C) 2005-2007 Ali Sabil <ali.sabil@gmail.com>
# Copyright (C) 2005-2006 Ole André Vadla Ravnås <oleavr@gmail.com>
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
# GNU General Public License for more details
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""Notification protocol Implementation
Implements the protocol used to communicate with the Notification Server."""

from base import BaseProtocol, ProtocolState
from message import Message
from constants import ProtocolConstant
from challenge import _msn_challenge

import pymsn
from pymsn.gnet.message.HTTP import HTTPMessage
from pymsn.util.queue import PriorityQueue, LastElementQueue
from pymsn.util.decorator import throttled
import pymsn.util.element_tree as ElementTree
import pymsn.profile as profile
import pymsn.service.SingleSignOn as SSO
import pymsn.service.AddressBook as AB
import pymsn.service.OfflineIM as OIM

import logging
import urllib
import gobject
import xml.sax.saxutils as xml_utils

__all__ = ['NotificationProtocol']

logger = logging.getLogger('protocol:notification')


class NotificationProtocol(BaseProtocol, gobject.GObject):
    """Protocol used to communicate with the Notification Server

        @undocumented: do_get_property, do_set_property
        @group Handlers: _handle_*, _default_handler, _error_handler

        @ivar state: the current protocol state
        @type state: integer
        @see L{base.ProtocolState}"""
    __gsignals__ = {
            "authentication-failed" : (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                ()),

            "mail-received" : (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                (object,)),

            "switchboard-invitation-received" : (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                (object, object)),

            "unmanaged-message-received" : (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                (object, object)),
            }

    __gproperties__ = {
            "state":  (gobject.TYPE_INT,
                "State",
                "The state of the communication with the server.",
                0, 6, ProtocolState.CLOSED,
                gobject.PARAM_READABLE)
            }

    def __init__(self, client, transport, proxies={}):
        """Initializer

            @param client: the parent instance of L{client.Client}
            @type client: L{client.Client}

            @param transport: The transport to use to speak the protocol
            @type transport: L{transport.BaseTransport}

            @param proxies: a dictonary mapping the proxy type to a
                L{gnet.proxy.ProxyInfos} instance
            @type proxies: {type: string, proxy:L{gnet.proxy.ProxyInfos}}
        """
        BaseProtocol.__init__(self, client, transport, proxies)
        gobject.GObject.__init__(self)
        self.__state = ProtocolState.CLOSED
        self._protocol_version = 0

    # Properties ------------------------------------------------------------
    def __get_state(self):
        return self.__state
    def __set_state(self, state):
        self.__state = state
        self.notify("state")
    state = property(__get_state)
    _state = property(__get_state, __set_state)

    def do_get_property(self, pspec):
        if pspec.name == "state":
            return self.__state
        else:
            raise AttributeError, "unknown property %s" % pspec.name

    def do_set_property(self, pspec, value):
        raise AttributeError, "unknown property %s" % pspec.name

    # Public API -------------------------------------------------------------
    @throttled(2000, LastElementQueue())
    def set_presence(self, presence, client_id=0, msn_object=None):
        """Publish the new user presence.

            @param presence: the new presence
            @type presence: string L{profile.Presence}"""
        if msn_object == None:
            msn_object = ""

        if presence == profile.Presence.OFFLINE:
            self.signoff()
        else:
            if msn_object:
                self._client._msn_object_store.publish(msn_object)
            self._send_command('CHG',
                    (presence, str(client_id), urllib.quote(str(msn_object))))

    @throttled(2000, LastElementQueue())
    def set_display_name(self, display_name):
        """Sets the new display name

            @param friendly_name: the new friendly name
            @type friendly_name: string"""
        self._send_command('PRP',
                ('MFN', urllib.quote(display_name)))

    @throttled(2000, LastElementQueue())
    def set_personal_message(self, personal_message='', current_media=None):
        """Sets the new personal message

            @param personal_message: the new personal message
            @type personal_message: string"""
        cm = ''
        if current_media is not None:
            cm ='\\0Music\\01\\0{0} - {1}\\0%s\\0%s\\0\\0' % \
                (xml_utils.escape(current_media[0]), 
                 xml_utils.escape(current_media[1]))

        message = xml_utils.escape(personal_message)
        pm = '<Data>'\
                '<PSM>%s</PSM>'\
                '<CurrentMedia>%s</CurrentMedia>'\
                '<MachineGuid>{CAFEBABE-DEAD-BEEF-BAAD-FEEDDEADC0DE}</MachineGuid>'\
            '</Data>' % (message, cm)
        self._send_command('UUX', payload=pm)
        self._client.profile._server_property_changed("personal-message",
                personal_message)
        if current_media is not None:
            self._client.profile._server_property_changed("current-media",
                current_media)

    def signoff(self):
        """Logout from the server"""
        self._send_command('OUT')
        self._transport.lose_connection()

    @throttled(7600, list())
    def request_switchboard(self, priority, callback, *callback_args):
        self.__switchboard_callbacks.add((callback, callback_args), priority)
        self._send_command('XFR', ('SB',))

    def add_contact_to_membership(self, account,
            network_id=profile.NetworkID.MSN,
            membership=profile.Membership.FORWARD):
        """Add a contact to a given membership.

            @param account: the contact identifier
            @type account: string

            @param network_id: the contact network
            @type network_id: integer
            @see L{pymsn.profile.NetworkID}

            @param membership: the list to be added to
            @type membership: integer
            @see L{pymsn.profile.Membership}"""

        if network_id == profile.NetworkID.MOBILE:
            payload = '<ml><t><c n="tel:%s" l="%d" /></t></ml>' % \
                    (contact, membership)
            self._send_command("ADL", payload=payload)
        else:
            contact, domain = account.split("@", 1)
            payload = '<ml><d n="%s"><c n="%s" l="%d" t="%d"/></d></ml>' % \
                    (domain, contact, membership, network_id)
            self._send_command("ADL", payload=payload)

    def remove_contact_from_membership(self, account,
            network_id=profile.NetworkID.MSN,
            membership=profile.Membership.FORWARD):
        """Remove a contact from a given membership.

            @param account: the contact identifier
            @type account: string

            @param network_id: the contact network
            @type network_id: integer
            @see L{pymsn.profile.NetworkID}

            @param membership: the list to be added to
            @type membership: integer
            @see L{pymsn.profile.Membership}"""

        if network_id == profile.NetworkID.MOBILE:
            payload = '<ml><t><c n="tel:%s" l="%d" /></t></ml>' % \
                    (contact, membership)
            self._send_command("RML", payload=payload)
        else:
            contact, domain = account.split("@", 1)
            payload = '<ml><d n="%s"><c n="%s" l="%d" t="%d"/></d></ml>' % \
                    (domain, contact, membership, network_id)
            self._send_command("RML", payload=payload)

    def send_unmanaged_message(self, contact, message):
        content_type = message.content_type[0]
        if content_type == 'text/x-msnmsgr-datacast':
            message_type = 3
        elif content_type == 'text/x-msmsgscontrol':
            message_type = 2
        else:
            message_type = 1
        self._send_command('UUM',
                (contact.account, contact.network_id, message_type),
                payload=message)
        
    # Handlers ---------------------------------------------------------------
    # --------- Connection ---------------------------------------------------
    def _handle_VER(self, command):
        assert(len(command.arguments) > 1), "Invalid VER response : " + str(command)
        self._protocol_version = int(command.arguments[0].lstrip('MSNP'))
        self._send_command('CVR',
                ProtocolConstant.CVR + (self._client.profile.account,))

    def _handle_CVR(self, command):
        if self._protocol_version >= 15:
            method = 'SSO'
        else:
            method = 'TWN'
        self._send_command('USR',
                (method, 'I', self._client.profile.account))

    def _handle_XFR(self, command):
        if command.arguments[0] == 'NS':
            try:
                host, port = command.arguments[1].split(":", 1)
                port = int(port)
            except ValueError:
                host = command.arguments[1]
                port = self._transport.server[1]
            logger.debug("<-> Redirecting to " + command.arguments[1])
            self._transport.reset_connection((host,port))
        else: # connect to a switchboard
            try:
                host, port = command.arguments[1].split(":", 1)
                port = int(port)
            except ValueError:
                host = command.arguments[1]
                port = self._transport.server[1]
            session_id = command.arguments[3]
            callback, callback_args = self.__switchboard_callbacks.pop(0)
            callback(((host, port), session_id, None), *callback_args)

    def _handle_USR(self, command):
        args_len = len(command.arguments)

        # MSNP15 have only 4 params for final USR
        assert(args_len == 3 or args_len == 4), \
                "Received USR with invalid number of params : " + str(command)

        if command.arguments[0] == "OK":
            self._state = ProtocolState.AUTHENTICATED

        # we need to authenticate with a passport server
        elif command.arguments[1] == "S":
            self._state = ProtocolState.AUTHENTICATING
            if command.arguments[0] == "SSO":
                self._client._sso.RequestMultipleSecurityTokens(
                    (self._sso_cb, command.arguments[3]),
                    (lambda *args: self.emit("authentication-failed"),),
                    SSO.LiveService.MESSENGER_CLEAR)
                
                self._client.address_book.connect("notify::state",
                    self._address_book_state_changed_cb)

                self._client.address_book.connect("messenger-contact-added",
                        self._address_book_contact_added_cb)
                self._client.address_book.connect("contact-accepted",
                        self._address_book_contact_accepted_cb)
                self._client.address_book.connect("contact-rejected",
                        self._address_book_contact_rejected_cb)
                self._client.address_book.connect("contact-deleted",
                        self._address_book_contact_deleted_cb)
                self._client.address_book.connect("contact-blocked",
                        self._address_book_contact_blocked_cb)
                self._client.address_book.connect("contact-unblocked",
                        self._address_book_contact_unblocked_cb)

            elif command.arguments[0] == "TWN":
                raise NotImplementedError, "Missing Implementation, please fix"

    def _handle_SBS(self, command): # unknown command
        pass

    def _handle_OUT(self, command):
        pass

    # --------- Presence & Privacy -------------------------------------------
    def _handle_BLP(self, command):
        self._client.profile._server_property_changed("privacy",
                command.arguments[0])

    def _handle_CHG(self, command):
        self._client.profile._server_property_changed("presence",
                command.arguments[0])
        if len(command.arguments) > 2:
            if command.arguments[2] != '0':
                msn_object = pymsn.p2p.MSNObject.parse(self._client,
                               urllib.unquote(command.arguments[2]))
            else:
                msn_object = None
            self._client.profile._server_property_changed("msn_object", msn_object)
        else:
            self._client.profile._server_property_changed("msn_object", None)

    def _handle_ILN(self,command):
        self._handle_NLN(command)

    def _handle_FLN(self,command):
        network_id = int(command.arguments[1])
        account = command.arguments[0]

        contacts = self._client.address_book.contacts.\
                search_by_network_id(network_id).\
                search_by_account(account)

        if len(contacts) == 0:
            logger.warning("Contact (network_id=%d) %s not found" % \
                    (network_id, account))

        for contact in contacts:
            contact._server_property_changed("presence",
                    profile.Presence.OFFLINE)

    def _handle_NLN(self,command):
        network_id = int(command.arguments[2])
        account = command.arguments[1]

        contacts = self._client.address_book.contacts.\
                search_by_network_id(network_id).\
                search_by_account(account)
        
        if len(contacts) == 0:
            logger.warning("Contact (network_id=%d) %s not found" % \
                    (network_id, account))
        for contact in contacts:
            presence = command.arguments[0]
            display_name = urllib.unquote(command.arguments[3])
            capabilities = int(command.arguments[4])
            contact._server_property_changed("presence", presence)
            contact._server_property_changed("display-name", display_name)
            contact._server_property_changed("client-capabilities", capabilities)
            if len(command.arguments) >= 6:
                if command.arguments[5] != '0':
                    msn_object = pymsn.p2p.MSNObject.parse(self._client,
                                   urllib.unquote(command.arguments[5]))
                    contact._server_property_changed("msn-object", msn_object)
                elif command.arguments[5] == '0':
                    contact._server_property_changed("msn-object", None)
                elif len(command.arguments) > 6:
                    icon_url = command.arguments[6]
                    contact._server_attribute_changed('icon_url', icon_url)

    # --------- Display name and co ------------------------------------------
    def _handle_PRP(self, command):
        ctype = command.arguments[0]
        if len(command.arguments) < 2: return
        if ctype == 'MFN':
            self._client.profile._server_property_changed('display-name',
                    urllib.unquote(command.arguments[1]))
        # TODO: add support for other stuff

    def _handle_UUX(self, command):
        pass

    def _handle_UBN(self,command): # contact infos
        if not command.payload:
            return
        print "RECEIVED UBN : %s\n%s" % (command, command.payload)
        
    def _handle_UBX(self,command): # contact infos
        if not command.payload:
            return
        
        network_id = int(command.arguments[1])
        account = command.arguments[0] 

        contacts = self._client.address_book.contacts.\
                search_by_network_id(network_id).\
                search_by_account(account)

        if len(contacts) == 0:
            logger.warning("Contact (network_id=%d) %s not found" % \
                    (network_id, account))
        for contact in contacts:
            cm = ElementTree.fromstring(command.payload).find("./CurrentMedia")
            if cm is not None and cm.text is not None:
                parts = cm.text.split('\\0')
                if parts[1] == 'Music' and parts[2] == '1':
                    cm = (parts[4].encode("utf-8"), parts[5].encode("utf-8"))
                    contact._server_property_changed("current-media", cm)
                    continue
                elif parts[2] == '0':
                    contact._server_property_changed("current-media", None)
            else:
                contact._server_property_changed("current-media", None)
            pm = ElementTree.fromstring(command.payload).find("./PSM")
            if pm is not None and pm.text is not None:
                pm = pm.text.encode("utf-8")
            else:
                pm = ""
            contact._server_property_changed("personal-message", pm)
    # --------- Contact List -------------------------------------------------
    def _handle_ADL(self, command):
        if command.transaction_id == 0: # incoming ADL from the server
            self._client.address_book.check_pending_invitations()
        if len(command.arguments) > 0 and command.arguments[0] == "OK":
            if self._state != ProtocolState.OPEN: # Initial ADL
                self._state = ProtocolState.OPEN
                self._transport.enable_ping()
            else: # contact Added
                pass

    # --------- Messages -----------------------------------------------------
    def _handle_MSG(self, command):
        message = Message(None, command.payload)
        content_type = message.content_type
        if content_type[0] == 'text/x-msmsgsprofile':
            self._client.profile._server_property_changed("profile",
                    command.payload)

            if self._protocol_version < 15:
                #self._send_command('SYN', ('0', '0'))
                raise NotImplementedError, "Missing Implementation, please fix"
            else:
                self._send_command("BLP",
                        (self._client.profile.privacy,))
                self._state = ProtocolState.SYNCHRONIZING
                self._client.address_book.sync()
        elif content_type[0] in \
                ('text/x-msmsgsinitialemailnotification', \
                 'text/x-msmsgsemailnotification'):
            self.emit("mail-received", message)
        elif content_type[0] in \
                ('text/x-msmsgsinitialmdatanotification', \
                 'text/x-msmsgsoimnotification'):
            if self._client.oim_box is not None:
                self._client.oim_box._state = \
                    OIM.OfflineMessagesBoxState.NOT_SYNCHRONIZED
                m = HTTPMessage()
                m.parse(message.body)
                mail_data = m.get_header('Mail-Data').strip()
                if mail_data == 'too-large':
                    mail_data = None
                self._client.oim_box.sync(mail_data)
        elif content_type[0] == 'text/x-msmsgsactivemailnotification':
            pass
    
    def _handle_UBM(self, command):
        network_id = int(command.arguments[1])
        account = command.arguments[0]

        contacts = self._client.address_book.contacts.\
                search_by_network_id(network_id).\
                search_by_account(account)

        if len(contacts) == 0:
            logger.warning("Contact (network_id=%d) %s not found" % \
                    (network_id, account))
        else:
            contact = contacts[0]
            message = Message(contact, command.payload)
            self.emit("unmanaged-message-received", contact, message)

    # --------- Invitation ---------------------------------------------------
    def _handle_RNG(self,command):
        session_id = command.arguments[0]
        host, port = command.arguments[1].split(':',1)
        port = int(port)
        key = command.arguments[3]
        account = command.arguments[4]
        display_name = urllib.unquote(command.arguments[5])

        session = ((host, port), session_id, key)
        inviter = (account, display_name)
        self.emit("switchboard-invitation-received", session, inviter)

    # --------- Challenge ----------------------------------------------------
    def _handle_QNG(self,command):
        pass

    def _handle_QRY(self,command):
        pass

    def _handle_CHL(self,command):
        response = _msn_challenge(command.arguments[0])
        self._send_command('QRY',
                (ProtocolConstant.PRODUCT_ID,), payload=response)

    # callbacks --------------------------------------------------------------
    def _connect_cb(self, transport):
        self.__switchboard_callbacks = PriorityQueue()
        self._state = ProtocolState.OPENING
        self._send_command('VER', ProtocolConstant.VER)

    def _disconnect_cb(self, transport, reason):
        self._state = ProtocolState.CLOSED

    def _sso_cb(self, tokens, nonce):
        clear_token = tokens[SSO.LiveService.MESSENGER_CLEAR]
        blob = clear_token.mbi_crypt(nonce)

        self._send_command("USR",
                ("SSO", "S", clear_token.security_token, blob))

    def _address_book_state_changed_cb(self, address_book, pspec):
        MAX_PAYLOAD_SIZE = 7500
        if address_book.state != AB.AddressBookState.SYNCHRONIZED:
            return
        self._client.profile._server_property_changed("display-name",
                address_book.profile.display_name)

        contacts = address_book.contacts\
                .search_by_memberships(profile.Membership.FORWARD)\
                .group_by_domain()
        
        payloads = ['<ml l="1">']
        mask = ~(profile.Membership.REVERSE | profile.Membership.PENDING)
        for domain, contacts in contacts.iteritems():
            payloads[-1] += '<d n="%s">' % domain
            for contact in contacts:
                user = contact.account.split("@", 1)[0]
                lists = contact.memberships & mask
                network_id = contact.network_id
                node = '<c n="%s" l="%d" t="%d"/>' % (user, lists, network_id)
                size = len(payloads[-1]) + len(node) + len('</d></ml>')
                if size >= MAX_PAYLOAD_SIZE:
                    payloads[-1] += '</d></ml>'
                    payloads.append('<ml l="1"><d n="%s">' % domain)
                payloads[-1] += node 
            payloads[-1] += '</d>'
        payloads[-1] += '</ml>'
        
        for payload in payloads:
            self._send_command("ADL", payload=payload)
        self._state = ProtocolState.SYNCHRONIZED

    def _address_book_contact_added_cb(self, address_book, contact):
        self.add_contact_to_membership(contact.account, contact.network_id,
                                       profile.Membership.ALLOW)
        
        self.add_contact_to_membership(contact.account, contact.network_id,
                                       profile.Membership.FORWARD)
        
        if contact.network_id != profile.NetworkID.MOBILE:
            account, domain = contact.account.split('@', 1)
            payload = '<ml l="2"><d n="%s"><c n="%s"/></d></ml>'% \
                    (domain, account)
            self._send_command("FQY", payload=payload)

    def _address_book_contact_deleted_cb(self, address_book, contact):
        self.remove_contact_from_membership(contact.account, contact.network_id,
                                            profile.Membership.ALLOW)

        self.add_contact_to_membership(contact.account, contact.network_id,
                                       profile.Membership.BLOCK)

        self.remove_contact_from_membership(contact.account, contact.network_id,
                                            profile.Membership.FORWARD)

    def _address_book_contact_accepted_cb(self, address_book, contact):
        mask = ~(profile.Membership.REVERSE | profile.Membership.PENDING)
        memberships = contact.memberships & mask
        if memberships:
            self.add_contact_to_membership(contact.account, contact.network_id,
                    memberships)

    def _address_book_contact_rejected_cb(self, address_book, contact):
        mask = ~(profile.Membership.REVERSE | profile.Membership.PENDING)
        memberships = contact.memberships & mask
        if memberships:
            self.add_contact_to_membership(contact.account, contact.network_id,
                    memberships)

    def _address_book_contact_blocked_cb(self, address_book, contact):
        self.remove_contact_from_membership(contact.account, contact.network_id,
                                            profile.Membership.ALLOW)

        self.add_contact_to_membership(contact.account, contact.network_id,
                                       profile.Membership.BLOCK)

    def _address_book_contact_unblocked_cb(self, address_book, contact):
        self.remove_contact_from_membership(contact.account, contact.network_id,
                                            profile.Membership.BLOCK)

        self.add_contact_to_membership(contact.account, contact.network_id,
                                       profile.Membership.ALLOW)
