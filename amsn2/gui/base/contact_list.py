
class aMSNContactList(object):
    def __init__(self, amsn_core):
        raise NotImplementedError

    def show(self):
        raise NotImplementedError

    def hide(self):
        raise NotImplementedError

    def contactUpdated(self, contact):
        raise NotImplementedError
    
    def contactRenamed(self, contact):
        raise NotImplementedError

    def groupUpdated(self, group):
        raise NotImplementedError

    def groupAdded(self, group):
        raise NotImplementedError

    def groupRemoved(self, group):
        raise NotImplementedError

    def configure(self, option, value):
        raise NotImplementedError

    def cget(self, option, value):
        raise NotImplementedError

