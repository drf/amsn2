cdef extern from "etk_range.h":
    ####################################################################
    # Signals
    int ETK_RANGE_VALUE_CHANGED_SIGNAL

    ####################################################################
    # Enumerations
    ####################################################################
    # Structures
    ctypedef struct Etk_Range

    ####################################################################
    # Functions
    Etk_Type* etk_range_type_get()
    void etk_range_increments_get(Etk_Range* __self, double* step, double* page)
    void etk_range_increments_set(Etk_Range* __self, double step, double page)
    double etk_range_page_size_get(Etk_Range* __self)
    void etk_range_page_size_set(Etk_Range* __self, double page_size)
    void etk_range_range_get(Etk_Range* __self, double* lower, double* upper)
    void etk_range_range_set(Etk_Range* __self, double lower, double upper)
    double etk_range_value_get(Etk_Range* __self)
    int etk_range_value_set(Etk_Range* __self, double value)

#########################################################################
# Objects
cdef public class Range(Widget) [object PyEtk_Range, type PyEtk_Range_Type]:
    pass

