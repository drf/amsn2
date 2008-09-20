
class aMSNChatWindow(object):
    def __init__(self, amsn_core):
        raise NotImplementedError

    def addChatWidget(self, chat_widget):
        raise NotImplementedError


class aMSNChatWidget(object):
    def __init__(self, amsn_conversation, parent):
        raise NotImplementedError

    def onUserJoined(self, contact):
        raise NotImplementedError

    def onUserLeft(self, contact):
        raise NotImplementedError

    def onUserTyping(self, contact):
        raise NotImplementedError

    def onMessageReceived(self, sender, message):
        raise NotImplementedError

    def onNudgeReceived(self, sender):
        raise NotImplementedError

