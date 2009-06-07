""" Backend that will not save anything, used for on-the-fly-sessions """

from amsn2.core.config import aMSNConfig

def getPassword(passwdElmt):
    return passwdElmt.text

def setPassword(password, root_section):
    elmt = SubElement(root_section, "password", backend='NullBackend')
    elmt.text = password
    return elmt

def saveConfig(account, config):
    pass

def loadConfig(account):
    c = aMSNConfig()
    c._config = {"ns_server":'messenger.hotmail.com',
                   "ns_port":1863,
                 }
    return c

