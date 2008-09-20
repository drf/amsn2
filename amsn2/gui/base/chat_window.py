
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
    def __init__(self, amsn_conversation, parent):
        """ create the chat widget for the 'parent' window, but don't attach to
        it."""
        raise NotImplementedError

    def onUserJoined(self, contact):
        """ contact: a contactView of the contact who joined """
        raise NotImplementedError

    def onUserLeft(self, contact):
        """ contact: a contactView of the contact who left """
        raise NotImplementedError

    def onUserTyping(self, contact):
        """ contact: a contactView of the contact who is typing """
        raise NotImplementedError

    def onMessageReceived(self, sender, message):
        """ sender: a contactView of the sender of the message 
            message: a stringView of the message sent"""
        raise NotImplementedError

    def onNudgeReceived(self, sender):
        """ sender: a contactView of the contact who sent the nudge """
        raise NotImplementedError

