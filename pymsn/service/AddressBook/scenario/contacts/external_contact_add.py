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
from pymsn.service.AddressBook.constants import *
from pymsn.service.description.AB.constants import ContactEmailType
from pymsn.profile import NetworkID

__all__ = ['ExternalContactAddScenario']

class ExternalContactAddScenario(BaseScenario):
    def __init__(self, ab, callback, errback, account='', 
                 network_id=NetworkID.EXTERNAL, contact_info={}, invite_info={}):
        """Adds an external messenger contact and updates the address book.

            @param ab: the address book service
            @param callback: tuple(callable, *args)
            @param errback: tuple(callable, *args)"""
        BaseScenario.__init__(self, 'ContactMsgrAPI', callback, errback)

        self._ab = ab

        self.account = account 
        self.network_id = network_id
        self.contact_info = contact_info
        self.invite_info = invite_info

    def execute(self):
        if self.contact_info.get('email', None) is None:
            self.contact_info['email'] = \
                { ContactEmailType.EXTERNAL : self.account }
        else:
            self.contact_info['email'][ContactEmailType.EXTERNAL] = self.account
        self.contact_info['capability'] = self.network_id
        self._ab.ContactAdd((self.__contact_add_callback,),
                            (self.__contact_add_errback,),
                            self._scenario, 
                            self.contact_info,
                            self.invite_info)

    def __contact_add_callback(self, contact_guid):
        self._ab.FindAll((self.__find_all_callback, contact_guid),
                         (self.__find_all_errback, contact_guid),
                         self._scenario, True)

    def __contact_add_errback(self, error_code):
        errcode = AddressBookError.UNKNOWN
        errback = self._errback[0]
        args = self._errback[1:]
        errback(errcode, *args)

    def __find_all_callback(self, delta, contact_guid):
        callback = self._callback
        callback[0](contact_guid, delta, *callback[1:])

    def __find_all_errback(self, error_code):
        errcode = AddressBookError.UNKNOWN
        errback = self._errback[0]
        args = self._errback[1:]
        errback(errcode, *args)
