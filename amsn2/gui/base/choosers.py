
class aMSNFileChooserWindow(object):
    """
    This Interface represent a window used to choose a file,
    which could be an image for the dp, a file to send, a theme file, etc.
    """
    def __init__(self, filters, directory, callback):
        """
        @type filter: dict of tuple
        @param filter: A dict whose keys are the names of the filters,
        and the values are a tuple containing strings,
        that will represent the patterns to filter.
        @type directory: str
        @param directory: The path to start from.
        @type callback: function
        @param callback: The function called when the file has been choosed.
        Its prototype is callback(file_path)

        This will eventually call the related show() method, so the window is
        displayed when created.
        """
        raise NotImplementedError

class aMSNDPChooserWindow(object):
    """
    This Interface represent a window used to choose a display picture,
    should show a list of default dps and the possibility to catch a picture from a webcam.
    """
    def __init__(self, callback, backend_manager):
        """
        @type callback: function
        @param callback: The function called when the dp has been choosed.
        Its prototype is callback(dp_path)
        @type backend_manager: aMSNBackendManager

        This will eventually call the related show() method, so the window is
        displayed when created.
        """
        raise NotImplementedError

