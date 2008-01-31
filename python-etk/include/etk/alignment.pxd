cdef extern from "etk_alignment.h":
    ####################################################################
    # Signals

    ####################################################################
    # Enumerations
    ####################################################################
    # Structures
    ctypedef struct Etk_Alignment

    ####################################################################
    # Functions
    Etk_Type* etk_alignment_type_get()
    Etk_Widget* etk_alignment_new(float xalign, float yalign, float xscale, float yscale)
    void etk_alignment_get(Etk_Alignment* __self, float* xalign, float* yalign, float* xscale, float* yscale)
    void etk_alignment_set(Etk_Alignment* __self, float xalign, float yalign, float xscale, float yscale)

#########################################################################
# Objects
cdef public class Alignment(Bin) [object PyEtk_Alignment, type PyEtk_Alignment_Type]:
    pass

