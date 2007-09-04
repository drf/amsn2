aMSN Plugins
============
ToDo: I need to figure out how to get an instance of the plugin after importing the module. The instance can then be registered by plugins.registerPlugin(instance).

example_plugin:
import plugins

class ExamplePlugin(plugins.aMSNPlugin):
	def load(self):
		self.log('Loading...')
		self.registerForEvent('someevent', self.someEventCallback)
	
	def unload(self):
		self.log('Unloading...')
	
	def someEventCallback(self, event, params):
		self.log('Test event called...')
		return params