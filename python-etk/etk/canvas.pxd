cdef extern from "etk_canvas.h":
    ####################################################################
    # Enumerations
    ####################################################################
    # Structures
    ctypedef struct Etk_Canvas

    ####################################################################
    # Functions
    Etk_Type* etk_canvas_type_get()
    Etk_Widget* etk_canvas_new()
    int etk_canvas_object_add(Etk_Canvas* __self, evas.c_evas.Evas_Object* object)
    void etk_canvas_object_geometry_get(Etk_Canvas* __self, evas.c_evas.Evas_Object* object, int* x, int* y, int* w, int* h)
    void etk_canvas_object_move(Etk_Canvas* __self, evas.c_evas.Evas_Object* object, int x, int y)
    void etk_canvas_object_remove(Etk_Canvas* __self, evas.c_evas.Evas_Object* object)

#########################################################################
# Objects
cdef public class Canvas(Widget) [object PyEtk_Canvas, type PyEtk_Canvas_Type]:
    pass

