cdef public class ComboboxEntry_Item(Widget) [object PyEtk_Combobox_Entry_Item, type PyEtk_Combobox_Entry_Item_Type]:
    def __init__(self, **kargs):
        self._data = None
        self._set_common_params(**kargs)

    def __del__(self):
        if self._data_free is not None and self._data is not None:
            self._data_free(self._data)
            
    def combobox_entry_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_entry_item_combobox_entry_get(<Etk_Combobox_Entry_Item*>self.obj))
        return (__ret)

    def data_get(self):
        return self._data

    def data_set(self, data):
        self.data_set_full(data, None)

    def data_set_full(self, data, free_cb):
        if self._data_free is not None and self._data is not None and self._data != data:
            self._data_free(self._data);

        self._data = data
        self._data_free = free_cb

    #cdef void * field_get(self, int column):
    #    return etk_combobox_entry_item_field_get
        # FIXME: unsupported method return
    #    pass

    #def field_set(self, int column, void* value):
        # FIXME: unsupported method arguments
    #    pass

    #def fields_get(self):
    #    etk_combobox_entry_item_fields_get(<Etk_Combobox_Entry_Item*>self.obj)

    #def fields_get_valist(self, va_list args):
        # FIXME: unsupported method arguments
    #    pass

    #def fields_set(self):
    #    etk_combobox_entry_item_fields_set(<Etk_Combobox_Entry_Item*>self.obj)

    #def fields_set_valist(self, va_list args):
        # FIXME: unsupported method arguments
    #    pass

    def next_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_entry_item_next_get(<Etk_Combobox_Entry_Item*>self.obj))
        return (__ret)

    def prev_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_entry_item_prev_get(<Etk_Combobox_Entry_Item*>self.obj))
        return (__ret)

    def remove(self):
        etk_combobox_entry_item_remove(<Etk_Combobox_Entry_Item*>self.obj)

    property combobox_entry:
        def __get__(self):
            return self.combobox_entry_get()

    property data:
        def __get__(self):
            return self.data_get()

        def __set__(self, data):
            self.data_set(data)

    #property fields:
    #    def __get__(self):
    #        return self.fields_get()

    property next:
        def __get__(self):
            return self.next_get()

    property prev:
        def __get__(self):
            return self.prev_get()

    def _set_common_params(self, data=None, **kargs):
        if data is not None:
            self.data_set(data)

        if kargs:
            Widget._set_common_params(self, **kargs)

cdef public class ComboboxEntry(Widget) [object PyEtk_Combobox_Entry, type PyEtk_Combobox_Entry_Type]:
    def __init__(self, build=False, **kargs):
        if self.obj == NULL:
            build = True
            if build == False:
                self._columns = []
                self._set_obj(<Etk_Object*>etk_combobox_entry_new())
            else:
                self._columns = [ComboboxEntryEnums.LABEL]
                self._set_obj(<Etk_Object*>etk_combobox_entry_new_default())
        self._set_common_params(**kargs)

    def active_item_get(self):
        __ret = Object_from_instance(<Etk_Object *>etk_combobox_entry_active_item_get(<Etk_Combobox_Entry*>self.obj))
        return (__ret)

    def active_item_num_get(self):
        __ret = etk_combobox_entry_active_item_num_get(<Etk_Combobox_Entry*>self.obj)
        return (__ret)

    def active_item_set(self, ComboboxEntry_Item item):
        etk_combobox_entry_active_item_set(<Etk_Combobox_Entry*>self.obj, <Etk_Combobox_Entry_Item*>item.obj)

    def build(self):
        return
        etk_combobox_entry_build(<Etk_Combobox_Entry*>self.obj)

    def clear(self):
        etk_combobox_entry_clear(<Etk_Combobox_Entry*>self.obj)

    def column_add(self, int col_type, int width, int fill_policy, float align):
        return
        self._columns.append(col_type)
        etk_combobox_entry_column_add(<Etk_Combobox_Entry*>self.obj, <Etk_Combobox_Entry_Column_Type>col_type, width, <Etk_Combobox_Entry_Fill_Policy>fill_policy, align)

    def entry_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_entry_entry_get(<Etk_Combobox_Entry*>self.obj))
        return (__ret)

    def first_item_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_entry_first_item_get(<Etk_Combobox_Entry*>self.obj))
        return (__ret)

    def is_popped_up(self):
        __ret = bool(<int> etk_combobox_entry_is_popped_up(<Etk_Combobox_Entry*>self.obj))
        return (__ret)

    def item_append(self, value):
        cdef char* val
        val = value
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_entry_item_append(<Etk_Combobox_Entry*>self.obj, val))
        return (__ret)

    def item_insert(self, ComboboxEntry_Item after, value):
        cdef char* val
        val = value
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_entry_item_insert(<Etk_Combobox_Entry*>self.obj, <Etk_Combobox_Entry_Item*>after.obj, val))
        return (__ret)

    #def item_insert_valist(self, ComboboxEntry_Item after, va_list args):
        # FIXME: unsupported method arguments
    #    pass

    def item_prepend(self, value):
        cdef char* val
        val = value
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_entry_item_prepend(<Etk_Combobox_Entry*>self.obj, val))
        return (__ret)

    def items_height_get(self):
        __ret = etk_combobox_entry_items_height_get(<Etk_Combobox_Entry*>self.obj)
        return (__ret)

    def items_height_set(self, int items_height):
        etk_combobox_entry_items_height_set(<Etk_Combobox_Entry*>self.obj, items_height)

    def last_item_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_entry_last_item_get(<Etk_Combobox_Entry*>self.obj))
        return (__ret)

    def nth_item_get(self, int index):
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_entry_nth_item_get(<Etk_Combobox_Entry*>self.obj, index))
        return (__ret)

    def pop_down(self):
        etk_combobox_entry_pop_down(<Etk_Combobox_Entry*>self.obj)

    def pop_up(self):
        etk_combobox_entry_pop_up(<Etk_Combobox_Entry*>self.obj)

    property active_item:
        def __get__(self):
            return self.active_item_get()

        def __set__(self, active_item):
            self.active_item_set(active_item)

    property active_item_num:
        def __get__(self):
            return self.active_item_num_get()

    property entry:
        def __get__(self):
            return self.entry_get()

    property first_item:
        def __get__(self):
            return self.first_item_get()

    property items_height:
        def __get__(self):
            return self.items_height_get()

        def __set__(self, items_height):
            self.items_height_set(items_height)

    property last_item:
        def __get__(self):
            return self.last_item_get()

    def _set_common_params(self, active_item=None, items_height=None, **kargs):
        if active_item is not None:
            self.active_item_set(active_item)
        if items_height is not None:
            self.items_height_set(items_height)

        if kargs:
            Widget._set_common_params(self, **kargs)


class ComboboxEntryEnums:
    LABEL = ETK_COMBOBOX_ENTRY_LABEL
    IMAGE = ETK_COMBOBOX_ENTRY_IMAGE
    OTHER = ETK_COMBOBOX_ENTRY_OTHER
    NONE = ETK_COMBOBOX_ENTRY_NONE
    EXPAND = ETK_COMBOBOX_ENTRY_EXPAND
    FILL = ETK_COMBOBOX_ENTRY_FILL
    EXPAND_FILL = ETK_COMBOBOX_ENTRY_EXPAND_FILL
