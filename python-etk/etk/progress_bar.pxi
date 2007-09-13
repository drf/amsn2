cdef public class ProgressBar(Widget) [object PyEtk_Progress_Bar, type PyEtk_Progress_Bar_Type]:
    def __init__(self, text=None, **kargs):
        if self.obj == NULL:
            if text is not None:
                self._set_obj(<Etk_Object*>etk_progress_bar_new_with_text(text))
            else:
                self._set_obj(<Etk_Object*>etk_progress_bar_new())
        self._set_common_params(**kargs)

    def direction_get(self):
        __ret = <int> etk_progress_bar_direction_get(<Etk_Progress_Bar*>self.obj)
        return (__ret)

    def direction_set(self, int direction):
        etk_progress_bar_direction_set(<Etk_Progress_Bar*>self.obj, <Etk_Progress_Bar_Direction>direction)

    def fraction_get(self):
        __ret = etk_progress_bar_fraction_get(<Etk_Progress_Bar*>self.obj)
        return (__ret)

    def fraction_set(self, double fraction):
        etk_progress_bar_fraction_set(<Etk_Progress_Bar*>self.obj, fraction)

    def pulse(self):
        etk_progress_bar_pulse(<Etk_Progress_Bar*>self.obj)

    def pulse_step_get(self):
        __ret = etk_progress_bar_pulse_step_get(<Etk_Progress_Bar*>self.obj)
        return (__ret)

    def pulse_step_set(self, double pulse_step):
        etk_progress_bar_pulse_step_set(<Etk_Progress_Bar*>self.obj, pulse_step)

    def text_get(self):
        cdef char *__char_ret
        __ret = None
        __char_ret = etk_progress_bar_text_get(<Etk_Progress_Bar*>self.obj)
        if __char_ret != NULL:
            __ret = __char_ret
        return (__ret)

    def text_set(self, char* label):
        etk_progress_bar_text_set(<Etk_Progress_Bar*>self.obj, label)

    property direction:
        def __get__(self):
            return self.direction_get()

        def __set__(self, direction):
            self.direction_set(direction)

    property fraction:
        def __get__(self):
            return self.fraction_get()

        def __set__(self, fraction):
            self.fraction_set(fraction)

    property pulse_step:
        def __get__(self):
            return self.pulse_step_get()

        def __set__(self, pulse_step):
            self.pulse_step_set(pulse_step)

    property text:
        def __get__(self):
            return self.text_get()

        def __set__(self, text):
            self.text_set(text)

    def _set_common_params(self, direction=None, fraction=None, pulse_step=None, text=None, **kargs):
        if direction is not None:
            self.direction_set(direction)
        if fraction is not None:
            self.fraction_set(fraction)
        if pulse_step is not None:
            self.pulse_step_set(pulse_step)
        if text is not None:
            self.text_set(text)

        if kargs:
            Widget._set_common_params(self, **kargs)


class ProgressBarEnums:
    LEFT_TO_RIGHT = ETK_PROGRESS_BAR_LEFT_TO_RIGHT
    RIGHT_TO_LEFT = ETK_PROGRESS_BAR_RIGHT_TO_LEFT
