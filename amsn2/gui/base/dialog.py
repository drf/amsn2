
class aMSNDialogWindow(object):
    """
    This Interface represent a dialog window, used to ask the user
    about something to do.
    """
    def __init__(self, message, actions):
        """
        @type message: str
        @type actions: tuple
        @param actions: A tuple containing the options between
        which the user can choose. Every option is a tuple itself, of the form (name, callback),
        where callback is the function that will be called if the option is selected.

        This will eventually call the related show() method, so the window is
        displayed when created.
        """
        raise NotImplementedError

