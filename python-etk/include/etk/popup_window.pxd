cdef extern from "etk_popup_window.h":
    ####################################################################
    # Signals
    int ETK_POPUP_WINDOW_POPPED_DOWN_SIGNAL
    int ETK_POPUP_WINDOW_POPPED_UP_SIGNAL
    
    ####################################################################
    # Enumerations
    ctypedef enum Etk_Popup_Direction:
        ETK_POPUP_BELOW_RIGHT
        ETK_POPUP_BELOW_LEFT
        ETK_POPUP_ABOVE_RIGHT
        ETK_POPUP_ABOVE_LEFT
        
    ####################################################################
    # Structures
    ctypedef struct Etk_Popup_Window

    ####################################################################
    # Functions
    void etk_popup_window_parent_set(Etk_Popup_Window* __self, Etk_Popup_Window* parent)
    Etk_Popup_Window* etk_popup_window_parent_get(Etk_Popup_Window* __self)
    void etk_popup_window_focused_window_set(Etk_Popup_Window* __self)
    Etk_Popup_Window* etk_popup_window_focused_window_get()
    void etk_popup_window_popup(Etk_Popup_Window* __self)
    void etk_popup_window_popup_in_direction(Etk_Popup_Window* __self, Etk_Popup_Direction direction)
    void etk_popup_window_popup_at_xy(Etk_Popup_Window* __self, int x, int y)
    void etk_popup_window_popup_at_xy_in_direction(Etk_Popup_Window* __self, int x, int y, Etk_Popup_Direction direction)
    void etk_popup_window_popdown(Etk_Popup_Window* __self)
    void etk_popup_window_popdown_all()
    Etk_Bool etk_popup_window_is_popped_up(Etk_Popup_Window* __self)
    

#########################################################################
# Objects
cdef public class PopupWindow(Window) [object PyEtk_Popup_Window, type PyEtk_Popup_Window_Type]:
    pass

