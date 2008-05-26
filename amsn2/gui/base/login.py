
class aMSNLoginWindow(object):
    def __init__(self, amsn_core):
        raise NotImplementedError

    def show(self):
        raise NotImplementedError
    
    def hide(self):
        raise NotImplementedError

    def switch_to_profile(self, profile):
        raise NotImplementedError

    def signin(self):
        raise NotImplementedError

    def onConnecting(self, message):
        raise NotImplementedError


