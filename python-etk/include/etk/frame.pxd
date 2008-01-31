cdef extern from "etk_frame.h":
    ####################################################################
    # Enumerations
    ####################################################################
    # Structures
    ctypedef struct Etk_Frame

    ####################################################################
    # Functions
    Etk_Type* etk_frame_type_get()
    Etk_Widget* etk_frame_new(char* label)
    char* etk_frame_label_get(Etk_Frame* __self)
    void etk_frame_label_set(Etk_Frame* __self, char* label)

#########################################################################
# Objects
cdef public class Frame(Bin) [object PyEtk_Frame, type PyEtk_Frame_Type]:
    pass

