cdef public class Canvas(Container) [object PyEtk_Canvas, type PyEtk_Canvas_Type]:
    def __init__(self, **kargs):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_canvas_new())
        self._set_common_params(**kargs)

    def child_position_get(self, Widget widget):
        cdef int x
        cdef int y
        etk_canvas_child_position_get(<Etk_Canvas*>self.obj, <Etk_Widget*>widget.obj, &x, &y)
        return (x, y)

    def move(self, Widget widget, int x, int y):
        etk_canvas_move(<Etk_Canvas*>self.obj, <Etk_Widget*>widget.obj, x, y)

    def object_add(self, evas.c_evas.Object evas_object):
        __ret = Object_from_instance(<Etk_Object*>etk_canvas_object_add(<Etk_Canvas*>self.obj, <evas.c_evas.Evas_Object*>evas_object.obj))
        return (__ret)

    def put(self, Widget widget, int x, int y):
        etk_canvas_put(<Etk_Canvas*>self.obj, <Etk_Widget*>widget.obj, x, y)


class CanvasEnums:
    pass
