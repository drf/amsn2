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
from pymsn.service.OfflineIM.constants import *
from pymsn.service.OfflineIM.scenario.base import BaseScenario

__all__ = ['SendMessageScenario']

class SendMessageScenario(BaseScenario):
    def __init__(self, oim, callback, errback):
        """Accepts an invitation.

            @param oim: the oim service
            @param callback: tuple(callable, *args)
            @param errback: tuple(callable, *args)
        """
        BaseScenario.__init__(self, callback, errback)
        self.__oim = oim

    def execute(self):
        # self.__oim.Store2((self.__store2_callback,),
        #                   (self.__store2_errback,))
        pass
            
    def __store2_callback(self):
        callback = self._callback
        callback[0](*callback[1:])

    def __store2_errback(self, error_code):
        errcode = OfflineMessagesBoxError.UNKNOWN
        errback = self._errback[0]
        args = self._errback[1:]
        errback(errcode, *args)
