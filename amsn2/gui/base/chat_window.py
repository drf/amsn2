
class aMSNChatWindow(object):
    def __init__(self, amsn_core):
        raise NotImplementedError

    def show(self):
        """ Show the chat window """
        raise NotImplementedError

    def hide(self):
        """ Hide the chat window """
        raise NotImplementedError

    def messageSent(self,  message):
        """ This method will be called to notify the chat window that a new message was sent and should be displayed.
        Message is a stringview, so the GUI doesn't care who sent it.
        """
        raise NotImplementedError
    
    def nudgeSent(self):
        """ This method will be called to notify the chat window that a nudge was sent.
        """
        raise NotImplementedError
        
    
    def userTyping(self,  message):
        """ This method notifies the window a user is typing. Message is the message that should be
        displayed, and is a stringview
        """
        raise NotImplementedError

