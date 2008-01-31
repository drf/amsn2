
# Virtual functions

cdef void _virtual_evas_position_get(Etk_Toplevel *toplevel, int *x, int *y) with gil:
    self = Object_from_instance(<Etk_Object *>toplevel)
    (x[0], y[0]) = self._evas_position_get()

cdef void _virtual_screen_position_get(Etk_Toplevel *toplevel, int *x, int *y) with gil:
    self = Object_from_instance(<Etk_Object *>toplevel)
    (x[0], y[0]) = self._screen_position_get()

cdef void _virtual_size_get(Etk_Toplevel *toplevel, int *w, int *h) with gil:
    self = Object_from_instance(<Etk_Object *>toplevel)
    (w[0], h[0]) = self._size_get()

cdef void _virtual_pointer_set(Etk_Toplevel *toplevel, Etk_Pointer_Type pointer_type) with gil:
    self = Object_from_instance(<Etk_Object *>toplevel)
    self._pointer_set(pointer_type)


cdef public class Toplevel(Bin) [object PyEtk_Toplevel, type PyEtk_Toplevel_Type]:
    cdef object _set_obj(self, Etk_Object *obj):
        cdef Etk_Toplevel *t
        Bin._set_obj(self, obj)
        t = <Etk_Toplevel*>obj

        if getattr3(self.__class__, "_evas_position_get", None) is not None:
            t.evas_position_get = _virtual_evas_position_get

        if getattr3(self.__class__, "_screen_position_get", None) is not None:
            t.screen_position_get = _virtual_screen_position_get

        if getattr3(self.__class__, "_size_get", None) is not None:
            t.size_get = _virtual_size_get

        if getattr3(self.__class__, "_pointer_set", None) is not None:
            t.pointer_set = _virtual_pointer_set

        return self

    def evas_get(self):
        __ret = evas.c_evas._Object_from_instance(<long>etk_toplevel_evas_get(<Etk_Toplevel*>self.obj))
        return (__ret)

    property evas:
        def __get__(self):
            return self.evas_get()

    def evas_position_get(self):
        cdef int x
        cdef int y
        etk_toplevel_evas_position_get(<Etk_Toplevel*>self.obj, &x, &y)
        return (x, y)

    property evas_position:
        def __get__(self):
            return self.evas_position_get()

    def focused_widget_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_toplevel_focused_widget_get(<Etk_Toplevel*>self.obj))
        return (__ret)

    def focused_widget_set(self, Widget widget):
        cdef Etk_Widget *w
        if widget is None:
            w = NULL
        else:
            w = <Etk_Widget*>widget.obj
        etk_toplevel_focused_widget_set(<Etk_Toplevel*>self.obj, w)

    property focused_widget:
        def __get__(self):
            return self.focused_widget_get()

        def __set__(self, value):
            self.focused_widget_set(value)

    def focused_widget_next_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_toplevel_focused_widget_next_get(<Etk_Toplevel*>self.obj))
        return (__ret)

    property focused_widget_next:
        def __get__(self):
            return self.focused_widget_next_get()

    def focused_widget_prev_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_toplevel_focused_widget_prev_get(<Etk_Toplevel*>self.obj))
        return (__ret)

    property focused_widget_prev:
        def __get__(self):
            return self.focused_widget_prev_get()

    def pointer_pop(self, int pointer_type):
        etk_toplevel_pointer_pop(<Etk_Toplevel*>self.obj, <Etk_Pointer_Type>pointer_type)

    def pointer_push(self, int pointer_type):
        etk_toplevel_pointer_push(<Etk_Toplevel*>self.obj, <Etk_Pointer_Type>pointer_type)

    def screen_position_get(self):
        cdef int x
        cdef int y
        etk_toplevel_screen_position_get(<Etk_Toplevel*>self.obj, &x, &y)
        return (x, y)

    property screen_position:
        def __get__(self):
            return self.screen_position_get()

    def size_get(self):
        cdef int w
        cdef int h
        etk_toplevel_size_get(<Etk_Toplevel*>self.obj, &w, &h)
        return (w, h)

    property size:
        def __get__(self):
            return self.size_get()


class ToplevelEnums:
    POINTER_NONE = ETK_POINTER_NONE
    POINTER_DEFAULT = ETK_POINTER_DEFAULT
    POINTER_MOVE = ETK_POINTER_MOVE
    POINTER_H_DOUBLE_ARROW = ETK_POINTER_H_DOUBLE_ARROW
    POINTER_V_DOUBLE_ARROW = ETK_POINTER_V_DOUBLE_ARROW
    POINTER_RESIZE = ETK_POINTER_RESIZE
    POINTER_RESIZE_TL = ETK_POINTER_RESIZE_TL
    POINTER_RESIZE_T = ETK_POINTER_RESIZE_T
    POINTER_RESIZE_TR = ETK_POINTER_RESIZE_TR
    POINTER_RESIZE_R = ETK_POINTER_RESIZE_R
    POINTER_RESIZE_BR = ETK_POINTER_RESIZE_BR
    POINTER_RESIZE_B = ETK_POINTER_RESIZE_B
    POINTER_RESIZE_BL = ETK_POINTER_RESIZE_BL
    POINTER_RESIZE_L = ETK_POINTER_RESIZE_L
    POINTER_TEXT_EDIT = ETK_POINTER_TEXT_EDIT
    POINTER_DND_DROP = ETK_POINTER_DND_DROP
