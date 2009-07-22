
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

