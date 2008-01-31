cdef public class Range(Widget) [object PyEtk_Range, type PyEtk_Range_Type]:
    def increments_get(self):
        cdef double step
        cdef double page
        etk_range_increments_get(<Etk_Range*>self.obj, &step, &page)
        return (step, page)

    def increments_set(self, double step, double page):
        etk_range_increments_set(<Etk_Range*>self.obj, step, page)

    def page_size_get(self):
        __ret = etk_range_page_size_get(<Etk_Range*>self.obj)
        return (__ret)

    def page_size_set(self, double page_size):
        etk_range_page_size_set(<Etk_Range*>self.obj, page_size)

    def range_get(self):
        cdef double lower
        cdef double upper
        etk_range_range_get(<Etk_Range*>self.obj, &lower, &upper)
        return (lower, upper)

    def range_set(self, double lower, double upper):
        etk_range_range_set(<Etk_Range*>self.obj, lower, upper)

    def value_get(self):
        __ret = etk_range_value_get(<Etk_Range*>self.obj)
        return (__ret)

    def value_set(self, double value):
        __ret = bool(<int> etk_range_value_set(<Etk_Range*>self.obj, value))
        return (__ret)

    property increments:
        def __get__(self):
            return self.increments_get()

        def __set__(self, increments):
            self.increments_set(*increments)

    property page_size:
        def __get__(self):
            return self.page_size_get()

        def __set__(self, page_size):
            self.page_size_set(page_size)

    property range:
        def __get__(self):
            return self.range_get()

        def __set__(self, range):
            self.range_set(*range)

    property value:
        def __get__(self):
            return self.value_get()

        def __set__(self, value):
            self.value_set(value)

    def _set_common_params(self, page_size=None, value=None, increments=None, range=None, **kargs):
        if page_size is not None:
            self.page_size_set(page_size)
        if value is not None:
            self.value_set(value)
        if increments is not None:
            self.increments_set(*increments)
        if range is not None:
            self.range_set(*range)

        if kargs:
            Widget._set_common_params(self, **kargs)

    property VALUE_CHANGED_SIGNAL:
        def __get__(self):
            return ETK_RANGE_VALUE_CHANGED_SIGNAL

    def on_value_changed(self, func, *a, **ka):
        self.connect(self.VALUE_CHANGED_SIGNAL, func, *a, **ka)


class RangeEnums:
    pass
