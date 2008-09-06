cdef public class EvasObject(Widget) [object PyEtk_Evas_Object, type PyEtk_Evas_Object_Type]:
    def __init__(self, evas.c_evas.Object evas_object=None):
        if self.obj == NULL:
            if evas_object is not None:
                self._set_obj(<Etk_Object*>etk_evas_object_new_from_object(<evas.c_evas.Evas_Object*>evas_object.obj))
            else:
                self._set_obj(<Etk_Object*>etk_evas_object_new())

    def get_object(self):
        __ret = evas.c_evas._Object_from_instance(<long>etk_evas_object_get(<Etk_Evas_Object*>self.obj))
        return (__ret)

    
    def set_object(self, evas.c_evas.Object evas_object):
        etk_evas_object_set_object(<Etk_Evas_Object*>self.obj, <evas.c_evas.Evas_Object*>evas_object.obj)
    property evas_object:
        def __get__(self):
            return self.get_object()

        def __set__(self, evas_object):
            self.set_object(evas_object)
