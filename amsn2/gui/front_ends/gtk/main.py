
from amsn2.gui import base

import gtk

class aMSNMainWindow(base.aMSNMainWindow):
    main_win = None
    
    def __init__(self, amsn_core):
        self._amsn_core = amsn_core
        self.main_win = gtk.Window()
        self.main_win.set_size_request(250, 500)
        self.view = None

    def show(self):
        self.main_win.show()
        self._amsn_core.idlerAdd(self.__on_show)
        
    def set_title(self, title):
        self.main_win.set_title(title)
        
    def hide(self):
        self.main_win.hide()
    
    def set_view(self, view):
        current = self.main_win.get_child()
        
        if current:
            self.main_win.remove(current)
        
        self.main_win.add(view)
        self.main_win.show_all()
    
    def __on_show(self):
        self._amsn_core.mainWindowShown()
       
