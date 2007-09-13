cdef public class Slider(Range) [object PyEtk_Slider, type PyEtk_Slider_Type]:
    def inverted_get(self):
        __ret = bool(<int> etk_slider_inverted_get(<Etk_Slider*>self.obj))
        return (__ret)

    def inverted_set(self, int inverted):
        etk_slider_inverted_set(<Etk_Slider*>self.obj, <Etk_Bool>inverted)

    def label_get(self):
        cdef char *__char_ret
        __ret = None
        __char_ret = etk_slider_label_get(<Etk_Slider*>self.obj)
        if __char_ret != NULL:
            __ret = __char_ret
        return (__ret)

    def label_set(self, char* label_format):
        etk_slider_label_set(<Etk_Slider*>self.obj, label_format)

    def update_policy_get(self):
        __ret = <int> etk_slider_update_policy_get(<Etk_Slider*>self.obj)
        return (__ret)

    def update_policy_set(self, int policy):
        etk_slider_update_policy_set(<Etk_Slider*>self.obj, <Etk_Slider_Update_Policy>policy)

    property inverted:
        def __get__(self):
            return self.inverted_get()

        def __set__(self, inverted):
            self.inverted_set(inverted)

    property label:
        def __get__(self):
            return self.label_get()

        def __set__(self, label):
            self.label_set(label)

    property update_policy:
        def __get__(self):
            return self.update_policy_get()

        def __set__(self, update_policy):
            self.update_policy_set(update_policy)

    def _set_common_params(self, inverted=None, label=None, update_policy=None, **kargs):
        if inverted is not None:
            self.inverted_set(inverted)
        if label is not None:
            self.label_set(label)
        if update_policy is not None:
            self.update_policy_set(update_policy)

        if kargs:
            Range._set_common_params(self, **kargs)

cdef public class HSlider(Slider) [object PyEtk_HSlider, type PyEtk_HSlider_Type]:
    def __init__(self, lower=0.0, upper=1.0, value=0.0, step_increment=0.1, page_increment=0.5, **kargs):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_hslider_new(lower, upper, value, step_increment, page_increment))
        self._set_common_params(**kargs)

cdef public class VSlider(Slider) [object PyEtk_VSlider, type PyEtk_VSlider_Type]:
    def __init__(self, lower=0.0, upper=1.0, value=0.0, step_increment=0.1, page_increment=0.5, **kargs):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_vslider_new(lower, upper, value, step_increment, page_increment))
        self._set_common_params(**kargs)


class SliderEnums:
    CONTINUOUS = ETK_SLIDER_CONTINUOUS
    DISCONTINUOUS = ETK_SLIDER_DISCONTINUOUS
    DELAYED = ETK_SLIDER_DELAYED
