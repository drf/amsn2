

import pymsn
import pymsn.event

class InviteEvents(pymsn.event.InviteEventInterface):

    def __init__(self, client, amsn_core):
        self._amsn_core = amsn_core
        pymsn.event.InviteEventInterface.__init__(self, client)
        
    def on_invite_conversation(self, conversation):
        self._amsn_core._conversation_manager.onInviteConversation(conversation)
