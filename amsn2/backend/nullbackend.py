""" Backend that will not save anything, used for on-the-fly-sessions """

from amsn2.core.config import aMSNConfig
import defaultaccountbackend

"""ElementTree independent from the available distribution"""
try:
    from xml.etree.cElementTree import *
except ImportError:
    try:
        from cElementTree import *
    except ImportError:
        from elementtree.ElementTree import *

class nullbackend(defaultaccountbackend.defaultaccountbackend):
    def __init__(self):
        defaultaccountbackend.defaultaccountbackend.__init__(self)

    def getPassword(self, passwdElmt):
        return passwdElmt.text

    def setPassword(self, password, root_section):
        elmt = SubElement(root_section, "password", backend='NullBackend')
        elmt.text = password
        return elmt

    def saveConfig(self, account, config):
        pass

    def loadConfig(self, account):
        c = aMSNConfig()
        c._config = {"ns_server":'messenger.hotmail.com',
                       "ns_port":1863,
                     }
        return c


