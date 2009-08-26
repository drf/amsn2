
class aMSNFileChooserWindow(object):
    """
    This Interface represent a window used to choose a file,
    which could be an image for the dp, a file to send, a theme file, etc.
    """
    def __init__(self, filter, directory):
        """
        @type filter: tuple
        @param filter: A tuple containing strings, that will represent the file
        formats to filter.
        @type directory: str
        @param directory: The path to start from.

        This will eventually call the related show() method, so the window is
        displayed when created.
        """
        raise NotImplementedError

class aMSNDPChooser(object):
    """
    This Interface represent a window used to choose a display picture,
    should show a list of default dps and the possibility to catch a picture from a webcam.
    """
    def __init__(self, default_dps, actions):
        """
        @type default_dps: tuple
        @params default_dps: a tuple containing strings representing the paths of the default dps.
        @type actions: tuple
        @param actions: A tuple containing the options between
        which the user can choose. Every option is a tuple itself, of the form (name, callback),
        where callback is the function that will be called if the option is selected.

        This will eventually call the related show() method, so the window is
        displayed when created.
        """
        raise NotImplementedError

