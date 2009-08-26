
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

class aMSNContactInputWindow(object): 
    """
    This Interface represent a window used to get a new contact.
    """
    def __init__(self, message, callback, groups):
        """
        @type message: tuple
        @param message: A tuple with the messages to be shown in the input window,
        of the form (account_string, invite_string).
        @type callback: function
        @param callback: The function that will be called when the contact info has been filled.
        The prototype is callback(email, invite_message, groups).
        @type groups: tuple
        @param groups: a list of existing groups
        """
        raise notImplementedError

class aMSNGroupInputWindow(object): 
    """
    This Interface represent a window used to get a new group.
    """
    def __init__(self, message, callback, contacts):
        """
        @type message: tuple
        @param message: A tuple with the messages to be shown in the input window.
        @type callback: function
        @param callback: The function that will be called when the group info has been filled.
        The prototype is callback(name_group, contacts).
        @type contacts: tuple
        @param contacts: a list of existing contacts
        """
        raise notImplementedError

class aMSNContactDeleteWindow(object): 
    """
    This Interface represent a window used to delete a contact.
    """
    def __init__(self, message, callback, contacts):
        """
        @type message: tuple
        @param message: A tuple with the messages to be shown in the window.
        @type callback: function
        @param callback: The function that will be called when the account has been entered.
        The prototype is callback(account), where account is the email of the account to delete.
        @type contacts: tuple
        @param contacts: a tuple with all the contacts that can be removed in the AddressBook.
        """
        raise notImplementedError

class aMSNGroupDeleteWindow(object): 
    """
    This Interface represent a window used to delete a group.
    """
    def __init__(self, message, callback, groups):
        """
        @type message: tuple
        @param message: A tuple with the messages to be shown in the window.
        @type callback: function
        @param callback: The function that will be called when the group has been entered.
        The prototype is callback(group), where group is the group name.
        @type groups: tuple
        @param groups: a tuple with all the groups that can be deleted.
        """
        raise notImplementedError

