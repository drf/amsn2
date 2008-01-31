cdef extern from "etk_event.h":
    ctypedef enum Etk_Modifiers:
        ETK_MODIFIER_NONE
        ETK_MODIFIER_CTRL
        ETK_MODIFIER_ALT
        ETK_MODIFIER_SHIFT
        ETK_MODIFIER_WIN

    ctypedef enum Etk_Locks:
        ETK_LOCK_NONE
        ETK_LOCK_NUM
        ETK_LOCK_CAPS
        ETK_LOCK_SCROLL

    ctypedef enum Etk_Mouse_Flags:
        ETK_MOUSE_NONE
        ETK_MOUSE_DOUBLE_CLICK
        ETK_MOUSE_TRIPLE_CLICK

    ctypedef enum Etk_Wheel_Direction:
        ETK_WHEEL_VERTICAL
        ETK_WHEEL_HORIZONTAL

    ctypedef struct Etk_Event_Mouse_In:
        int buttons
        Etk_Position canvas
        Etk_Position widget
        Etk_Modifiers modifiers
        Etk_Locks locks
        unsigned int timestamp

    ctypedef struct Etk_Event_Mouse_Out:
        int buttons
        Etk_Position canvas
        Etk_Position widget
        Etk_Modifiers modifiers
        Etk_Locks locks
        unsigned int timestamp

    ctypedef struct _Canvas_Widget_Position:
        Etk_Position canvas
        Etk_Position widget

    ctypedef struct Etk_Event_Mouse_Move:
        int buttons
        _Canvas_Widget_Position cur
        _Canvas_Widget_Position prev
        Etk_Modifiers modifiers
        Etk_Locks locks
        unsigned int timestamp

    ctypedef struct Etk_Event_Mouse_Down:
        int button
        Etk_Position canvas
        Etk_Position widget
        Etk_Modifiers modifiers
        Etk_Locks locks
        Etk_Mouse_Flags flags
        unsigned int timestamp

    ctypedef struct Etk_Event_Mouse_Up:
        int button
        Etk_Position canvas
        Etk_Position widget
        Etk_Modifiers modifiers
        Etk_Locks locks
        Etk_Mouse_Flags flags
        unsigned int timestamp

    ctypedef struct Etk_Event_Mouse_Wheel:
        Etk_Wheel_Direction direction
        int z
        Etk_Position canvas
        Etk_Position widget
        Etk_Modifiers modifiers
        Etk_Locks locks
        unsigned int timestamp

    ctypedef struct Etk_Event_Key_Down:
        char *keyname
        Etk_Modifiers modifiers
        Etk_Locks locks
        char *key
        char *string
        char *compose
        unsigned int timestamp

    ctypedef struct Etk_Event_Key_Up:
        char *keyname
        Etk_Modifiers modifiers
        Etk_Locks locks
        char *key
        char *string
        char *compose
        unsigned int timestamp
