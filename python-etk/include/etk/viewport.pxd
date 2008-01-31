cdef extern from "etk_viewport.h":
    ####################################################################
    # Signals

    ####################################################################
    # Enumerations
    ####################################################################
    # Structures
    ctypedef struct Etk_Viewport

    ####################################################################
    # Functions
    Etk_Type* etk_viewport_type_get()
    Etk_Widget* etk_viewport_new()

#########################################################################
# Objects
cdef public class Viewport(Bin) [object PyEtk_Viewport, type PyEtk_Viewport_Type]:
    pass

