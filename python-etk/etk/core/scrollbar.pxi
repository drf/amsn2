cdef public class VScrollbar(Scrollbar) [object PyEtk_VScrollbar, type PyEtk_VScrollbar_Type]:
    def __init__(self, lower, upper, value, step_increment, page_increment,
                 page_size, **kargs):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_vscrollbar_new(lower, upper, value,
                                                          step_increment,
                                                          page_increment,
                                                          page_size))
        self._set_common_params(**kargs)


cdef public class HScrollbar(Scrollbar) [object PyEtk_HScrollbar, type PyEtk_HScrollbar_Type]:
    def __init__(self, lower, upper, value, step_increment, page_increment,
                 page_size, **kargs):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_hscrollbar_new(lower, upper, value,
                                                          step_increment,
                                                          page_increment,
                                                          page_size))
        self._set_common_params(**kargs)


cdef public class Scrollbar(Range) [object PyEtk_Scrollbar, type PyEtk_Scrollbar_Type]:
    pass


class ScrollbarEnums:
    pass
