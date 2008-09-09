# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2007 Ali Sabil <ali.sabil@gmail.com>
# Copyright (C) 2007-2008 Johann Prieur <johann.prieur@gmail.com>
# Copyright (C) 2007 Ole André Vadla Ravnås <oleavr@gmail.com>
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

import ab
import sharing
import scenario

import pymsn
import pymsn.profile as profile
from pymsn.profile import NetworkID
from pymsn.util.decorator import rw_property
from pymsn.profile import ContactType
from pymsn.service.AddressBook.constants import *
from pymsn.service.description.AB.constants import *
from pymsn.service.AddressBook.scenario.contacts import *

import gobject

__all__ = ['AddressBook', 'AddressBookState']

class AddressBookStorage(set):
    def __init__(self, initial_set=()):
        set.__init__(self, initial_set)

    def __repr__(self):
        return "AddressBook : %d contact(s)" % len(self)

    def __getitem__(self, key):
        i = 0
        for contact in self:
            if i == key:
                return contact
            i += 1
        raise IndexError("Index out of range")

    def __getattr__(self, name):
        if name.startswith("search_by_"):
            field = name[10:]
            def search_by_func(criteria):
                return self.search_by(field, criteria)
            search_by_func.__name__ = name
            return search_by_func
        elif name.startswith("group_by_"):
            field = name[9:]
            def group_by_func():
                return self.group_by(field)
            group_by_func.__name__ = name
            return group_by_func
        else:
            raise AttributeError, name
        
    def search_by_memberships(self, memberships):
        result = []
        for contact in self:
            if contact.is_member(memberships):
                result.append(contact)
                # Do not break here, as the account
                # might exist in multiple networks
        return AddressBookStorage(result)

    def search_by_groups(self, *groups):
        result = []
        groups = set(groups)
        for contact in self:
            if groups <= contact.groups:
                result.append(contact)
        return AddressBookStorage(result)

    def group_by_group(self):
        result = {}
        for contact in self:
            groups = contact.groups
            for group in groups:
                if group not in result:
                    result[group] = set()
                result[group].add(contact)
        return result

    def search_by_predicate(self, predicate):
        result = []
        for contact in self:
            if predicate(contact):
                result.append(contact)
        return AddressBookStorage(result)

    def search_by(self, field, value):
        result = []
        if isinstance(value, basestring):
            value = value.lower()
        for contact in self:
            contact_field_value = getattr(contact, field)
            if isinstance(contact_field_value, basestring):
                contact_field_value = contact_field_value.lower()
            if contact_field_value == value:
                result.append(contact)
                # Do not break here, as the account
                # might exist in multiple networks
        return AddressBookStorage(result)

    def group_by(self, field):
        result = {}
        for contact in self:
            value = getattr(contact, field)
            if value not in result:
                result[value] = AddressBookStorage()
            result[value].add(contact)
        return result


class AddressBook(gobject.GObject):

    __gsignals__ = {
            "error" : (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                (object,)),

            "messenger-contact-added" : (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                (object,)),
#             "email-contact-added"     : (gobject.SIGNAL_RUN_FIRST,
#                 gobject.TYPE_NONE,
#                 (object,)),
#             "mobile-contact-added"    : (gobject.SIGNAL_RUN_FIRST,
#                 gobject.TYPE_NONE,
#                 (object,)),

            "contact-deleted"         : (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                 (object,)),

            # FIXME: those signals will be removed in the future and will be
            # moved to profile.Contact
            "contact-accepted"         : (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                (object,)),
            "contact-rejected"       : (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                (object,)),
            "contact-blocked"         : (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                (object,)),
            "contact-unblocked"       : (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                (object,)),

            "group-added"             : (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                (object,)),
            "group-deleted"           : (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                (object,)),
            "group-renamed"           : (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                (object,)),

            "group-contact-added"     : (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                (object, object)),
            "group-contact-deleted"   : (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                (object, object))
            }

    __gproperties__ = {
        "state":  (gobject.TYPE_INT,
                   "State",
                   "The state of the addressbook.",
                   0, 2, AddressBookState.NOT_SYNCHRONIZED,
                   gobject.PARAM_READABLE)
        }

    def __init__(self, sso, proxies=None):
        """The address book object."""
        gobject.GObject.__init__(self)

        self._ab = ab.AB(sso, proxies)
        self._sharing = sharing.Sharing(sso, proxies)

        self.__state = AddressBookState.NOT_SYNCHRONIZED

        self.groups = set()
        self.contacts = AddressBookStorage()
        self._profile = None

    # Properties
    @property
    def state(self):
        return self.__state

    @rw_property
    def _state():
        def fget(self):
            return self.__state
        def fset(self, state):
            self.__state = state
            self.notify("state")
        return locals()

    @property
    def profile(self):
        return self._profile

    def sync(self):
        if self._state != AddressBookState.NOT_SYNCHRONIZED:
            return
        self._state = AddressBookState.SYNCHRONIZING

        def callback(address_book, memberships):
            ab = address_book.ab
            contacts = address_book.contacts
            groups = address_book.groups
            for group in groups:
                g = profile.Group(group.Id, group.Name.encode("utf-8"))
                self.groups.add(g)
            for contact in contacts:
                c = self.__build_contact(contact)
                if c is None:
                    continue
                if contact.Type == ContactType.ME:
                    self._profile = c
                else:
                    self.contacts.add(c)
            self.__update_memberships(memberships)
            self._state = AddressBookState.SYNCHRONIZED

        initial_sync = scenario.InitialSyncScenario(self._ab, self._sharing,
                (callback,),
                (self.__common_errback,))
        initial_sync()

    # Public API
    def accept_contact_invitation(self, pending_contact, add_to_contact_list=True):
        def callback(contact_infos, memberships):
            pending_contact.freeze_notify()
            pending_contact._id = contact_infos.Id
            pending_contact._cid = contact_infos.CID
            pending_contact._set_memberships(memberships)
            pending_contact.thaw_notify()
            self.emit('contact-accepted', pending_contact)
        ai = scenario.AcceptInviteScenario(self._ab, self._sharing,
                 (callback,),
                 (self.__common_errback,))
        ai.account = pending_contact.account
        ai.network = pending_contact.network_id
        ai.memberships = pending_contact.memberships
        ai.add_to_contact_list = add_to_contact_list
        ai()

    def decline_contact_invitation(self, pending_contact, block=True):
        def callback(memberships):
            pending_contact._set_memberships(memberships)
            self.emit('contact-rejected', pending_contact)
        di = scenario.DeclineInviteScenario(self._sharing,
                 (callback,),
                 (self.__common_errback,))
        di.account = pending_contact.account
        di.network = pending_contact.network_id
        di.memberships = pending_contact.memberships
        di.block = block
        di()

    def add_messenger_contact(self, account, invite_display_name='', 
            invite_message='', groups=[], network_id=NetworkID.MSN):
        def callback(contact_guid, address_book_delta):
            contacts = address_book_delta.contacts
            for contact in contacts:
                if contact.Id != contact_guid:
                    continue
                try:
                    c = self.contacts.search_by_account(contact.PassportName).\
                            search_by_network_id(NetworkID.MSN)[0]
                    c.freeze_notify()
                    c._id = contact.Id
                    c._cid = contact.CID
                    c._display_name = contact.DisplayName
                    for group in self.groups:
                        if group.id in contact.Groups:
                            c._add_group_ownership(group)
                    c._add_membership(profile.Membership.FORWARD)
                    c._add_membership(profile.Membership.ALLOW)

                    annotations = contact.Annotations
                    for key in annotations:
                        annotations[key] = annotations[key].encode("utf-8")
                    contact_infos = {ContactGeneral.ANNOTATIONS : annotations}

                    c._server_infos_changed(contact_infos)
                    c.thaw_notify()
                    self.unblock_contact(c)
                except IndexError:
                    c = self.__build_contact(contact)
                    if c.is_member(profile.Membership.FORWARD):
                        c._add_membership(profile.Membership.ALLOW)
                    if c is None:
                        continue
                    self.contacts.add(c)
                    self.emit('messenger-contact-added', c)
                    self.unblock_contact(c)
                for group in groups:
                    self.add_contact_to_group(group, c)

        try:
            contact = self.contacts.search_by_account(account).\
                search_by_network_id(NetworkID.MSN)[0]
            if not contact.is_member(profile.Membership.FORWARD) and \
                    contact.id != "00000000-0000-0000-0000-000000000000":
                self.__upgrade_mail_contact(contact, groups)
            elif contact.id == "00000000-0000-0000-0000-000000000000":
                raise IndexError
            else:
                return
        except IndexError:
            if network_id == NetworkID.MSN:
                scenario_class = MessengerContactAddScenario
            elif network_id == NetworkID.EXTERNAL:
                scenario_class = ExternalContactAddScenario
            s = scenario_class(self._ab, (callback,), (self.__common_errback,))
            s.account = account
            s.invite_display_name = invite_display_name
            s.invite_message = invite_message
            s()

    def __upgrade_mail_contact(self, contact, groups=[]):
        def callback():
            contact._add_memberships(profile.Membership.ALLOW)
            for group in groups:
                self.add_contact_to_group(group, contact)

        up = scenario.ContactUpdatePropertiesScenario(self._ab,
                (callback,), (self.__common_errback,))
        up.contact_guid = contact.id
        up.contact_properties = { 'is_messenger_user' : True }
        up.enable_allow_list_management = True
        up()

#     def add_email_contact(self, email_address):
#         ae = scenario.EmailContactAddScenario(self._ab,
#                 (self.__add_email_contact_cb,),
#                 (self.__common_errback,))
#         ae.email_address = email_address
#         ae()

#     def add_mobile_contact(self, phone_number):
#         am = scenario.MobileContactAddScenario(self._ab,
#                 (self.__add_mobile_contact_cb,),
#                 (self.__common_errback,))
#         am.phone_number = phone_number
#         am()

    def delete_contact(self, contact):
        def callback():
            self.contacts.discard(contact)
            self.emit('contact-deleted', contact)
        dc = scenario.ContactDeleteScenario(self._ab,
                (callback,),
                (self.__common_errback,))
        dc.contact_guid = contact.id
        dc()

    def update_contact_infos(self, contact, infos):
        def callback():
            contact._server_infos_changed(infos)
        up = scenario.ContactUpdatePropertiesScenario(self._ab,
                (callback,),
                (self.__common_errback,))
        up.contact_guid = contact.id
        up.contact_properties = infos
        up()

    def block_contact(self, contact):
        def callback(memberships):
            contact._set_memberships(memberships)
            self.emit('contact-blocked', contact)
        bc = scenario.BlockContactScenario(self._sharing,
                (callback,),
                (self.__common_errback,))
        bc.account = contact.account
        bc.network = contact.network_id
        bc.membership = contact.memberships
        bc()

    def unblock_contact(self, contact):
        def callback(memberships):
            contact._set_memberships(memberships)
            self.emit('contact-unblocked', contact)
        uc = scenario.UnblockContactScenario(self._sharing,
                (callback,),
                (self.__common_errback,))
        uc.account = contact.account
        uc.network = contact.network_id
        uc.membership = contact.memberships
        uc()

    def add_group(self, group_name):
        def callback(group_id):
            group = profile.Group(group_id, group_name)
            self.groups.add(group)
            self.emit('group-added', group)
        ag = scenario.GroupAddScenario(self._ab,
                (callback,),
                (self.__common_errback,))
        ag.group_name = group_name
        ag()

    def delete_group(self, group):
        def callback():
            for contact in self.contacts:
                contact._delete_group_ownership(group)
            self.groups.discard(group)
            self.emit('group-deleted', group)
        dg = scenario.GroupDeleteScenario(self._ab,
                (callback,),
                (self.__common_errback,))
        dg.group_guid = group.id
        dg()

    def rename_group(self, group, new_name):
        def callback():
            group._name = group_name
            self.emit('group-renamed', group)
        rg = scenario.GroupRenameScenario(self._ab,
                (callback,),
                (self.__common_errback,))
        rg.group_guid = group.id
        rg.group_name = new_name
        rg()

    def add_contact_to_group(self, group, contact):
        def callback():
            contact._add_group_ownership(group)
            self.emit('group-contact-added', group, contact)
        ac = scenario.GroupContactAddScenario(self._ab,
                (callback,),
                (self.__common_errback,))
        ac.group_guid = group.id
        ac.contact_guid = contact.id
        ac()

    def delete_contact_from_group(self, group, contact):
        def callback():
            contact._delete_group_ownership(group)
            self.emit('group-contact-deleted', group, contact)
        dc = scenario.GroupContactDeleteScenario(self._ab,
                (callback,),
                (self.__common_errback,))
        dc.group_guid = group.id
        dc.contact_guid = contact.id
        dc()
    # End of public API

    def check_pending_invitations(self):
        cp = scenario.CheckPendingInviteScenario(self._sharing,
                 (self.__update_memberships,),
                 (self.__common_errback,))
        cp()

    def __build_contact(self, contact):
        external_email = None
        for email in contact.Emails:
            if email.Type == ContactEmailType.EXTERNAL:
                external_email = email
                break

        if (not contact.IsMessengerUser) and (external_email is not None):
            display_name = contact.DisplayName
            if display_name == "":
                display_name = external_email.Email

            annotations = contact.Annotations
            for key in annotations:
                annotations[key] = annotations[key].encode("utf-8")
            contact_infos = { ContactGeneral.ANNOTATIONS : annotations }

            if contact.IsMessengerUser:
                memberships = profile.Membership.FORWARD
            else:
                memberships = profile.Membership.NONE
            c = profile.Contact(contact.Id,
                    NetworkID.EXTERNAL,
                    external_email.Email.encode("utf-8"),
                    display_name.encode("utf-8"),
                    contact.CID,
                    memberships,
                    contact.Type)
            c._server_infos_changed(contact_infos)

            for group in self.groups:
                if group.id in contact.Groups:
                    c._add_group_ownership(group)

            return c

        elif contact.PassportName == "":
            # FIXME : mobile phone and mail contacts here
            return None
        else:
            display_name = contact.DisplayName
            if display_name == "":
                display_name = contact.QuickName
            if display_name == "":
                display_name = contact.PassportName

            annotations = contact.Annotations
            for key in annotations:
                annotations[key] = annotations[key].encode("utf-8")
            contact_infos = {ContactGeneral.ANNOTATIONS : annotations}

            if contact.IsMessengerUser:
                memberships = profile.Membership.FORWARD
            else:
                memberships = profile.Membership.NONE
            c = profile.Contact(contact.Id,
                    NetworkID.MSN,
                    contact.PassportName.encode("utf-8"),
                    display_name.encode("utf-8"),
                    contact.CID,
                    memberships)
            c._server_infos_changed(contact_infos)

            for group in self.groups:
                if group.id in contact.Groups:
                    c._add_group_ownership(group)

            return c
        return None

    def __update_memberships(self, memberships):
        for member in memberships:
            if isinstance(member, sharing.PassportMember):
                network = NetworkID.MSN
            elif isinstance(member, sharing.EmailMember):
                network = NetworkID.EXTERNAL
            else:
                continue

            try:
                contact = self.contacts.search_by_account(member.Account).\
                    search_by_network_id(network)[0]
            except IndexError:
                contact = None

            new_contact = False
            if contact is None:
                new_contact = True
                try:
                    cid = member.CID
                except AttributeError:
                    cid = None
                msg = member.Annotations.get('MSN.IM.InviteMessage', u'')
                c = profile.Contact("00000000-0000-0000-0000-000000000000",
                        network,
                        member.Account.encode("utf-8"),
                        member.DisplayName.encode("utf-8"),
                        cid)
                c._server_attribute_changed('invite_message', msg.encode("utf-8"))
                self.contacts.add(c)
                contact = c

            for role in member.Roles:
                if role == "Allow":
                    membership = profile.Membership.ALLOW
                elif role == "Block":
                    membership = profile.Membership.BLOCK
                elif role == "Reverse":
                    membership = profile.Membership.REVERSE
                elif role == "Pending":
                    membership = profile.Membership.PENDING
                else:
                    raise NotImplementedError("Unknown Membership Type : " + membership)
                contact._add_membership(membership)

            if new_contact and self.state == AddressBookState.SYNCHRONIZED:
                self.emit('messenger-contact-added', contact)

    # Callbacks
    def __common_errback(self, error_code, *args):
        self.emit('error', error_code)

gobject.type_register(AddressBook)

if __name__ == '__main__':
    def get_proxies():
        import urllib
        proxies = urllib.getproxies()
        result = {}
        if 'https' not in proxies and \
                'http' in proxies:
            url = proxies['http'].replace("http://", "https://")
            result['https'] = pymsn.Proxy(url)
        for type, url in proxies.items():
            if type == 'no': continue
            if type == 'https' and url.startswith('http://'):
                url = url.replace('http://', 'https://', 1)
            result[type] = pymsn.Proxy(url)
        return result

    import sys
    import getpass
    import signal
    import gobject
    import logging
    from pymsn.service.SingleSignOn import *
    from pymsn.service.description.AB.constants import ContactGeneral

    logging.basicConfig(level=logging.DEBUG)

    if len(sys.argv) < 2:
        account = raw_input('Account: ')
    else:
        account = sys.argv[1]

    if len(sys.argv) < 3:
        password = getpass.getpass('Password: ')
    else:
        password = sys.argv[2]

    mainloop = gobject.MainLoop(is_running=True)
    
    signal.signal(signal.SIGTERM,
            lambda *args: gobject.idle_add(mainloop.quit()))
    
    def address_book_state_changed(address_book, pspec):
        if address_book.state == AddressBookState.SYNCHRONIZED:
            for group in address_book.groups:
                print "Group : %s " % group.name

            for contact in address_book.contacts:
                print "Contact : %s (%s) %s" % \
                    (contact.account, 
                     contact.display_name, 
                     contact.network_id)

            print address_book.contacts[0].account
            address_book.update_contact_infos(address_book.contacts[0], {ContactGeneral.FIRST_NAME : "lolibouep"})

            #address_book._check_pending_invitations()
            #address_book.accept_contact_invitation(address_book.pending_contacts.pop())
            #print address_book.pending_contacts.pop()
            #address_book.accept_contact_invitation(address_book.pending_contacts.pop())
            #address_book.add_group("ouch2")
            #address_book.add_group("callback test6")
            #group = address_book.groups.values()[0]
            #address_book.delete_group(group)
            #address_book.delete_group(group)
            #address_book.rename_group(address_book.groups.values()[0], "ouch")
            #address_book.add_contact_to_group(address_book.groups.values()[1],
            #                                  address_book.contacts[0])
            #contact = address_book.contacts[0]
            #address_book.delete_contact_from_group(address_book.groups.values()[0],
            #                                       contact)
            #address_book.delete_contact_from_group(address_book.groups.values()[0],
            #                                       contact)
            #address_book.block_contact(address_book.contacts.search_by_account('pymsn.rewrite@yahoo.com')[0])
            #address_book.block_contact(address_book.contacts.search_by_account('pymsn.rewrite@yahoo.com')[0])
            #address_book.unblock_contact(address_book.contacts[0])
            #address_book.block_contact(address_book.contacts[0])
            #contact = address_book.contacts[2]
            #address_book.delete_contact(contact)
            #address_book.delete_contact(contact)
            #g=list(address_book.groups)
            #address_book.add_messenger_contact("wikipedia-bot@hotmail.com",groups=g)

            #for i in range(5):
            #    address_book.delete_contact(address_book.contacts[i])
            #address_book.add_messenger_contact("johanssn.prieur@gmail.com")

    def messenger_contact_added(address_book, contact):
        print "Added contact : %s (%s) %s %s" % (contact.account, 
                                                 contact.display_name, 
                                                 contact.network_id,
                                                 contact.memberships)

    sso = SingleSignOn(account, password, proxies=get_proxies())
    address_book = AddressBook(sso, proxies=get_proxies())
    address_book.connect("notify::state", address_book_state_changed)
    address_book.connect("messenger-contact-added", messenger_contact_added)
    address_book.sync()

    while mainloop.is_running():
        try:
            mainloop.run()
        except KeyboardInterrupt:
            mainloop.quit()
