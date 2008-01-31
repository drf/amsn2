# -*- coding: utf-8 -*-
#
# pymsn - a python client library for Msn
#
# Copyright (C) 2005-2006 Ali Sabil <ali.sabil@gmail.com>
# Copyright (C) 2007-2008 Johann Prieur <johann.prieur@gmail.com>
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
contacts in his/her contact list.

    @sort: Profile, Contact, Group, ClientCapabilities
    @group Enums: Presence, Membership, Privacy, NetworkID
    @sort: Presence, Membership, Privacy, NetworkID"""

from pymsn.util.decorator import rw_property

import gobject

__all__ = ['Profile', 'Contact', 'Group', 
        'Presence', 'Membership', 'ContactType', 'Privacy', 'NetworkID', 'ClientCapabilities']


class ClientCapabilities(object):
    """Capabilities of the client. This allow adverstising what the User Agent
    is capable of, for example being able to receive video stream, and being
    able to receive nudges...
    
        @ivar is_bot: is the client a bot
        @type is_bot: bool

        @ivar is_mobile_device: is the client running on a mobile device
        @type is_mobile_device: bool

        @ivar is_msn_mobile: is the client an MSN Mobile device
        @type is_msn_mobile: bool

        @ivar is_msn_direct_device: is the client an MSN Direct device
        @type is_msn_direct_device: bool

        @ivar is_media_center_user: is the client running on a Media Center
        @type is_media_center_user: bool

        @ivar is_msn8_user: is the client using WLM 8
        @type is_msn8_user: bool

        @ivar is_web_client: is the client web based
        @type is_web_client: bool

        @ivar is_tgw_client: is the client a gateway
        @type is_tgw_client: bool

        @ivar has_space: does the user has a space account
        @type has_space: bool

        @ivar has_webcam: does the user has a webcam plugged in
        @type has_webcam: bool

        @ivar has_onecare: does the user has the OneCare service
        @type has_onecare: bool

        @ivar renders_gif: can the client render gif (for ink)
        @type renders_gif: bool

        @ivar renders_isf: can the client render ISF (for ink)
        @type renders_isf: bool

        @ivar supports_chunking: does the client supports chunking messages
        @type supports_chunking: bool

        @ivar supports_direct_im: does the client supports direct IM
        @type supports_direct_im: bool

        @ivar supports_winks: does the client supports Winks
        @type supports_winks: bool

        @ivar supports_shared_search: does the client supports Shared Search
        @type supports_shared_search: bool

        @ivar supports_voice_im: does the client supports voice clips
        @type supports_voice_im: bool

        @ivar supports_secure_channel: does the client supports secure channels
        @type supports_secure_channel: bool

        @ivar supports_sip_invite: does the client supports SIP
        @type supports_sip_invite: bool

        @ivar supports_shared_drive: does the client supports File sharing
        @type supports_shared_drive: bool

        @ivar p2p_supports_turn: does the client supports TURN for p2p transfer
        @type p2p_supports_turn: bool

        @ivar p2p_bootstrap_via_uun: is the client able to use and understand UUN commands
        @type p2p_bootstrap_via_uun: bool

        @undocumented: __getattr__, __setattr__, __str__
        """

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
        """Initializer

            @param msnc: The MSNC version
            @type msnc: integer < 8 and >= 0

            @param client_id: the full client ID"""
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
                object.__setattr__(self, 'client_id', self.client_id | mask)
            else:
                object.__setattr__(self, 'client_id', self.client_id ^ mask)
        else:
            raise AttributeError("object 'ClientCapabilities' has no attribute '%s'" % name)

    def __str__(self):
        return str(self.client_id)


class NetworkID(object):
    """Refers to the contact Network ID"""

    MSN = 1
    """Microsoft Network"""

    LCS = 2
    """Microsoft Live Communication Server"""

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
    """User privacy, defines the default policy concerning contacts not
    belonging to the ALLOW list nor to the BLOCK list.

        @cvar ALLOW: allow by default
        @cvar BLOCK: block by default"""
    ALLOW = 'AL'
    BLOCK = 'BL'


class Membership(object):
    """Contact Membership"""

    NONE = 0
    """Contact doesn't belong to the contact list, but belongs to the address book"""

    FORWARD = 1
    """Contact belongs to our contact list"""

    ALLOW   = 2
    """Contact is explicitely allowed to see our presence regardless of the
    currently set L{Privacy<pymsn.profile.Privacy>}"""

    BLOCK   = 4
    """Contact is explicitely forbidden from seeing our presence regardless of
    the currently set L{Privacy<pymsn.profile.Privacy>}"""

    REVERSE = 8
    """We belong to the FORWARD list of the contact"""

    PENDING = 16
    """Contact pending"""


class ContactType(object):
    """Automatic update status flag"""

    ME = "Me"
    """Contact is the user so there's no automatic update relationship"""

    EXTERNAL = "Messenger2"
    """Contact is part of an external messenger service so there's no automatic
    update relationship with the user"""

    REGULAR = "Regular"
    """Contact has no automatic update relationship with the user"""

    LIVE = "Live"
    """Contact has an automatic update relationship with the user and an 
    automatic update already occured"""

    LIVE_PENDING = "LivePending"
    """Contact was requested automatic update from the user and didn't
    give its authorization yet"""

    LIVE_REJECTED = "LiveRejected"
    """Contact was requested automatic update from the user and rejected
    the request"""

    LIVE_DROPPED = "LiveDropped"
    """Contact had an automatic update relationship with the user but
    the contact dropped it"""


class Profile(gobject.GObject):
    """Profile of the User connecting to the service

        @undocumented: __gsignals__, __gproperties__, do_get_property"""

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

            "msn-object": (gobject.TYPE_STRING,
                "MSN Object",
                "MSN Object attached to the user, this generally represent "
                "its display picture",
                "",
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
        #self.client_id.supports_sip_invite = True
        #FIXME: this should only be advertised when a webcam is plugged
        #self.client_id.has_webcam = True

        self._msn_object = None

        self.__pending_set_presence = [self._presence, self.client_id, self._msn_object]
        self.__pending_set_personal_message = [self._personal_message, self._current_media]

    @property
    def account(self):
        """The user account
            @type: utf-8 encoded string"""
        return self._account

    @property
    def password(self):
        """The user password
            @type: utf-8 encoded string"""
        return self._password

    @property
    def profile(self):
        """The user profile retrieved from the MSN servers
            @type: utf-8 encoded string"""
        return self._profile

    @property
    def id(self):
        """The user identifier in a GUID form
            @type: GUID string"""
        return "00000000-0000-0000-0000-000000000000"

    @rw_property
    def display_name():
        """The display name shown to you contacts
            @type: utf-8 encoded string"""
        def fset(self, display_name):
            if not display_name:
                return
            self._ns_client.set_display_name(display_name)
        def fget(self):
            return self._display_name
        return locals()

    @rw_property
    def presence():
        """The presence displayed to you contacts
            @type: L{Presence<pymsn.profile.Presence>}"""
        def fset(self, presence):
            if presence == self._presence:
                return
            self.__pending_set_presence[0] = presence
            self._ns_client.set_presence(*self.__pending_set_presence)
        def fget(self):
            return self._presence
        return locals()

    @rw_property
    def privacy():
        """The default privacy, can be either Privacy.ALLOW or Privacy.BLOCK
            @type: L{Privacy<pymsn.profile.Privacy>}"""
        def fset(self, privacy):
            pass #FIXME: set the privacy setting
        def fget(self):
            return self._privacy
        return locals()

    @rw_property
    def personal_message():
        """The personal message displayed to you contacts
            @type: utf-8 encoded string"""
        def fset(self, personal_message):
            if personal_message == self._personal_message:
                return
            self.__pending_set_personal_message[0] = personal_message
            self._ns_client.set_personal_message(*self.__pending_set_personal_message)
        def fget(self):
            return self._personal_message
        return locals()

    @rw_property
    def current_media():
        """The current media displayed to you contacts
            @type: (artist: string, track: string)"""
        def fset(self, current_media):
            if current_media == self._current_media:
                return
            self.__pending_set_personal_message[1] = current_media
            self._ns_client.set_personal_message(*self.__pending_set_personal_message)
        def fget(self):
            return self._current_media
        return locals()

    @rw_property
    def msn_object():
        """The MSNObject attached to your contact, this MSNObject represents the
        display picture to be shown to your peers
            @type: L{MSNObject<pymsn.p2p.MSNObject>}"""
        def fset(self, msn_object):
            if msn_object == self._msn_object:
                return
            self.__pending_set_presence[2] = msn_object
            self._ns_client.set_presence(*self.__pending_set_presence)
        def fget(self):
            return self._msn_object
        return locals()

    @rw_property
    def presence_msn_object():
        def fset(self, args):
            presence, msn_object = args
            if presence == self._presence and msn_object == self._msn_object:
                return
            self.__pending_set_presence[0] = presence
            self.__pending_set_presence[2] = msn_object
            self._ns_client.set_presence(*self.__pending_set_presence)
        def fget(self):
            return self._presence, self._msn_object
        return locals()

    @rw_property
    def personal_message_current_media():
        def fset(self, args):
            personal_message, current_media = args
            if personal_message == self._personal_message and \
                    current_media == self._current_media:
                return
            self.__pending_set_personal_message[0] = personal_message
            self.__pending_set_personal_message[1] = current_media
            self._ns_client.set_personal_message(*self.__pending_set_personal_message)
        def fget(self):
            return self._personal_message, self._current_media
        return locals()

    def _server_property_changed(self, name, value):
        attr_name = "_" + name.lower().replace("-", "_")
        old_value = getattr(self, attr_name)
        if value != old_value:
            setattr(self, attr_name, value)
            self.notify(name)

    def do_get_property(self, pspec):
        name = pspec.name.lower().replace("-", "_")
        return getattr(self, name)
gobject.type_register(Profile)


class Contact(gobject.GObject):
    """Contact related information
        @undocumented: __gsignals__, __gproperties__, do_get_property"""

    __gsignals__ =  {
            "infos-changed": (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                (object,)),
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

            "infos": (gobject.TYPE_PYOBJECT,
                "Informations",
                "The contact informations",
                gobject.PARAM_READABLE),

            "contact-type": (gobject.TYPE_PYOBJECT,
                "Contact type",
                "The contact automatic update status flag",
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

    def __init__(self, id, network_id, account, display_name, cid=None,
            memberships=Membership.NONE, contact_type=ContactType.REGULAR):
        """Initializer"""
        gobject.GObject.__init__(self)
        self._id = id
        self._cid = cid or "00000000-0000-0000-0000-000000000000"
        self._network_id = network_id
        self._account = account

        self._display_name = display_name
        self._presence = Presence.OFFLINE
        self._personal_message = ""
        self._current_media = None
        self._groups = set()

        self._memberships = memberships
        self._contact_type = contact_type
        self._client_capabilities = ClientCapabilities()
        self._msn_object = None
        self._infos = {}
        self._attributes = {'icon_url' : None}

    def __repr__(self):
        def memberships_str():
            m = []
            memberships = self._memberships
            if memberships & Membership.FORWARD:
                m.append('FORWARD')
            if memberships & Membership.ALLOW:
                m.append('ALLOW')
            if memberships & Membership.BLOCK:
                m.append('BLOCK')
            if memberships & Membership.REVERSE:
                m.append('REVERSE')
            if memberships & Membership.PENDING:
                m.append('PENDING')
            return " | ".join(m)
        template = "<pymsn.Contact id='%s' network='%u' account='%s' memberships='%s'>"
        return template % (self._id, self._network_id, self._account, memberships_str())

    @property
    def id(self):
        """Contact identifier in a GUID form
            @type: GUID string"""
        return self._id

    @property
    def attributes(self):
        """Contact attributes
            @type: {key: string => value: string}"""
        return self._attributes.copy()

    @property
    def cid(self):
        """Contact ID
            @type: GUID string"""
        return self._cid

    @property
    def network_id(self):
        """Contact network ID
            @type: L{NetworkID<pymsn.profile.NetworkID>}"""
        return self._network_id

    @property
    def account(self):
        """Contact account
            @type: utf-8 encoded string"""
        return self._account
    
    @property
    def presence(self):
        """Contact presence
            @type: L{Presence<pymsn.profile.Presence>}"""
        return self._presence

    @property
    def display_name(self):
        """Contact display name
            @type: utf-8 encoded string"""
        return self._display_name

    @property
    def personal_message(self):
        """Contact personal message
            @type: utf-8 encoded string"""
        return self._personal_message

    @property
    def current_media(self):
        """Contact current media
            @type: (artist: string, track: string)"""
        return self._current_media

    @property
    def groups(self):
        """Contact list of groups
            @type: set(L{Group<pymsn.profile.Group>}...)"""
        return self._groups

    @property
    def infos(self):
        """Contact informations
            @type: {key: string => value: string}"""
        return self._infos

    @property
    def memberships(self):
        """Contact membership value
            @type: bitmask of L{Membership<pymsn.profile.Membership>}s"""
        return self._memberships

    @property
    def contact_type(self):
        """Contact automatic update status flag
            @type: L{ContactType<pymsn.profile.ContactType>}"""
        return self._contact_type

    @property
    def client_capabilities(self):
        """Contact client capabilities
            @type: L{ClientCapabilities}"""
        return self._client_capabilities
    
    @property
    def msn_object(self):
        """Contact MSN Object
            @type: L{MSNObject<pymsn.p2p.MSNObject>}"""
        return self._msn_object

    @property
    def domain(self):
        """Contact domain, which is basically the part after @ in the account
            @type: utf-8 encoded string"""
        result = self._account.split('@', 1)
        if len(result) > 1:
            return result[1]
        else:
            return ""

    ### membership management
    def is_member(self, memberships):
        """Determines if this contact belongs to the specified memberships
            @type memberships: bitmask of L{Membership<pymsn.profile.Membership>}s"""
        return (self.memberships & memberships) == memberships

    def _set_memberships(self, memberships):
        self._memberships = memberships
        self.notify("memberships")

    def _add_membership(self, membership):
        self._memberships |= membership
        self.notify("memberships")

    def _remove_membership(self, membership):
        """removes the given membership from the contact

            @param membership: the membership to remove
            @type membership: int L{Membership}"""
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

    def _server_attribute_changed(self, name, value):
        self._attributes[name] = value

    def _server_infos_changed(self, updated_infos):
        self._infos.update(updated_infos)
        self.emit("infos-changed", updated_infos)
        self.notify("infos")

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
    """Group
        @undocumented: __gsignals__, __gproperties__, do_get_property"""

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
        """Group identifier in a GUID form
            @type: GUID string"""
        return self._id

    @property
    def name(self):
        """Group name
            @type: utf-8 encoded string"""
        return self._name

    def _server_property_changed(self, name, value):
        attr_name = "_" + name.lower().replace("-", "_")
        old_value = getattr(self, attr_name)
        if value != old_value:
            setattr(self, attr_name, value)
            self.notify(name)

    def do_get_property(self, pspec):
        name = pspec.name.lower().replace("-", "_")
        return getattr(self, name)
gobject.type_register(Group)

