# plugins module for amsn2
"""
Plugins with amsn2 will be a subclass of the aMSNPlugin() class.
When this module is initially imported it should load the plugins from the last session. Done in the init() proc.
Then the GUI should call plugins.loadPlugin(name) or plugins.unLoadPlugin(name) in order to deal with plugins.
"""

# init()
# Called when the plugins module is imported (only for the first time).
# Should find plugins and populate a list ready for getPlugins().
# Should also auto-update all plugins.
def init(): pass

# loadPlugin(plugin_name)
# Called (by the GUI or from init()) to load a plugin. plugin_name as set in plugin's XML (or from getPlugins()).
# This loads the module for the plugin. The module is then responsible for calling plugins.registerPlugin(instance).
def loadPlugin(plugin_name): pass

# unLoadPlugin(plugin_name)
# Called to unload a plugin. Name is name as set in plugin's XML.
def unLoadPlugin(plugin_name): pass

# registerPlugin(plugin_instance)
# Saves the instance of the plugin, and registers it in the loaded list.
def registerPlugin(plugin_instance): pass

# getPlugins()
# Returns a list of all available plugins, as in ['Plugin 1', 'Plugin 2']
def getPlugins(): pass

# getPluginsWithStatus()
# Returns a list with a list item for each plugin with the plugin's name, and Loaded or NotLoaded either way.
# IE: [['Plugin 1', 'Loaded'], ['Plugin 2', 'NotLoaded']]
def getPluginsWithStatus(): pass

# getLoadedPlugins()
# Returns a list of loaded plugins. as in ['Plugin 1', 'Plugin N']
def getLoadedPlugins(): pass

# findPlugin(plugin_name)
# Retruns the running instance of the plugin with name plugin_name, or None if not found.
def findPlugin(plugin_name): pass

# saveConfig(plugin_name, data)
def saveConfig(plugin_name, data): pass

# Calls the init procedure.
# Will only be called on the first import (thanks to python).
init()
