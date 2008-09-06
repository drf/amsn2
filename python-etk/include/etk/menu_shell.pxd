cdef extern from "etk_menu_item.h":
    ctypedef struct Etk_Menu_Item

cdef extern from "etk_menu_shell.h":
    ####################################################################
    # Signals
    int ETK_MENU_SHELL_ITEM_ADDED_SIGNAL
    int ETK_MENU_SHELL_ITEM_REMOVED_SIGNAL
    
    ####################################################################
    # Structures
    ctypedef struct Etk_Menu_Shell

    ####################################################################
    # Functions
    void etk_menu_shell_prepend(Etk_Menu_Shell* __self, Etk_Menu_Item* item)
    void etk_menu_shell_append(Etk_Menu_Shell* __self, Etk_Menu_Item* item)
    void etk_menu_shell_prepend_relative(Etk_Menu_Shell* __self, Etk_Menu_Item* item, Etk_Menu_Item* relative)
    void etk_menu_shell_append_relative(Etk_Menu_Shell* __self, Etk_Menu_Item* item, Etk_Menu_Item* relative)
    void etk_menu_shell_insert(Etk_Menu_Shell* __self, Etk_Menu_Item* item, int position)
    void etk_menu_shell_remove(Etk_Menu_Shell* __self, Etk_Menu_Item* item)
    evas.c_evas.Evas_List* etk_menu_shell_items_get(Etk_Menu_Shell* __self)

#########################################################################
# Objects
cdef public class MenuShell(Widget) [object PyEtk_Menu_Shell, type PyEtk_Menu_Shell_Type]:
    pass

