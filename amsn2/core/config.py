


class aMSNConfig:
    def __init__(self):
        self._config = {}

    def getKey(self, key, default = None):
        try:
            return self._config[key]
        except KeyError:
            return default

    def setKey(self, key, value):
        self._config[key] = value
