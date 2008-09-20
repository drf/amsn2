cdef public class FilechooserWidget(Widget) [object PyEtk_Filechooser_Widget, type PyEtk_Filechooser_Widget_Type]:
    def __init__(self, **kargs):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_filechooser_widget_new())
        self._set_common_params(**kargs)

    def current_folder_get(self):
        cdef char *__char_ret
        __ret = None
        __char_ret = etk_filechooser_widget_current_folder_get(<Etk_Filechooser_Widget*>self.obj)
        if __char_ret != NULL:
            __ret = __char_ret
        return (__ret)

    def current_folder_set(self, char* folder):
        etk_filechooser_widget_current_folder_set(<Etk_Filechooser_Widget*>self.obj, folder)

    def is_save_get(self):
        __ret = bool(<int> etk_filechooser_widget_is_save_get(<Etk_Filechooser_Widget*>self.obj))
        return (__ret)

    def is_save_set(self, int is_save):
        etk_filechooser_widget_is_save_set(<Etk_Filechooser_Widget*>self.obj, <Etk_Bool>is_save)

    def select_multiple_get(self):
        __ret = bool(<int> etk_filechooser_widget_select_multiple_get(<Etk_Filechooser_Widget*>self.obj))
        return (__ret)

    def select_multiple_set(self, int select_multiple):
        etk_filechooser_widget_select_multiple_set(<Etk_Filechooser_Widget*>self.obj, <Etk_Bool>select_multiple)

    def selected_file_get(self):
        cdef char *__char_ret
        __ret = None
        __char_ret = etk_filechooser_widget_selected_file_get(<Etk_Filechooser_Widget*>self.obj)
        if __char_ret != NULL:
            __ret = __char_ret
        return (__ret)

    def selected_file_set(self, char* filename):
        __ret = bool(<int> etk_filechooser_widget_selected_file_set(<Etk_Filechooser_Widget*>self.obj, filename))
        return (__ret)

    def selected_files_get(self):
        cdef Evas_List* __lst
        __ret = []

        __lst = etk_filechooser_widget_selected_files_get(<Etk_Filechooser_Widget*>self.obj)
        while __lst != NULL:
            __ret.append(<char*> __lst.data)
            __lst = __lst.next

        evas.c_evas.evas_list_free(__lst)
        return (__ret)

    def show_hidden_get(self):
        __ret = bool(<int> etk_filechooser_widget_show_hidden_get(<Etk_Filechooser_Widget*>self.obj))
        return (__ret)

    def show_hidden_set(self, int show_hidden):
        etk_filechooser_widget_show_hidden_set(<Etk_Filechooser_Widget*>self.obj, <Etk_Bool>show_hidden)

    property current_folder:
        def __get__(self):
            return self.current_folder_get()

        def __set__(self, current_folder):
            self.current_folder_set(current_folder)

    property is_save:
        def __get__(self):
            return self.is_save_get()

        def __set__(self, is_save):
            self.is_save_set(is_save)

    property select_multiple:
        def __get__(self):
            return self.select_multiple_get()

        def __set__(self, select_multiple):
            self.select_multiple_set(select_multiple)

    property selected_file:
        def __get__(self):
            return self.selected_file_get()

        def __set__(self, selected_file):
            self.selected_file_set(selected_file)

    property selected_files:
        def __get__(self):
            return self.selected_files_get()

    property show_hidden:
        def __get__(self):
            return self.show_hidden_get()

        def __set__(self, show_hidden):
            self.show_hidden_set(show_hidden)

    def _set_common_params(self, current_folder=None, is_save=None, select_multiple=None, selected_file=None, show_hidden=None, **kargs):
        if current_folder is not None:
            self.current_folder_set(current_folder)
        if is_save is not None:
            self.is_save_set(is_save)
        if select_multiple is not None:
            self.select_multiple_set(select_multiple)
        if selected_file is not None:
            self.selected_file_set(selected_file)
        if show_hidden is not None:
            self.show_hidden_set(show_hidden)

        if kargs:
            Widget._set_common_params(self, **kargs)
