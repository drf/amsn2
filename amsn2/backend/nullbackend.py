
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
        self.config_dir = None

    def setAccount(self, email):
        dir = tempfile.mkdtemp()
        self.accounts_dir = dir
        defaultaccountbackend.defaultaccountbackend.accounts_dir = dir
        defaultaccountbackend.defaultaccountbackend.setAccount(self, email)

    def saveConfig(self, account, config):
        # Is it necessary to temporarily save the config?
        pass

    def loadConfig(self, account):
        c = aMSNConfig()
        c._config = {"ns_server":'messenger.hotmail.com',
                       "ns_port":1863,
                     }
        return c

    def clean(self):
        if self.config_dir is not None and os.path.isdir(self.config_dir):
            for [root, subdirs, subfiles] in os.walk(self.config_dir, False):
                for subfile in subfiles:
                    os.remove(os.path.join(root, subfile))
                for subdir in subdirs:
                    os.rmdir(os.path.join(root, subdir))

    def __del__(self):
        if self.config_dir is not None:
            self.clean()
            os.rmdir(self.config_dir)


