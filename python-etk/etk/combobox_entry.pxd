cdef extern from "etk_combobox_entry.h":
    ####################################################################
    # Enumerations
    ctypedef enum Etk_Combobox_Entry_Column_Type:
        ETK_COMBOBOX_ENTRY_LABEL
        ETK_COMBOBOX_ENTRY_IMAGE
        ETK_COMBOBOX_ENTRY_OTHER

    ctypedef enum Etk_Combobox_Entry_Fill_Policy:
        ETK_COMBOBOX_ENTRY_NONE
        ETK_COMBOBOX_ENTRY_EXPAND
        ETK_COMBOBOX_ENTRY_FILL
        ETK_COMBOBOX_ENTRY_EXPAND_FILL

    ####################################################################
    # Structures
    ctypedef struct Etk_Combobox_Entry_Item
    ctypedef struct Etk_Combobox_Entry
    ctypedef struct Etk_Combobox_Entry_Column

    ####################################################################
    # Functions
    Etk_Type* etk_combobox_entry_item_type_get()
    Etk_Widget* etk_combobox_entry_new_default()
    Etk_Type* etk_combobox_entry_type_get()
    Etk_Combobox_Entry* etk_combobox_entry_item_combobox_entry_get(Etk_Combobox_Entry_Item* __self)
    void* etk_combobox_entry_item_data_get(Etk_Combobox_Entry_Item* __self)
    void etk_combobox_entry_item_data_set(Etk_Combobox_Entry_Item* __self, void* data)
    void etk_combobox_entry_item_data_set_full(Etk_Combobox_Entry_Item* __self, void* data)
    void* etk_combobox_entry_item_field_get(Etk_Combobox_Entry_Item* __self, int column)
    void etk_combobox_entry_item_field_set(Etk_Combobox_Entry_Item* __self, int column, void* value)
    void etk_combobox_entry_item_fields_get(Etk_Combobox_Entry_Item* __self)
    void etk_combobox_entry_item_fields_get_valist(Etk_Combobox_Entry_Item* __self, va_list args)
    void etk_combobox_entry_item_fields_set(Etk_Combobox_Entry_Item* __self)
    void etk_combobox_entry_item_fields_set_valist(Etk_Combobox_Entry_Item* __self, va_list args)
    Etk_Combobox_Entry_Item* etk_combobox_entry_item_next_get(Etk_Combobox_Entry_Item* __self)
    Etk_Combobox_Entry_Item* etk_combobox_entry_item_prev_get(Etk_Combobox_Entry_Item* __self)
    void etk_combobox_entry_item_remove(Etk_Combobox_Entry_Item* __self)
    Etk_Widget* etk_combobox_entry_new()
    Etk_Combobox_Entry_Item* etk_combobox_entry_active_item_get(Etk_Combobox_Entry* __self)
    int etk_combobox_entry_active_item_num_get(Etk_Combobox_Entry* __self)
    void etk_combobox_entry_active_item_set(Etk_Combobox_Entry* __self, Etk_Combobox_Entry_Item* item)
    void etk_combobox_entry_build(Etk_Combobox_Entry* __self)
    void etk_combobox_entry_clear(Etk_Combobox_Entry* __self)
    void etk_combobox_entry_column_add(Etk_Combobox_Entry* __self, int col_type, int width, int fill_policy, float align)
    Etk_Widget* etk_combobox_entry_entry_get(Etk_Combobox_Entry* __self)
    Etk_Combobox_Entry_Item* etk_combobox_entry_first_item_get(Etk_Combobox_Entry* __self)
    int etk_combobox_entry_is_popped_up(Etk_Combobox_Entry* __self)
    Etk_Combobox_Entry_Item* etk_combobox_entry_item_append(Etk_Combobox_Entry* __self, ...)
    Etk_Combobox_Entry_Item* etk_combobox_entry_item_insert(Etk_Combobox_Entry* __self, Etk_Combobox_Entry_Item* after, ...)
    Etk_Combobox_Entry_Item* etk_combobox_entry_item_insert_valist(Etk_Combobox_Entry* __self, Etk_Combobox_Entry_Item* after, va_list args)
    Etk_Combobox_Entry_Item* etk_combobox_entry_item_prepend(Etk_Combobox_Entry* __self, ...)
    int etk_combobox_entry_items_height_get(Etk_Combobox_Entry* __self)
    void etk_combobox_entry_items_height_set(Etk_Combobox_Entry* __self, int items_height)
    Etk_Combobox_Entry_Item* etk_combobox_entry_last_item_get(Etk_Combobox_Entry* __self)
    Etk_Combobox_Entry_Item* etk_combobox_entry_nth_item_get(Etk_Combobox_Entry* __self, int index)
    void etk_combobox_entry_pop_down(Etk_Combobox_Entry* __self)
    void etk_combobox_entry_pop_up(Etk_Combobox_Entry* __self)

#########################################################################
# Objects
cdef public class ComboboxEntry_Item(Widget) [object PyEtk_Combobox_Entry_Item, type PyEtk_Combobox_Entry_Item_Type]:
    pass
cdef public class ComboboxEntry(Widget) [object PyEtk_Combobox_Entry, type PyEtk_Combobox_Entry_Type]:
    pass

