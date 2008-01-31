class EventMouseIn:
    def __init__(self, buttons, canvas, widget, modifiers, locks, timestamp):
        self.buttons = buttons
        self.canvas = canvas
        self.widget = widget
        self.modifiers = modifiers
        self.locks = locks
        self.timestamp = timestamp

cdef object _translation_event_mouse_in(void *data):
    cdef Etk_Event_Mouse_In *ev
    ev = <Etk_Event_Mouse_In*>data
    return EventMouseIn(ev.buttons, (ev.canvas.x, ev.canvas.y), (ev.widget.x, ev.widget.y),
                        ev.modifiers, ev.locks, ev.timestamp)


class EventMouseOut:
    def __init__(self, buttons, canvas, widget, modifiers, locks, timestamp):
        self.buttons = buttons
        self.canvas = canvas
        self.widget = widget
        self.modifiers = modifiers
        self.locks = locks
        self.timestamp = timestamp

cdef object _translation_event_mouse_out(void *data):
    cdef Etk_Event_Mouse_Out *ev
    ev = <Etk_Event_Mouse_Out*>data
    return EventMouseOut(ev.buttons, (ev.canvas.x, ev.canvas.y), (ev.widget.x, ev.widget.y),
                        ev.modifiers, ev.locks, ev.timestamp)


class EventMouseMove:
    def __init__(self, button, cur_canvas, cur_widget, prev_canvas, prev_widget,
                 modifiers, locks, timestamp):
        self.button = button
        self.cur_canvas = cur_canvas
        self.cur_widget = cur_widget
        self.prev_canvas = prev_canvas
        self.prev_widget = prev_widget
        self.modifiers = modifiers
        self.locks = locks
        self.timestamp = timestamp

cdef object _translation_event_mouse_move(void *data):
    cdef Etk_Event_Mouse_Move *ev
    ev = <Etk_Event_Mouse_Move*>data
    return EventMouseMove(ev.buttons,
            (ev.cur.canvas.x, ev.cur.canvas.y), (ev.cur.widget.x, ev.cur.widget.y),
            (ev.prev.canvas.x, ev.prev.canvas.y), (ev.prev.widget.x, ev.prev.widget.y),
            ev.modifiers, ev.locks, ev.timestamp)


class EventMouseDown:
    def __init__(self, button, canvas, widget, modifiers, locks, flags, timestamp):
        self.button = button
        self.canvas = canvas
        self.widget = widget
        self.modifiers = modifiers
        self.locks = locks
        self.flags = flags
        self.timestamp = timestamp

cdef object _translation_event_mouse_down(void *data):
    cdef Etk_Event_Mouse_Down *ev
    ev = <Etk_Event_Mouse_Down*>data
    return EventMouseDown(ev.button, (ev.canvas.x, ev.canvas.y), (ev.widget.x, ev.widget.y),
                        ev.modifiers, ev.locks, ev.flags, ev.timestamp)


class EventMouseUp:
    def __init__(self, button, canvas, widget, modifiers, locks, flags, timestamp):
        self.button = button
        self.canvas = canvas
        self.widget = widget
        self.modifiers = modifiers
        self.locks = locks
        self.flags = flags
        self.timestamp = timestamp

cdef object _translation_event_mouse_up(void *data):
    cdef Etk_Event_Mouse_Up *ev
    ev = <Etk_Event_Mouse_Up*>data
    return EventMouseUp(ev.button, (ev.canvas.x, ev.canvas.y), (ev.widget.x, ev.widget.y),
                        ev.modifiers, ev.locks, ev.flags, ev.timestamp)


class EventMouseWheel:
    def __init__(self, direction, z, canvas, widget, modifiers, locks, timestamp):
        self.direction = direction
        self.z = z
        self.canvas = canvas
        self.widget = widget
        self.modifiers = modifiers
        self.locks = locks
        self.timestamp = timestamp

cdef object _translation_event_mouse_wheel(void *data):
    cdef Etk_Event_Mouse_Wheel *ev
    ev = <Etk_Event_Mouse_Wheel*>data
    return EventMouseWheel(ev.direction, ev.z, (ev.canvas.x, ev.canvas.y),
                           (ev.widget.x, ev.widget.y),
                           ev.modifiers, ev.locks, ev.timestamp)


class EventKey:
    def __init__(self, keyname, modifiers, locks, key, string, compose, timestamp):
        self.keyname = keyname
        self.modifiers = modifiers
        self.locks = locks
        self.key = key
        self.string = string
        self.compose = compose
        self.timestamp = timestamp


class EventKeyDown(EventKey):
    pass

cdef object _translation_event_key_down(void *data):
    cdef Etk_Event_Key_Down *ev
    ev = <Etk_Event_Key_Down*>data
    return EventKeyDown(ev.keyname, ev.modifiers, ev.locks, ev.key, ev.string,
                        ev.compose, ev.timestamp)


class EventKeyUp(EventKey):
    pass

cdef object _translation_event_key_up(void *data):
    cdef Etk_Event_Key_Up *ev
    ev = <Etk_Event_Key_Up*>data
    return EventKeyUp(ev.keyname, ev.modifiers, ev.locks, ev.key, ev.string,
                      ev.compose, ev.timestamp)


cdef object _event_translation_mapping(name, void *ev):
    if name == "mouse-in":
        return _translation_event_mouse_in(ev)
    if name == "mouse-out":
        return _translation_event_mouse_out(ev)
    if name == "mouse-move":
        return _translation_event_mouse_move(ev)
    if name == "mouse-down":
        return _translation_event_mouse_down(ev)
    if name == "mouse-up":
        return _translation_event_mouse_up(ev)
    if name == "mouse-click":
        return _translation_event_mouse_up(ev)
    if name == "mouse-wheel":
        return _translation_event_mouse_wheel(ev)
    if name == "key-down":
        return _translation_event_key_down(ev)
    if name == "key-up":
        return _translation_event_key_up(ev)
    else:
        return None


class EventEnums:
        MODIFIER_NONE      =  ETK_MODIFIER_NONE
        MODIFIER_CTRL      =  ETK_MODIFIER_CTRL
        MODIFIER_ALT       =  ETK_MODIFIER_ALT
        MODIFIER_SHIFT     =  ETK_MODIFIER_SHIFT
        MODIFIER_WIN       =  ETK_MODIFIER_WIN

        LOCK_NONE          =  ETK_LOCK_NONE
        LOCK_NUM           =  ETK_LOCK_NUM
        LOCK_CAPS          =  ETK_LOCK_CAPS
        LOCK_SCROLL        =  ETK_LOCK_SCROLL

        MOUSE_NONE         =  ETK_MOUSE_NONE
        MOUSE_DOUBLE_CLICK =  ETK_MOUSE_DOUBLE_CLICK
        MOUSE_TRIPLE_CLICK =  ETK_MOUSE_TRIPLE_CLICK

        WHEEL_VERTICAL     =  ETK_WHEEL_VERTICAL
        WHEEL_HORIZONTAL   =  ETK_WHEEL_HORIZONTAL
