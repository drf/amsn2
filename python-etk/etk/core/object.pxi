import traceback

cdef class SignalConnection:
    cdef object callback
    cdef Etk_Signal *signal
    cdef object obj
    cdef object args
    cdef object kargs
    cdef Etk_Callback cb

    def __new__(self, Object obj, callback, long cb, a, ka):
        self.callback = callback
        self.obj = obj
        self.args = a
        self.kargs = ka
        self.cb = <Etk_Callback>cb

    cdef set_signal(self, Etk_Signal *signal):
        self.signal = signal


cdef Etk_Bool obj_free_cb(Etk_Object *obj, void *data) with gil:
    cdef Object self
    self = <Object>data
    self._unset_obj()
    return True


cdef Etk_Bool obj_signal_void(Etk_Object *o, void *data) with gil:
    cdef SignalConnection conn
    cdef Object obj
    cdef Etk_Bool ret

    conn = <SignalConnection>data
    obj = conn.obj
    ret = False

    try:
        if conn.callback(obj, *conn.args, **conn.kargs):
            ret = True
    except Exception, e:
        traceback.print_exc()

    return ret


cdef Etk_Bool obj_signal_int(Etk_Object *o, int v1, void *data) with gil:
    cdef SignalConnection conn
    cdef Object obj
    cdef Etk_Bool ret

    conn = <SignalConnection>data
    obj = conn.obj
    ret = False

    try:
        if conn.callback(obj, v1, *conn.args, **conn.kargs):
            ret = True
    except Exception, e:
        traceback.print_exc()

    return ret


cdef Etk_Bool obj_signal_int_int(Etk_Object *o, int v1, int v2,
                                 void *data) with gil:
    cdef SignalConnection conn
    cdef Object obj
    cdef Etk_Bool ret

    conn = <SignalConnection>data
    obj = conn.obj
    ret = False

    try:
        if conn.callback(obj, v1, v2, *conn.args, **conn.kargs):
            ret = True
    except Exception, e:
        traceback.print_exc()

    return ret


cdef Etk_Bool obj_signal_double(Etk_Object *o, double value,
                                void *data) with gil:
    cdef SignalConnection conn
    cdef Object obj
    cdef Etk_Bool ret

    conn = <SignalConnection>data
    obj = conn.obj
    ret = False

    try:
        if conn.callback(obj, value, *conn.args, **conn.kargs):
            ret = True
    except Exception, e:
        traceback.print_exc()

    return ret


cdef Etk_Bool obj_signal_object(Etk_Object *o, Etk_Object *value,
                                void *data) with gil:
    cdef SignalConnection conn
    cdef Object obj
    cdef Etk_Bool ret

    conn = <SignalConnection>data
    obj = conn.obj
    ret = False

    try:
        wrapped = Object_from_instance(value)
        if conn.callback(obj, wrapped, *conn.args, **conn.kargs):
            ret = True
    except Exception, e:
        traceback.print_exc()

    return ret


cdef Etk_Bool obj_signal_pointer(Etk_Object *o, void *value,
                                 void *data) with gil:
    cdef SignalConnection conn
    cdef Object obj
    cdef Etk_Bool ret

    conn = <SignalConnection>data
    obj = conn.obj
    ret = False

    # Special case for Event data
    ev = _event_translation_mapping(conn.signal.name, value)
    if ev is None:
        ev = <long>value

    try:
        if conn.callback(obj, ev, *conn.args, **conn.kargs):
            ret = True
    except Exception, e:
        traceback.print_exc()

    return ret


cdef Etk_Bool obj_signal_pointer_pointer(Etk_Object *o, void *v1,
                                         void *v2, void *data) with gil:
    cdef SignalConnection conn
    cdef Object obj
    cdef Etk_Bool ret

    conn = <SignalConnection>data
    obj = conn.obj
    ret = False

    try:
        if conn.callback(obj, <long>v1, <long>v2, *conn.args, **conn.kargs):
            ret = True
    except Exception, e:
        traceback.print_exc()

    return ret


cdef Etk_Bool obj_signal_int_pointer(Etk_Object *o, int v1, void *v2,
                                 void *data) with gil:
    cdef SignalConnection conn
    cdef Object obj
    cdef Etk_Bool ret

    conn = <SignalConnection>data
    obj = conn.obj
    ret = False

    try:
        if conn.callback(obj, v1, <long>v2, *conn.args, **conn.kargs):
            ret = True
    except Exception, e:
        traceback.print_exc()

    return ret


cdef Etk_Signal* _get_signal(Etk_Object *obj, s):
    """Given a name or code returns the (Etk_Signal *) for the signal"""
    cdef Etk_Signal *signal

    if type(s) is int:
        signal = etk_type_signal_get(obj.type, s)
        if signal == NULL:
            raise ValueError("Unknown signal code %d" % s)
    elif type(s) is str:
        signal = etk_type_signal_get_by_name(obj.type, s)
        if signal == NULL:
            raise ValueError("Unknown signal name \"%s\"" % s)
    else:
        raise TypeError("Invalid type for describing a signal")
    return signal


cdef Etk_Callback _cb_for_signal(Etk_Object *obj, Etk_Signal *signal):
    if signal == NULL:
        return NULL
    if signal.marshaller == <Etk_Marshaller>etk_marshaller_VOID:
        return <Etk_Callback>obj_signal_void
    elif signal.marshaller == <Etk_Marshaller>etk_marshaller_INT:
        return <Etk_Callback>obj_signal_int
    elif signal.marshaller == <Etk_Marshaller>etk_marshaller_INT_INT:
        return <Etk_Callback>obj_signal_int_int
    elif signal.marshaller == <Etk_Marshaller>etk_marshaller_DOUBLE:
        return <Etk_Callback>obj_signal_double
    elif signal.marshaller == <Etk_Marshaller>etk_marshaller_OBJECT:
        return <Etk_Callback>obj_signal_object
    elif signal.marshaller == <Etk_Marshaller>etk_marshaller_POINTER:
        return <Etk_Callback>obj_signal_pointer
    elif signal.marshaller == <Etk_Marshaller>etk_marshaller_POINTER_POINTER:
        return <Etk_Callback>obj_signal_pointer_pointer
    elif signal.marshaller == <Etk_Marshaller>etk_marshaller_INT_POINTER:
        return <Etk_Callback>obj_signal_int_pointer
    else:
        return NULL


cdef public class Object [object PyEtk_Object, type PyEtk_Object_Type]:
    def __new__(self, *a, **ka):
        self.obj = NULL
        self._data = dict()
        self._connections = dict()

    cdef int _unset_obj(self) except 0:
        """Unbind the Etk object from it's Python equivalent.

        When created PyEtk objects have a pointer to Etk object that it
        represents (in self.obj), and the Etk object has a reference
        (manually counted) to its PyEtk object. Unset removes this
        connection and decrements the refcount, letting the PyEtk object be
        destroyed by Python's GC if it's the case.

        It's usually called by the destroy callback created for every PyEtk
        object.
        """
        assert self.obj != NULL, "Object must wrap something"
        assert etk_object_data_get(self.obj, "python-etk") == \
               <void *>self, "Object wrapped should refer to self"
        etk_signal_disconnect("destroyed", self.obj, <Etk_Callback>obj_free_cb,
                              <void *>self)
        etk_object_data_set(self.obj, "python-etk", NULL)
        self.obj = NULL
        self._connections = None
        python.Py_DECREF(self)
        return 1

    cdef object _set_obj(self, Etk_Object *obj):
        assert self.obj == NULL, "Object must be clean"
        self.obj = obj
        python.Py_INCREF(self)
        etk_object_data_set(obj, "python-etk", <void *>self)
        etk_signal_connect("destroyed", self.obj, <Etk_Callback>obj_free_cb,
                           <void*>self)
        #_register_decorated_callbacks(self)
        return self

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
            # "destroyed" signal was already emitted and etk_object_destroy()
            # was already called, so do nothing else.
            return

        self.obj = NULL
        data = etk_object_data_get(obj, "python-etk")
        assert data == NULL, "Object must not be wrapped!"

        # don't need the callback, we did everything it does already
        etk_signal_disconnect("destroyed", self.obj, <Etk_Callback>obj_free_cb,
                              <void *>self)
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

    def connect(self, s, func, *a, **ka):
        return self.connect_full(s, False, func, *a, **ka)

    def connect_after(self, s, func, *a, **ka):
        return self.connect_full(s, True, func, *a, **ka)

    def connect_full(self, s, after, func, *a, **ka):
        cdef Etk_Callback cb
        cdef SignalConnection conn
        cdef Etk_Signal *signal

        if self.obj == NULL:
            return

        signal = _get_signal(self.obj, s)
        cb = _cb_for_signal(self.obj, signal)
        if cb == NULL:
            raise ValueError("Unknown signal \"%s\"" % signal.name)

        conn = SignalConnection(self, func, <long>cb, a, ka)
        conn.set_signal(signal)
        if signal.code in self._connections:
            self._connections[signal.code].append(conn)
        else:
            self._connections[signal.code] = [conn]

        if after:
            etk_signal_connect_after_by_code(signal.code, self.obj, cb,
                                             <void *>conn)
        else:
            etk_signal_connect_by_code(signal.code, self.obj, cb,
                                       <void *>conn)
        return conn

    def disconnect(self, s, func, *a, **ka):
        cdef SignalConnection conn

        (signal_code, conns, delete_list) = self._sc_find(s, func, *a, **ka)

        for i in delete_list:
            conn = conns[i]
            etk_signal_disconnect_by_code(signal_code, self.obj,
                                          <Etk_Callback>conn.cb, <void *>conn)
            del conns[i]

    def disconnect_by_id(self, SignalConnection id):
        if self.obj == NULL:
            return

        conns = self._connections.get(id.signal.code, None)
        if conns is None:
            raise ValueError("Disconnecting a non-existent callback Id for"
                             "signal %s" % id.signal.code)

        if not id in conns:
            raise ValueError("Disconnecting a non-existent callback Id for"
                             "signal %s" % id.signal.code)

        idx = conns.index(id)
        etk_signal_disconnect_by_code(id.signal.code, self.obj,
                                      <Etk_Callback>id.cb, <void *>id)
        del conns[idx]

    def disconnect_all(self, s):
        cdef SignalConnection conn

        if self.obj == NULL:
            return

        if type(s) is int:
            signal_code = s
        elif type(s) is str:
            signal_code = _get_signal(self.obj, s).code
        else:
            raise TypeError("Invalid type for describing a signal")

        etk_signal_disconnect_all_by_code(signal_code, self.obj)

        conn = self._connections.get(signal_code, None)
        if conn is not None:
            conn.callbacks = None
            del self._connections[signal_code]

    def block(self, s, func, *a, **ka):
        cdef SignalConnection conn

        (signal_code, conns, block_list) = self._sc_find(s, func, *a, **ka)

        for i in block_list:
            conn = conns[i]
            etk_signal_block_by_code(signal_code, self.obj,
                                     <Etk_Callback>conn.cb, <void *>conn)

    def unblock(self, s, func, *a, **ka):
        cdef SignalConnection conn

        (signal_code, conns, unblock_list) = self._sc_find(s, func, *a, **ka)

        for i in unblock_list:
            conn = conns[i]
            etk_signal_unblock_by_code(signal_code, self.obj,
                                       <Etk_Callback>conn.cb, <void *>conn)

    def _sc_find(self, s, func, *a, **ka):
        cdef SignalConnection conn

        if self.obj == NULL:
            return

        if type(s) is int:
            signal_code = s
        elif type(s) is str:
            signal_code = _get_signal(self.obj, s).code
        else:
            raise TypeError("Invalid type for describing a signal")

        conns = self._connections.get(signal_code, None)
        if conns is None:
            raise ValueError("No callbacks registered for signal %s" %
                             signal_code)
        else:
            indexes = []

            for i, conn in enumerate(conns):
                if func == conn.callback and a == conn.args \
                    and ka == conn.kargs:
                    indexes.append(i)
                    break
            else:
                raise ValueError("Callback %s was not registered for signal %s"
                                    % (func, signal_code))

            return (signal_code, conns, indexes)

    property DESTROYED_SIGNAL:
        def __get__(self):
            return ETK_OBJECT_DESTROYED_SIGNAL

    def on_destroyed(self, func, *a, **ka):
        self.connect(self.DESTROYED_SIGNAL, func, *a, **ka)
