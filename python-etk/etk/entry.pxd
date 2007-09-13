cdef extern from "etk_entry.h":
    ####################################################################
    # Enumerations
    ctypedef enum Etk_Entry_Image_Position:
        ETK_ENTRY_IMAGE_PRIMARY
        ETK_ENTRY_IMAGE_SECONDARY

    ####################################################################
    # Structures
    ctypedef struct Etk_Entry

    ####################################################################
    # Functions
    Etk_Type* etk_entry_type_get()
    Etk_Widget* etk_entry_new()
    void etk_entry_clear(Etk_Entry* __self)
    void etk_entry_clear_button_add(Etk_Entry* __self)
    Etk_Image* etk_entry_image_get(Etk_Entry* __self, int position)
    void etk_entry_image_highlight_set(Etk_Entry* __self, int position, int highlight)
    void etk_entry_image_set(Etk_Entry* __self, int position, Etk_Image* image)
    int etk_entry_password_mode_get(Etk_Entry* __self)
    void etk_entry_password_mode_set(Etk_Entry* __self, int password_mode)
    char* etk_entry_text_get(Etk_Entry* __self)
    void etk_entry_text_set(Etk_Entry* __self, char* text)

#########################################################################
# Objects
cdef public class Entry(Widget) [object PyEtk_Entry, type PyEtk_Entry_Type]:
    pass

