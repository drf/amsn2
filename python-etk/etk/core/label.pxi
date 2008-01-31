cdef public class Label(Widget) [object PyEtk_Label, type PyEtk_Label_Type]:
    def __init__(self, text=None, **kargs):
        cdef char *ctext
        if self.obj == NULL:
            if text is not None:
                ctext = text
            else:
                ctext = NULL
            self._set_obj(<Etk_Object*>etk_label_new(ctext))
        self._set_common_params(**kargs)

    def alignment_get(self):
        cdef float xalign
        cdef float yalign
        etk_label_alignment_get(<Etk_Label*>self.obj, &xalign, &yalign)
        return (xalign, yalign)

    def alignment_set(self, float xalign, float yalign):
        etk_label_alignment_set(<Etk_Label*>self.obj, xalign, yalign)

    def get(self):
        cdef char *__char_ret
        __ret = None
        __char_ret = etk_label_get(<Etk_Label*>self.obj)
        if __char_ret != NULL:
            __ret = __char_ret
        return (__ret)

    def set(self, char* text):
        etk_label_set(<Etk_Label*>self.obj, text)

    property text:
        def __get__(self):
            return self.get()

        def __set__(self, text):
            self.set(text)

    property alignment:
        def __get__(self):
            return self.alignment_get()

        def __set__(self, alignment):
            self.alignment_set(*alignment)

    def _set_common_params(self, alignment=None, text=None, **kargs):
        if alignment is not None:
            self.alignment_set(*alignment)
        if text is not None:
            self.set(text)

        if kargs:
            Widget._set_common_params(self, **kargs)


class LabelEnums:
    pass
