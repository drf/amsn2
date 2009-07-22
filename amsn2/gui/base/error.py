
class aMSNErrorWindow(object):
    """ This Interface represent an error window """
    def __init__(self, error_text):
        """
        @type error_text: str

        This will eventually call the related show() method, so the window is
        displayed when created.
        """
        raise NotImplementedError

