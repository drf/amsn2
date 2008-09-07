
class aMSNWindow(object):
    """ This Interface represents a window of the application. Everything will be done from here """
    def __init__(self, amsn_core):
        raise NotImplementedError

    def show(self):
        """ This launches the window, creates it, etc.."""
        raise NotImplementedError

    def hide(self):
        """ This should hide the window"""
        raise NotImplementedError

    def setTitle(self, text):
        """ This will allow the core to change the current window's title
        @text : a string
        """
        raise NotImplementedError
    
    def setMenu(self, menu):
        """ This will allow the core to change the current window's main menu
        @menu : a MenuView
        """
        raise NotImplementedError
