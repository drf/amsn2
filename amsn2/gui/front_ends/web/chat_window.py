
class aMSNChatWindow(object):
    """ This interface will represent a chat window of the UI
        It can have many aMSNChatWidgets"""
    def __init__(self, amsn_core):
        self._amsn_core = amsn_core

    def addChatWidget(self, chat_widget):
        """ add an aMSNChatWidget to the window """
        pass

    def show(self):
        pass

    def hide(self):
        pass

    def add(self):
        pass

    def move(self):
        pass

    def remove(self):
        pass

    def attach(self):
        pass

    def detach(self):
        pass

    def close(self):
        pass

    def flash(self):
        pass
    """TODO: move, remove, detach, attach (shouldn't we use add ?), close,
        flash..."""


class aMSNChatWidget(object):
    """ This interface will present a chat widget of the UI """
    def __init__(self, amsn_conversation, parent):
        """ create the chat widget for the 'parent' window, but don't attach to
        it."""
        pass

    def onMessageReceived(self, messageview):
        """ Called for incoming and outgoing messages
            message: a MessageView of the message"""
        pass

    def nudge(self):
        pass

