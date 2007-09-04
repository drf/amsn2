# aMSNPlugin(object)
# Plugin developers should subclass this class in order to register themselves when called by the loadPlugin(plugin_name) proc.
# that.load() will be called when the plugin has been registered by calling plugins.registerPlugin(plugin_obj).
# that.unload() will be called when the plugin is unloaded or the client quits.
# To register for an event call self.registerForEvent(event, callback)
# To de-register call self.unRegisterForEvent(event)
class aMSNPlugin(object):
	# These are called when the plugin is loaded or un-loaded.
	def load(self): pass
	def unload(self): pass
	
	# Used to access the _name or _dir private variables.
	def getName(self):
		return str(self._name)
	def getDir(self):
		return str(self._dir)
	
	# Used to log data.
	def log(self, message):
		plugins.log(self._name, message)
	
	# Used to register/de-register for events.
	def registerForEvent(self, event, callback): pass
	def unRegisterForEvent(self, event): pass
