# -*- coding: utf-8 -*-
#
# Copyright (C) 2007  Ali Sabil <ali.sabil@gmail.com>
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

"""Invite event interfaces

The interfaces defined in this module allow receiving notification events when
we get invited into an activity with other users."""

from pymsn.event import BaseEventInterface

__all__ = ["InviteEventInterface"]

class InviteEventInterface(BaseEventInterface):
    def __init__(self, client):
        """Initializer
            @param client: the client we want to be notified for its events
            @type client: L{Client<pymsn.Client>}"""
        BaseEventInterface.__init__(self, client)

    def on_invite_conversation(self, conversation):
        """Called when we get invited into a conversation
            @param conversation: the conversation
            @type conversation: L{Conversation<pymsn.conversation.ConversationInterface>}"""
        pass

