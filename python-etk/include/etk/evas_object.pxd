cdef extern from "etk_evas_object.h":
    ####################################################################
    # Signals

    ####################################################################
    # Enumerations
    ####################################################################
    # Structures
    ctypedef struct Etk_Evas_Object

    ####################################################################
    # Functions
    Etk_Widget* etk_evas_object_new()
    Etk_Widget* etk_evas_object_new_from_object(evas.c_evas.Evas_Object* evas_object)
    void etk_evas_object_set_object(Etk_Evas_Object* __self, evas.c_evas.Evas_Object* evas_object)
    evas.c_evas.Evas_Object* etk_evas_object_get(Etk_Evas_Object* __self)

#########################################################################
# Objects
cdef public class EvasObject(Widget) [object PyEtk_Evas_Object, type PyEtk_Evas_Object_Type]:
    pass
