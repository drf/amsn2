cimport evas.c_evas

cdef void _for_each_cb(Etk_Widget *child, void *data):
    func, args, kargs = <object>data
    c = Object_from_instance(<Etk_Object*>child)
    try:
        func(c, *args, **kargs)
    except Exception, e:
        import traceback
        traceback.print_exc()


cdef void _virtual_child_add(Etk_Container *container, Etk_Widget *widget):
    self = Object_from_instance(<Etk_Object *>container)
    obj = Object_from_instance(<Etk_Object *>widget)
    self._child_add(obj)

cdef void _virtual_child_remove(Etk_Container *container, Etk_Widget *widget):
    self = Object_from_instance(<Etk_Object *>container)
    obj = Object_from_instance(<Etk_Object *>widget)
    self._child_remove(obj)

cdef Evas_List *_virtual_children_get(Etk_Container *container):
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
    cdef int _set_obj(self, Etk_Object *obj) except 0:
        cdef Etk_Container *c
        Widget._set_obj(self, obj)
        c = <Etk_Container*>obj

        if getattr(self.__class__, "_child_add", None) is not None:
            c.child_add = _virtual_child_add

        if getattr(self.__class__, "_child_remove", None) is not None:
            c.child_remove = _virtual_child_remove

        if getattr(self.__class__, "_children_get", None) is not None:
            c.children_get = _virtual_children_get

        return 1

    def add(self, Widget widget):
        etk_container_add(<Etk_Container*>self.obj, <Etk_Widget*>widget.obj)

    def border_width_get(self):
        __ret = etk_container_border_width_get(<Etk_Container*>self.obj)
        return (__ret)

    def border_width_set(self, int border_width):
        etk_container_border_width_set(<Etk_Container*>self.obj, border_width)

    property border_width:
        def __get__(self):
            return self.border_width_get()

        def __set__(self, value):
            self.border_width_set(value)

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

    property children:
        def __get__(self):
            return self.children_get()

    def for_each(self, func, *args, **kargs):
        data = (func, args, kargs)
        etk_container_for_each_data(<Etk_Container*>self.obj, _for_each_cb,
                                    <void*>data)

    def is_child(self, Widget widget):
        return bool(<int>etk_container_is_child(<Etk_Container*>self.obj,
                                                <Etk_Widget*>widget.obj))

    def remove_all(self):
        etk_container_remove_all(<Etk_Container*>self.obj)

