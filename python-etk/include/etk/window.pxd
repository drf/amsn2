cdef extern from "etk_window.h":
    ####################################################################
    # Signals
    int ETK_WINDOW_MOVED_SIGNAL
    int ETK_WINDOW_RESIZED_SIGNAL
    int ETK_WINDOW_FOCUSED_IN_SIGNAL
    int ETK_WINDOW_FOCUSED_OUT_SIGNAL
    int ETK_WINDOW_DELETE_EVENT_SIGNAL

    ####################################################################
    # Enumerations
    ctypedef enum Etk_Window_Stacking:
        ETK_WINDOW_NORMAL
        ETK_WINDOW_ABOVE
        ETK_WINDOW_BELOW

    ####################################################################
    # Structures
    ctypedef struct Etk_Window

    ####################################################################
    # Functions
    int etk_window_hide_on_delete(Etk_Object* window, void* data)
    Etk_Type* etk_window_type_get()
    Etk_Widget* etk_window_new()
    void etk_window_center_on_window(Etk_Window* __self, Etk_Window* window)
    int etk_window_decorated_get(Etk_Window* __self)
    void etk_window_decorated_set(Etk_Window* __self, int decorated)
    void etk_window_delete_request(Etk_Window* __self)
    int etk_window_focused_get(Etk_Window* __self)
    void etk_window_focused_set(Etk_Window* __self, int focused)
    int etk_window_fullscreen_get(Etk_Window* __self)
    void etk_window_fullscreen_set(Etk_Window* __self, int fullscreen)
    void etk_window_geometry_get(Etk_Window* __self, int* x, int* y, int* w, int* h)
    int etk_window_has_alpha_get(Etk_Window* __self)
    void etk_window_has_alpha_set(Etk_Window* __self, int has_alpha)
    int etk_window_iconified_get(Etk_Window* __self)
    void etk_window_iconified_set(Etk_Window* __self, int iconified)
    void etk_window_lower(Etk_Window* __self)
    int etk_window_maximized_get(Etk_Window* __self)
    void etk_window_maximized_set(Etk_Window* __self, int maximized)
    void etk_window_modal_for_window(Etk_Window* __self, Etk_Window* window)
    void etk_window_move(Etk_Window* __self, int x, int y)
    void etk_window_move_to_mouse(Etk_Window* __self)
    void etk_window_raise(Etk_Window* __self)
    void etk_window_resize(Etk_Window* __self, int w, int h)
    int etk_window_shaped_get(Etk_Window* __self)
    void etk_window_shaped_set(Etk_Window* __self, int shaped)
    int etk_window_skip_pager_hint_get(Etk_Window* __self)
    void etk_window_skip_pager_hint_set(Etk_Window* __self, int skip_pager_hint)
    int etk_window_skip_taskbar_hint_get(Etk_Window* __self)
    void etk_window_skip_taskbar_hint_set(Etk_Window* __self, int skip_taskbar_hint)
    int etk_window_stacking_get(Etk_Window* __self)
    void etk_window_stacking_set(Etk_Window* __self, int stacking)
    int etk_window_sticky_get(Etk_Window* __self)
    void etk_window_sticky_set(Etk_Window* __self, int sticky)
    char* etk_window_title_get(Etk_Window* __self)
    void etk_window_title_set(Etk_Window* __self, char* title)
    void etk_window_wmclass_set(Etk_Window* __self, char* window_name, char* window_class)

#########################################################################
# Objects
cdef public class Window(Toplevel) [object PyEtk_Window, type PyEtk_Window_Type]:
    pass

