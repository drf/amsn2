
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
        self._amsn_conversation.onUserJoined(contact)

    def on_conversation_user_left(self, contact):
        self._amsn_conversation.onUserLeft(contact)

    def on_conversation_user_typing(self, contact):
        self._amsn_conversation.onUserTyping(contact)

    def on_conversation_message_received(self, sender, message):
        self._amsn_conversation.onMessageReceived(sender,  message)
    
    def on_conversation_nudge_received(self, sender):
        self._amsn_conversation.onNudgeReceived(sender)

