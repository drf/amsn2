cdef void _pointer_set_cb(void *pointer_data, Etk_Pointer_Type pointer_type) \
        with gil:
    self = Object_from_instance(<Etk_Object *>pointer_data)
    if self.__set_pointer_func is not None:
        self.__set_pointer_func(self.__set_pointer_data, pointer_type)


cdef void _position_get_cb(void *pointer_data, int *x, int *y) with gil:
    self = Object_from_instance(<Etk_Object *>pointer_data)
    if self.__get_position_func is not None:
        (x[0], y[0]) = self.__get_position_func(self.__get_position_data)


cdef public class Embed(Toplevel) [object PyEtk_Embed, type PyEtk_Embed_Type]:
    def __init__(self, evas):
        e = Embed_Accessor(evas)
        if self.obj == NULL:
            e._set_embed_obj(self)

        self.__set_pointer_func = None
        self.__set_pointer_data = None
        self.__get_position_func = None
        self.__get_position_data = None

    def object_get(self):
        __ret = evas.c_evas._Object_from_instance(<long>etk_embed_object_get(<Etk_Embed*>self.obj))
        return (__ret)

    def pointer_method_set(self, func, data):
        self.__set_pointer_func = func
        self.__set_pointer_data = data
        etk_embed_pointer_method_set(<Etk_Embed*>self.obj, _pointer_set_cb, <void *>self.obj)

    def position_method_set(self, func, data):
        self.__get_position_func = func
        self.__get_position_data = data
        etk_embed_position_method_set(<Etk_Embed*>self.obj, _position_get_cb, <void *>self.obj)

    property object:
        def __get__(self):
            return self.object_get()


cdef class Embed_Accessor(evas.c_evas.Object):
    def _new_obj(self):
       pass
    def _set_embed_obj(self, Embed embed):
       embed._set_obj(<Etk_Object*>etk_embed_new(<Evas*>self.evas.obj))


class EmbedEnums(ToplevelEnums):
    pass
