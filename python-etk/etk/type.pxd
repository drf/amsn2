cdef extern from "etk_type.h":
    ####################################################################
    # Structures
    ctypedef struct Etk_Type

    ####################################################################
    # Functions
    Etk_Type* etk_type_get_from_name(char* name)
    void etk_type_shutdown()
