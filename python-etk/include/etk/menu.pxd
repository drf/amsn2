cdef extern from "etk_menu.h":
    ####################################################################
    # Signals
    int ETK_MENU_POPPED_DOWN_SIGNAL
    int ETK_MENU_POPPED_UP_SIGNAL

    ####################################################################
    # Structures
    ctypedef struct Etk_Menu

    ####################################################################
    # Functions
    Etk_Widget* etk_menu_new()
    Etk_Menu_Item* etk_menu_parent_item_get(Etk_Menu* __self)
    void etk_menu_popup(Etk_Menu* __self)
    void etk_menu_popup_in_direction(Etk_Menu* __self, Etk_Popup_Direction direction)
    void etk_menu_popup_at_xy(Etk_Menu* __self, int x, int y)
    void etk_menu_popup_at_xy_in_direction(Etk_Menu* __self, int x, int y, Etk_Popup_Direction direction)
    void etk_menu_popdown(Etk_Menu* __self)

#########################################################################
# Objects
cdef public class Menu(MenuShell) [object PyEtk_Menu, type PyEtk_Menu_Type]:
    pass

