
from amsn2.gui import base

import common
import skins
import gtk

class aMSNMainWindow(base.aMSNMainWindow):
    """
    @ivar main_win:
    @type main_win: gtk.Window
    """
    main_win = None

    def __init__(self, amsn_core):
        self._amsn_core = amsn_core
        self.main_win = gtk.Window()
        self.main_win.set_default_size(250, 500)
        self.main_win.connect('delete-event', self.__on_close)
        self.main_menu = gtk.MenuBar()
        inner = gtk.VBox()
        inner.pack_start(self.main_menu, False, False)
        self.main_win.add(inner)
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
        @type menu: MenuView
        """
        chldn = self.main_menu.get_children()
        if len(chldn) is not 0:
            for chl in chldn:
                self.main_menu.remove(chl)
        common.createMenuItemsFromView(self.main_menu, menu.items)
        self.main_menu.show()

    def set_view(self, view):
        inner = self.main_win.get_child()
        chldn = inner.get_children()
        for c in chldn:
            if isinstance(c, base.aMSNLoginWindow) or isinstance(c, base.aMSNContactListWindow):
                inner.remove(c)

        inner.pack_start(view)
        self.main_win.show_all()

