
import pymsn
import pymsn.event


class ConversationEvents(pymsn.event.ConversationInterface):
    def __init__(self, conversation, client_profile,  amsn_core):
        self._amsn_core = amsn_core
        self._conversation = conversation
        pymsn.event.ConversationInterface.__init__(self, conversation)

    def on_conversation_state_changed(self, state):
        """@attention: not implemented"""
        pass

    def on_conversation_error(self, type, error):
        self._amsn_core.conversationError(self._client._amsn_profile, self._conversation,  type)
        pass

    def on_conversation_user_joined(self, contact):
        self._amsn_core.conversationUserJoined(self._client._amsn_profile, self._conversation,  contact)
        pass

    def on_conversation_user_left(self, contact):
        self._amsn_core.conversationUserLeft(self._client._amsn_profile, self._conversation,  contact)
        pass

    def on_conversation_user_typing(self, contact):
        self._amsn_core.conversationUserTyping(self._client._amsn_profile, self._conversation,  contact)
        pass

    def on_conversation_message_received(self, sender, message):
        self._amsn_core.conversationMessageReceived(self._client._amsn_profile, self._conversation,  sender,  message)
        pass
    
    def on_conversation_nudge_received(self, sender):
        self._amsn_core.conversationNudgeReceived(self._client._amsn_profile, self._conversation,  sender)
        pass

