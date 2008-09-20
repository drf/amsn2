cdef extern from "etk_spinner.h":
    ####################################################################
    # Signals

    ####################################################################
    # Enumerations
    ####################################################################
    # Structures
    ctypedef struct Etk_Spinner

    ####################################################################
    # Functions
    Etk_Type* etk_spinner_type_get()
    Etk_Widget* etk_spinner_new(double lower, double upper, double value, double step_increment, double page_increment)
    int etk_spinner_digits_get(Etk_Spinner* __self)
    void etk_spinner_digits_set(Etk_Spinner* __self, int digits)
    int etk_spinner_snap_to_ticks_get(Etk_Spinner* __self)
    void etk_spinner_snap_to_ticks_set(Etk_Spinner* __self, int snap_to_ticks)
    int etk_spinner_wrap_get(Etk_Spinner* __self)
    void etk_spinner_wrap_set(Etk_Spinner* __self, int wrap)

#########################################################################
# Objects
cdef public class Spinner(Range) [object PyEtk_Spinner, type PyEtk_Spinner_Type]:
    pass
