cdef extern from "etk_string.h":

    ####################################################################
    # Structures
    ctypedef struct Etk_String

    ####################################################################
    # Functions
    Etk_String * etk_string_new (char *value)
    char * etk_string_get (Etk_String *__self)
    Etk_String * etk_string_set (Etk_String *__self, char *value)


#########################################################################
# Objects
cdef public class String(Object) [object PyEtk_String, type PyEtk_String_Type]:
    pass

