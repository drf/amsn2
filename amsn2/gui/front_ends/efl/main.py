from constants import *
import ecore
import ecore.evas
import ecore.x

from amsn2.gui import base

class aMSNMainWindow(base.aMSNMainWindow):
    def __init__(self, amsn_core):     
        self._amsn_core = amsn_core

        self._evas = ecore.evas.SoftwareX11(w=WIDTH, h=HEIGHT)
        self._evas.callback_delete_request = self.__on_delete_request
        self._evas.callback_resize = self.__on_resize
        self._evas.callback_show = self.__on_show
        self._evas.title = TITLE
        self._evas.name_class = (WM_NAME, WM_CLASS)
        self._evas.fullscreen = False
        self._evas.size = (WIDTH, HEIGHT)
        self._evas.size_min_set(MIN_WIDTH, MIN_HEIGHT)

    def show(self):
        self._evas.show()

    def hide(self):
        self._evas.hide()
        
    # Private methods
    def __on_show(self, evas_obj):
        self._amsn_core.mainWindowShown()

    def __on_resize(self, evas_obj):
        x, y, w, h = evas_obj.evas.viewport
        size = (w, h)
        for key in evas_obj.data.keys():
            evas_obj.data[key].size = size

    def __on_delete_request(self, evas_obj):
        self._amsn_core.exit()
