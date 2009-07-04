
class aMSNBackendManager(object):
    def __init__(self):
        self._backend = None
        self.switchToBackend('nullbackend')

    def setBackendForFunc(self, funcname, backend):
        try:
            f = getattr(backend, funcname)
            self.__setattr__(funcname, f)
        except AttributeError:
            self.__setattr__(funcname, self.__missingFunc)

    def switchToBackend(self, backend):
        try:
            m = __import__(backend, globals(), locals(), [], -1)
        except ImportError:
            m = __import__('defaultbackend', globals(), locals(), [], -1)
            print 'Trying to switch to non existent backend %s, using default instead' % backend
        backend_class = getattr(m, backend)

        del self._backend
        self._backend = backend_class()
        self.current_backend = backend

        self.setBackendForFunc('getPassword', self._backend)
        self.setBackendForFunc('setPassword', self._backend)
        self.setBackendForFunc('saveConfig', self._backend)
        self.setBackendForFunc('loadConfig', self._backend)
        self.setBackendForFunc('loadAccount', self._backend)
        self.setBackendForFunc('loadAccounts', self._backend)
        self.setBackendForFunc('saveAccount', self._backend)
        self.setBackendForFunc('removeAccount', self._backend)

    def __missingFunc(*args):
        print 'Function missing for %s' % self.current_backend


