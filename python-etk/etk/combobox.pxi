cdef public class ComboboxItem(Widget) [object PyEtk_Combobox_Item, type PyEtk_Combobox_Item_Type]:
    def __init__(self, **kargs):
        self._data = None
        self._set_common_params(**kargs)

    def __del__(self):
        if self._data_free is not None and self._data is not None:
            self._data_free(self._data)
        
    def combobox_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_item_combobox_get(<Etk_Combobox_Item*>self.obj))
        return (__ret)

    def data_get(self):
        return self._data

    def data_set(self, data):
        self.data_set_full(data, None)

    def data_set_full(self, data, func):
        if self._data_free is not None and self._data is not None and self._data != data:
            self._data_free(self._data);

        self._data = data
        self._data_free = free_cb

    #def field_get(self, int column):
        # FIXME: unsupported method return
    #    pass

    #def field_set(self, int column, void* value):
        # FIXME: unsupported method arguments
    #    pass

    #def fields_get(self):
    #    etk_combobox_item_fields_get(<Etk_Combobox_Item*>self.obj)

    #def fields_get_valist(self, va_list args):
        # FIXME: unsupported method arguments
    #    pass

    #def fields_set(self):
    #    etk_combobox_item_fields_set(<Etk_Combobox_Item*>self.obj)

    #def fields_set_valist(self, va_list args):
        # FIXME: unsupported method arguments
    #    pass

    def next_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_item_next_get(<Etk_Combobox_Item*>self.obj))
        return (__ret)

    def prev_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_item_prev_get(<Etk_Combobox_Item*>self.obj))
        return (__ret)

    def remove(self):
        etk_combobox_item_remove(<Etk_Combobox_Item*>self.obj)

    property combobox:
        def __get__(self):
            return self.combobox_get()

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

cdef public class Combobox(Widget) [object PyEtk_Combobox, type PyEtk_Combobox_Type]:
    def __init__(self, **kargs):
        if self.obj == NULL:
            build = True
            if build == False:
                self._columns = []
                self._set_obj(<Etk_Object*>etk_combobox_new())
            else:
                self._columns = [ComboboxEnums.LABEL]
                self._set_obj(<Etk_Object*>etk_combobox_new_default())
        self._set_common_params(**kargs)

    def active_item_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_active_item_get(<Etk_Combobox*>self.obj))
        return (__ret)

    def active_item_num_get(self):
        __ret = etk_combobox_active_item_num_get(<Etk_Combobox*>self.obj)
        return (__ret)

    def active_item_set(self, ComboboxItem item):
        etk_combobox_active_item_set(<Etk_Combobox*>self.obj, <Etk_Combobox_Item*>item.obj)

    def build(self):
        return
        etk_combobox_build(<Etk_Combobox*>self.obj)

    def clear(self):
        etk_combobox_clear(<Etk_Combobox*>self.obj)

    def column_add(self, int col_type, int width, int fill_policy, float align):
        return
        etk_combobox_column_add(<Etk_Combobox*>self.obj, <Etk_Combobox_Column_Type>col_type, width, <Etk_Combobox_Fill_Policy>fill_policy, align)

    #def fields_set(self):
    #    etk_combobox_fields_set(<Etk_Combobox*>self.obj)

    #def fields_set_valist(self, va_list args):
        # FIXME: unsupported method arguments
    #    pass

    def first_item_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_first_item_get(<Etk_Combobox*>self.obj))
        return (__ret)

    def item_append(self, value):
        cdef char* val
        val = value
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_item_append(<Etk_Combobox*>self.obj, val))
        return (__ret)

    def item_insert(self, ComboboxItem after, value):
        cdef char* val
        val = value
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_item_insert(<Etk_Combobox*>self.obj, <Etk_Combobox_Item*>after.obj, val))
        return (__ret)

    #def item_insert_valist(self, ComboboxItem after, va_list args):
        # FIXME: unsupported method arguments
    #    pass

    def item_prepend(self, value):
        cdef char* val
        val = value
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_item_prepend(<Etk_Combobox*>self.obj, val))
        return (__ret)

    def items_height_get(self):
        __ret = etk_combobox_items_height_get(<Etk_Combobox*>self.obj)
        return (__ret)

    def items_height_set(self, int items_height):
        etk_combobox_items_height_set(<Etk_Combobox*>self.obj, items_height)

    def last_item_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_last_item_get(<Etk_Combobox*>self.obj))
        return (__ret)

    def nth_item_get(self, int index):
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_nth_item_get(<Etk_Combobox*>self.obj, index))
        return (__ret)

    property active_item:
        def __get__(self):
            return self.active_item_get()

        def __set__(self, active_item):
            self.active_item_set(active_item)

    property active_item_num:
        def __get__(self):
            return self.active_item_num_get()

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


class ComboboxEnums:
    LABEL = ETK_COMBOBOX_LABEL
    IMAGE = ETK_COMBOBOX_IMAGE
    OTHER = ETK_COMBOBOX_OTHER
    NONE = ETK_COMBOBOX_NONE
    EXPAND = ETK_COMBOBOX_EXPAND
    FILL = ETK_COMBOBOX_FILL
    EXPAND_FILL = ETK_COMBOBOX_EXPAND_FILL
