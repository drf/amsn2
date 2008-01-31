# -*- coding: utf-8 -*-
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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
from pymsn.service.AddressBook.scenario.base import BaseScenario
from pymsn.service.AddressBook.scenario.base import Scenario
from messenger_contact_add import MessengerContactAddScenario
from external_contact_add import ExternalContactAddScenario
from update_memberships import UpdateMembershipsScenario

from pymsn.service.AddressBook.constants import *
from pymsn.profile import NetworkID, Membership

__all__ = ['AcceptInviteScenario']

class AcceptInviteScenario(BaseScenario):
    def __init__(self, ab, sharing, callback, errback,
                 account='',
                 memberships=Membership.NONE,
                 network=NetworkID.MSN,
                 state='Accepted'):
        """Accepts an invitation.

            @param ab: the address book service
            @param sharing: the membership service
            @param callback: tuple(callable, *args)
            @param errback: tuple(callable, *args)
        """
        BaseScenario.__init__(self, Scenario.CONTACT_MSGR_API, callback, errback)
        self.__ab = ab
        self.__sharing = sharing

        self.add_to_contact_list = True

        self.account = account
        self.memberships = memberships
        self.network = network
        self.state = state

    def execute(self):
        if self.add_to_contact_list and not (self.memberships & Membership.FORWARD):
            if self.network == NetworkID.MSN:
                am = MessengerContactAddScenario(self.__ab,
                         (self.__add_contact_callback,),
                         (self.__add_contact_errback,),
                         self.account)
                am()
            elif self.network == NetworkID.EXTERNAL:
                em = ExternalContactAddScenario(self.__ab,
                         (self.__add_contact_callback,),
                         (self.__add_contact_errback,),
                         self.account)
                em()
            else:
                # FIXME: maybe raise an exception ?
                self.__update_memberships()
        else:
            self.__update_memberships()

    def __update_memberships(self):
        new_membership = (self.memberships & ~Membership.PENDING) | \
                Membership.ALLOW | Membership.REVERSE
        um = UpdateMembershipsScenario(self.__sharing,
                (self.__update_memberships_callback,),
                (self.__update_memberships_errback,),
                self._scenario,
                self.account,
                self.network,
                self.state,
                self.memberships,
                new_membership)
        um()

    def __add_contact_callback(self, contact_guid, address_book_delta):
        contacts = address_book_delta.contacts
        self.memberships |= Membership.ALLOW | Membership.FORWARD
        for contact in contacts:
            if contact.Id != contact_guid:
                continue
            self._added_contact = contact
            break
        self.__update_memberships()

    def __add_contact_errback(self, error_code):
        errcode = AddressBookError.UNKNOWN
        if error_code == 'ContactAlreadyExists':
            errcode = AddressBookError.CONTACT_ALREADY_EXISTS
        elif error_code == 'InvalidPassportUser':
            errcode = AddressBookError.INVALID_CONTACT_ADDRESS
        errback = self._errback[0]
        args = self._errback[1:]
        errback(errcode, *args)

    def __update_memberships_callback(self, memberships):
        self.memberships = memberships
        contact = self._added_contact
        callback[0](contact, memberships, *callback[1:])

    def __update_memberships_errback(self, error_code, done, failed):
        errcode = AddressBookError.UNKNOWN
        errback = self._errback[0]
        args = self._errback[1:]
        errback(errcode, *args)
