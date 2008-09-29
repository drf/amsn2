from contact_manager import *
from conversation import aMSNConversation

class aMSNConversationManager:
    def __init__(self, core):
        self._core = core
        self._convs = []
        self._wins = []

    def onInviteConversation(self, conversation):
        print "new conv"
        contacts_id = [c.id for c in conversation.participants]
        contacts = [ContactView.getContact(cid) for cid in contacts_id]
        #TODO: What if the contact_manager has not build a view for that contact?
        c = aMSNConversation(self._core, self, conversation, contacts)
        self._convs.append(c)

    def newConversation(self, contacts):
        """ contacts is a list of contact views """
        #TODO: check if no conversation like this one already exists
        c = aMSNConversation(self._core, self, None, contacts)
        self._convs.append(c)



    def getConversationWindow(self, amsn_conversation):
        #contacts should be a list of contact view
        # for the moment, always create a new win
        win = self._core._gui.gui.aMSNChatWindow(self)
        self._wins.append(win)
        return win


