
cdef public class String(Object) [object PyEtk_String, type PyEtk_String_Type]:
    def __init__(self, label=None, **kargs):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_string_new(""))

    def string_set(self, char* string):
        self._set_obj(<Etk_Object *> etk_string_set(<Etk_String*>self.obj, string))

    def string_get(self):
        cdef char *__char_ret
        __ret = None
        __char_ret = etk_string_get(<Etk_String*>self.obj)
        if __char_ret != NULL:
            __ret = __char_ret
        return (__ret)

    property string:
        def __get__(self):
            return self.string_get()

        def __set__(self, string):
            self.string_set(string)

