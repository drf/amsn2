cdef extern from "etk_combobox.h":
    ####################################################################
    # Signals
    int ETK_COMBOBOX_ITEM_ACTIVATED_SIGNAL
    int ETK_COMBOBOX_ACTIVE_ITEM_CHANGED_SIGNAL
    int ETK_COMBOBOX_ITEM_ACTIVATED_SIGNAL

    ####################################################################
    # Enumerations
    ctypedef enum Etk_Combobox_Column_Type:
        ETK_COMBOBOX_LABEL
        ETK_COMBOBOX_IMAGE
        ETK_COMBOBOX_OTHER

    ctypedef enum Etk_Combobox_Fill_Policy:
        ETK_COMBOBOX_NONE
        ETK_COMBOBOX_EXPAND
        ETK_COMBOBOX_FILL
        ETK_COMBOBOX_EXPAND_FILL

    ####################################################################
    # Structures
    ctypedef struct Etk_Combobox
    ctypedef struct Etk_Combobox_Item
    ctypedef struct Etk_Combobox_Column

    ####################################################################
    # Functions
    Etk_Type* etk_combobox_item_type_get()
    Etk_Widget* etk_combobox_new_default()
    Etk_Type* etk_combobox_type_get()
    Etk_Widget* etk_combobox_new()
    Etk_Combobox_Item* etk_combobox_active_item_get(Etk_Combobox* __self)
    int etk_combobox_active_item_num_get(Etk_Combobox* __self)
    void etk_combobox_active_item_set(Etk_Combobox* __self, Etk_Combobox_Item* item)
    void etk_combobox_build(Etk_Combobox* __self)
    void etk_combobox_clear(Etk_Combobox* __self)
    void etk_combobox_column_add(Etk_Combobox* __self, int col_type, int width, int fill_policy, float align)
    void etk_combobox_fields_set(Etk_Combobox* __self)
    void etk_combobox_fields_set_valist(Etk_Combobox* __self, va_list args)
    Etk_Combobox_Item* etk_combobox_first_item_get(Etk_Combobox* __self)
    Etk_Combobox_Item* etk_combobox_item_append(Etk_Combobox* __self)
    Etk_Combobox_Item* etk_combobox_item_append_empty(Etk_Combobox* __self)
    Etk_Combobox_Item* etk_combobox_item_insert(Etk_Combobox* __self, Etk_Combobox_Item* after)
    Etk_Combobox_Item* etk_combobox_item_insert_empty(Etk_Combobox* __self, Etk_Combobox_Item* after)
    Etk_Combobox_Item* etk_combobox_item_insert_valist(Etk_Combobox* __self, Etk_Combobox_Item* after, va_list args)
    Etk_Combobox_Item* etk_combobox_item_prepend(Etk_Combobox* __self)
    Etk_Combobox_Item* etk_combobox_item_prepend_empty(Etk_Combobox* __self)
    int etk_combobox_items_height_get(Etk_Combobox* __self)
    void etk_combobox_items_height_set(Etk_Combobox* __self, int items_height)
    Etk_Combobox_Item* etk_combobox_last_item_get(Etk_Combobox* __self)
    Etk_Combobox_Item* etk_combobox_nth_item_get(Etk_Combobox* __self, int index)
    Etk_Combobox* etk_combobox_item_combobox_get(Etk_Combobox_Item* __self)
    void* etk_combobox_item_data_get(Etk_Combobox_Item* __self)
    void etk_combobox_item_data_set(Etk_Combobox_Item* __self, void* data)
    void etk_combobox_item_data_set_full(Etk_Combobox_Item* __self, void* data, void (*free_cb)(void *data))
    void* etk_combobox_item_field_get(Etk_Combobox_Item* __self, int column)
    void etk_combobox_item_field_set(Etk_Combobox_Item* __self, int column, void* value)
    void etk_combobox_item_fields_get(Etk_Combobox_Item* __self)
    void etk_combobox_item_fields_get_valist(Etk_Combobox_Item* __self, va_list args)
    void etk_combobox_item_fields_set(Etk_Combobox_Item* __self)
    void etk_combobox_item_fields_set_valist(Etk_Combobox_Item* __self, va_list args)
    Etk_Combobox_Item* etk_combobox_item_next_get(Etk_Combobox_Item* __self)
    Etk_Combobox_Item* etk_combobox_item_prev_get(Etk_Combobox_Item* __self)
    void etk_combobox_item_remove(Etk_Combobox_Item* __self)

#########################################################################
# Objects
cdef public class Combobox(Widget) [object PyEtk_Combobox, type PyEtk_Combobox_Type]:
    pass
cdef public class ComboboxItem(Widget) [object PyEtk_Combobox_Item, type PyEtk_Combobox_Item_Type]:
    pass

