cdef public class Alignment(Bin) [object PyEtk_Alignment, type PyEtk_Alignment_Type]:
    def __init__(self, xalign=0, yalign=0, xscale=0, yscale=0, **kargs):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_alignment_new(xalign, yalign,
                                                         xscale, yscale))
        self._set_common_params(**kargs)

    def get(self):
        cdef float xalign
        cdef float yalign
        cdef float xscale
        cdef float yscale
        etk_alignment_get(<Etk_Alignment*>self.obj, &xalign, &yalign, &xscale, &yscale)
        return (xalign, yalign, xscale, yscale)

    def set(self, float xalign, float yalign, float xscale, float yscale):
        etk_alignment_set(<Etk_Alignment*>self.obj, xalign, yalign, xscale, yscale)


class AlignmentEnums:
    pass
