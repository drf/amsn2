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

from amsn2.protocol import conversation
import pymsn

class aMSNConversation:
    def __init__(self, core, conv_manager, conv = None, contacts = None):
        if (contacts is None):
            raise ValueError, InvalidArgument

        self._core = core
        self._conversation_manager = conv_manager
        self._contacts = contacts
        if conv is None:
            #New conversation
            pymsn_contacts = [c.pymsn_contact for c in contacts]
            self._conv = pymsn.Conversation(self._core._profile.client, pymsn_contacts)
        else:
            #From an existing conversation
            self._conv = conv

        self._win = self._conversation_manager.getConversationWindow(self)
        self._convo_events = conversation.ConversationEvents(self)
        self._convWidget = core._gui.gui.aMSNChatWidget(self, self._win)
        self._win.addChatWidget(self._convWidget)
        self._win.show()


    """ events from outside """
    def onStateChanged(self, state):
        print "state changed"

    def onError(self, type, error):
        print error

    def onUserJoined(self, contact):
        self._convWidget.onUserJoined(contact)

    def onUserLeft(self, contact):
        self._convWidget.onUserLeft(contact)
        pass

    def onUserTyping(self, contact):
        self._convWidget.onUserTyping(contact)

    def onMessageReceived(self, sender, message):
        self._convWidget.onMessageReceived(sender, message)

    def onNudgeReceived(self, sender):
        self._convWidget.onNudgeReceived(sender)

    """ Actions from ourselves """
    def sendMessage(self, msg):
        """ msg is a StringView """
        # for the moment, no formatting
        message = pymsn.ConversationMessage(msg.toString())
        self._conv.send_text_message(message)

    def sendNudge(self):
        self._conv.send_nudge()
        
    def sendTypingNotification(self):
        self._conv.send_typing_notification()
        
    def leave(self):
        self._conv.leave()
        
    def inviteContact(self, contact):
        """ contact is a ContactView """
        self._conv.invite_user(contact.pymsn_contact)

    #TODO: ...
