cimport evas.c_evas

cdef void _for_each_cb(Etk_Widget *child, void *data) with gil:
    func, args, kargs = <object>data
    c = Object_from_instance(<Etk_Object*>child)
    try:
        func(c, *args, **kargs)
    except Exception, e:
        import traceback
        traceback.print_exc()


cdef void _virtual_child_add(Etk_Container *container, Etk_Widget *widget) \
        with gil:
    self = Object_from_instance(<Etk_Object *>container)
    obj = Object_from_instance(<Etk_Object *>widget)
    self._child_add(obj)

cdef void _virtual_child_remove(Etk_Container *container, Etk_Widget *widget) \
        with gil:
    self = Object_from_instance(<Etk_Object *>container)
    obj = Object_from_instance(<Etk_Object *>widget)
    self._child_remove(obj)

cdef Evas_List *_virtual_children_get(Etk_Container *container) \
        with gil:
    cdef Evas_List* lst
    self = Object_from_instance(<Etk_Object *>container)
    children = self._children_get()
    lst = NULL

    for c in children:
        cobj = c._get_obj()
        if cobj:
            lst = evas.c_evas.evas_list_append(lst, <Etk_Widget*>cobj)

    return lst

cdef public class Container(Widget) [object PyEtk_Container, type PyEtk_Container_Type]:
    cdef object _set_obj(self, Etk_Object *obj):
        cdef Etk_Container *c
        Widget._set_obj(self, obj)
        c = <Etk_Container*>obj

        if getattr3(self.__class__, "_child_add", None) is not None:
            c.child_add = _virtual_child_add

        if getattr3(self.__class__, "_child_remove", None) is not None:
            c.child_remove = _virtual_child_remove

        if getattr3(self.__class__, "_children_get", None) is not None:
            c.children_get = _virtual_children_get

        return self

    def add(self, Widget widget):
        etk_container_add(<Etk_Container*>self.obj, <Etk_Widget*>widget.obj)

    def border_width_get(self):
        __ret = etk_container_border_width_get(<Etk_Container*>self.obj)
        return (__ret)

    def border_width_set(self, int border_width):
        etk_container_border_width_set(<Etk_Container*>self.obj, border_width)

    def children_get(self):
        cdef Evas_List* __lst
        cdef Object o
        __ret = []

        __lst = etk_container_children_get(<Etk_Container*>self.obj)
        while __lst != NULL:
            o = Object_from_instance(<Etk_Object*>__lst.data)
            __ret.append(o)
            __lst = __lst.next

        evas.c_evas.evas_list_free(__lst)
        return (__ret)

    def for_each(self, func, *args, **kargs):
        data = (func, args, kargs)
        etk_container_for_each_data(<Etk_Container*>self.obj, _for_each_cb,
                                    <void*>data)

    def is_child(self, Widget widget):
        return bool(<int>etk_container_is_child(<Etk_Container*>self.obj,
                                                <Etk_Widget*>widget.obj))

    def remove_all(self):
        etk_container_remove_all(<Etk_Container*>self.obj)

    property border_width:
        def __get__(self):
            return self.border_width_get()

        def __set__(self, value):
            self.border_width_set(value)

    property children:
        def __get__(self):
            return self.children_get()

    def _set_common_params(self, border_width=None, **kargs):
        if border_width is not None:
            self.border_width_set(border_width)

        if kargs:
            Widget._set_common_params(self, **kargs)

    property CHILD_ADDED_SIGNAL:
        def __get__(self):
            return ETK_CONTAINER_CHILD_ADDED_SIGNAL

    def on_child_added(self, func, *a, **ka):
        self.connect(self.CHILD_ADDED_SIGNAL, func, *a, **ka)

    property CHILD_REMOVED_SIGNAL:
        def __get__(self):
            return ETK_CONTAINER_CHILD_REMOVED_SIGNAL

    def on_child_removed(self, func, *a, **ka):
        self.connect(self.CHILD_REMOVED_SIGNAL, func, *a, **ka)

class ContainerEnums:
    pass
