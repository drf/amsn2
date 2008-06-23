
class aMSNChatWindow(object):
    def __init__(self, amsn_core, parent):
        raise NotImplementedError

    def show(self):
        """ Show the chat window """
        raise NotImplementedError

    def hide(self):
        """ Hide the chat window """
        raise NotImplementedError

    def messageSent(self, contact,  message):
        """ This method will be called to notify the chat window that a new message was sent from contact.
        Message is a stringview, so it should be treated correctly.
        """
        raise NotImplementedError
    
    def nudgeSent(self, contact):
        """ This method will be called to notify the chat window that a nudge was sent from contact.
        """
        raise NotImplementedError

