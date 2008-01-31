cdef public class Combobox(Widget) [object PyEtk_Combobox, type PyEtk_Combobox_Type]:
    def __init__(self, columns=None, **kargs):
        if self.obj == NULL:
            if columns is not None:
                self._set_obj(<Etk_Object*>etk_combobox_new())
                self._columns = columns
                self._add_columns_and_build(columns)
            else:
                self._set_obj(<Etk_Object*>etk_combobox_new_default())
                self._columns = [(ComboboxEnums.LABEL, 100,
                                  ComboboxEnums.EXPAND, 0.0)]
        self._set_common_params(**kargs)

    def _add_columns_and_build(self, columns):
        for t, w, f, a in columns:
            etk_combobox_column_add(<Etk_Combobox*>self.obj,
                                    t, w, f, a)
        etk_combobox_build(<Etk_Combobox*>self.obj)

    def active_item_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_active_item_get(
            <Etk_Combobox*>self.obj))
        return (__ret)

    def active_item_num_get(self):
        __ret = etk_combobox_active_item_num_get(<Etk_Combobox*>self.obj)
        return (__ret)

    def active_item_set(self, ComboboxItem item):
        etk_combobox_active_item_set(<Etk_Combobox*>self.obj,
                                     <Etk_Combobox_Item*>item.obj)

    def clear(self):
        etk_combobox_clear(<Etk_Combobox*>self.obj)

    def first_item_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_first_item_get(<Etk_Combobox*>self.obj))
        return (__ret)

    def item_append(self, *args):
        item = Object_from_instance(<Etk_Object*>etk_combobox_item_append_empty(<Etk_Combobox*>self.obj))
        if item and args:
            item.fields_set(*args)
        return item

    def item_insert(self, ComboboxItem after, *args):
        item = Object_from_instance(<Etk_Object*>etk_combobox_item_insert_empty(<Etk_Combobox*>self.obj, <Etk_Combobox_Item*>after.obj))
        if item and args:
            item.fields_set(*args)
        return item

    def item_prepend(self, *args):
        item = Object_from_instance(<Etk_Object*>etk_combobox_item_prepend_empty(<Etk_Combobox*>self.obj))
        if item and args:
            item.fields_set(*args)
        return item

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

    property ITEM_ACTIVATED_SIGNAL:
        def __get__(self):
            return ETK_COMBOBOX_ITEM_ACTIVATED_SIGNAL

    def on_item_activated(self, func, *a, **ka):
        self.connect(self.ITEM_ACTIVATED_SIGNAL, func, *a, **ka)

    property ACTIVE_ITEM_CHANGED_SIGNAL:
        def __get__(self):
            return ETK_COMBOBOX_ACTIVE_ITEM_CHANGED_SIGNAL

    def on_active_item_changed(self, func, *a, **ka):
        self.connect(self.ACTIVE_ITEM_CHANGED_SIGNAL, func, *a, **ka)


cdef void _item_data_free_cb(void *data) with gil:
    cdef ComboboxItem self
    self = <ComboboxItem>data
    self._item_data = None


cdef public class ComboboxItem(Widget) [object PyEtk_Combobox_Item, type PyEtk_Combobox_Item_Type]:
    def __init__(self, **kargs):
        self._item_data = None
        self._set_common_params(**kargs)

    def combobox_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_item_combobox_get(<Etk_Combobox_Item*>self.obj))
        return (__ret)

    def item_data_get(self):
        return self._item_data

    def item_data_set(self, data):
        self._item_data = data
        etk_combobox_item_data_set_full(<Etk_Combobox_Item*>self.obj,
                                        <void*>self, _item_data_free_cb)

    def field_get(self, int column):
        cdef char *__ret

        # XXX: this special case will disappear when Etk_Base comes to life
        if self.combobox._columns[column][0] == ComboboxEnums.LABEL:
            __ret = <char *> etk_combobox_item_field_get(
                                <Etk_Combobox_Item*>self.obj, column)
            if __ret != NULL:
                return __ret
        else:
            o = Object_from_instance(<Etk_Object*>etk_combobox_item_field_get(
                    <Etk_Combobox_Item*>self.obj, column))
            return o

    def field_set(self, int column, value):
        cdef char *s

        ctype = self.combobox._columns[column][0]
        if ctype == ComboboxEnums.LABEL and isinstance(value, basestring):
            s = value
            etk_combobox_item_field_set(<Etk_Combobox_Item*>self.obj,
                                        column, <void*>s)
        elif ctype == ComboboxEnums.IMAGE and isinstance(value, Image):
            self._field_set_widget(column, value)
        elif ctype == ComboboxEnums.OTHER and isinstance(value, Widget):
            self._field_set_widget(column, value)
        else:
            raise TypeError("Column type and value type doesn't match")

    def _field_set_widget(self, int column, Widget value):
        etk_combobox_item_field_set(<Etk_Combobox_Item*>self.obj,
                                    column, <Etk_Widget*>value.obj)

    def fields_get(self):
        return [self.field_get(i) for i in range(0, len(self.combobox._columns))]

    def fields_set(self, *values):
        for i, v in enumerate(values):
            self.field_set(i, v)

    def next_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_item_next_get(
            <Etk_Combobox_Item*>self.obj))
        return (__ret)

    def prev_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_combobox_item_prev_get(
            <Etk_Combobox_Item*>self.obj))
        return (__ret)

    def remove(self):
        etk_combobox_item_remove(<Etk_Combobox_Item*>self.obj)

    property combobox:
        def __get__(self):
            return self.combobox_get()

    property item_data:
        def __get__(self):
            return self.item_data_get()

        def __set__(self, data):
            self.item_data_set(data)

    property fields:
        def __get__(self):
            return self.fields_get()

    property next:
        def __get__(self):
            return self.next_get()

    property prev:
        def __get__(self):
            return self.prev_get()

    def _set_common_params(self, item_data=None, **kargs):
        if item_data is not None:
            self.item_data_set(item_data)

        if kargs:
            Widget._set_common_params(self, **kargs)

    property ACTIVATED_SIGNAL:
        def __get__(self):
            return ETK_COMBOBOX_ITEM_ACTIVATED_SIGNAL

    def on_activated(self, func, *a, **ka):
        self.connect(self.ACTIVATED_SIGNAL, func, *a, **ka)


class ComboboxEnums:
    LABEL = ETK_COMBOBOX_LABEL
    IMAGE = ETK_COMBOBOX_IMAGE
    OTHER = ETK_COMBOBOX_OTHER
    NONE = ETK_COMBOBOX_NONE
    EXPAND = ETK_COMBOBOX_EXPAND
    FILL = ETK_COMBOBOX_FILL
    EXPAND_FILL = ETK_COMBOBOX_EXPAND_FILL
