cdef extern from "etk_menu_item.h":
    ####################################################################
    # Signals
    int ETK_MENU_ITEM_SELECTED_SIGNAL
    int ETK_MENU_ITEM_UNSELECTED_SIGNAL
    int ETK_MENU_ITEM_ACTIVATED_SIGNAL
    int ETK_MENU_ITEM_CHECK_TOGGLED_SIGNAL

    ####################################################################
    # Structures
    ctypedef struct Etk_Menu_Item
    ctypedef struct Etk_Menu_Item_Separator
    ctypedef struct Etk_Menu_Item_Image
    ctypedef struct Etk_Menu_Item_Check
    ctypedef struct Etk_Menu_Item_Radio

    ####################################################################
    # Functions
    Etk_Widget* etk_menu_item_new()
    Etk_Widget* etk_menu_item_new_with_label(char* label)
    Etk_Widget* etk_menu_item_new_from_stock(Etk_Stock_Id stock_id)
    void etk_menu_item_label_set(Etk_Menu_Item* __self, char* label)
    char* etk_menu_item_label_get(Etk_Menu_Item* __self)
    void etk_menu_item_set_from_stock(Etk_Menu_Item* __self, Etk_Stock_Id stock_id)
    void etk_menu_item_submenu_set(Etk_Menu_Item* __self, Etk_Menu* submenu)
    Etk_Menu* etk_menu_item_submenu_get(Etk_Menu_Item* __self)
    void etk_menu_item_select(Etk_Menu_Item* __self)
    void etk_menu_item_unselect(Etk_Menu_Item* __self)
    void etk_menu_item_activate(Etk_Menu_Item* __self)
    Etk_Widget* etk_menu_item_separator_new()
    Etk_Widget* etk_menu_item_image_new()
    Etk_Widget* etk_menu_item_image_new_with_label(char* label)
    Etk_Widget* etk_menu_item_image_new_from_stock(Etk_Stock_Id stock_id)
    void etk_menu_item_image_set(Etk_Menu_Item_Image* __self, Etk_Image* image)
    Etk_Widget* etk_menu_item_check_new()
    Etk_Widget* etk_menu_item_check_new_with_label(char* label)
    void etk_menu_item_check_active_set(Etk_Menu_Item_Check* __self, Etk_Bool active)
    Etk_Bool etk_menu_item_check_active_get(Etk_Menu_Item_Check* __self)
    Etk_Widget* etk_menu_item_radio_new(evas.c_evas.Evas_List** group)
    Etk_Widget* etk_menu_item_radio_new_from_widget(Etk_Menu_Item_Radio* radio_item)
    Etk_Widget* etk_menu_item_radio_new_with_label_from_widget(char* label, Etk_Menu_Item_Radio* radio_item)
    void etk_menu_item_radio_group_set(Etk_Menu_Item_Radio* __self, evas.c_evas.Evas_List** group)
    evas.c_evas.Evas_List** etk_menu_item_radio_group_get(Etk_Menu_Item_Radio* __self)
    

#########################################################################
# Objects
cdef public class MenuItem(Widget) [object PyEtk_Menu_Item, type PyEtk_Menu_Item_Type]:
    pass
cdef public class MenuItemSeparator(MenuItem) [object PyEtk_Menu_Item_Separator, type PyEtk_Menu_Item_Separator_Type]:
    pass
cdef public class MenuItemImage(MenuItem) [object PyEtk_Menu_Item_Image, type PyEtk_Menu_Item_ImageType]:
    pass
cdef public class MenuItemCheck(MenuItem) [object PyEtk_Menu_Item_Check, type PyEtk_Menu_Item_Check_Type]:
    pass
cdef public class MenuItemRadio(MenuItemCheck) [object PyEtk_Menu_Item_Radio, type PyEtk_Menu_Item_Radio_Type]:
    pass
