cdef public class Window(Toplevel) [object PyEtk_Window, type PyEtk_Window_Type]:
    def __init__(self, **kargs):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_window_new())
        self._set_common_params(**kargs)

    def center_on_window(self, Window window):
        etk_window_center_on_window(<Etk_Window*>self.obj, <Etk_Window*>window.obj)

    def decorated_get(self):
        __ret = bool(<int> etk_window_decorated_get(<Etk_Window*>self.obj))
        return (__ret)

    def decorated_set(self, int decorated):
        etk_window_decorated_set(<Etk_Window*>self.obj, <Etk_Bool>decorated)

    def delete_request(self):
        etk_window_delete_request(<Etk_Window*>self.obj)

    def focused_get(self):
        __ret = bool(<int> etk_window_focused_get(<Etk_Window*>self.obj))
        return (__ret)

    def focused_set(self, int focused):
        etk_window_focused_set(<Etk_Window*>self.obj, <Etk_Bool>focused)

    def fullscreen_get(self):
        __ret = bool(<int> etk_window_fullscreen_get(<Etk_Window*>self.obj))
        return (__ret)

    def fullscreen_set(self, int fullscreen):
        etk_window_fullscreen_set(<Etk_Window*>self.obj, <Etk_Bool>fullscreen)

    def geometry_get(self):
        cdef int x
        cdef int y
        cdef int w
        cdef int h
        etk_window_geometry_get(<Etk_Window*>self.obj, &x, &y, &w, &h)
        return (x, y, w, h)

    def has_alpha_get(self):
        __ret = bool(<int> etk_window_has_alpha_get(<Etk_Window*>self.obj))
        return (__ret)

    def has_alpha_set(self, int has_alpha):
        etk_window_has_alpha_set(<Etk_Window*>self.obj, <Etk_Bool>has_alpha)

    def iconified_get(self):
        __ret = bool(<int> etk_window_iconified_get(<Etk_Window*>self.obj))
        return (__ret)

    def iconified_set(self, int iconified):
        etk_window_iconified_set(<Etk_Window*>self.obj, <Etk_Bool>iconified)

    def lower(self):
        etk_window_lower(<Etk_Window*>self.obj)

    def maximized_get(self):
        __ret = bool(<int> etk_window_maximized_get(<Etk_Window*>self.obj))
        return (__ret)

    def maximized_set(self, int maximized):
        etk_window_maximized_set(<Etk_Window*>self.obj, <Etk_Bool>maximized)

    def modal_for_window(self, Window window):
        etk_window_modal_for_window(<Etk_Window*>self.obj, <Etk_Window*>window.obj)

    def move(self, int x, int y):
        etk_window_move(<Etk_Window*>self.obj, x, y)

    def move_to_mouse(self):
        etk_window_move_to_mouse(<Etk_Window*>self.obj)

    def raise_(self):
        etk_window_raise(<Etk_Window*>self.obj)

    def resize(self, int w, int h):
        etk_window_resize(<Etk_Window*>self.obj, w, h)

    def shaped_get(self):
        __ret = bool(<int> etk_window_shaped_get(<Etk_Window*>self.obj))
        return (__ret)

    def shaped_set(self, int shaped):
        etk_window_shaped_set(<Etk_Window*>self.obj, <Etk_Bool>shaped)

    def skip_pager_hint_get(self):
        __ret = bool(<int> etk_window_skip_pager_hint_get(<Etk_Window*>self.obj))
        return (__ret)

    def skip_pager_hint_set(self, int skip_pager_hint):
        etk_window_skip_pager_hint_set(<Etk_Window*>self.obj, <Etk_Bool>skip_pager_hint)

    def skip_taskbar_hint_get(self):
        __ret = bool(<int> etk_window_skip_taskbar_hint_get(<Etk_Window*>self.obj))
        return (__ret)

    def skip_taskbar_hint_set(self, int skip_taskbar_hint):
        etk_window_skip_taskbar_hint_set(<Etk_Window*>self.obj, <Etk_Bool>skip_taskbar_hint)

    def stacking_get(self):
        __ret = <int> etk_window_stacking_get(<Etk_Window*>self.obj)
        return (__ret)

    def stacking_set(self, int stacking):
        etk_window_stacking_set(<Etk_Window*>self.obj, <Etk_Window_Stacking>stacking)

    def sticky_get(self):
        __ret = bool(<int> etk_window_sticky_get(<Etk_Window*>self.obj))
        return (__ret)

    def sticky_set(self, int sticky):
        etk_window_sticky_set(<Etk_Window*>self.obj, <Etk_Bool>sticky)

    def title_get(self):
        cdef char *__char_ret
        __ret = None
        __char_ret = etk_window_title_get(<Etk_Window*>self.obj)
        if __char_ret != NULL:
            __ret = __char_ret
        return (__ret)

    def title_set(self, char* title):
        etk_window_title_set(<Etk_Window*>self.obj, title)

    def wmclass_set(self, char* window_name, char* window_class):
        etk_window_wmclass_set(<Etk_Window*>self.obj, window_name, window_class)

    property decorated:
        def __get__(self):
            return self.decorated_get()

        def __set__(self, decorated):
            self.decorated_set(decorated)

    property focused:
        def __get__(self):
            return self.focused_get()

        def __set__(self, focused):
            self.focused_set(focused)

    property fullscreen:
        def __get__(self):
            return self.fullscreen_get()

        def __set__(self, fullscreen):
            self.fullscreen_set(fullscreen)

    property geometry:
        def __get__(self):
            return self.geometry_get()

    property has_alpha:
        def __get__(self):
            return self.has_alpha_get()

        def __set__(self, has_alpha):
            self.has_alpha_set(has_alpha)

    property iconified:
        def __get__(self):
            return self.iconified_get()

        def __set__(self, iconified):
            self.iconified_set(iconified)

    property maximized:
        def __get__(self):
            return self.maximized_get()

        def __set__(self, maximized):
            self.maximized_set(maximized)

    property shaped:
        def __get__(self):
            return self.shaped_get()

        def __set__(self, shaped):
            self.shaped_set(shaped)

    property skip_pager_hint:
        def __get__(self):
            return self.skip_pager_hint_get()

        def __set__(self, skip_pager_hint):
            self.skip_pager_hint_set(skip_pager_hint)

    property skip_taskbar_hint:
        def __get__(self):
            return self.skip_taskbar_hint_get()

        def __set__(self, skip_taskbar_hint):
            self.skip_taskbar_hint_set(skip_taskbar_hint)

    property stacking:
        def __get__(self):
            return self.stacking_get()

        def __set__(self, stacking):
            self.stacking_set(stacking)

    property sticky:
        def __get__(self):
            return self.sticky_get()

        def __set__(self, sticky):
            self.sticky_set(sticky)

    property title:
        def __get__(self):
            return self.title_get()

        def __set__(self, title):
            self.title_set(title)

    def _set_common_params(self, decorated=None, focused=None, fullscreen=None, has_alpha=None, iconified=None, maximized=None, shaped=None, skip_pager_hint=None, skip_taskbar_hint=None, stacking=None, sticky=None, title=None, **kargs):
        if decorated is not None:
            self.decorated_set(decorated)
        if focused is not None:
            self.focused_set(focused)
        if fullscreen is not None:
            self.fullscreen_set(fullscreen)
        if has_alpha is not None:
            self.has_alpha_set(has_alpha)
        if iconified is not None:
            self.iconified_set(iconified)
        if maximized is not None:
            self.maximized_set(maximized)
        if shaped is not None:
            self.shaped_set(shaped)
        if skip_pager_hint is not None:
            self.skip_pager_hint_set(skip_pager_hint)
        if skip_taskbar_hint is not None:
            self.skip_taskbar_hint_set(skip_taskbar_hint)
        if stacking is not None:
            self.stacking_set(stacking)
        if sticky is not None:
            self.sticky_set(sticky)
        if title is not None:
            self.title_set(title)

        if kargs:
            Toplevel._set_common_params(self, **kargs)


class WindowEnums(ToplevelEnums):
    NORMAL = ETK_WINDOW_NORMAL
    ABOVE = ETK_WINDOW_ABOVE
    BELOW = ETK_WINDOW_BELOW
