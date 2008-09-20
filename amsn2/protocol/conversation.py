from amsn2.core.views import *
import pymsn
import pymsn.event


class ConversationEvents(pymsn.event.ConversationEventInterface):
    def __init__(self, amsn_conversation):
        self._amsn_conversation = amsn_conversation
        self._conversation = amsn_conversation._conv
        pymsn.event.ConversationEventInterface.__init__(self, self._conversation)

    def on_conversation_state_changed(self, state):
        self._amsn_conversation.onStateChanged(state)

    def on_conversation_error(self, type, error):
        self._amsn_conversation.onError(type, error)

    def on_conversation_user_joined(self, contact):
        c = ContactView.getContact(contact.id)
        self._amsn_conversation.onUserJoined(c)

    def on_conversation_user_left(self, contact):
        c = ContactView.getContact(contact.id)
        self._amsn_conversation.onUserLeft(c)

    def on_conversation_user_typing(self, contact):
        c = ContactView.getContact(contact.id)
        self._amsn_conversation.onUserTyping(c)

    def on_conversation_message_received(self, sender, message):
        c = ContactView.getContact(sender.id)
        str = StringView()
        str.appendText(message.content)
        self._amsn_conversation.onMessageReceived(c, str)

    def on_conversation_nudge_received(self, sender):
        c = ContactView.getContact(sender.id)
        self._amsn_conversation.onNudgeReceived(c)

