class aMSNPluginSelectorWindow(object):
	def drawWindow(self): pass
	def showWindow(self): pass
	def closeWindow(self): pass
	def getPlugins(self):
		return getPlugins()
	def getPluginsWithStatus(self): 
		return plugins.getPluginsWithStatus()
	def loadPlugin(self, plugin_name): pass
	def unLoadPlugin(self, plugin_name): pass
	def configurePlugin(self, plugin_name): pass

class aMSNPluginConfigurationWindow(object):
	# __init__(self, plugin_name)
	# Calls plugins.findPlugin(plugin_name) to get a plugin.
	# If the plugin is found and is loaded then save an instance of it in self._plugin.
	# We cannot configure unloaded plugins so do not show the window if the plugin isn't found.
	# Then draw the window and show it.
	def __init__(self, plugin_name): pass
	
	# drawWindow(self)
	# Handles pre-loading the window contents before the window is shown.
	def drawWindow(self): pass
	
	# showWindow(self)
	# If the window is drawn then simply show the window.
	def showWindow(self): pass
	
	# closeWindow(self)
	# Handles closing the window. Shouldn't just hide it.
	def closeWindow(self): pass
	
	# getConfig(self)
	# Returns a copy of the plugins config as a keyed array.
	def getConfig(self): pass
	
	# saveConfig(self): pass
	# Saves the config via plugins.saveConfig(plugin_name, data)
	def saveConfig(self, config): pass
