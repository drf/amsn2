
from amsn2.gui import base

class aMSNMainWindow(base.aMSNMainWindow):
    def __init__(self, amsn_core):
        self._amsn_core = amsn_core

    def show(self):
        self._amsn_core.idlerAdd(self.__on_show)

    def hide(self):
        pass
    
    def setTitle(self,title):
        pass

    def setMenu(self,menu):
        pass

    def __on_show(self):
        self._amsn_core.mainWindowShown()
       
