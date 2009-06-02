"""ElementTree independent from the available distribution"""
try:
    from xml.etree.cElementTree import *
except ImportError:
    try:
        from cElementTree import *
    except ImportError:
        from elementtree.ElementTree import *
from amsn2.core.config import aMSNConfig

def getPassword(passwdElmt):
    return passwdElmt.text

def setPassword(password, root_section):
    elmt = SubElement(root_section, "password", backend='DefaultBackend')
    elmt.text = password
    return elmt


"""
TODO: Give an aMSNAccount as argument so that the backend can store information
on how to get/set stuff??
"""

def saveConfig(config, name):
    #TODO
    pass

def loadConfig(name):
    #TODO
    if name == 'General':
        c = aMSNConfig()
        c._config = {"ns_server":'messenger.hotmail.com',
                     "ns_port":1863,
                    }
        return c
    else:
        return None
