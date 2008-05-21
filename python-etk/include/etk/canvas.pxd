cdef extern from "etk_canvas.h":
    ####################################################################
    # Signals

    ####################################################################
    # Enumerations
    ####################################################################
    # Structures
    ctypedef struct Etk_Canvas

    ####################################################################
    # Functions
    Etk_Type* etk_canvas_type_get()
    Etk_Widget* etk_canvas_new()
    void etk_canvas_child_position_get(Etk_Canvas* __self, Etk_Widget* widget, int* x, int* y)
    void etk_canvas_move(Etk_Canvas* __self, Etk_Widget* widget, int x, int y)
    Etk_Widget* etk_canvas_object_add(Etk_Canvas* __self, evas.c_evas.Evas_Object* evas_object)
    void etk_canvas_put(Etk_Canvas* __self, Etk_Widget* widget, int x, int y)

#########################################################################
# Objects
cdef public class Canvas(Container) [object PyEtk_Canvas, type PyEtk_Canvas_Type]:
    pass

