cdef public class Menu(MenuShell) [object PyEtk_Menu, type PyEtk_Menu_Type]:
    def __init__(self, **kargs):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_menu_new())

    def parent_item_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_menu_parent_item_get(<Etk_Menu*>self.obj))
        return (__ret)

    def popup(self):
        etk_menu_popup(<Etk_Menu*>self.obj)

    def popup_in_direction(self, direction):
        etk_menu_popup_in_direction(<Etk_Menu*>self.obj, direction)

    def popup_at_xy(self, int x, int y):
        etk_menu_popup_at_xy(<Etk_Menu*>self.obj, x, y)

    def popup_at_xy_in_direction(self, int x, int y, direction):
        etk_menu_popup_at_xy_in_direction(<Etk_Menu*>self.obj, x, y, direction)

    def popdown(self):
        etk_menu_popdown(<Etk_Menu*>self.obj)

    property parent_item:
        def __get__(self):
            return self.parent_item_get()

    property POPPED_DOWN_SIGNAL:
        def __get__(self):
            return ETK_MENU_POPPED_DOWN_SIGNAL

    def on_popped_down(self, func, *a, **ka):
        self.connect(self.POPPED_DOWN_SIGNAL, func, *a, **ka)

    property POPPED_UP_SIGNAL:
        def __get__(self):
            return ETK_MENU_POPPED_UP_SIGNAL

    def on_popped_up(self, func, *a, **ka):
        self.connect(self.POPPED_UP_SIGNAL, func, *a, **ka)
