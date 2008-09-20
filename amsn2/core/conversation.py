
from amsn2.protocol import conversation
import pymsn

class aMSNConversation:
    def __init__(self, core, conv_manager, conv = None):
        self._core = core
        self._conversation_manager = conv_manager
        if conv is None:
            self._conv = pymsn.Conversation(self, contacts)
        else:
            self._conv = conv
        self._convo_events = conversation.ConversationEvents(self)

    def onStateChanged(self, state):
        pass

    def onError(self, type, error):
        pass

    def onUserJoined(self, contact):
        pass

    def onUserLeft(self, contact):
        pass

    def onUserTyping(self, contact):
        pass

    def onMessageReceived(self, sender, message):
        print "%s says: %s" % (sender.account, message.content)

    def onNudgeReceived(self, sender):
        pass
