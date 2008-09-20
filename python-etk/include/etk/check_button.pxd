cdef extern from "etk_check_button.h":
    ####################################################################
    # Signals
    ####################################################################
    # Enumerations
    ####################################################################
    # Structures
    ctypedef struct Etk_Check_Button

    ####################################################################
    # Functions
    Etk_Type* etk_check_button_type_get()
    Etk_Widget* etk_check_button_new()
    Etk_Widget* etk_check_button_new_with_label(char *label)

#########################################################################
# Objects
cdef public class CheckButton(ToggleButton) [object PyEtk_Check_Button, type PyEtk_Check_Button_Type]:
    pass
