
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

