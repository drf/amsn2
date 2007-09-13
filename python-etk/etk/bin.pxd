cdef extern from "etk_bin.h":
    ####################################################################
    # Enumerations
    ####################################################################
    # Structures
    ctypedef struct Etk_Bin

    ####################################################################
    # Functions
    Etk_Type* etk_bin_type_get()
    Etk_Widget* etk_bin_child_get(Etk_Bin* __self)
    void etk_bin_child_set(Etk_Bin* __self, Etk_Widget* child)

#########################################################################
# Objects
cdef public class Bin(Container) [object PyEtk_Bin, type PyEtk_Bin_Type]:
    pass

