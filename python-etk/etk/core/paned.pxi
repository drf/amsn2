cdef public class Paned(Container) [object PyEtk_Paned, type PyEtk_Paned_Type]:
    def child1_set(self, Widget child, int expand):
        etk_paned_child1_set(<Etk_Paned *>self.obj, <Etk_Widget *>child.obj, expand)

    def child2_set(self, Widget child, int expand):
        etk_paned_child2_set(<Etk_Paned *>self.obj, <Etk_Widget *>child.obj, expand)

    def child1_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_paned_child1_get(<Etk_Paned *>self.obj))
        return (__ret)

    def child2_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_paned_child2_get(<Etk_Paned *>self.obj))
        return (__ret)

    def child1_expand_set(self, int expand):
        etk_paned_child1_expand_set(<Etk_Paned *>self.obj, expand)

    def child1_expand_get(self):
        return etk_paned_child1_expand_get(<Etk_Paned *>self.obj)

    def child2_expand_set(self, int expand):
        etk_paned_child2_expand_set(<Etk_Paned *>self.obj, expand)

    def child2_expand_get(self):
        return etk_paned_child2_expand_get(<Etk_Paned *>self.obj)

    def position_set(self, int position):
        etk_paned_position_set(<Etk_Paned*>self.obj, position)

    def position_get(self):
        return etk_paned_position_get(<Etk_Paned*>self.obj)

    property child1_expand:
        def __get__(self):
            return self.child1_expand_get()

        def __set__(self, arg):
            self.child1_expand_set(arg)

    property child2_expand:
        def __get__(self):
            return self.child2_expand_get()

        def __set__(self, arg):
            self.child2_expand_set(arg)

    property position:
        def __get__(self):
            return self.position_get()

        def __set__(self, arg):
            self.position_set(arg)


cdef public class HPaned(Paned) [object PyEtk_HPaned, type PyEtk_HPaned_Type]:
    def __init__(self, **kargs):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_hpaned_new())
        Container._set_common_params(self, **kargs)

cdef public class VPaned(Paned) [object PyEtk_VPaned, type PyEtk_VPaned_Type]:
    def __init__(self, **kargs):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_vpaned_new())
        Container._set_common_params(self, **kargs)
