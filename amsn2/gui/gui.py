
class InvalidFrontEndException(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

    def __str__(self):
        return str(self.message)


class GUIManager(object):
    front_ends = {}
    
    def __init__(self, core, gui_name):
        self._core = core
        self._name = gui_name
        
        if GUIManager.frontEndExists(self._name) is False:
            raise InvalidFrontEndException("Invalid Front End. Available front ends are : " + str(GUIManager.listFrontEnds()))
        else:
            self.gui = GUIManager.front_ends[self._name]
            self.gui = self.gui.load()
        
    @staticmethod
    def registerFrontEnd(name, module):
        GUIManager.front_ends[name] = module
        
    @staticmethod
    def listFrontEnds():
        return GUIManager.front_ends.keys();
    
    @staticmethod
    def frontEndExists(front_end):
        return front_end in GUIManager.listFrontEnds()
   



