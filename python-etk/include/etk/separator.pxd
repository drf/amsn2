cdef extern from "etk_separator.h":
    ####################################################################
    # Signals

    ####################################################################
    # Enumerations
    ####################################################################
    # Structures
    ctypedef struct Etk_VSeparator
    ctypedef struct Etk_HSeparator
    ctypedef struct Etk_Separator

    ####################################################################
    # Functions
    Etk_Type* etk_hseparator_type_get()
    Etk_Type* etk_separator_type_get()
    Etk_Type* etk_vseparator_type_get()

    Etk_Widget *etk_hseparator_new()
    Etk_Widget *etk_vseparator_new()

#########################################################################
# Objects
cdef public class Separator(Widget) [object PyEtk_Separator, type PyEtk_Separator_Type]:
    pass

cdef public class VSeparator(Separator) [object PyEtk_VSeparator, type PyEtk_VSeparator_Type]:
    pass

cdef public class HSeparator(Separator) [object PyEtk_HSeparator, type PyEtk_HSeparator_Type]:
    pass
