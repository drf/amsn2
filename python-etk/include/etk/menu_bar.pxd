cdef extern from "etk_menu_bar.h":
    ####################################################################
    # Structures
    ctypedef struct Etk_Menu_Bar

    ####################################################################
    # Functions
    Etk_Widget* etk_menu_bar_new()

#########################################################################
# Objects
cdef public class MenuBar(MenuShell) [object PyEtk_Menu_Bar, type PyEtk_Menu_Bar_Type]:
    pass
