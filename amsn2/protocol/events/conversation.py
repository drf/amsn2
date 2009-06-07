# -*- coding: utf-8 -*-
#
# amsn - a python client for the WLM Network
#
# Copyright (C) 2008 Dario Freddi <drf54321@gmail.com>
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

from amsn2.core.views import *
import papyon
import papyon.event


class ConversationEvents(papyon.event.ConversationEventInterface):
    def __init__(self, amsn_conversation):
        self._amsn_conversation = amsn_conversation
        self._conversation = amsn_conversation._conv
        papyon.event.ConversationEventInterface.__init__(self, self._conversation)

    def on_conversation_state_changed(self, state):
        self._amsn_conversation.onStateChanged(state)

    def on_conversation_error(self, type, error):
        self._amsn_conversation.onError(type, error)

    def on_conversation_user_joined(self, contact):
        self._amsn_conversation.onUserJoined(contact.id)

    def on_conversation_user_left(self, contact):
        self._amsn_conversation.onUserLeft(contact.id)

    def on_conversation_user_typing(self, contact):
        self._amsn_conversation.onUserTyping(contact.id)

    def on_conversation_message_received(self, sender, message):
        """ Powers of the stringview, here we come! We need to parse the message,
        that could actually contain some emoticons. In that case, we simply replace
        them into the stringview """
        #TODO: have Smiley object in the stringView to keep image+trigger
        strv = StringView()
        if message.content in message.msn_objects.keys():
            print "single emoticon"
            strv.appendImage(message.msn_objects[message.content]._location)
            self._amsn_conversation.onMessageReceived(strv, sender.id)
            return

        strlist = [message.content]

        for smile in message.msn_objects.keys():
            newlist = []
            for str in strlist:
                li = str.split(smile)
                for part in li:
                    newlist.append(part)
                    newlist.append(message.msn_objects[smile]._location)
                newlist.pop()

            strlist = newlist

        for str in strlist:
            if str in message.msn_objects.keys():
                strv.appendImage(str)
            else:
                strv.appendText(str)

        self._amsn_conversation.onMessageReceived(strv, sender.id, message.formatting)

    def on_conversation_nudge_received(self, sender):
        self._amsn_conversation.onNudgeReceived(sender.id)

