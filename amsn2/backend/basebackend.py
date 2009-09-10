
class basebackend():
    """
    Base backend, used as a model to implement others backends.
    It contains the functions that should be available for every backend.
    """

    def saveConfig(self, amsn_account, config):
        raise NotImplementedError

    def loadConfig(self, amsn_account):
        raise NotImplementedError

    def loadAccount(self, email):
        raise NotImplementedError

    def loadAccounts(self):
        raise NotImplementedError

    def saveAccount(self, amsn_account):
        raise NotImplementedError

    def setAccount(self, email):
        raise NotImplementedError

    def clean(self):
        """
        Delete temporary things and prepare the backend to be detached
        or to begin another session with the same backend (e.g. with nullbackend)
        """
        raise NotImplementedError


    """ DPs """
    def getFileLocationDP(self, email, uid, shaci):
        raise NotImplementedError

    def getDPs(self, email):
        raise NotImplementedError
