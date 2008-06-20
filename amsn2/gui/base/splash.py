
class aMSNSplashScreen(object):
    """ This interface will represent the splashscreen of the UI"""
    def __init__(self, amsn_core):
        """Initialize the interface. You should store the reference to the core in here """
        raise NotImplementedError

    def show(self):
        """ Draw the splashscreen """
        raise NotImplementedError
    
    def hide(self):
        """ Hide the splashscreen """
        raise NotImplementedError
    
    def showText(self, text):
        """ Shows a different text inside the splashscreen """
        raise NotImplementedError
    
    def setImage(self, image): #TODO: Should we give a path here or is Image correct?
        raise NotImplementedError



