cdef extern from "etk_filechooser_widget.h":
    ####################################################################
    # Signals

    ####################################################################
    # Enumerations
    ####################################################################
    # Structures
    ctypedef struct Etk_Filechooser_Widget

    ####################################################################
    # Functions
    Etk_Type* etk_filechooser_widget_type_get()
    Etk_Widget* etk_filechooser_widget_new()
    char* etk_filechooser_widget_current_folder_get(Etk_Filechooser_Widget* __self)
    void etk_filechooser_widget_current_folder_set(Etk_Filechooser_Widget* __self, char* folder)
    int etk_filechooser_widget_is_save_get(Etk_Filechooser_Widget* __self)
    void etk_filechooser_widget_is_save_set(Etk_Filechooser_Widget* __self, int is_save)
    int etk_filechooser_widget_select_multiple_get(Etk_Filechooser_Widget* __self)
    void etk_filechooser_widget_select_multiple_set(Etk_Filechooser_Widget* __self, int select_multiple)
    char* etk_filechooser_widget_selected_file_get(Etk_Filechooser_Widget* __self)
    int etk_filechooser_widget_selected_file_set(Etk_Filechooser_Widget* __self, char* filename)
    evas.c_evas.Evas_List* etk_filechooser_widget_selected_files_get(Etk_Filechooser_Widget* __self)
    int etk_filechooser_widget_show_hidden_get(Etk_Filechooser_Widget* __self)
    void etk_filechooser_widget_show_hidden_set(Etk_Filechooser_Widget* __self, int show_hidden)

#########################################################################
# Objects
cdef public class FilechooserWidget(Widget) [object PyEtk_Filechooser_Widget, type PyEtk_Filechooser_Widget_Type]:
    pass
