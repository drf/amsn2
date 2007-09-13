cdef public class Frame(Bin) [object PyEtk_Frame, type PyEtk_Frame_Type]:
    def __init__(self, label=None, **kargs):
        cdef char *clabel
        if self.obj == NULL:
            if label is not None:
                clabel = label
            else:
                clabel = NULL
            self._set_obj(<Etk_Object*>etk_frame_new(clabel))
        self._set_common_params(**kargs)

    def label_get(self):
        cdef char *__char_ret
        __ret = None
        __char_ret = etk_frame_label_get(<Etk_Frame*>self.obj)
        if __char_ret != NULL:
            __ret = __char_ret
        return (__ret)

    def label_set(self, char* label):
        etk_frame_label_set(<Etk_Frame*>self.obj, label)

    property label:
        def __get__(self):
            return self.label_get()

        def __set__(self, label):
            self.label_set(label)

    def _set_common_params(self, label=None, **kargs):
        if label is not None:
            self.label_set(label)

        if kargs:
            Bin._set_common_params(self, **kargs)


class FrameEnums:
    pass
