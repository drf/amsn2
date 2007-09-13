cdef public class ToggleButton(Button) [object PyEtk_Toggle_Button, type PyEtk_Toggle_Button_Type]:
    def __init__(self, label=None, **kargs):
        if self.obj == NULL:
            if label is None:
                self._set_obj(<Etk_Object*>etk_toggle_button_new())
            else:
                self._set_obj(<Etk_Object*>etk_toggle_button_new_with_label(label))
        self._set_common_params(**kargs)

    def active_get(self):
        __ret = bool(<int> etk_toggle_button_active_get(<Etk_Toggle_Button*>self.obj))
        return (__ret)

    def active_set(self, int active):
        etk_toggle_button_active_set(<Etk_Toggle_Button*>self.obj, <Etk_Bool>active)

    def toggle(self):
        etk_toggle_button_toggle(<Etk_Toggle_Button*>self.obj)

    property active:
        def __get__(self):
            return self.active_get()

        def __set__(self, active):
            self.active_set(active)

    def _set_common_params(self, active=None, **kargs):
        if active is not None:
            self.active_set(active)

        if kargs:
            Button._set_common_params(self, **kargs)


class ToggleButtonEnums:
    pass
