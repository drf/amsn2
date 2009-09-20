
from constants import *
import ecore
import ecore.evas
import ecore.x
import elementary

from amsn2.gui import base
from amsn2.core.views import MenuView, MenuItemView

class aMSNWindow(elementary.Window, base.aMSNWindow):
    def __init__(self, amsn_core):
        self._amsn_core = amsn_core
        elementary.Window.__init__(self, "aMSN", elementary.ELM_WIN_BASIC)
        self.resize(WIDTH, HEIGHT)
        self.on_key_down_add(self._on_key_down)
        self.fullscreen = False
        self.name_class_set = (WM_NAME, WM_CLASS)
        #self._has_menu = False

        self._bg = elementary.Background(self)
        self.resize_object_add(self._bg)
        self._bg.size_hint_weight_set(1.0, 1.0)
        self._bg.show()

    @property
    def _evas(self):
        return self.canvas

    def hide(self):
        pass

    def setTitle(self, text):
        self.title_set(text)

    def setMenu(self, menu):
        pass

    def toggleMenu(self):
        pass

    def _on_key_down(self, obj, event):
        pass

