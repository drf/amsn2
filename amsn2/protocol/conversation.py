
import pymsn
import pymsn.event


class ConversationEvents(pymsn.event.ConversationInterface):
    def __init__(self, conversation, amsn_core):
        self._amsn_core = amsn_core
        pymsn.event.ConversationInterface.__init__(self, conversation)



