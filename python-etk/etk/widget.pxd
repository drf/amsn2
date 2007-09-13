cdef extern from "etk_widget.h":
    ####################################################################
    # Enumerations
    ctypedef enum Etk_Widget_Swallow_Error:
        ETK_SWALLOW_ERROR_NONE
        ETK_SWALLOW_ERROR_INCOMPATIBLE_PARENT
        ETK_SWALLOW_ERROR_NOT_REALIZED
        ETK_SWALLOW_ERROR_NO_PART

    ####################################################################
    # Structures
    ctypedef struct Etk_Widget:
        void (*size_request)(Etk_Widget *widget, Etk_Size *size_requisition)
        void (*size_allocate)(Etk_Widget *widget, Etk_Geometry geometry)
        void (*theme_signal_emit)(Etk_Widget *widget, char *signal, Etk_Bool size_recalc)
        void (*scroll_size_get)(Etk_Widget *widget, Etk_Size scrollview_size, Etk_Size scrollbar_size, Etk_Size *scroll_size)
        void (*scroll_margins_get)(Etk_Widget *widget, Etk_Size *margin_size)
        void (*scroll)(Etk_Widget *widget, int x, int y)


    ####################################################################
    # Functions
    Evas_List* etk_widget_dnd_dest_widgets_get()
    int etk_widget_swallow_error_get()
    Etk_Type* etk_widget_type_get()
    Etk_Widget* etk_widget_new(Etk_Type* widget_type)
    evas.c_evas.Evas_Object* etk_widget_clip_get(Etk_Widget* __self)
    void etk_widget_clip_set(Etk_Widget* __self, evas.c_evas.Evas_Object* clip)
    void etk_widget_clip_unset(Etk_Widget* __self)
    void etk_widget_color_get(Etk_Widget* __self, int* r, int* g, int* b, int* a)
    void etk_widget_color_set(Etk_Widget* __self, int r, int g, int b, int a)
    int etk_widget_disabled_get(Etk_Widget* __self)
    void etk_widget_disabled_set(Etk_Widget* __self, int disabled)
    void etk_widget_disabled_set_all(Etk_Widget* __self, int disabled)
    int etk_widget_dnd_dest_get(Etk_Widget* __self)
    void etk_widget_dnd_dest_set(Etk_Widget* __self, int on)
    void etk_widget_dnd_drag_data_set(Etk_Widget* __self, char** types, int num_types, void* data, int data_size)
    Etk_Widget* etk_widget_dnd_drag_widget_get(Etk_Widget* __self)
    void etk_widget_dnd_drag_widget_set(Etk_Widget* __self, Etk_Widget* drag_widget)
    char** etk_widget_dnd_files_get(Etk_Widget* __self, int* num_files)
    int etk_widget_dnd_internal_get(Etk_Widget* __self)
    void etk_widget_dnd_internal_set(Etk_Widget* __self, int on)
    int etk_widget_dnd_source_get(Etk_Widget* __self)
    void etk_widget_dnd_source_set(Etk_Widget* __self, int on)
    char** etk_widget_dnd_types_get(Etk_Widget* __self, int* num)
    void etk_widget_dnd_types_set(Etk_Widget* __self, char** types, int num)
    void etk_widget_enter(Etk_Widget* __self)
    void etk_widget_focus(Etk_Widget* __self)
    int etk_widget_focusable_get(Etk_Widget* __self)
    void etk_widget_focusable_set(Etk_Widget* __self, int focusable)
    void etk_widget_geometry_get(Etk_Widget* __self, int* x, int* y, int* w, int* h)
    int etk_widget_has_event_object_get(Etk_Widget* __self)
    void etk_widget_has_event_object_set(Etk_Widget* __self, int has_event_object)
    void etk_widget_hide(Etk_Widget* __self)
    void etk_widget_hide_all(Etk_Widget* __self)
    void etk_widget_inner_geometry_get(Etk_Widget* __self, int* x, int* y, int* w, int* h)
    int etk_widget_internal_get(Etk_Widget* __self)
    void etk_widget_internal_set(Etk_Widget* __self, int internal)
    int etk_widget_is_focused(Etk_Widget* __self)
    int etk_widget_is_swallowed(Etk_Widget* __self)
    int etk_widget_is_visible(Etk_Widget* __self)
    void etk_widget_leave(Etk_Widget* __self)
    void etk_widget_lower(Etk_Widget* __self)
    int etk_widget_member_object_add(Etk_Widget* __self, evas.c_evas.Evas_Object* object)
    void etk_widget_member_object_del(Etk_Widget* __self, evas.c_evas.Evas_Object* object)
    void etk_widget_member_object_lower(Etk_Widget* __self, evas.c_evas.Evas_Object* object)
    void etk_widget_member_object_raise(Etk_Widget* __self, evas.c_evas.Evas_Object* object)
    void etk_widget_member_object_stack_above(Etk_Widget* __self, evas.c_evas.Evas_Object* object, evas.c_evas.Evas_Object* above)
    void etk_widget_member_object_stack_below(Etk_Widget* __self, evas.c_evas.Evas_Object* object, evas.c_evas.Evas_Object* below)
    void etk_widget_padding_get(Etk_Widget* __self, int* left, int* right, int* top, int* bottom)
    void etk_widget_padding_set(Etk_Widget* __self, int left, int right, int top, int bottom)
    Etk_Widget* etk_widget_parent_get(Etk_Widget* __self)
    void etk_widget_parent_set(Etk_Widget* __self, Etk_Widget* parent)
    int etk_widget_pass_mouse_events_get(Etk_Widget* __self)
    void etk_widget_pass_mouse_events_set(Etk_Widget* __self, int pass_mouse_events)
    int etk_widget_propagate_color_get(Etk_Widget* __self)
    void etk_widget_propagate_color_set(Etk_Widget* __self, int propagate_color)
    void etk_widget_raise(Etk_Widget* __self)
    void etk_widget_redraw_queue(Etk_Widget* __self)
    int etk_widget_repeat_mouse_events_get(Etk_Widget* __self)
    void etk_widget_repeat_mouse_events_set(Etk_Widget* __self, int repeat_mouse_events)
    void etk_widget_show(Etk_Widget* __self)
    void etk_widget_show_all(Etk_Widget* __self)
    void etk_widget_size_allocate(Etk_Widget* __self, Etk_Geometry geometry)
    void etk_widget_size_recalc_queue(Etk_Widget* __self)
    void etk_widget_size_request(Etk_Widget* __self, Etk_Size* size_requisition)
    void etk_widget_size_request_full(Etk_Widget* __self, Etk_Size* size_requisition, int hidden_has_no_size)
    void etk_widget_size_request_set(Etk_Widget* __self, int w, int h)
    int etk_widget_swallow_object(Etk_Widget* __self, char* part, evas.c_evas.Evas_Object* object)
    int etk_widget_swallow_widget(Etk_Widget* __self, char* part, Etk_Widget* to_swallow)
    int etk_widget_theme_data_get(Etk_Widget* __self, char* data_name, char* format)
    char* etk_widget_theme_file_get(Etk_Widget* __self)
    void etk_widget_theme_file_set(Etk_Widget* __self, char* theme_file)
    char* etk_widget_theme_group_get(Etk_Widget* __self)
    void etk_widget_theme_group_set(Etk_Widget* __self, char* theme_group)
    Etk_Widget* etk_widget_theme_parent_get(Etk_Widget* __self)
    void etk_widget_theme_parent_set(Etk_Widget* __self, Etk_Widget* theme_parent)
    void etk_widget_theme_part_text_set(Etk_Widget* __self, char* part_name, char* text)
    void etk_widget_theme_set(Etk_Widget* __self, char* theme_file, char* theme_group)
    void etk_widget_theme_signal_emit(Etk_Widget* __self, char* signal_name, int size_recalc)
    evas.c_evas.Evas* etk_widget_toplevel_evas_get(Etk_Widget* __self)
    Etk_Toplevel* etk_widget_toplevel_parent_get(Etk_Widget* __self)
    void etk_widget_unfocus(Etk_Widget* __self)
    void etk_widget_unswallow_object(Etk_Widget* __self, evas.c_evas.Evas_Object* object)
    void etk_widget_unswallow_widget(Etk_Widget* __self, Etk_Widget* swallowed)

#########################################################################
# Objects
cdef public class Widget(Object) [object PyEtk_Widget, type PyEtk_Widget_Type]:
    cdef object _virtual_size_request

    cdef int _set_obj(self, Etk_Object *obj) except 0

