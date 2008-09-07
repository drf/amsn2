from constants import *
import ecore
import ecore.evas
import ecore.x
import etk
import skins

from amsn2.gui import base
from amsn2.core.views import MenuView, MenuItemView

class aMSNMainWindow(base.aMSNMainWindow):
    def __init__(self, amsn_core):     
        self._amsn_core = amsn_core
        counter = 0
        self._vbox = etk.VBox()
        self._win = etk.Window(title="aMSN",
                               size_request=(MIN_WIDTH,MIN_HEIGHT),
                               child=self._vbox)
        self._win.on_destroyed(self.__on_delete_request)
        self._win.on_shown(self.__on_show)
        self._win.on_key_down(self.__on_key_down)
        self._win.fullscreen = False
        self._win.wmclass_set(WM_NAME, WM_CLASS)
        self._win.resize(WIDTH, HEIGHT)
        self._has_menu = False
        self._vbox.show()

    @property
    def _evas(self):
        return self._win.toplevel_evas_get()

    def show(self):
        self._win.show_all()

    def hide(self):
        self._win.hide()
        
    def setTitle(self, text):
        self._win.title_set(text)

    def setMenu(self, menu):
        if menu is None:
            if self._has_menu:
                #Remove the menubar
                menu_bar = self._vbox.child_get_at(etk.VBox.START, 1)
                menu_bar.parent = None
        else:
            if self._has_menu:
                menu_bar = self._vbox.child_get_at(etk.VBox.START, 1)
                #Clear the menubar:
                for menu_item in menu_bar.items_get:
                    menu_bar.remove(menu_item)
            else:
                menu_bar = etk.MenuBar()
                self._vbox.prepend(menu_bar, etk.VBox.START, etk.VBox.FILL, 0)
            #TODO: improve :)
            for item in menu.items:
                if item.type is MenuItemView.CASCADE_MENU:
                    m = etk.Menu()
                    mi = etk.MenuItem(label=item.label)
                    print item.label
                    for item_ in item.items:
                        if item_.type is MenuItemView.COMMAND:
                            if item_.icon is None:
                                mi_ = etk.MenuItem(label=item_.label)
                            else:
                                mi_ = etk.MenuItemImage(label=item_.label)
                            m.append(mi_)
                            print item_.label
                            #TODO: command
                    mi.submenu = m
                    menu_bar.append(mi)


        
    
    def setChild(self, child):
        obj = self.getChild()
        if obj is not None:
            obj.parent = None
        self._vbox.append(child, etk.VBox.START, etk.VBox.EXPAND_FILL, 0)

    def getChild(self):
        if self._has_menu:
            pos = 2
        else:
            pos = 1
        pass
        return self._vbox.child_get_at(etk.VBox.START, pos)

    # Private methods
    def __on_show(self, evas_obj):
        self._amsn_core.mainWindowShown()

    def __on_delete_request(self, evas_obj):
        self._amsn_core.quit()

    def __on_key_down(self, obj, event):
        if event.keyname in ("F6", "f"):
            self._win.fullscreen = not self._win.fullscreen
        elif event.keyname in ("F5", "b"):
            self._win.decorated = not self._win.decorated
        elif event.keyname == "Escape":
            self._amsn_core.quit()
        #TODO: ^M: show menu or not


