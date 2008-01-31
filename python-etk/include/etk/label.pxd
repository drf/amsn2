cdef extern from "etk_label.h":
    ####################################################################
    # Enumerations
    ####################################################################
    # Structures
    ctypedef struct Etk_Label

    ####################################################################
    # Functions
    Etk_Type* etk_label_type_get()
    Etk_Widget* etk_label_new(char* text)
    void etk_label_alignment_get(Etk_Label* __self, float* xalign, float* yalign)
    void etk_label_alignment_set(Etk_Label* __self, float xalign, float yalign)
    char* etk_label_get(Etk_Label* __self)
    void etk_label_set(Etk_Label* __self, char* text)

#########################################################################
# Objects
cdef public class Label(Widget) [object PyEtk_Label, type PyEtk_Label_Type]:
    pass

