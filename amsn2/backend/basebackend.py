"""
Base backend, should be used as a model to implement others backends
As it is right now it's not used directly by aMSN2's code
"""

class basebackend():
    def getPassword(self, passwdElmt):
        raise NotImplementedError

    def setPassword(self, password, root_section):
        raise NotImplementedError

    def saveConfig(self, account, config):
        raise NotImplementedError

    def loadConfig(self, account):
        raise NotImplementedError

    def loadAccount(self, account):
        raise NotImplementedError

    def loadAccounts(self):
        raise NotImplementedError

    def saveAccount(self, amsn_account):
        raise NotImplementedError

    def clean(self):
        raise NotImplementedError

