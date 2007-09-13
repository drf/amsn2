cdef extern from "etk_object.h":
    ####################################################################
    # Enumerations
    ####################################################################
    # Structures
    ctypedef struct Etk_Notification_Callback

    ####################################################################
    # Functions
    Etk_Object* etk_object_name_find(char* name)
    Etk_Object* etk_object_new_valist(Etk_Type* object_type, char* first_property, va_list args)
    void etk_object_purge()
    void etk_object_shutdown()
    Etk_Type* etk_object_type_get()
    Etk_Object* etk_object_new(Etk_Type* object_type, char* first_property)
    Etk_Object* etk_object_check_cast(Etk_Object* __self, Etk_Type* type)
    void* etk_object_data_get(Etk_Object* __self, char* key)
    void etk_object_data_set(Etk_Object* __self, char* key, void* value)
    void etk_object_data_set_full(Etk_Object* __self, char* key, void* value)
    void etk_object_destroy(Etk_Object* __self)
    char* etk_object_name_get(Etk_Object* __self)
    void etk_object_name_set(Etk_Object* __self, char* name)
    void etk_object_notification_callback_add(Etk_Object* __self, char* property_name)
    void etk_object_notification_callback_remove(Etk_Object* __self, char* property_name)
    void etk_object_notify(Etk_Object* __self, char* property_name)
    Etk_Type* etk_object_object_type_get(Etk_Object* __self)
    void etk_object_properties_get(Etk_Object* __self, char* first_property)
    void etk_object_properties_get_valist(Etk_Object* __self, char* first_property, va_list args)
    void etk_object_properties_set(Etk_Object* __self, char* first_property)
    void etk_object_properties_set_valist(Etk_Object* __self, char* first_property, va_list args)
    void etk_object_property_reset(Etk_Object* __self, char* property_name)
    void etk_object_signal_callback_add(Etk_Object* __self, Etk_Signal_Callback* signal_callback, int after)
    void etk_object_signal_callback_remove(Etk_Object* __self, Etk_Signal_Callback* signal_callback)
    void etk_object_signal_callbacks_get(Etk_Object* __self, Etk_Signal* signal, Evas_List** callbacks)
    void etk_object_weak_pointer_add(Etk_Object* __self, void** pointer_location)
    void etk_object_weak_pointer_remove(Etk_Object* __self, void** pointer_location)

    void etk_marshaller_VOID__VOID(Etk_Callback callback, Etk_Object *object, void *data, void *return_value, va_list arguments)
    void etk_marshaller_VOID__INT(Etk_Callback callback, Etk_Object *object, void *data, void *return_value, va_list arguments)
    void etk_marshaller_VOID__INT_INT(Etk_Callback callback, Etk_Object *object, void *data, void *return_value, va_list arguments)
    void etk_marshaller_VOID__DOUBLE(Etk_Callback callback, Etk_Object *object, void *data, void *return_value, va_list arguments)
    void etk_marshaller_VOID__OBJECT(Etk_Callback callback, Etk_Object *object, void *data, void *return_value, va_list arguments)
    void etk_marshaller_VOID__POINTER(Etk_Callback callback, Etk_Object *object, void *data, void *return_value, va_list arguments)
    void etk_marshaller_VOID__POINTER_POINTER(Etk_Callback callback, Etk_Object *object, void *data, void *return_value, va_list arguments)
    void etk_marshaller_VOID__INT_POINTER(Etk_Callback callback, Etk_Object *object, void *data, void *return_value, va_list arguments)
    void etk_marshaller_BOOL__VOID(Etk_Callback callback, Etk_Object *object, void *data, void *return_value, va_list arguments)
    void etk_marshaller_BOOL__DOUBLE(Etk_Callback callback, Etk_Object *object, void *data, void *return_value, va_list arguments)
    void etk_marshaller_BOOL__POINTER_POINTER(Etk_Callback callback, Etk_Object *object, void *data, void *return_value, va_list arguments)


#########################################################################
# Objects
cdef public class Object [object PyEtk_Object, type PyEtk_Object_Type]:
    cdef Etk_Object *obj
    cdef object _data
    cdef object _connections

    cdef int _unset_obj(self) except 0
    cdef int _set_obj(self, Etk_Object *obj) except 0
