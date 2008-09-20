
from conversation import aMSNConversation


class aMSNConversationManager:
    def __init__(self, core):
        self._core = core
        self._convs = []
        self._wins = []

    def onInviteConversation(self, conversation):
        print "new conv"
        contacts_id = [c.id for c in conversation.participants]
        print contacts_id
        #TODO: contacts_id to views
        win = self.__newConversationWindow(contacts_id)
        c = aMSNConversation(self._core, self, conversation, win)
        self._convs.append(c)
        win.show()

    def newConversation(self, contacts):
        """ contacts is a list of contact ids ?"""

    def __newConversationWindow(self, contacts):
        #contacts should be a list of contact view
        # for the moment, always create a new win
        win = self._core._gui.gui.aMSNChatWindow(self)
        self._wins.append(win)
        return win


