cdef extern from "etk_type.h":
    ####################################################################
    # Structures
    ctypedef struct Etk_Type

    ####################################################################
    # Functions
    Etk_Type* etk_type_get_from_name(char* name)
    void etk_type_shutdown()
    Etk_Signal *etk_type_signal_get(Etk_Type *type, int signal_code)
    Etk_Signal *etk_type_signal_get_by_name(Etk_Type *type, char *signal_name)
