"""ElementTree independent from the available distribution"""
try:
    from xml.etree.cElementTree import *
except ImportError:
    try:
        from cElementTree import *
    except ImportError:
        from elementtree.ElementTree import *

class aMSNBackendManager(object):
    def __init__(self):
        self.setBackendForFunc('setPassword', 'defaultbackend')
        self.setBackendForFunc('saveConfig',  'defaultbackend')
        self.setBackendForFunc('loadConfig',  'defaultbackend')

    def setBackendForFunc(self, funcname, backendname):
        try:
            m = __import__(backendname, globals(), locals(), [], -1)
        except ImportError:
            m = __import__('defaultbackend', globals(), locals(), [], -1)
        try:
            f = getattr(m, funcname)
        except AttributeError:
            return
        self.__setattr__(funcname, f)

    def getPassword(self, passwdElmt):
        backendname = passwdElmt.attrib['backend']
        try:
            m = __import__(backendname, globals(), locals(), [], -1)
        except ImportError:
            m = __import__('defaultbackend', globals(), locals(), [], -1)

        return m.getPassword(passwdElmt)



