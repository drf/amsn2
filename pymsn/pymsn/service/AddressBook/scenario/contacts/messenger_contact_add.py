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

from pymsn.service.AddressBook.constants import *
from pymsn.profile import ContactType

__all__ = ['MessengerContactAddScenario']

class MessengerContactAddScenario(BaseScenario):
    def __init__(self, ab, callback, errback,
                 account='', 
                 contact_type=ContactType.REGULAR,
                 contact_info={},
                 invite_display_name='',
                 invite_message=''):
        """Adds a messenger contact and updates the address book.

            @param ab: the address book service
            @param callback: tuple(callable, *args)
            @param errback: tuple(callable, *args)"""
        BaseScenario.__init__(self, Scenario.CONTACT_SAVE, callback, errback)

        self._ab = ab

        self.account = account 

        self.contact_type = contact_type
        self.contact_info = contact_info

        self.invite_display_name = invite_display_name
        self.invite_message = invite_message
        self.auto_manage_allow_list = True

    def execute(self):
        invite_info = { 'display_name' : self.invite_display_name ,
                        'invite_message' : self.invite_message }

        self.contact_info['passport_name'] = self.account
        self.contact_info['contact_type'] = self.contact_type
        self.contact_info['is_messenger_user'] = True
        self._ab.ContactAdd((self.__contact_add_callback,),
                            (self.__contact_add_errback,),
                            self._scenario, 
                            self.contact_info,
                            invite_info,
                            self.auto_manage_allow_list)

    def __contact_add_callback(self, contact_guid):
        self._ab.FindAll((self.__find_all_callback, contact_guid),
                         (self.__find_all_errback, contact_guid),
                         self._scenario, True)

    def __contact_add_errback(self, error_code):
        errcode = AddressBookError.UNKNOWN
        if error_code == 'ContactAlreadyExists':
            errcode = AddressBookError.CONTACT_ALREADY_EXISTS
        elif error_code == 'InvalidPassportUser':
            errcode = AddressBookError.INVALID_CONTACT_ADDRESS
        errback = self._errback[0]
        args = self._errback[1:]
        errback(errcode, *args)

    def __find_all_callback(self, address_book_delta, contact_guid):
        callback = self._callback
        callback[0](contact_guid, address_book_delta, *callback[1:])

    def __find_all_errback(self, error_code):
        errcode = AddressBookError.UNKNOWN
        errback = self._errback[0]
        args = self._errback[1:]
        errback(errcode, *args)
