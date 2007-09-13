cdef extern from "etk_toggle_button.h":
    ####################################################################
    # Enumerations
    ####################################################################
    # Structures
    ctypedef struct Etk_Toggle_Button


    ####################################################################
    # Functions
    Etk_Widget* etk_toggle_button_new_with_label(char* label)
    Etk_Type* etk_toggle_button_type_get()
    Etk_Widget* etk_toggle_button_new()
    int etk_toggle_button_active_get(Etk_Toggle_Button* __self)
    void etk_toggle_button_active_set(Etk_Toggle_Button* __self, int active)
    void etk_toggle_button_toggle(Etk_Toggle_Button* __self)

#########################################################################
# Objects
cdef public class ToggleButton(Button) [object PyEtk_Toggle_Button, type PyEtk_Toggle_Button_Type]:
    pass

