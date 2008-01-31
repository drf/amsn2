cdef public class VSeparator(Separator) [object PyEtk_VSeparator, type PyEtk_VSeparator_Type]:
    def __init__(self, **kargs):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_vseparator_new())
        self._set_common_params(**kargs)


cdef public class HSeparator(Separator) [object PyEtk_HSeparator, type PyEtk_HSeparator_Type]:
    def __init__(self, **kargs):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_hseparator_new())
        self._set_common_params(**kargs)


cdef public class Separator(Widget) [object PyEtk_Separator, type PyEtk_Separator_Type]:
    pass


class SeparatorEnums:
    pass
