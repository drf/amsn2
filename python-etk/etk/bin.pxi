cdef public class Bin(Container) [object PyEtk_Bin, type PyEtk_Bin_Type]:
    def child_get(self):
        __ret = Object_from_instance(<Etk_Object*>etk_bin_child_get(<Etk_Bin*>self.obj))
        return (__ret)

    def child_set(self, Widget child):
        etk_bin_child_set(<Etk_Bin*>self.obj, <Etk_Widget*>child.obj)

    property child:
        def __get__(self):
            return self.child_get()

        def __set__(self, child):
            self.child_set(child)

    def _set_common_params(self, child=None, **kargs):
        if child is not None:
            self.child_set(child)

        if kargs:
            Container._set_common_params(self, **kargs)


class BinEnums:
    pass
