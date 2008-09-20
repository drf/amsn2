cdef public class Spinner(Range) [object PyEtk_Spinner, type PyEtk_Spinner_Type]:
    def __init__(self, lower=0.0, upper=10.0, value=0.0, step_increment=1.0, page_increment=5.0, **kargs):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_spinner_new(lower, upper, value, step_increment, page_increment))
        self._set_common_params(**kargs)

    def digits_get(self):
        __ret = etk_spinner_digits_get(<Etk_Spinner*>self.obj)
        return (__ret)

    def digits_set(self, int digits):
        etk_spinner_digits_set(<Etk_Spinner*>self.obj, digits)

    def snap_to_ticks_get(self):
        __ret = bool(<int> etk_spinner_snap_to_ticks_get(<Etk_Spinner*>self.obj))
        return (__ret)

    def snap_to_ticks_set(self, int snap_to_ticks):
        etk_spinner_snap_to_ticks_set(<Etk_Spinner*>self.obj, <Etk_Bool>snap_to_ticks)

    def wrap_get(self):
        __ret = bool(<int> etk_spinner_wrap_get(<Etk_Spinner*>self.obj))
        return (__ret)

    def wrap_set(self, int wrap):
        etk_spinner_wrap_set(<Etk_Spinner*>self.obj, <Etk_Bool>wrap)

    property digits:
        def __get__(self):
            return self.digits_get()

        def __set__(self, digits):
            self.digits_set(digits)

    property snap_to_ticks:
        def __get__(self):
            return self.snap_to_ticks_get()

        def __set__(self, snap_to_ticks):
            self.snap_to_ticks_set(snap_to_ticks)

    property wrap:
        def __get__(self):
            return self.wrap_get()

        def __set__(self, wrap):
            self.wrap_set(wrap)

    def _set_common_params(self, digits=None, snap_to_ticks=None, wrap=None, **kargs):
        if digits is not None:
            self.digits_set(digits)
        if snap_to_ticks is not None:
            self.snap_to_ticks_set(snap_to_ticks)
        if wrap is not None:
            self.wrap_set(wrap)

        if kargs:
            Range._set_common_params(self, **kargs)
