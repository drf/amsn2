cdef extern from "etk_signal.h":
    ####################################################################
    # Enumerations
    ####################################################################
    # Structures
    ctypedef struct Etk_Signal

    ####################################################################
    # Functions
    void etk_signal_block(char* signal_name, Etk_Object* object, Etk_Callback callback)
    void etk_signal_connect(char* signal_name, Etk_Object* object, Etk_Callback callback, void* data)
    void etk_signal_connect_after(char* signal_name, Etk_Object* object, Etk_Callback callback, void* data)
    void etk_signal_connect_swapped(char* signal_name, Etk_Object* object, Etk_Callback callback, void* data)
    void etk_signal_disconnect(char* signal_name, Etk_Object* object, Etk_Callback callback)
    void etk_signal_disconnect_all(char* signal_name, Etk_Object* object)
    Etk_Bool etk_signal_emit_by_name(char* signal_name, Etk_Object* object, void* return_value)
    Evas_List* etk_signal_get_all()
    Etk_Signal* etk_signal_lookup(char* signal_name, Etk_Type* type)
    void etk_signal_shutdown()
    void etk_signal_stop()
    void etk_signal_unblock(char* signal_name, Etk_Object* object, Etk_Callback callback)
