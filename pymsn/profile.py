# -*- coding: utf-8 -*-
#
# pymsn - a python client library for Msn
#
# Copyright (C) 2005-2006 Ali Sabil <ali.sabil@gmail.com>
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

"""Profile of the User connecting to the service, as well as the profile of
contacts in his/her contact list."""

import gobject

__all__ = ['Presence', 'User', 'Contact']


class ClientCapabilities(object):

    _CAPABILITIES = {
            'is_bot': 0x00020000,
            'is_mobile_device': 0x00000001,
            'is_msn_mobile': 0x00000040,
            'is_msn_direct_device': 0x00000080,

            'is_media_center_user': 0x00002000,
            'is_msn8_user': 0x00000002,

            'is_web_client': 0x00000200,
            'is_tgw_client': 0x00000800,

            'has_space': 0x00001000,
            'has_webcam': 0x00000010,
            'has_onecare': 0x01000000,

            'renders_gif': 0x00000004,
            'renders_isf': 0x00000008,

            'supports_chunking': 0x00000020,
            'supports_direct_im': 0x00004000,
            'supports_winks': 0x00008000,
            'supports_shared_search': 0x00010000,
            'supports_voice_im': 0x00040000,
            'supports_secure_channel': 0x00080000,
            'supports_sip_invite': 0x00100000,
            'supports_shared_drive': 0x00400000,

            'p2p_supports_turn': 0x02000000,
            'p2p_bootstrap_via_uun': 0x04000000
            }

    def __init__(self, msnc=0, client_id=0):
        MSNC = (0x0,        # MSNC0
                0x10000000, # MSNC1
                0x20000000, # MSNC2
                0x30000000, # MSNC3
                0x40000000, # MSNC4
                0x50000000, # MSNC5
                0x60000000, # MSNC6
                0x70000000) # MSNC7
        object.__setattr__(self, 'client_id', MSNC[msnc] | client_id)

    def __getattr__(self, name):
        if name == "p2p_aware":
            mask = 0xf0000000
        elif name in self._CAPABILITIES:
            mask = self._CAPABILITIES[name]
        else:
            raise AttributeError("object 'ClientCapabilities' has no attribute '%s'" % name)
        return (self.client_id & mask != 0)

    def __setattr__(self, name, value):
        if name in self._CAPABILITIES:
            mask = self._CAPABILITIES[name]
            if value:
                self.client_id |= mask
            else:
                self.client_id ^= mask
        else:
            raise AttributeError("object 'ClientCapabilities' has no attribute '%s'" % name)

    def __str__(self):
        return str(self.client_id)


class NetworkID(object):
    """Refers to the contact Network ID"""
    MSN = 1
    """Microsoft Network"""
    LCS = 2
    """Microsoft Live COmmunication Server"""
    MOBILE = 4
    """Mobile phones"""
    EXTERNAL = 32
    """External IM etwork, currently Yahoo!"""


class Presence(object):
    """Presence states.

    The members of this class are used to identify the Presence that a user
    wants to advertise to the contacts on his/her contact list.

        @cvar ONLINE: online
        @cvar BUSY: busy
        @cvar IDLE: idle
        @cvar AWAY: away
        @cvar BE_RIGHT_BACK: be right back
        @cvar ON_THE_PHONE: on the phone
        @cvar OUT_TO_LUNCH: out to lunch
        @cvar INVISIBLE: status hidden from contacts
        @cvar OFFLINE: offline"""
    ONLINE = 'NLN'
    BUSY = 'BSY'
    IDLE = 'IDL'
    AWAY = 'AWY'
    BE_RIGHT_BACK = 'BRB'
    ON_THE_PHONE = 'PHN'
    OUT_TO_LUNCH = 'LUN'
    INVISIBLE = 'HDN'
    OFFLINE = 'FLN'


class Privacy(object):
    """User privacy, defines the default policy concerning contacts
    not belonging to the ALLOW list nor to the BLOCK list

        @cvar ALLOW: allow by default
        @cvar BLOCK: block by default"""
    ALLOW = 'AL'
    BLOCK = 'BL'


class Membership(object):
    UNKNOWN = 0
    FORWARD = 1
    ALLOW   = 2
    BLOCK   = 4
    REVERSE = 8
    PENDING = 16

class User(gobject.GObject):
    """Profile of the User connecting to the service

        @undocumented: do_get_property, do_set_property, __gproperties__

        @ivar account: the account name
        @ivar password: the password used to authenticate
        @ivar profile: the profile sent by the server
        @ivar display_name: the display name shown to contacts
        @ivar presence: the presence advertised
        @ivar personal_message: the personal message shown to contacts"""""

    __gproperties__ = {
            "display-name": (gobject.TYPE_STRING,
                "Friendly name",
                "A nickname that the user chooses to display to others",
                "",
                gobject.PARAM_READABLE),

            "personal-message": (gobject.TYPE_STRING,
                "Personal message",
                "The personal message that the user wants to display",
                "",
                gobject.PARAM_READABLE),

            "current-media": (gobject.TYPE_PYOBJECT,
                "Current media",
                "The current media that the user wants to display",
                gobject.PARAM_READABLE),

            "profile": (gobject.TYPE_STRING,
                "Profile",
                "the text/x-msmsgsprofile sent by the server",
                "",
                gobject.PARAM_READABLE),

            "presence": (gobject.TYPE_STRING,
                "Presence",
                "The presence to show to others",
                Presence.OFFLINE,
                gobject.PARAM_READABLE),

            "privacy": (gobject.TYPE_STRING,
                "Privacy",
                "The privacy policy to use",
                Privacy.BLOCK,
                gobject.PARAM_READABLE),
            }

    def __init__(self, account, ns_client):
        gobject.GObject.__init__(self)
        self._ns_client = ns_client
        self._account = account[0]
        self._password = account[1]

        self._profile = ""
        self._display_name = self._account.split("@", 1)[0]
        self._presence = Presence.OFFLINE
        self._privacy = Privacy.BLOCK
        self._personal_message = ""
        self._current_media = None

        self.client_id = ClientCapabilities(7)

        #FIXME: Display Picture

    @property
    def account(self):
        return self._account

    @property
    def password(self):
        return self._password

    @property
    def profile(self):
        return self._profile

    def __set_display_name(self, display_name):
        if not display_name:
            return
        self._ns_client.set_display_name(display_name)
    def __get_display_name(self):
        return self._display_name
    display_name = property(__get_display_name, __set_display_name)

    def __set_presence(self, presence):
        if presence == self._presence:
            return
        self._ns_client.set_presence(presence)
    def __get_presence(self):
        return self._presence
    presence = property(__get_presence, __set_presence)

    def __set_privacy(self, privacy):
        pass #FIXME: set the privacy setting
    def __get_privacy(self):
        return self._privacy
    privacy = property(__get_privacy, __set_privacy)

    def __set_personal_message(self, personal_message):
        if personal_message == self._personal_message:
            return
        self._ns_client.set_personal_message(personal_message,
                                             self._current_media)
    def __get_personal_message(self):
        return self._personal_message
    personal_message = property(__get_personal_message, __set_personal_message)

    def __set_current_media(self, current_media):
        if current_media == self._current_media:
            return
        self._ns_client.set_personal_message(self._personal_message,
                                             current_media)
    def __get_current_media(self):
        return self._current_media
    current_media = property(__get_current_media, __set_current_media)

    def _server_property_changed(self, name, value):
        attr_name = "_" + name.lower().replace("-", "_")
        old_value = getattr(self, attr_name)
        if value != old_value:
            setattr(self, attr_name, value)
            self.notify(name)

    def do_get_property(self, pspec):
        name = pspec.name.lower().replace("-", "_")
        return getattr(self, name)
gobject.type_register(User)


class Contact(gobject.GObject):
    """Contact related information
        @undocumented: do_get_property, do_set_property, __gproperties__"""

    __gsignals__ =  {
            "added": (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                ()),
            "added-me": (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                ()),
            "removed": (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                ()),
            "removed-me": (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                ()),
            "blocked": (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                ()),
            "allowed": (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                ()),
            }

    __gproperties__ = {
            "memberships": (gobject.TYPE_UINT,
                "Memberships",
                "Membership relation with the contact.",
                0, 15, 0, gobject.PARAM_READABLE),

            "display-name": (gobject.TYPE_STRING,
                "Friendly name",
                "A nickname that the user chooses to display to others",
                "",
                gobject.PARAM_READWRITE),

            "personal-message": (gobject.TYPE_STRING,
                "Personal message",
                "The personal message that the user wants to display",
                "",
                gobject.PARAM_READABLE),

            "current-media": (gobject.TYPE_PYOBJECT,
                "Current media",
                "The current media that the user wants to display",
                gobject.PARAM_READABLE),

            "presence": (gobject.TYPE_STRING,
                "Presence",
                "The presence to show to others",
                Presence.OFFLINE,
                gobject.PARAM_READABLE),

             "groups": (gobject.TYPE_PYOBJECT,
                 "Groups",
                 "The groups the contact belongs to",
                 gobject.PARAM_READABLE),

            "client-capabilities": (gobject.TYPE_UINT64,
                "Client capabilities",
                "The client capabilities of the contact 's client",
                0, 0xFFFFFFFF, 0,
                gobject.PARAM_READABLE),

            "msn-object": (gobject.TYPE_STRING,
                "MSN Object",
                "MSN Object attached to the contact, this generally represent "
                "its display picture",
                "",
                gobject.PARAM_READABLE),
            }

    def __init__(self, id, network_id, account, display_name, cid,
            memberships=Membership.UNKNOWN):
        """Initializer"""
        gobject.GObject.__init__(self)
        self._id = id
        self._cid = cid
        self._network_id = network_id
        self._account = account

        self._display_name = display_name
        self._presence = Presence.OFFLINE
        self._personal_message = ""
        self._current_media = None
        self._groups = set()

        self._memberships = memberships
        self._client_capabilities = ClientCapabilities()
        self._msn_object = ""
        self._attributes = {'im_contact' : False}

    @property
    def id(self):
        """Contact identifier in a GUID form"""
        return self._id

    @property
    def attributes(self):
        """Contact attributes"""
        return self._attributes.copy()

    @property
    def cid(self):
        """Contact ID"""
        return self._cid

    @property
    def network_id(self):
        """Contact network ID"""
        return self._network_id

    @property
    def account(self):
        """Contact account"""
        return self._account
    
    @property
    def presence(self):
        """Contact presence"""
        return self._presence

    @property
    def display_name(self):
        """Contact display name"""
        return self._display_name
    
    @property
    def personal_message(self):
        """Contact personal message"""
        return self._personal_message

    @property
    def current_media(self):
        """Contact current media"""
        return self._current_media

    @property
    def groups(self):
        """Contact list of groups"""
        return self._groups

    @property
    def memberships(self):
        """Contact membership value"""
        return self._memberships

    @property
    def client_capabilities(self):
        """Contact client capabilities"""
        return self._client_capabilities
    
    @property
    def msn_object(self):
        """Contact MSN Object"""
        return self._msn_object

    @property
    def domain(self):
        """Contact domain"""
        result = self._account.split('@', 1)
        if len(result) > 1:
            return result[1]
        else:
            return ""

    ### membership management
    def is_member(self, memberships):
        return (self.memberships & memberships) == memberships

    def _add_membership(self, membership):
        if not self.is_member(Membership.REVERSE) and \
                membership == Membership.REVERSE:
            self.emit("added-me")
        elif not self.is_member(Membership.FORWARD) and \
                membership == Membership.FORWARD:
            self.emit("added")

        self._memberships |= membership
        self.notify("memberships")

    def _remove_membership(self, membership):
        """removes the given membership from the contact

            @param membership: the membership to remove
            @type membership: int L{Membership}"""
        if self.is_member(Membership.REVERSE) and \
                membership == Membership.REVERSE:
            self.emit("removed-me")
        elif self.is_member(Membership.FORWARD) and \
                membership == Membership.FORWARD:
            self.emit("removed")

        self._memberships ^= membership
        self.notify("memberships")

    def _server_property_changed(self, name, value): #FIXME, should not be used for memberships
        if name == "client-capabilities":
            value = ClientCapabilities(client_id=value)
        attr_name = "_" + name.lower().replace("-", "_")
        old_value = getattr(self, attr_name)
        if value != old_value:
            setattr(self, attr_name, value)
            self.notify(name)

    def _server_contact_attribute_changed(self, name, value):
        self._attributes[name] = value
        
    ### group management
    def _add_group_ownership(self, group):
        self._groups.add(group)

    def _delete_group_ownership(self, group):
        self._groups.discard(group)

    def do_get_property(self, pspec):
        name = pspec.name.lower().replace("-", "_")
        return getattr(self, name)
gobject.type_register(Contact)

class Group(gobject.GObject):

    __gsignals__ = {
        "updated": (gobject.SIGNAL_RUN_FIRST,
                    gobject.TYPE_NONE,
                    ())
        }

    __gproperties__ = {
        "name": (gobject.TYPE_STRING,
                 "Group name",
                 "Name that the user chooses for the group",
                 "",
                 gobject.PARAM_READABLE)
        }

    def __init__(self, id, name):
        """Initializer"""
        gobject.GObject.__init__(self)
        self._id = id
        self._name = name

    @property
    def id(self):
        "Group identifier in a GUID form"""
        return self._id

    @property
    def name(self):
        "Group name"
        return self._name

    def do_get_property(self, pspec):
        name = pspec.name.lower().replace("-", "_")
        return getattr(self, name)

gobject.type_register(Group)

