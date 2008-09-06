cdef public class ScrolledView(Bin) [object PyEtk_Scrolled_View, type PyEtk_Scrolled_View_Type]:
    def __init__(self, **kargs):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_scrolled_view_new())
        self._set_common_params(**kargs)

    def add_with_viewport(self, Widget child):
        etk_scrolled_view_add_with_viewport(<Etk_Scrolled_View*>self.obj, <Etk_Widget*>child.obj)

    def hscrollbar_get(self):
        return Object_from_instance(<Etk_Object*>etk_scrolled_view_hscrollbar_get(<Etk_Scrolled_View*>self.obj))

    def policy_get(self):
        cdef Etk_Scrolled_View_Policy hpolicy
        cdef Etk_Scrolled_View_Policy vpolicy
        etk_scrolled_view_policy_get(<Etk_Scrolled_View*>self.obj, &hpolicy, &vpolicy)
        return (hpolicy, vpolicy)

    def policy_set(self, int hpolicy, int vpolicy):
        etk_scrolled_view_policy_set(<Etk_Scrolled_View*>self.obj, <Etk_Scrolled_View_Policy>hpolicy, <Etk_Scrolled_View_Policy>vpolicy)

    def dragable_get(self):
        return etk_scrolled_view_dragable_get(<Etk_Scrolled_View*>self.obj)

    def dragable_set(self, Etk_Bool dragable):
        etk_scrolled_view_dragable_set(<Etk_Scrolled_View*>self.obj, <Etk_Bool>dragable)

    def drag_bouncy_get(self):
        return etk_scrolled_view_drag_bouncy_get(<Etk_Scrolled_View*>self.obj)

    def drag_bouncy_set(self, Etk_Bool bouncy):
        etk_scrolled_view_drag_bouncy_set(<Etk_Scrolled_View*>self.obj, <Etk_Bool>bouncy)

    def drag_interval_get(self):
        return etk_scrolled_view_drag_sample_interval_get(<Etk_Scrolled_View*>self.obj)

    def drag_interval_set(self, double interval):
        return etk_scrolled_view_drag_sample_interval_set(<Etk_Scrolled_View*>self.obj, <double>interval)

    def drag_damping_get(self):
        return etk_scrolled_view_drag_damping_get(<Etk_Scrolled_View*>self.obj)

    def drag_damping_set(self, unsigned int damping):
        return etk_scrolled_view_drag_damping_set(<Etk_Scrolled_View*>self.obj, <unsigned int>damping)

    def vscrollbar_get(self):
        return Object_from_instance(<Etk_Object*>etk_scrolled_view_vscrollbar_get(<Etk_Scrolled_View*>self.obj))

    property dragable:
        def __get__(self):
            return self.dragable_get()

        def __set__(self, v):
            self.dragable_set(v)

    property drag_bouncy:
        def __get__(self):
            return self.drag_bouncy_get()

        def __set__(self, v):
            self.drag_bouncy_set(v)

    property drag_interval:
        def __get__(self):
            return self.drag_interval_get()

        def __set__(self, v):
            self.drag_interval_set(v)

    property drag_damping:
        def __get__(self):
            return self.drag_damping_get()

        def __set__(self, v):
            self.drag_damping_set(v)

    property hscrollbar:
        def __get__(self):
            return self.hscrollbar_get()

    property policy:
        def __get__(self):
            return self.policy_get()

        def __set__(self, policy):
            self.policy_set(*policy)

    property vscrollbar:
        def __get__(self):
            return self.vscrollbar_get()

    def _set_common_params(self, policy=None, **kargs):
        if policy is not None:
            self.policy_set(*policy)

        if kargs:
            Bin._set_common_params(self, **kargs)


class ScrolledViewEnums:
    AUTO = ETK_POLICY_AUTO
    SHOW = ETK_POLICY_SHOW
    HIDE = ETK_POLICY_HIDE
