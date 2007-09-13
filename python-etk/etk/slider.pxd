cdef extern from "etk_slider.h":
    ####################################################################
    # Enumerations
    ctypedef enum Etk_Slider_Update_Policy:
        ETK_SLIDER_CONTINUOUS
        ETK_SLIDER_DISCONTINUOUS
        ETK_SLIDER_DELAYED

    ####################################################################
    # Structures
    ctypedef struct Etk_Slider
    ctypedef struct Etk_HSlider
    ctypedef struct Etk_VSlider

    ####################################################################
    # Functions
    Etk_Type* etk_hslider_type_get()
    Etk_Type* etk_slider_type_get()
    Etk_Type* etk_vslider_type_get()
    int etk_slider_inverted_get(Etk_Slider* __self)
    void etk_slider_inverted_set(Etk_Slider* __self, int inverted)
    char* etk_slider_label_get(Etk_Slider* __self)
    void etk_slider_label_set(Etk_Slider* __self, char* label_format)
    int etk_slider_update_policy_get(Etk_Slider* __self)
    void etk_slider_update_policy_set(Etk_Slider* __self, int policy)
    Etk_Widget* etk_hslider_new(double lower, double upper, double value, double step_increment, double page_increment)
    Etk_Widget* etk_vslider_new(double lower, double upper, double value, double step_increment, double page_increment)

#########################################################################
# Objects
cdef public class Slider(Range) [object PyEtk_Slider, type PyEtk_Slider_Type]:
    pass
cdef public class HSlider(Slider) [object PyEtk_HSlider, type PyEtk_HSlider_Type]:
    pass
cdef public class VSlider(Slider) [object PyEtk_VSlider, type PyEtk_VSlider_Type]:
    pass

