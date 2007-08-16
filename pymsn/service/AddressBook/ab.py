# -*- coding: utf-8 -*-
#
# pymsn - a python client library for Msn
#
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

from pymsn.service.SOAPService import SOAPService
from pymsn.util.ElementTree import XMLTYPE
from pymsn.service.SingleSignOn import *
from pymsn.service.AddressBook.common import *

__all__ = ['AB']

class ABResult(object):
    """ABFindAll Result object"""
    def __init__(self, ab, contacts, groups):
        self.ab = ab
        self.contacts = contacts
        self.groups = groups

class Group(object):
    def __init__(self, group):
        self.Id = group.findtext("./ab:groupId")

        group_info = group.find("./ab:groupInfo")

        self.Type = group_info.findtext("./ab:groupType")
        self.Name = group_info.findtext("./ab:name")
        self.IsNotMobileVisible = group_info.findtext("./ab:IsNotMobileVisible", "bool")
        self.IsPrivate = group_info.findtext("./ab:IsPrivate", "bool")

        self.Annotations = annotations_to_dict(group_info.find("./ab:Annotations"))
        
        self.PropertiesChanged = [] #FIXME: implement this
        self.Deleted = group.findtext("./ab:fDeleted", "bool")
        self.LastChanged = group.findtext("./ab:lastChange", "bool")

    def __hash__(self):
        return hash(self.Id)

    def __eq__(self, other):
        return self.Id == other.Id

    def __repr__(self):
        return "<Group id=%s>" % self.Id

class ContactEmail(object):
    def __init__(self, email):
        self.Type = email.findtext("./ab:contactEmailType")
        self.Email = email.findtext("./ab:email")
        self.IsMessengerEnabled = email.findtext("./ab:isMessengerEnabled", "bool")
        self.Capability = email.findtext("./ab:Capability", "int")
        self.MessengerEnabledExternally = email.findtext("./ab:MessengerEnabledExternally", "bool")

class ContactPhone(object):
    def __init__(self, phone):
        self.Type = phone.findtext("./ab:contactPhoneType")
        self.Number = phone.findtext("./ab:number")
        self.IsMessengerEnabled = phone.findtext("./ab:isMessengerEnabled", "bool")
        self.PropertiesChanged = phone.findtext("./ab:propertiesChanged").split(' ')

class ContactLocation(object):
    def __init__(self, location):
        self.Type = location.findtext("./ab:contactLocationType")
        self.Name = location.findtext("./ab:name")
        self.City = location.findtext("./ab:city")
        self.Country = location.findtext("./ab:country")
        self.PostalCode = location.findtext("./ab:postalcode")
        self.Changes = location.findtext("./ab:Changes").split(' ')

class Contact(object):
    def __init__(self, contact):
        self.Id = contact.findtext("./ab:contactId")

        contact_info = contact.find("./ab:contactInfo")

        self.Groups = []
        groups = contact_info.find("./ab:groupIds")
        if groups is not None:
            for group in groups:
                self.Groups.append(group.text)

        self.Type = contact_info.findtext("./ab:contactType")
        self.QuickName = contact_info.findtext("./ab:quickName")
        self.PassportName = contact_info.findtext("./ab:passportName")
        self.DisplayName = contact_info.findtext("./ab:displayName")
        self.IsPassportNameHidden = contact_info.findtext("./ab:IsPassportNameHidden", "bool")

        self.FirstName = contact_info.findtext("./ab:firstName")
        self.LastName = contact_info.findtext("./ab:lastName")

        self.PUID = contact_info.findtext("./ab:puid", "int")
        self.CID = contact_info.findtext("./ab:CID", "int")

        self.IsNotMobileVisible = contact_info.findtext("./ab:IsNotMobileVisible", "bool")
        self.IsMobileIMEnabled = contact_info.findtext("./ab:isMobileIMEnabled", "bool")
        self.IsMessengerUser = contact_info.findtext("./ab:isMessengerUser", "bool")
        self.IsFavorite = contact_info.findtext("./ab:isFavorite", "bool")
        self.IsSmtp = contact_info.findtext("./ab:isSmtp", "bool")
        self.HasSpace = contact_info.findtext("./ab:hasSpace", "bool")

        self.SpotWatchState = contact_info.findtext("./ab:spotWatchState")
        # HACK: handle pyxml iso8601 incompleteness
        #birthdate = contact_info.findtext("./ab:birthdate") + ".00+00:00"
        #self.Birthdate = XMLTYPE.datetime.decode()

        self.PrimaryEmailType = contact_info.findtext("./ab:primaryEmailType")
        self.PrimaryLocation = contact_info.findtext("./ab:PrimaryLocation")
        self.PrimaryPhone = contact_info.findtext("./ab:primaryPhone")

        self.IsPrivate = contact_info.findtext("./ab:IsPrivate", "bool")
        self.Gender = contact_info.findtext("./ab:Gender")
        self.TimeZone = contact_info.findtext("./ab:TimeZone")

        self.Annotations = annotations_to_dict(contact_info.find("./ab:annotations"))
        
        self.Emails = []
        emails = contact_info.find("./ab:emails") or []
        for contact_email in emails:
            self.Emails.append(ContactEmail(contact_email))

        self.PropertiesChanged = [] #FIXME: implement this
        self.Deleted = contact.findtext("./ab:fDeleted", "bool")
        self.LastChanged = contact.findtext("./ab:lastChanged", "datetime")

    @staticmethod
    def new(contact):
        contact_type = contact.findtext("./ab:contactInfo/ab:contactType")

        if contact_type == "Live":
            return LiveContact(contact)
        if contact_type == "LivePending":
            return LivePendingContact(contact)
        if contact_type == "LiveRejected":
            return LiveRejectedContact(contact)
        if contact_type == "LiveDropped":
            return LiveDroppedContact(contact)
        elif contact_type == "Me":
            return MeContact(contact)
        elif contact_type == "Regular":
            return RegularContact(contact)
        else:
            raise NotImplementedError("Contact Type not implemented : " + contact_type)

class LiveContact(Contact):
    pass

class LivePendingContact(LiveContact):
    pass

class LiveRejectedContact(LiveContact):
    pass

class LiveDroppedContact(LiveContact):
    pass

class MeContact(LiveContact):
    pass

class RegularContact(Contact):
    pass


class AB(SOAPService):
    def __init__(self, sso, proxies=None):
        self._sso = sso
        self._tokens = {}
        SOAPService.__init__(self, "AB", proxies)

        self._last_changes = "0001-01-01T00:00:00.0000000-08:00"
   
    @RequireSecurityTokens(LiveService.CONTACTS)
    def Add(self, callback, errback, scenario, account):
        """Creates the address book on the server.

            @param callback: tuple(callable, *args)
            @param errback: tuple(callable, *args)
            @param scenario: "Initial"
            @param account: the owner account"""
        self.__soap_request(self._service.ABAll, scenario, (account,),
                            callback, errback)

    def _HandleABAddResponse(self, callback, errback, response, user_data):
        return None

    @RequireSecurityTokens(LiveService.CONTACTS)
    def FindAll(self, callback, errback, scenario, deltas_only):
        """Requests the contact list.
            @param scenario: "Initial" | "ContactSave" ...
            @param deltas_only: True if the method should only check changes
                since last_change, otherwise False
            @param last_change: an ISO 8601 timestamp
                (previously sent by the server), or
                0001-01-01T00:00:00.0000000-08:00 to get the whole list
            @param callback: tuple(callable, *args)
            @param errback: tuple(callable, *args)"""            
        self.__soap_request(self._service.ABFindAll, scenario,
                (XMLTYPE.bool.encode(deltas_only), self._last_changes),
                callback, errback)

    def _HandleABFindAllResponse(self, callback, errback, response, user_data):
        last_changes = response[0].find("./ab:lastChange")
        if last_changes is not None:
            self._last_changes = last_changes.text

        groups = []
        contacts = []
        for group in response[1]:
            groups.append(Group(group))

        for contact in response[2]:
            contacts.append(Contact.new(contact))
        
        address_book =  ABResult(None, contacts, groups) #FIXME: add support for the ab param
        callback[0](address_book, *callback[1:])

    @RequireSecurityTokens(LiveService.CONTACTS)
    def ContactAdd(self, callback, errback, scenario,
            contact_info, invite_info):
        """Adds a contact to the contact list.

            @param scenario: "ContactSave" | "ContactMsgrAPI"
            @param contact_info: info dict concerning the new contact
            @param invite_info: info dict concerning the sent invite
            @param callback: tuple(callable, *args)
            @param errback: tuple(callable, *args)
        """
        is_messenger_user = contact_info.get('is_messenger_user', None)
        if is_messenger_user is not None:
            is_messenger_user = XMLTYPE.bool.encode(is_messenger_user)
        self.__soap_request(self._service.ABContactAdd, scenario,
                (contact_info.get('passport_name', None), 
                    is_messenger_user,
                    contact_info.get('contact_type', None),
                    contact_info.get('first_name', None),
                    contact_info.get('last_name', None),
                    contact_info.get('birth_date', None),
                    contact_info.get('email', None),
                    contact_info.get('phone', None),
                    contact_info.get('location', None),
                    contact_info.get('web_site', None),
                    contact_info.get('annotation', None),
                    contact_info.get('comment', None),
                    contact_info.get('anniversary', None),
                    invite_info.get('display_name', None),
                    invite_info.get('invite_message', None),
                    contact_info.get('capability', None)),
                callback, errback)

    def _HandleABContactAddResponse(self, callback, errback, response, user_data):
        callback[0](response.text, *callback[1:])

    @RequireSecurityTokens(LiveService.CONTACTS)
    def ContactDelete(self, callback, errback, scenario,
            contact_id):
        """Deletes a contact from the contact list.
        
            @param scenario: "Timer" | ...
            @param contact_id: the contact id (a GUID)
            @param callback: tuple(callable, *args)
            @param errback: tuple(callable, *args)
        """
        self.__soap_request(self._service.ABContactDelete, scenario,
                (contact_id,), callback, errback)
        
    def _HandleABContactDeleteResponse(self, callback, errback, response, user_data):
        callback[0](*callback[1:])

    @RequireSecurityTokens(LiveService.CONTACTS)
    def ContactUpdate(self, callback, errback,
            scenario, contact_id, contact_info):
        # TODO : maybe put contact_id in contact_info
        """Updates a contact informations.
        
            @param scenario: "ContactSave" | "Timer" | ...
            @param contact_id: the contact id (a GUID)
            @param contact_info: info dict
            @param callback: tuple(callable, *args)
            @param errback: tuple(callable, *args)
        """
        if 'is_messenger_user' in contact_info:
            contact_info['is_messenger_user'] = \
                    XMLTYPE.bool.encode(contact_info['is_messenger_user'])
        
        self.__soap_request(self._service.ABContactUpdate, scenario,
                (contact_id,
                    contact_info.get('display_name', None),
                    contact_info.get('is_messenger_user', None),
                    contact_info.get('contact_type', None),
                    contact_info.get('first_name', None),
                    contact_info.get('last_name', None),
                    contact_info.get('birth_date', None),
                    contact_info.get('email', None),
                    contact_info.get('phone', None),
                    contact_info.get('location', None),
                    contact_info.get('web_site', None),
                    contact_info.get('annotation', None),
                    contact_info.get('comment', None),
                    contact_info.get('anniversary', None),
                    contact_info.get('has_space', None)),
                callback, errback)

    def _HandleABContactUpdateResponse(self, callback, errback, response, user_data):
        callback[0](*callback[1:])
        
    @RequireSecurityTokens(LiveService.CONTACTS)
    def GroupAdd(self, callback, errback, scenario,
            group_name):
        """Adds a group to the address book.

            @param scenario: "GroupSave" | ...
            @param group_name: the name of the group
            @param callback: tuple(callable, *args)
            @param errback: tuple(callable, *args)
        """
        self.__soap_request(self._service.ABGroupAdd, scenario,
                (group_name,),
                callback, errback)

    def _HandleABGroupAddResponse(self, callback, errback, response, user_data):
        callback[0](response.text, *callback[1:])

    @RequireSecurityTokens(LiveService.CONTACTS)
    def GroupDelete(self, callback, errback, scenario,
            group_id):
        """Deletes a group from the address book.

            @param scenario: "Timer" | ...
            @param group_id: the id of the group (a GUID)
            @param callback: tuple(callable, *args)
            @param errback: tuple(callable, *args)
        """
        self.__soap_request(self._service.ABGroupDelete, scenario,
                (group_id,), callback, errback)

    def _HandleABGroupDeleteResponse(self, callback, errback, response, user_data):
        callback[0](*callback[1:])

    @RequireSecurityTokens(LiveService.CONTACTS)
    def GroupUpdate(self, callback, errback, scenario,
            group_id, group_name):
        """Updates a group name.

            @param scenario: "GroupSave" | ...
            @param group_id: the id of the group (a GUID)
            @param group_name: the new name for the group
            @param callback: tuple(callable, *args)
            @param errback: tuple(callable, *args)
        """
        self.__soap_request(self._service.ABGroupUpdate, scenario,
                (group_id, group_name), callback, errback)

    def _HandleABGroupUpdateResponse(self, callback, errback, response, user_data):
        callback[0](*callback[1:])

    @RequireSecurityTokens(LiveService.CONTACTS)
    def GroupContactAdd(self, callback, errback, scenario,
            group_id, contact_id):
        """Adds a contact to a group.

            @param scenario: "GroupSave" | ...
            @param group_id: the id of the group (a GUID)
            @param contact_id: the id of the contact to add to the
                               group (a GUID)
            @param callback: tuple(callable, *args)
            @param errback: tuple(callable, *args)
        """
        self.__soap_request(self._service.ABGroupContactAdd, scenario,
                (group_id, contact_id), callback, errback)

    def _HandleABGroupContactAddResponse(self, callback, errback, response, user_data):
        callback[0](*callback[1:])

    @RequireSecurityTokens(LiveService.CONTACTS)
    def GroupContactDelete(self, callback, errback, scenario,
            group_id, contact_id):
        """Deletes a contact from a group.

            @param scenario: "GroupSave" | ...
            @param group_id: the id of the group (a GUID)
            @param contact_id: the id of the contact to delete from the 
                               group (a GUID)
            @param callback: tuple(callable, *args)
            @param errback: tuple(callable, *args)
        """
        self.__soap_request(self._service.ABGroupContactDelete, scenario,
                (group_id, contact_id), callback, errback)

    def _HandleABGroupContactDeleteResponse(self, callback, errback, response, user_data):
        callback[0](*callback[1:])

    def __soap_request(self, method, scenario, args, callback, errback):
        token = str(self._tokens[LiveService.CONTACTS])

        http_headers = method.transport_headers()
        soap_action = method.soap_action()

        soap_header = method.soap_header(scenario, token)
        soap_body = method.soap_body(*args)
        
        method_name = method.__name__.rsplit(".", 1)[1]
        self._send_request(method_name,
                           self._service.url, 
                           soap_header, soap_body, soap_action, 
                           callback, errback,
                           http_headers)

    def _HandleSOAPFault(self, request_id, callback, errback,
            soap_response, user_data):
        error_code = soap_response.fault.find("./detail/ab:errorcode").text
        errback[0](error_code, *errback[1:])

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

    def ab_callback(contacts, groups):
        print contacts
        print groups

    sso = SingleSignOn(account, password)
    ab = AB(sso)
    ab.FindAll((ab_callback,), None, 'Initial', False)

    while mainloop.is_running():
        try:
            mainloop.run()
        except KeyboardInterrupt:
            mainloop.quit()
