cdef extern from "etk_scrolled_view.h":
    ####################################################################
    # Signals

    ####################################################################
    # Enumerations
    ctypedef enum Etk_Scrolled_View_Policy:
        ETK_POLICY_AUTO
        ETK_POLICY_SHOW
        ETK_POLICY_HIDE

    ####################################################################
    # Structures
    ctypedef struct Etk_Scrolled_View

    ####################################################################
    # Functions
    Etk_Type* etk_scrolled_view_type_get()
    Etk_Widget* etk_scrolled_view_new()
    void etk_scrolled_view_add_with_viewport(Etk_Scrolled_View* __self, Etk_Widget* child)
    Etk_Range* etk_scrolled_view_hscrollbar_get(Etk_Scrolled_View* __self)
    void etk_scrolled_view_policy_get(Etk_Scrolled_View* __self, Etk_Scrolled_View_Policy* hpolicy, Etk_Scrolled_View_Policy* vpolicy)
    void etk_scrolled_view_policy_set(Etk_Scrolled_View* __self, int hpolicy, int vpolicy)
    Etk_Bool etk_scrolled_view_dragable_get(Etk_Scrolled_View* __self)
    void etk_scrolled_view_dragable_set(Etk_Scrolled_View* __self, Etk_Bool dragable)
    Etk_Bool etk_scrolled_view_drag_bouncy_get(Etk_Scrolled_View* __self)
    void etk_scrolled_view_drag_bouncy_set(Etk_Scrolled_View* __self, Etk_Bool bouncy)
    double etk_scrolled_view_drag_sample_interval_get(Etk_Scrolled_View* __self)
    double etk_scrolled_view_drag_sample_interval_set(Etk_Scrolled_View* __self, double interval)
    unsigned int etk_scrolled_view_drag_damping_get(Etk_Scrolled_View* __self)
    unsigned int etk_scrolled_view_drag_damping_set(Etk_Scrolled_View* __self, unsigned int damping)
    Etk_Range* etk_scrolled_view_vscrollbar_get(Etk_Scrolled_View* __self)

#########################################################################
# Objects
cdef public class ScrolledView(Bin) [object PyEtk_Scrolled_View, type PyEtk_Scrolled_View_Type]:
    pass

