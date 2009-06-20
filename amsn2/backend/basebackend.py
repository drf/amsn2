"""
Base backend, should be used as a model to implement others backends
As it is right now it's not used directly by aMSN2's code
"""

def getPassword(passwdElmt):
    raise NotImplementedError

def setPassword(password, root_section):
    raise NotImplementedError

def saveConfig(account, config):
    raise NotImplementedError

def loadConfig(account):
    raise NotImplementedError

