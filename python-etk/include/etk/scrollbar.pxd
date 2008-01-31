cdef extern from "etk_scrollbar.h":
    ####################################################################
    # Signals

    ####################################################################
    # Enumerations
    ####################################################################
    # Structures
    ctypedef struct Etk_VScrollbar
    ctypedef struct Etk_HScrollbar
    ctypedef struct Etk_Scrollbar

    ####################################################################
    # Functions
    Etk_Type* etk_hscrollbar_type_get()
    Etk_Type* etk_scrollbar_type_get()
    Etk_Type* etk_vscrollbar_type_get()

    Etk_Widget *etk_hscrollbar_new(double lower, double upper, double value,
                                   double step_increment, double page_increment,
                                   double page_size)
    Etk_Widget *etk_vscrollbar_new(double lower, double upper, double value,
                                   double step_increment, double page_increment,
                                   double page_size)


#########################################################################
# Objects
cdef public class Scrollbar(Range) [object PyEtk_Scrollbar, type PyEtk_Scrollbar_Type]:
    pass
cdef public class VScrollbar(Scrollbar) [object PyEtk_VScrollbar, type PyEtk_VScrollbar_Type]:
    pass
cdef public class HScrollbar(Scrollbar) [object PyEtk_HScrollbar, type PyEtk_HScrollbar_Type]:
    pass
