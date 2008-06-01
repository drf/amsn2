
class Image(object):
    """ This interface will represent an image to be used by the UI"""
    def __init__(self, amsn_core):
        """Initialize the interface. You should store the reference to the core in here """
        raise NotImplementedError

    def loadFromFile(self, filename):
        """ This method is used to load an image from a file """
        raise NotImplementedError

    def loadFromResource(self, resource_name):
        """ This method is used to load an image using the name of a resource """
        raise NotImplementedError


