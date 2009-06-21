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
        self.switchToBackend('nullbackend')

    def setBackendForFunc(self, funcname, backendname):
        try:
            m = __import__(backendname, globals(), locals(), [], -1)
        except ImportError:
            m = __import__('defaultbackend', globals(), locals(), [], -1)
        try:
            f = getattr(m, funcname)
            self.__setattr__(funcname, f)
        except AttributeError:
            self.__setattr__(funcname, self.__missingFunc)

    def switchToBackend(self, backend):
        self.setBackendForFunc('getPassword', backend)
        self.setBackendForFunc('setPassword', backend)
        self.setBackendForFunc('saveConfig',  backend)
        self.setBackendForFunc('loadConfig',  backend)

    def __missingFunc(*args):
        print 'Function not implemented for this backend'

