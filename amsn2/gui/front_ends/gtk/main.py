
from amsn2.gui import base
from amsn2.core.views import MenuItemView

import skins
import gtk

class aMSNMainWindow(base.aMSNMainWindow):
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
        self._createMenuItemsFromView(self.main_menu, menu.items)
        self.main_menu.show()

    def _createMenuItemsFromView(self, menu, items):
        # TODO: images & radio groups, for now only basic representation
        for item in items:
            if item.type is MenuItemView.COMMAND:
                it = gtk.MenuItem(item.label)
                it.connect("activate", lambda i, item: item.command(), item )
                it.show()
                menu.append(it)
            elif item.type is MenuItemView.CASCADE_MENU:
                men = gtk.Menu()
                it = gtk.MenuItem(item.label)
                self._createMenuItemsFromView(men, item.items)
                it.set_submenu(men)
                it.show()
                menu.append(it)
            elif item.type is MenuItemView.SEPARATOR:
                it = gtk.SeperatorMenuItem()
                it.show()
                menu.append(it)
            elif item.type is MenuItemView.CHECKBUTTON:
                it = gtk.CheckMenuItem(item.label)
                if item.checkbox:
                    it.set_active()
                it.show()
                menu.append(it)
            elif item.type is MenuItemView.RADIOBUTTON:
                it = gtk.RadioMenuItem(item.label)
                it.show()
                menu.append(it)
            elif item.type is MenuItemView.RADIOBUTTONGROUP:
                pass
    def set_view(self, view):
        inner = self.main_win.get_child()
        chldn = inner.get_children()
        for c in chldn:
            if isinstance(c, base.aMSNLoginWindow) or isinstance(c, base.aMSNContactListWindow):
                inner.remove(c)

        inner.pack_start(view)
        self.main_win.show_all()

