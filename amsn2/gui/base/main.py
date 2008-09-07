
class aMSNMainWindow(object):
    """ This Interface represents the main window of the application. Everything will be done from here """
    def __init__(self, amsn_core):
        raise NotImplementedError

    def show(self):
        """ This launches the main window, creates it, etc..
        and should notify the core of the main window being created"""
        raise NotImplementedError

    def hide(self):
        """ This should hide the main window, creates it, etc..
        and should notify the core of the main window being created"""
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
