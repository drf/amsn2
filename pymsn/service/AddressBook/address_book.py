# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2007 Ali Sabil <ali.sabil@gmail.com>
# Copyright (C) 2007 Johann Prieur <johann.prieur@gmail.com>
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
from pymsn.service.AddressBook.constants import *
from pymsn.service.description.AB.constants import *

import gobject

__all__ = ['AddressBook', 'AddressBookState', 'PendingContact']

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
        return None

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

    def search_by(self, field, value):
        result = []
        for contact in self:
            if getattr(contact, field) == value:
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

class PendingContact(object):
    
    def __init__(self, account, network, display_name='', invite_message=''):
        self._account = account
        self._network = network
        self._display_name = display_name
        self._invite_message = invite_message

    @property
    def account(self):
        return self._account

    @property
    def network(self):
        return self._network
    
    @property
    def display_name(self):
        return self._display_name

    @property
    def invite_message(self):
        return self._invite_message

    def __eq__(self, pending_contact):
        return self._account == pending_contact.account & \
            self._network == pending_contact.network

    def __str__(self):
        return "%s (%s) %s %s" % (self.account, self.display_name, 
                                  self.network, self.invite_message)

class AddressBook(gobject.GObject):
    
    __gsignals__ = {
            "error" : (gobject.SIGNAL_RUN_FIRST,
                gobject.TYPE_NONE,
                (object,)),

            "new-pending-contact" : (gobject.SIGNAL_RUN_FIRST,
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
                   gobject.PARAM_READABLE),
        "pending-contacts" : (gobject.TYPE_PYOBJECT,
                              "Pending contacts",
                              "The pending contacts",
                              gobject.PARAM_READABLE)
        }

    def __init__(self, sso, proxies=None):
        """The address book object."""
        gobject.GObject.__init__(self)

        self._ab = ab.AB(sso, proxies)
        self._sharing = sharing.Sharing(sso, proxies)

        self.__state = AddressBookState.NOT_SYNCHRONIZED
        self.__pending_contacts = set()

        self.groups = {}
        self.contacts = AddressBookStorage()
        self._profile = None

    # Properties
    def __get_state(self):
        return self.__state
    def __set_state(self, state):
        self.__state = state
        self.notify("state")
    state = property(__get_state)
    _state = property(__get_state, __set_state)

    def __get_pending_contacts(self):
        return self.__pending_contacts
    def __set_pending_contacts(self, pending_contacts):
        self.__pending_contacts = pending_contacts
        self.notify("pending-contacts")
    pending_contacts = property(__get_pending_contacts)
    _pending_contacts = property(__get_pending_contacts, 
                                 __set_pending_contacts)

    @property
    def profile(self):
        return self._profile

    def sync(self):
        if self._state != AddressBookState.NOT_SYNCHRONIZED:
            return
        self._state = AddressBookState.SYNCHRONIZING
        
        initial_sync = scenario.InitialSyncScenario(self._ab, self._sharing,
                (self.__initial_sync_callback,),
                (self.__common_errback,))
        initial_sync()

    # Public API
    def accept_contact_invitation(self, pending_contact, add_to_contact_list=True):
        self._pending_contacts.discard(pending_contact)
        ai = scenario.AcceptInviteScenario(self._ab, self._sharing,
                 (self.__accept_contact_invitation_cb),
                 (self.__common_errback,),
                 add_to_contact_list)
        ai.account = pending_contact.account
        ai.network = pending_contact.network
        ai()

    def decline_contact_invitation(self, pending_contact):
        self._pending_contacts.discard(pending_contact)
        di = scenario.DeclineInviteScenario(self._ab, self._sharing,
                 (self.__decline_contact_invitation_cb),
                 (self.__common_errback,))
        di.account = pending_contact.account
        di.network = pending_contact.network
        di()

    def add_messenger_contact(self, account):
        am = scenario.MessengerContactAddScenario(self._ab,
                (self.__add_messenger_contact_cb,),
                (self.__common_errback,))
        am.account = account
        am()
        if account.split("@", 1)[1].startswith("yahoo"):
            accounts = self.contacts.search_by_account(account)
            for contact in accounts:
                if contact.network_id == profile.NetworkID.EXTERNAL:
                    return            

            ae = scenario.ExternalContactAddScenario(self._ab,
                    (self.__add_messenger_contact_cb,),
                    (self.__common_errback,))
            ae.account = account
            ae()

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
        dc = scenario.ContactDeleteScenario(self._ab,
                (self.__delete_contact_cb, contact),
                (self.__common_errback,))
        dc.contact_guid = contact.id
        dc()

    def block_contact(self, contact):
        bc = scenario.BlockContactScenario(self._sharing,
                (self.__common_callback, 'contact-blocked', contact),
                (self.__common_errback,))
        bc.account = contact.account
        bc.network = contact.network_id
        bc()

    def unblock_contact(self, contact):
        uc = scenario.UnblockContactScenario(self._sharing,
                (self.__common_callback, 'contact-unblocked', contact),
                (self.__common_errback,))
        uc.account = contact.account
        uc.network = contact.network_id
        uc()

    def add_group(self, group_name):
        ag = scenario.GroupAddScenario(self._ab,
                (self.__add_group_cb, group_name),
                (self.__common_errback,))
        ag.group_name = group_name
        ag()

    def delete_group(self, group):
        dg = scenario.GroupDeleteScenario(self._ab,
                (self.__delete_group_cb, group),
                (self.__common_errback,))
        dg.group_guid = group.id
        dg()

    def rename_group(self, group, new_name):
        rg = scenario.GroupRenameScenario(self._ab,
                (self.__rename_group_cb, group, new_name),
                (self.__common_errback,))
        rg.group_guid = group.id
        rg.group_name = new_name
        rg()

    def add_contact_to_group(self, group, contact):
        ac = scenario.GroupContactAddScenario(self._ab,
                (self.__add_contact_to_group_cb, group, contact),
                (self.__common_errback,))
        ac.group_guid = group.id
        ac.contact_guid = contact.id
        ac()

    def delete_contact_from_group(self, group, contact):
        dc = scenario.GroupContactDeleteScenario(self._ab,
                (self.__delete_contact_from_group_cb, group, contact),
                (self.__common_errback,))
        dc.group_guid = group.id
        dc.contact_guid = contact.id
        dc()
    # End of public API

    def _check_pending_invitations(self):
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

        if not contact.IsMessengerUser and external_email is not None:
            display_name = \
                contact.Annotations.get(ContactAnnotations.NICKNAME,
                                        contact.DisplayName)
            if display_name == "":
                display_name = external_email.Email

            c = profile.Contact(contact.Id,
                                profile.NetworkID.EXTERNAL,
                                external_email.Email.encode("utf-8"),
                                display_name.encode("utf-8"),
                                contact.CID,
                                profile.Membership.FORWARD)
                
            for group_id in contact.Groups:
                c._add_group_ownership(self.groups[group_id])
            
            return c

        elif (not contact.IsMessengerUser and contact.Type != "Me") or \
                contact.PassportName == "":
            # FIXME : mobile phone and mail contacts here
            return None
        else:
            display_name = contact.DisplayName
            if display_name == "":
                display_name = contact.QuickName
            if display_name == "":
                display_name = contact.PassportName

            c = profile.Contact(contact.Id,
                                profile.NetworkID.MSN,
                                contact.PassportName.encode("utf-8"),
                                display_name.encode("utf-8"),
                                contact.CID,
                                profile.Membership.FORWARD)
            c._server_contact_attribute_changed("im_contact",
                                                contact.IsMessengerUser)
            
            for group_id in contact.Groups:
                c._add_group_ownership(self.groups[group_id])
                
            return c
        return None
            
    def __update_memberships(self, memberships):
        for member in memberships:
            if isinstance(member, sharing.PassportMember):
                network = profile.NetworkID.MSN
            elif isinstance(member, sharing.EmailMember):
                network = profile.NetworkID.EXTERNAL
            else:
                continue

            contact = self.contacts.search_by_account(member.Account).\
                search_by_network_id(network)[0]
            
            if contact is None:
                if 'Pending' in member.Roles:
                    # Pending contact
                    msg = member.Annotations.get('MSN.IM.InviteMessage', '')
                    p = PendingContact(member.Account.encode("utf-8"), network,
                                       member.DisplayName.encode("utf-8"), 
                                       msg.encode("utf-8"))
                    self._pending_contacts.add(p)
                    self.emit("new-pending-contact", p)
            else:
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

    # Callbacks
    def __initial_sync_callback(self, address_book, memberships):
        ab = address_book.ab
        contacts = address_book.contacts
        groups = address_book.groups

        for group in groups:
            self.groups[group.Id] = profile.Group(group.Id, group.Name)

        for contact in contacts:
            c = self.__build_contact(contact)
        
            if c is None:
                continue

            if contact.Type == "Me":
                self._profile = c
            else:
                self.contacts.add(c)

        self.__update_memberships(memberships)
        self._state = AddressBookState.SYNCHRONIZED

    def __accept_contact_invitation_cb(self, contact_guid, address_book_delta):
        self.__add_messenger_contact_cb(self, contact_guid, address_book_delta)

    def __decline_contact_invitation_cb(self):
        pass

    def __add_messenger_contact_cb(self, contact_guid, address_book_delta):
        contacts = address_book_delta.contacts
        for contact in contacts:
            if contact.Id != contact_guid:
                continue

            c = self.__build_contact(contact)
            if c is None:
                continue
            
            self.contacts.add(c)
            self.emit('messenger-contact-added', c)

    def __delete_contact_cb(self, contact):
        self.contacts.discard(contact)
        self.emit('contact-deleted', contact)

    def __add_group_cb(self, group_id, group_name):
        group = profile.Group(group_id, group_name)
        self.groups[group_id] = group
        self.emit('group-added', group)

    def __delete_group_cb(self, group):
        for contact in self.contacts:
            contact._delete_group_ownership(group)
        del self.groups[group.id]
        self.emit('group-deleted', group)

    def __rename_group_cb(self, group, group_name):
        group._name = group_name
        self.emit('group-renamed', group)

    def __add_contact_to_group_cb(self, group, contact):
        contact._add_group_ownership(group)
        self.emit('group-contact-added', group, contact)

    def __delete_contact_from_group_cb(self, group, contact):
        contact._delete_group_ownership(group)
        self.emit('group-contact-deleted', group, contact)

    def __common_callback(self, signal, *args):
        self.emit(signal, *args)

    def __common_errback(self, error_code, *args):
        self.emit('error', error_code)

gobject.type_register(AddressBook)

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

if __name__ == '__main__':
    import sys
    import getpass
    import signal
    import gobject
    import logging
    from pymsn.service.SingleSignOn import *

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
            for guid, group in address_book.groups.iteritems():
                print "Group : %s (%s)" % (guid, group.name)

            for contact in address_book.contacts:
                print "Contact : %s (%s) %s" % \
                    (contact.account, 
                     contact.display_name, 
                     contact.network_id)

            for pending in address_book.pending_contacts:
                print "Pending contact : %s" % pending

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
            #address_book.unblock_contact(address_book.contacts[0])
            #address_book.block_contact(address_book.contacts[0])
            #contact = address_book.contacts[2]
            #address_book.delete_contact(contact)
            #address_book.delete_contact(contact)
            #address_book.add_messenger_contact("tryggve2@gmail.com")

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
