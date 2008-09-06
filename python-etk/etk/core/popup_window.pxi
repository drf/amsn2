def popdown_all():
    etk_popup_window_popdown_all()

cdef public class PopupWindow(Window) [object PyEtk_Popup_Window, type PyEtk_Popup_Window_Type]:
    cdef object _set_obj(self, Etk_Object *obj):
        cdef Etk_Popup_Window *popup_win
        Window._set_obj(self, obj)
        popup_win = <Etk_Popup_Window*>obj
        return self

    def parent_set(self, parent):
        etk_popup_window_parent_set(<Etk_Popup_Window*>self.obj, <Etk_Popup_Window*>parent.obj)
    
    def parent_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_popup_window_parent_get(<Etk_Popup_Window*>self.obj))
        return (__ret)

    def focused_window_set(self):
        etk_popup_window_focused_window_set(<Etk_Popup_Window*>self.obj)

    def focused_window_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_popup_window_focused_window_get())
        return (__ret)

    def popup(self):
        etk_popup_window_popup(<Etk_Popup_Window*>self.obj)

    def popup_in_direction(self, direction):
        etk_popup_window_popup_in_direction(<Etk_Popup_Window*>self.obj, <Etk_Popup_Direction>direction)

    def popup_at_xy(self, int x, int y):
        etk_popup_window_popup_at_xy(<Etk_Popup_Window*>self.obj, x, y)

    def popup_at_xy_in_direction(self, int x, int y, direction):
        etk_popup_window_popup_at_xy_in_direction(<Etk_Popup_Window*>self.obj, x, y, <Etk_Popup_Direction>direction)

    def popdown(self):
        etk_popup_window_popdown(<Etk_Popup_Window*>self.obj)

    def is_popped_up(self):
        __ret = bool(<int> etk_popup_window_is_popped_up(<Etk_Popup_Window*>self.obj))
        return (__ret)

    property parent:
        def __get__(self):
            return self.parent_get()

        def __set__(self, parent):
            self.parent_set(*parent)

    property POPPED_DOWN_SIGNAL:
        def __get__(self):
            return ETK_POPUP_WINDOW_POPPED_DOWN_SIGNAL
    
    def on_popped_down(self, func, *a, **ka):
        self.connect(self.POPPED_DOWN_SIGNAL, func, *a, **ka)
    
    property POPPED_UP_SIGNAL:
        def __get__(self):
            return ETK_POPUP_WINDOW_POPPED_UP_SIGNAL
    
    def on_popped_up(self, func, *a, **ka):
        self.connect(self.POPPED_UP_SIGNAL, func, *a, **ka)
    
class PopupDirectionEnums:
    BELOW_RIGHT = ETK_POPUP_BELOW_RIGHT
    BELOW_LEFT = ETK_POPUP_BELOW_LEFT
    ABOVE_RIGHT = ETK_POPUP_ABOVE_RIGHT
    ABOVE_LEFT = ETK_POPUP_ABOVE_LEFT
