
from conversation import aMSNConversation


class aMSNConversationManager:
    def __init__(self, core):
        self._core = core
        self._convs = []

    def onInviteConversation(self, conversation):
        c = aMSNConversation(self._core, self, conversation)
        self._convs.append(c)

