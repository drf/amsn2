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
        msg = "Button clicked %d times"
        b = etk.Button(label=msg % counter)
        self._win = etk.Window(title="aMSN", size_request=(MIN_WIDTH,MIN_HEIGHT))
        self._win.on_destroyed(self.__on_delete_request)
        self._win.on_shown(self.__on_show)
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
