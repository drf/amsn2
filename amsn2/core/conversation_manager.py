from contactlist_manager import *
from conversation import aMSNConversation

class aMSNConversationManager:
    def __init__(self, core):
        self._core = core
        self._convs = []
        self._wins = []

    def onInviteConversation(self, conversation):
        print "new conv"
        contacts_uid = [c.id for c in conversation.participants]
        #TODO: What if the contact_manager has not build a view for that contact?
        c = aMSNConversation(self._core, self, conversation, contacts_uid)
        self._convs.append(c)

    def newConversation(self, contacts_uid):
        """ contacts_uid is a list of contact uid """
        #TODO: check if no conversation like this one already exists
        c = aMSNConversation(self._core, self, None, contacts_uid)
        self._convs.append(c)



    def getConversationWindow(self, amsn_conversation):
        #TODO:
        #contacts should be a list of contact view
        # for the moment, always create a new win
        win = self._core._gui.gui.aMSNChatWindow(self)
        self._wins.append(win)
        return win


