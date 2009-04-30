
from amsn2.gui import base

import skins
import gtk

class aMSNMainWindow(base.aMSNMainWindow):
    main_win = None
    
    def __init__(self, amsn_core):
        self._amsn_core = amsn_core
        self.main_win = gtk.Window()
        self.main_win.set_default_size(250, 500)
        self.main_win.connect('delete-event', self.__on_close)
        self.view = None
        
    def __on_show(self):
        self._amsn_core.mainWindowShown()
        
    def __on_close(self, widget, event):
        self._amsn_core.quit()

    def show(self):
        self.main_win.show()
        self._amsn_core.idlerAdd(self.__on_show)
        
    def setTitle(self, title):
        self.main_win.set_title(title)
        
    def hide(self):
        self.main_win.hide()
    
    def setMenu(self, menu):
        """ This will allow the core to change the current window's main menu
        @menu : a MenuView
        """
        pass
        
    def set_view(self, view):
        current = self.main_win.get_child()
        
        if current:
            self.main_win.remove(current)
        
        self.main_win.add(view)
        self.main_win.show_all()
       
