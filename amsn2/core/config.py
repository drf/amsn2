


class aMSNConfig:
    def __init__(self):
        self._config = {}

    def getKey(self, key, default = None):
        """
        Get a existing config key or a default value in any other case.

        @type key: str
        @param key: name of the config key.
        @type default: Any
        @param default: default value to return if key doesn't exist.
        @rtype: Any
        @return: config key value.
        """

        try:
            return self._config[key]
        except KeyError:
            return default

    def setKey(self, key, value):
        """
        Set a key value

        @type key: str
        @param key: name of the config key.
        @type value: Any
        @param value: value of the key to be set.
        """

        self._config[key] = value
