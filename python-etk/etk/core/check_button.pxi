cdef public class CheckButton(ToggleButton) [object PyEtk_Check_Button, type PyEtk_Check_Button_Type]:
    def __init__(self, label=None, **kargs):
        if self.obj == NULL:
            if label is None:
                self._set_obj(<Etk_Object*>etk_check_button_new())
            else:
                self._set_obj(<Etk_Object*>etk_check_button_new_with_label(label))
        self._set_common_params(**kargs)
