cdef public class Viewport(Bin) [object PyEtk_Viewport, type PyEtk_Viewport_Type]:
    def __init__(self, **kargs):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_viewport_new())
        self._set_common_params(**kargs)


class ViewportEnums:
    pass
