
from amsn2.gui import base
from bend import Backend

class aMSNMainWindow(base.aMSNMainWindow,Backend):
    def __init__(self, amsn_core):
        Backend.__init__(self,"/tmp/test.in","/tmp/test.out")
        self._amsn_core = amsn_core
        self._amsn_core.timerAdd(1,self.checkEvent)
 
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
