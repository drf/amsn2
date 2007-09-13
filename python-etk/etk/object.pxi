import traceback


# XXX: caution w/ threads
_emitted_signals = []

def signal_stop():
    if _emitted_signals:
        _emitted_signals[-1].stop_emission = True

cdef class SignalConnection:
    cdef object callbacks
    cdef object signal_name
    cdef object obj
    cdef Etk_Callback cb

    def __new__(self, Object obj, char *signal_name, callbacks, long cb):
        self.callbacks = callbacks
        self.signal_name = signal_name
        self.obj = obj
        self.cb = <Etk_Callback>cb


class SignalEmitted:
    def __init__(self, signal_conn):
        self.signal_conn = signal_conn
        self.stop_emission = False


cdef void obj_free_cb(Etk_Object *obj, void *data):
    cdef Object self
    self = <Object>data
    self.obj = NULL
    python.Py_DECREF(self)


cdef void obj_signal_void_void(Etk_Object *o, void *data):
    cdef SignalConnection conn
    cdef Object obj

    conn = <SignalConnection>data
    obj = conn.obj
    emitted = SignalEmitted(conn)

    _emitted_signals.append(emitted)
    for func, args, kargs in conn.callbacks:
        if emitted.stop_emission:
            break

        try:
            func(obj, *args, **kargs)
        except Exception, e:
            traceback.print_exc()
    _emitted_signals.pop()

cdef void obj_signal_void_int(Etk_Object *o, int value, void *data):
    cdef SignalConnection conn
    cdef Object obj

    conn = <SignalConnection>data
    obj = conn.obj
    emitted = SignalEmitted(conn)

    _emitted_signals.append(emitted)
    for func, args, kargs in conn.callbacks:
        if emitted.stop_emission:
            break

        try:
            func(obj, value, *args, **kargs)
        except Exception, e:
            traceback.print_exc()
    _emitted_signals.pop()


cdef void obj_signal_void_int_int(Etk_Object *o, int v1, int v2, void *data):
    cdef SignalConnection conn
    cdef Object obj

    conn = <SignalConnection>data
    obj = conn.obj
    emitted = SignalEmitted(conn)

    _emitted_signals.append(emitted)
    for func, args, kargs in conn.callbacks:
        if emitted.stop_emission:
            break

        try:
            func(obj, v1, v2, *args, **kargs)
        except Exception, e:
            traceback.print_exc()
    _emitted_signals.pop()


cdef void obj_signal_void_double(Etk_Object *o, double value, void *data):
    cdef SignalConnection conn
    cdef Object obj

    conn = <SignalConnection>data
    obj = conn.obj
    emitted = SignalEmitted(conn)

    _emitted_signals.append(emitted)
    for func, args, kargs in conn.callbacks:
        if emitted.stop_emission:
            break

        try:
            func(obj, value, *args, **kargs)
        except Exception, e:
            traceback.print_exc()
    _emitted_signals.pop()


cdef void obj_signal_void_object(Etk_Object *o, Etk_Object *value, void *data):
    cdef SignalConnection conn
    cdef Object obj

    conn = <SignalConnection>data
    obj = conn.obj
    emitted = SignalEmitted(conn)

    _emitted_signals.append(emitted)
    for func, args, kargs in conn.callbacks:
        if emitted.stop_emission:
            break

        try:
            wrapped = Object_from_instance(value)
            func(obj, wrapped, *args, **kargs)
        except Exception, e:
            traceback.print_exc()
    _emitted_signals.pop()


cdef void obj_signal_void_pointer(Etk_Object *o, void *value, void *data):
    cdef SignalConnection conn
    cdef Object obj

    conn = <SignalConnection>data
    obj = conn.obj
    emitted = SignalEmitted(conn)

    # Special case for Event data
    ev = _event_translation_mapping(conn.signal_name, value)
    if ev is None:
        ev = <long>value

    _emitted_signals.append(emitted)
    for func, args, kargs in conn.callbacks:
        if emitted.stop_emission:
            break

        try:
            func(obj, ev, *args, **kargs)
        except Exception, e:
            traceback.print_exc()
    _emitted_signals.pop()


cdef void obj_signal_void_pointer_pointer(Etk_Object *o, void *v1, void *v2,
                                          void *data):
    cdef SignalConnection conn
    cdef Object obj

    conn = <SignalConnection>data
    obj = conn.obj
    emitted = SignalEmitted(conn)

    _emitted_signals.append(emitted)
    for func, args, kargs in conn.callbacks:
        if emitted.stop_emission:
            break

        try:
            func(obj, <long>v1, <long>v2, *args, **kargs)
        except Exception, e:
            traceback.print_exc()
    _emitted_signals.pop()


cdef void obj_signal_void_int_pointer(Etk_Object *o, int v1, void *v2,
                                      void *data):
    cdef SignalConnection conn
    cdef Object obj

    conn = <SignalConnection>data
    obj = conn.obj
    emitted = SignalEmitted(conn)

    _emitted_signals.append(emitted)
    for func, args, kargs in conn.callbacks:
        if emitted.stop_emission:
            break

        try:
            func(obj, v1, <long>v2, *args, **kargs)
        except Exception, e:
            traceback.print_exc()
    _emitted_signals.pop()


# XXX: implement etk semantics of run_last, etc.
cdef Etk_Bool obj_signal_bool_void(Etk_Object *o, void *data):
    cdef SignalConnection conn
    cdef Object obj
    cdef int ret

    conn = <SignalConnection>data
    obj = conn.obj
    emitted = SignalEmitted(conn)
    ret = 0

    _emitted_signals.append(emitted)
    for func, args, kargs in conn.callbacks:
        if emitted.stop_emission:
            break

        try:
            ret = func(obj, *args, **kargs)
        except Exception, e:
            traceback.print_exc()
    _emitted_signals.pop()

    return <Etk_Bool>ret


# XXX: implement etk semantics of run_last, etc.
cdef Etk_Bool obj_signal_bool_double(Etk_Object *o, double value, void *data):
    cdef SignalConnection conn
    cdef Object obj
    cdef int ret

    conn = <SignalConnection>data
    obj = conn.obj
    emitted = SignalEmitted(conn)
    ret = 0

    _emitted_signals.append(emitted)
    for func, args, kargs in conn.callbacks:
        if emitted.stop_emission:
            break

        try:
            ret = func(obj, value, *args, **kargs)
        except Exception, e:
            traceback.print_exc()
    _emitted_signals.pop()

    return <Etk_Bool>ret


# XXX: implement etk semantics of run_last, etc.
cdef Etk_Bool obj_signal_bool_pointer_pointer(Etk_Object *o, void *v1,
                                              void *v2, void *data):
    cdef SignalConnection conn
    cdef Object obj
    cdef int ret

    conn = <SignalConnection>data
    obj = conn.obj
    emitted = SignalEmitted(conn)
    ret = 0

    _emitted_signals.append(emitted)
    for func, args, kargs in conn.callbacks:
        if emitted.stop_emission:
            break

        try:
            ret = func(obj, <long>v1, <long>v2, *args, **kargs)
        except Exception, e:
            traceback.print_exc()
    _emitted_signals.pop()

    return <Etk_Bool>ret



cdef Etk_Callback _cb_for_signal(Etk_Object *obj, char *signal_name):
    cdef Etk_Signal *signal

    signal = etk_signal_lookup(signal_name, etk_object_object_type_get(obj))
    if signal == NULL:
        return NULL
    if signal.marshaller == <Etk_Marshaller>etk_marshaller_VOID__VOID:
        return <Etk_Callback>obj_signal_void_void
    elif signal.marshaller == <Etk_Marshaller>etk_marshaller_VOID__INT:
        return <Etk_Callback>obj_signal_void_int
    elif signal.marshaller == <Etk_Marshaller>etk_marshaller_VOID__INT_INT:
        return <Etk_Callback>obj_signal_void_int_int
    elif signal.marshaller == <Etk_Marshaller>etk_marshaller_VOID__DOUBLE:
        return <Etk_Callback>obj_signal_void_double
    elif signal.marshaller == <Etk_Marshaller>etk_marshaller_VOID__OBJECT:
        return <Etk_Callback>obj_signal_void_object
    elif signal.marshaller == <Etk_Marshaller>etk_marshaller_VOID__POINTER:
        return <Etk_Callback>obj_signal_void_pointer
    elif signal.marshaller == <Etk_Marshaller>etk_marshaller_VOID__POINTER_POINTER:
        return <Etk_Callback>obj_signal_void_pointer_pointer
    elif signal.marshaller == <Etk_Marshaller>etk_marshaller_VOID__INT_POINTER:
        return <Etk_Callback>obj_signal_void_int_pointer
    elif signal.marshaller == <Etk_Marshaller>etk_marshaller_BOOL__VOID:
        return <Etk_Callback>obj_signal_bool_void
    elif signal.marshaller == <Etk_Marshaller>etk_marshaller_BOOL__DOUBLE:
        return <Etk_Callback>obj_signal_bool_double
    elif signal.marshaller == <Etk_Marshaller>etk_marshaller_BOOL__POINTER_POINTER:
        return <Etk_Callback>obj_signal_bool_pointer_pointer
    else:
        return NULL


cdef public class Object [object PyEtk_Object, type PyEtk_Object_Type]:
    def __new__(self, *a, **ka):
        self.obj = NULL
        self._data = dict()
        self._connections = dict()

    cdef int _unset_obj(self) except 0:
        assert self.obj != NULL, "Object must wrap something"
        assert etk_object_data_get(self.obj, "python-etk") == \
               <void *>self, "Object wrapped should refer to self"
        etk_signal_disconnect("destroyed", self.obj, <Etk_Callback>obj_free_cb)
        etk_object_data_set(self.obj, "python-etk", NULL)
        self.obj = NULL
        python.Py_DECREF(self)
        return 1

    cdef int _set_obj(self, Etk_Object *obj) except 0:
        assert self.obj == NULL, "Object must be clean"
        self.obj = obj
        python.Py_INCREF(self)
        etk_object_data_set(obj, "python-etk", <void *>self)
        etk_signal_connect("destroyed", self.obj, <Etk_Callback>obj_free_cb,
                           <void*>self)
        #_register_decorated_callbacks(self)
        return 1

    def _get_obj(self):
        if self.obj == NULL:
            return None
        else:
            return <long>self.obj

    def __dealloc__(self):
        cdef void *data
        cdef Etk_Object *obj

        self._data = None
        self._connections = None
        obj = self.obj
        if self.obj == NULL:
            return
        self.obj = NULL

        data = etk_object_data_get(obj, "python-etk")
        assert data == NULL, "Object must not be wrapped!"
        etk_signal_disconnect("destroyed", self.obj, <Etk_Callback>obj_free_cb)
        etk_object_destroy(obj)

    def destroy(self):
        etk_object_destroy(<Etk_Object*>self.obj)

    def _set_common_params(self, **kargs):
        pass

    property data:
        def __get__(self):
            return self._data

    def name_get(self):
        cdef char *__ret
        __ret = etk_object_name_get(<Etk_Object*>self.obj)
        if __ret != NULL:
            return __ret

    def name_set(self, char* name):
        etk_object_name_set(<Etk_Object*>self.obj, name)

##     def notification_callback_add(self, char* property_name):
##         etk_object_notification_callback_add(<Etk_Object*>self.obj, property_name)

##     def notification_callback_remove(self, char* property_name):
##         etk_object_notification_callback_remove(<Etk_Object*>self.obj, property_name)

    def notify(self, char* property_name):
        etk_object_notify(<Etk_Object*>self.obj, property_name)

##     def properties_get(self, *names):
##         cdef Etk_Property_Value *prop_value
##         cdef Etk_Object *obj
##         cdef Etk_Type *type
##         cdef Etk_Property *prop
##         cdef Etk_Property_Type prop_type
##         cdef void *pvalue

##         obj = self.obj
##         if obj == NULL:
##             return tuple()
##         if not names:
##             return tuple()

##         values = []
##         prop_value = etk_property_value_new()
##         for name in names:
##             if etk_type_property_find(obj->type, name, &type, &prop) == 1:
##                if type->property_get != NULL:
##                    type->property_get(obj, prop->id, prop_value)
##                    prop_type = etk_property_value_type_get(prop_value)
##                    etk_property_value_get(prop_value, prop_type, pvalue)

##                    if prop_type == ETK_PROPERTY_INT:
##                        values.append(*<int*>pvalue)
##                    elif prop_type == ETK_PROPERTY_BOOL:
##                        values.append(bool(*<int*>pvalue))
##                    elif prop_type == ETK_PROPERTY_CHAR:
##                        values.append(chr(*<int*>pvalue))
##                    elif prop_type == ETK_PROPERTY_FLOAT:
##                        values.append(*<float*>pvalue)
##                    elif prop_type == ETK_PROPERTY_DOUBLE:
##                        values.append(*<double*>pvalue)
##                    elif prop_type == ETK_PROPERTY_SHORT:
##                        values.append(*<short*>pvalue)
##                    elif prop_type == ETK_PROPERTY_LONG:
##                        values.append(*<long*>pvalue)
##                    elif prop_type == ETK_PROPERTY_STRING:
##                        if pvalue == NULL:
##                            values.append(None)
##                        else:
##                            values.append(<char*>pvalue)
##                    else:
##                        etk_property_value_delete(property_value)
##                        raise ValueError("Unsupported property value type %d" %
##                                         prop_type)
##             else:
##                 etk_property_value_delete(property_value)
##                 raise ValueError(("The object of type \"%s\" has no property "
##                                   "called \"%s\"") %
##                                  obj->type->name, prop_name)

##         etk_property_value_delete(property_value)
##         return values

##     def properties_set(self, *arg_values):
##         etk_object_properties_set(<Etk_Object*>self.obj, first_property)

##     def property_reset(self, char* property_name):
##         etk_object_property_reset(<Etk_Object*>self.obj, property_name)

##     def signal_callback_add(self, Etk_Signal_Callback* signal_callback, int after):
##         # FIXME: unsupported method arguments
##         pass

##     def signal_callback_remove(self, Etk_Signal_Callback* signal_callback):
##         # FIXME: unsupported method arguments
##         pass

##     def signal_callbacks_get(self, Etk_Signal* signal, Evas_List** callbacks):
##         # FIXME: unsupported method arguments
##         pass

##     def weak_pointer_add(self, void** pointer_location):
##         # FIXME: unsupported method arguments
##         pass

##     def weak_pointer_remove(self, void** pointer_location):
##         # FIXME: unsupported method arguments
##         pass

    def connect(self, char *signal_name, func, *a, **ka):
        self.connect_full(signal_name, False, func, *a, **ka)

    def connect_full(self, char *signal_name, after, func, *a, **ka):
        cdef Etk_Callback cb
        cdef SignalConnection conn

        if self.obj == NULL:
            return

        r = (func, a, ka)
        conn = self._connections.get(signal_name, None)
        if conn is not None:
            if after:
                conn.callbacks.append(r)
            else:
                conn.callbacks.insert(0, r)
        else:
            cb = _cb_for_signal(self.obj, signal_name)
            if cb == NULL:
                raise ValueError("Unknown signal %s" % signal_name)
            conn = SignalConnection(self, signal_name, [r], <long>cb)
            self._connections[signal_name] = conn
            etk_signal_connect(signal_name, self.obj, cb, <void*>conn)


    def disconnect(self, char *signal_name, func):
        cdef SignalConnection conn

        if self.obj == NULL:
            return

        conn = self._connections.get(signal_name, None)
        if conn is None:
            raise ValueError("No callbacks registered for signal %s" %
                             signal_name)
        else:
            idx = None
            for i, (f, a, k) in enumerate(conn.callbacks):
                if func == f:
                    idx = i
                    break
            else:
                raise ValueError("Callback %s was not registered for signal %s"
                                 % (func, signal_name))

            del conn.callbacks[idx]
            if not conn.callbacks:
                del self._connections[signal_name]
                etk_signal_disconnect(signal_name, self.obj, conn.cb)


    def disconnect_all(self, char *signal_name):
        cdef SignalConnection conn

        if self.obj == NULL:
            return

        etk_signal_disconnect_all(signal_name, self.obj)

        conn = self._connections.get(signal_name, None)
        if conn is not None:
            conn.callbacks = None
            del self._connections[signal_name]
