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
from pymsn.profile import NetworkID

__all__ = ['UnblockContactScenario']

class UnblockContactScenario(BaseScenario):
    def __init__(self, sharing, callback, errback, account='', 
                 network=NetworkID.MSN, state='Accepted'):
        """Unblocks a contact.

            @param sharing: the membership service
            @param callback: tuple(callable, *args)
            @param errback: tuple(callable, *args)
            @param type: 'Passport' | 'Email'
        """
        BaseScenario.__init__(self, 'BlockUnblock', callback, errback)
        self.__sharing = sharing
        
        self.account = account
        self.network = network
        self.state = state

    def _type(self):
        if self.network == NetworkID.MSN:
            return 'Passport'
        elif self.network == NetworkID.EXTERNAL:
            return 'Email'

    def execute(self):
        self.__sharing.DeleteMember((self.__delete_member_callback,),
                                    (self.__delete_member_errback,),
                                    self._scenario, 'Block', self._type(),
                                    self.state, self.account)

    def __delete_member_callback(self):
        self.__sharing.AddMember((self.__add_member_callback,),
                                 (self.__add_member_errback,),
                                 self._scenario, 'Allow', self._type(), 
                                 self.state, self.account)

    def __delete_member_errback(self, error_code):
        errcode = AddressBookError.UNKNOWN
        errback = self._errback[0]
        args = self._errback[1:]
        errback(errcode, *args)
    
    def __add_member_callback(self):
        callback = self._callback
        callback[0](*callback[1:])

    def __add_member_errback(self, error_code):
        errcode = AddressBookError.UNKNOWN
        errback = self._errback[0]
        args = self._errback[1:]
        errback(errcode, *args)
