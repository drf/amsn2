
class aMSNChatWindow(object):
    """ This interface will represent a chat window of the UI
        It can have many aMSNChatWidgets"""
    def __init__(self, amsn_core):
        raise NotImplementedError

    def addChatWidget(self, chat_widget):
        """ add an aMSNChatWidget to the window """
        raise NotImplementedError

    """TODO: move, remove, detach, attach (shouldn't we use add ?), close,
        flash..."""


class aMSNChatWidget(object):
    """ This interface will present a chat widget of the UI """
    def __init__(self, amsn_conversation, parent, contacts_uid):
        """ create the chat widget for the 'parent' window, but don't attach to
        it."""
        raise NotImplementedError

    def onMessageReceived(self, messageview):
        """ Called for incoming and outgoing messages
            message: a MessageView of the message"""
        raise NotImplementedError

    def nudge(self):
        raise NotImplementedError

