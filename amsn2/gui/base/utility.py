
class aMSNErrorWindow(object):
    """ This Interface represent an error window """
    def __init__(self, error_text):
        """
        @type error_text: str

        This will eventually call the related show() method, so the window is
        displayed when created.
        """
        raise NotImplementedError

class aMSNNotificationWindow(object):
    """
    This Interface represent a window used to display a notification message,
    generally when an operation has finished succesfully.
    """
    def __init__(self, notification_text):
        """
        @type notification_text: str

        This will eventually call the related show() method, so the window is
        displayed when created.
        """
        raise NotImplementedError

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

class aMSNInputWindow(object): 
    """
    This Interface represent a window used to get an input,
    like a new contact or a new group.
    """
    def __init__(self, message, type, callback, params):
        """
        @type message: str
        @type type: ContactView or GroupView
        @param type: contains the view to fill.
        @type callback: function
        @param callback: The function that will be called when the view has been filled.
        The prototype is callback(view), where view is the ContactView or the Grouview
        filled, or None if the input has been canceled.
        @type params: tuple
        @param params: a list of existing contacts or groups
        """
        raise notImplementedError

