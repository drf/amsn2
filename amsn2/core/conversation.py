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

from amsn2.protocol.events import conversation
from amsn2.core.contactlist_manager import *
from amsn2.core.views import *
import papyon

class aMSNConversation:
    def __init__(self, core, conv_manager, conv = None, contacts_uid = None):
        """
        @type core: aMSNCore
        @type conv_manager: aMSNConversationManager
        @type conv:
        @type contacts_uid:
        """

        if (contacts_uid is None):
            raise ValueError, InvalidArgument

        self._core = core
        self._conversation_manager = conv_manager
        self._contacts_uid = contacts_uid
        if conv is None:
            #New conversation
            papyon_contacts = [core._contactlist_manager.getContact(uid) for uid in contacts_uid]
            papyon_contacts = [c._papyon_contact for c in papyon_contacts if c is not None]
            #if c was None.... wtf?
            self._conv = papyon.Conversation(self._core._profile.client, papyon_contacts)
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

    def onUserJoined(self, contact_uid):
        #TODO
        pass

    def onUserLeft(self, contact_uid):
        #TODO
        pass

    def onUserTyping(self, contact_uid):
        c = self._core._contactlist_manager.getContact(contact_uid)
        self._convWidget.onUserTyping(c.nickname)

    def onMessageReceived(self, message, sender_uid=None, formatting=None):
        #TODO: messageView
        mv = MessageView()
        if sender_uid is None:
            mv.sender.appendStringView(self._core._personalinfo_manager._personalinfoview.nick)
        else:
            c = self._core._contactlist_manager.getContact(sender_uid)
            mv.sender_icon = c.icon
            mv.message_type = MessageView.MESSAGE_OUTGOING
            mv.sender.appendStringView(c.nickname)
        mv.msg = message
        self._convWidget.onMessageReceived(mv, formatting)

    def onNudgeReceived(self, sender_uid):
        self._convWidget.nudge()

    """ Actions from ourselves """
    def sendMessage(self, msg, formatting=None):
        """ msg is a StringView """
        # for the moment, no formatting, no smiley substitution... (TODO)
        # peacey: Added formatting of styles
        self.onMessageReceived(msg, formatting=formatting)
        message = papyon.ConversationMessage(str(msg), formatting)
        self._conv.send_text_message(message)

    def sendNudge(self):
        self._conv.send_nudge()

    def sendTypingNotification(self):
        self._conv.send_typing_notification()

    def leave(self):
        self._conv.leave()

    def inviteContact(self, contact_uid):
        """ contact_uid is the Id of the contact to invite """
        c = self._core._contactlist_manager.getContact(contact_uid)
        self._conv.invite_user(contact.papyon_contact)

    #TODO: ...
