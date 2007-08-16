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

import rsi
import oim
import scenario

from pymsn.service.SOAPUtils import *
from pymsn.service.OfflineIM.constants import *

import pymsn.util.ElementTree as ElementTree
import pymsn.util.StringIO as StringIO
import gobject

import logging

__all__ = ['OfflineMessagesBox', 'OfflineMessage']

logger = logging.getLogger('Service')

class OfflineMessagesStorage(set):
    def __init__(self, initial_set=()):
        set.__init__(self, initial_set)

    def __repr__(self):
        return "OfflineMessagesBox : %d message(s)" % len(self)

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
        
    def search_by_sender(self, sender):
        result = []
        for message in self:
            if message.sender == sender:
                result.append(message)
        return OfflineMessagesStorage(result)

    def search_by_groups(self, *groups):
        result = []
        groups = set(groups)
        for contact in self:
            if groups <= contact.groups:
                result.append(contact)
        return OfflineMessagesStorage(result)

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
        return OfflineMessagesStorage(result)

    def group_by(self, field):
        result = {}
        for contact in self:
            value = getattr(contact, field)
            if value not in result:
                result[value] = OfflineMessagesStorage()
            result[value].add(contact)
        return result


class OfflineMessage(object):

    def __init__(self, id, sender, display_name='', date=None):
        self._id = id
        self._sender = sender
        self._display_name = display_name

        if date is None:
            # FIXME : set the date attribute using the current date
            pass
        else:
            self._date = date

        self.__text = None
        self.__run_id = ''
        self.__seq_num = ''
        self.__is_mobile = False

    @property
    def id(self):
        return self._id

    @property
    def sender(self):
        return self._sender

    @property
    def display_name(self):
        return self._display_name

    @property
    def date(self):
        return self._date

    def __get_text(self):
        return self.__text
    def __set_text(self, text):
        self.__text = text
    text = property(__get_text)
    _text = property(__get_text, __set_text)

    def __get_run_id(self):
        return self.__run_id
    def __set_run_id(self, run_id):
        self.__run_id = run_id
    run_id = property(__get_run_id)
    _run_id = property(__get_run_id, __set_run_id)

    def __get_seq_num(self):
        return self.__seq_num
    def __set_seq_num(self, seq_num):
        self.__seq_num = seq_num
    seq_num = property(__get_seq_num)
    _seq_num = property(__get_seq_num, __set_seq_num)

    def __get_is_mobile(self):
        return self.__is_mobile
    def __set_is_mobile(self, is_mobile):
        self.__is_mobile = is_mobile
    is_mobile = property(__get_is_mobile)
    _is_mobile = property(__get_is_mobile, __set_is_mobile)

    def __str__(self):
        return self.__text

    def __repr__(self):
        return str(self)

class Metadata(ElementTree.XMLResponse):
    def __init__(self, metadata):
        ElementTree.XMLResponse.__init__(self, metadata)
        if self.tree is None:
            logger.warning("Metadata: Invalid metadata")
            
    def is_valid(self):
        return self.tree is not None

    def _parse(self, data):
        data = StringIO.StringIO(data)
        return ElementTree.parse(data)

class OfflineMessagesBox(gobject.GObject):

    __gsignals__ = {
            "messages-fetched" : (gobject.SIGNAL_RUN_FIRST,
                                  gobject.TYPE_NONE,
                                  (object,)),
            "messages-deleted" : (gobject.SIGNAL_RUN_FIRST,
                                  gobject.TYPE_NONE, ()),
            "message-sent"     : (gobject.SIGNAL_RUN_FIRST,
                                  gobject.TYPE_NONE, ())
            }

    __gproperties__ = {
        "state":  (gobject.TYPE_INT,
                   "State",
                   "The state of the offline messages box.",
                   0, 2, OfflineMessagesBoxState.NOT_SYNCHRONIZED,
                   gobject.PARAM_READABLE),
        "messages" : (gobject.TYPE_PYOBJECT,
                      "Offline messages",
                      "The fetched offline messages.",
                      gobject.PARAM_READABLE)
        }

    def __init__(self, sso, proxies=None):
        gobject.GObject.__init__(self)

        self._rsi = rsi.RSI(sso, proxies)
        self._oim = oim.OIM(sso, proxies)

        self.__state = OfflineMessagesBoxState.NOT_SYNCHRONIZED
        self.__messages = {}

    # Properties
    def __get_state(self):
        return self.__state
    def __set_state(self, state):
        self.__state = state
        self.notify("state")
    state = property(__get_state)
    _state = property(__get_state, __set_state)

    def __get_messages(self):
        return self.__messages
    def __set_messages(self, messages):
        self.__messages = messages
        self.notify("messages")
    messages = property(__get_messages)
    _messages = property(__get_messages, 
                         __set_messages)

    def sync(self, xml_data=None):
        if self._state != OfflineMessagesBoxState.NOT_SYNCHRONIZED:
            return
        self._state = OfflineMessagesBoxState.SYNCHRONIZING

        if xml_data is None:
            sh = scenario.SyncHeadersScenario(self._rsi,
                                              (self.__parse_metadata,),
                                              (self.__common_errback,))
            sh()
        else:
            self.__parse_metadata(xml_data)

    def __parse_metadata(self, xml_data):
        metadata = Metadata(xml_data)
        for m in metadata.findall('./M'):
            id = m.findtext('./I')
            sender = m.findtext('./E')

            name = m.findtext('./N').replace(' ','').\
                split('?')[3].decode('base64')

            date = m.find('./RT')
            if date is not None:
                date = date.text

            message = OfflineMessage(id, sender, date, name)
            self.__messages[message._id] = message

        self._state = OfflineMessagesBoxState.SYNCHRONIZED

    # Public API
    def fetch_messages(self):
        fm = scenario.FetchMessagesScenario(self._rsi,
                 (self.__fetch_message_cb,),
                 (self.__common_errback,),
                 (self.__fetch_messages_cb,))
        fm.message_ids = self._messages.keys()
        fm()

    def send_message(self, recipient, message):
        sm = scenario.SendMessageScenario(self._oim,
                 (self.__common_callback, 'message-sent'),
                 (self.__common_errback,))
        # FIXME : fill the scenario
        sm()

    def delete_messages(self):
        dm = scenario.DeleteMessages(self._rsi,
                 (self.__delete_messages_cb,),
                 (self.__common_errback,))
        dm.message_ids = self._messages.keys()
        dm()

    # Callbacks
    def __fetch_message_cb(self, id, run_id, seq_num, text):
        self._messages[id]._run_id = run_id
        self._messages[id]._seq_num = seq_num
        self._messages[id]._text = text

    def __fetch_messages_cb(self):
        self.emit('messages-fetched', self.messages)

    def __delete_messages_cb(self):
        self._messages = []
        self.emit('messages-deleted')

    def __common_callback(self, signal, *args):
        self.emit(signal, *args)

    def __common_errback(self, error_code, *args):
        print "The offline messages service got the error (%s)" % error_code

gobject.type_register(OfflineMessagesBox)


if __name__ == '__main__':
    import sys
    import getpass
    import signal
    import gobject
    import logging
    from pymsn.service.SingleSignOn import *
    from pymsn.service.AddressBook import AddressBook

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

    def sso_callback(arg):
        print arg

    def sso_errback():
        pass

    sso = SingleSignOn(account, password)
#    address_book = AddressBook(sso)
#    address_book.connect("notify::state", address_book_state_changed)
#    address_book.connect("messenger-contact-added", messenger_contact_added)
#    address_book.sync()
    box = OfflineMessagesBox(sso)
    box.sync()

#     sso.RequestMultipleSecurityTokens((sso_callback,), (sso_errback,),
#                                       LiveService.CONTACTS)
#     sso.RequestMultipleSecurityTokens((sso_callback,), (sso_errback,),
#                                       LiveService.MESSENGER)
#     sso.RequestMultipleSecurityTokens((sso_callback,), (sso_errback,),
#                                       LiveService.MESSENGER_CLEAR)
#     sso.RequestMultipleSecurityTokens((sso_callback,), (sso_errback,),
#                                       LiveService.MESSENGER_SECURE)
#     sso.RequestMultipleSecurityTokens((sso_callback,), (sso_errback,),
#                                       LiveService.SPACES)
#     sso.RequestMultipleSecurityTokens((sso_callback,), (sso_errback,),
#                                       LiveService.TB)
#     sso.RequestMultipleSecurityTokens((sso_callback,), (sso_errback,),
#                                       LiveService.VOICE)

    while mainloop.is_running():
        try:
            mainloop.run()
        except KeyboardInterrupt:
            mainloop.quit()
