
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
    def __init__(self, default_dps, actions, callback):
        """
        @type default_dps: list
        @params default_dps: a list containing strings representing the paths of the default dps.
        @type actions: tuple
        @param actions: A tuple containing the options between
        which the user can choose. Every option is a tuple itself, of the form (name, callback),
        where callback is the function that will be called if the option is selected.
        @type callback: function
        @param callback: The function called when the dp has been choosed.
        Its prototype is callback(dp_path)

        This will eventually call the related show() method, so the window is
        displayed when created.
        """
        raise NotImplementedError

    def update_dp_list(self, default_dps):
        """
        @type default_dps: tuple
        @params default_dps: a tuple containing strings representing the paths of the default dps.

        This function updated the list of the dps that can be chosen,
        for example after opening a file or taking a picture.
        """
        raise NotImplementedError

