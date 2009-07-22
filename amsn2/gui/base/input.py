
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
