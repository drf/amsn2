cdef public class ComboboxEntry(Widget) [object PyEtk_Combobox_Entry, type PyEtk_Combobox_Entry_Type]:
    def __init__(self, columns=None, **kargs):
        if self.obj == NULL:
            if columns is not None:
                self._set_obj(<Etk_Object*>etk_combobox_entry_new())
                self._columns = columns
                self._add_columns_and_build(columns)
            else:
                self._set_obj(<Etk_Object*>etk_combobox_entry_new_default())
                self._columns = [(ComboboxEntryEnums.LABEL, 100,
                                  ComboboxEntryEnums.EXPAND, 0.0)]
        self._set_common_params(**kargs)

    def _add_columns_and_build(self, columns):
        for t, w, f, a in columns:
            etk_combobox_entry_column_add(<Etk_Combobox_Entry*>self.obj,
                                          t, w, f, a)
        etk_combobox_entry_build(<Etk_Combobox_Entry*>self.obj)

    def active_item_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_entry_active_item_get(<Etk_Combobox_Entry*>self.obj))
        return (__ret)

    def active_item_num_get(self):
        __ret = etk_combobox_entry_active_item_num_get(<Etk_Combobox_Entry*>self.obj)
        return (__ret)

    def active_item_set(self, ComboboxEntryItem item):
        etk_combobox_entry_active_item_set(<Etk_Combobox_Entry*>self.obj,
                                           <Etk_Combobox_Entry_Item*>item.obj)

    def clear(self):
        etk_combobox_entry_clear(<Etk_Combobox_Entry*>self.obj)

    def entry_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_entry_entry_get(<Etk_Combobox_Entry*>self.obj))
        return (__ret)

    def first_item_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_entry_first_item_get(<Etk_Combobox_Entry*>self.obj))
        return (__ret)

    def is_popped_up(self):
        __ret = bool(<int> etk_combobox_entry_is_popped_up(<Etk_Combobox_Entry*>self.obj))
        return (__ret)

    def item_append(self, *args):
        item = Object_from_instance(<Etk_Object*>etk_combobox_entry_item_append_empty(<Etk_Combobox_Entry*>self.obj))
        if item and args:
            item.fields_set(*args)
        return item

    def item_insert(self, ComboboxEntryItem after, *args):
        item = Object_from_instance(<Etk_Object*>etk_combobox_entry_item_insert_empty(<Etk_Combobox_Entry*>self.obj, <Etk_Combobox_Entry_Item*>after.obj))
        if item and args:
            item.fields_set(*args)
        return item

    def item_prepend(self, *args):
        item = Object_from_instance(<Etk_Object*>etk_combobox_entry_item_prepend_empty(<Etk_Combobox_Entry*>self.obj))
        if item and args:
            item.fields_set(*args)
        return item

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

    property ACTIVE_ITEM_CHANGED_SIGNAL:
        def __get__(self):
            return ETK_COMBOBOX_ENTRY_ACTIVE_ITEM_CHANGED_SIGNAL

    def on_active_item_changed(self, func, *a, **ka):
        self.connect(self.ACTIVE_ITEM_CHANGED_SIGNAL, func, *a, **ka)


cdef void _entry_item_data_free_cb(void *data) with gil:
    cdef ComboboxEntryItem self
    self = <ComboboxEntryItem>data
    self._item_data = None


cdef public class ComboboxEntryItem(Widget) [object PyEtk_Combobox_Entry_Item, type PyEtk_Combobox_Entry_Item_Type]:
    def __init__(self, **kargs):
        self._item_data = None
        self._set_common_params(**kargs)

    def combobox_entry_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_entry_item_combobox_entry_get(<Etk_Combobox_Entry_Item*>self.obj))
        return (__ret)

    def item_data_get(self):
        return self._item_data

    def item_data_set(self, data):
        self._item_data = data
        etk_combobox_entry_item_data_set_full(
                <Etk_Combobox_Entry_Item*>self.obj,
                <void*>self, _entry_item_data_free_cb)

    def field_get(self, int column):
        cdef char *__ret

        # XXX: this special case will disappear when Etk_Base comes to life
        if self.combobox_entry._columns[column][0] == ComboboxEntryEnums.LABEL:
            __ret = <char *> etk_combobox_entry_item_field_get(
                                <Etk_Combobox_Entry_Item*>self.obj, column)
            if __ret != NULL:
                return __ret
        else:
            o = Object_from_instance(
                    <Etk_Object*>etk_combobox_entry_item_field_get(
                    <Etk_Combobox_Entry_Item*>self.obj, column))
            return o

    def field_set(self, int column, value):
        cdef char *s

        ctype = self.combobox_entry._columns[column][0]
        if ctype == ComboboxEntryEnums.LABEL and isinstance(value, basestring):
            s = value
            etk_combobox_entry_item_field_set(
                    <Etk_Combobox_Entry_Item*>self.obj, column, <void*>s)
        elif ctype == ComboboxEntryEnums.IMAGE and isinstance(value, Image):
            self._field_set_widget(column, value)
        elif ctype == ComboboxEntryEnums.OTHER and isinstance(value, Widget):
            self._field_set_widget(column, value)
        else:
            raise TypeError("Column type and value type doesn't match")

    def _field_set_widget(self, int column, Widget value):
        etk_combobox_entry_item_field_set(
                <Etk_Combobox_Entry_Item*>self.obj,
                column, <Etk_Widget*>value.obj)

    def fields_get(self):
        return [self.field_get(i) for i in range(0, len(self.combobox._columns))]

    def fields_set(self, *values):
        for i, v in enumerate(values):
            self.field_set(i, v)

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

    property item_data:
        def __get__(self):
            return self.data_get()

        def __set__(self, data):
            self.data_set(data)

    property fields:
        def __get__(self):
            return self.fields_get()

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


class ComboboxEntryEnums:
    LABEL = ETK_COMBOBOX_ENTRY_LABEL
    IMAGE = ETK_COMBOBOX_ENTRY_IMAGE
    OTHER = ETK_COMBOBOX_ENTRY_OTHER
    NONE = ETK_COMBOBOX_ENTRY_NONE
    EXPAND = ETK_COMBOBOX_ENTRY_EXPAND
    FILL = ETK_COMBOBOX_ENTRY_FILL
    EXPAND_FILL = ETK_COMBOBOX_ENTRY_EXPAND_FILL
