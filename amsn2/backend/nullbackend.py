
from amsn2.core.config import aMSNConfig
import defaultaccountbackend

import tempfile
import os

"""ElementTree independent from the available distribution"""
try:
    from xml.etree.cElementTree import *
except ImportError:
    try:
        from cElementTree import *
    except ImportError:
        from elementtree.ElementTree import *

class nullbackend(defaultaccountbackend.defaultaccountbackend):
    """
    Backend that will not save anything permanentely, used for on-the-fly-sessions.
    """

    def __init__(self):
        defaultaccountbackend.defaultaccountbackend.__init__(self)

        self.config_dir = tempfile.mkdtemp()

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

    def clean(self):
        if os.path.isdir(self.config_dir):
            for [root, subdirs, subfiles] in os.walk(self.config_dir, False):
                for subfile in subfiles:
                    os.remove(os.path.join(root, subfile))
                for subdir in subdirs:
                    os.rmdir(os.path.join(root, subdir))

    def __del__(self):
        self.clean()
        os.rmdir(self.config_dir)


