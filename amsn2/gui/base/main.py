
class aMSNMainWindow(object):
    """ This Interface represents the main window of the application. Everythin will be done from here """
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
    
