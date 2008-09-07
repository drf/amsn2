from constants import *
import ecore
import ecore.evas
import ecore.x
import etk
import skins

from amsn2.gui import base

class aMSNMainWindow(base.aMSNMainWindow):
    def __init__(self, amsn_core):     
        self._amsn_core = amsn_core
        counter = 0
        self._win = etk.Window(title="aMSN", size_request=(MIN_WIDTH,MIN_HEIGHT))
        self._win.on_destroyed(self.__on_delete_request)
        self._win.on_shown(self.__on_show)
        self._win.on_key_down(self.__on_key_down)
        self._win.fullscreen = False
        self._win.wmclass_set(WM_NAME, WM_CLASS)
        self._win.resize(WIDTH, HEIGHT)

    @property
    def _evas(self):
        return self._win.toplevel_evas_get()

    def show(self):
        self._win.show_all()

    def hide(self):
        self._win.hide()
        
    def setTitle(self, text):
        self._win.title_set(text)

    def setMainMenu(self, menu):
        pass
        
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
