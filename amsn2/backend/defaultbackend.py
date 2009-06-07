import os
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


def saveConfig(account, config, name):
    #TODO: improve
    if name == 'General':
        root_section = Element("aMSNConfig")
        for e in config._config:
            val = config._config[e]
            elmt = SubElement(root_section, "entry",
                              type=type(val).__name__,
                              name=str(e))
            elmt.text = str(val)

        accpath = os.path.join(account.account_dir, "config.xml")
        xml_tree = ElementTree(root_section)
        xml_tree.write(accpath, encoding='utf-8')

def loadConfig(account, name):
    if name == 'General':
        c = aMSNConfig()
        c._config = {"ns_server":'messenger.hotmail.com',
                     "ns_port":1863,
                    }
        configpath = os.path.join(account.account_dir, "config.xml")
        configfile = file(configpath, "r")
        root_tree = ElementTree(file=configfile)
        configfile.close()
        config = root_tree.getroot()
        if config.tag == "aMSNConfig":
           lst = config.findall("entry")
           for elmt in lst:
               if elmt.attrib['type'] == 'int':
                   c.setKey(elmt.attrib['name'], int(elmt.text))
               else:
                   c.setKey(elmt.attrib['name'], elmt.text)
        print repr(c._config)
        return c
    else:
        return None
