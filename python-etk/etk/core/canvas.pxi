cdef public class Canvas(Widget) [object PyEtk_Canvas, type PyEtk_Canvas_Type]:
    def __init__(self, **kargs):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_canvas_new())
        self._set_common_params(**kargs)

    def object_add(self, evas.c_evas.Object object):
        __ret = bool(<int> etk_canvas_object_add(<Etk_Canvas*>self.obj, <evas.c_evas.Evas_Object*>object.obj))
        return (__ret)

    def object_geometry_get(self, evas.c_evas.Object object):
        cdef int x
        cdef int y
        cdef int w
        cdef int h
        etk_canvas_object_geometry_get(<Etk_Canvas*>self.obj, <evas.c_evas.Evas_Object*>object.obj, &x, &y, &w, &h)
        return (x, y, w, h)

    def object_move(self, evas.c_evas.Object object, int x, int y):
        etk_canvas_object_move(<Etk_Canvas*>self.obj, <evas.c_evas.Evas_Object*>object.obj, x, y)

    def object_remove(self, evas.c_evas.Object object):
        etk_canvas_object_remove(<Etk_Canvas*>self.obj, <evas.c_evas.Evas_Object*>object.obj)


class CanvasEnums:
    pass
