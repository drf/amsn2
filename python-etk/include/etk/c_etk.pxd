from evas.c_evas cimport Evas_List, Evas_Hash, Evas_Object, Evas
cimport evas.c_evas
import evas.c_evas

cdef extern from "stdarg.h":
    ctypedef void *va_list
    void va_start(va_list ap, void *last)
    void va_end(va_list ap)

cdef extern from "etk_main.h":
    int etk_init(int argc, char **argv)
    void etk_main()
    void etk_main_iterate()
    void etk_main_quit()
    int etk_shutdown()


cdef extern from "etk_types.h":
    ctypedef int Etk_Bool
    ctypedef struct Etk_Geometry:
        int x
        int y
        int w
        int h
    ctypedef struct Etk_Size:
        int w
        int h
    ctypedef struct Etk_Position:
        int x
        int y

    ctypedef struct Etk_Type
    ctypedef struct Etk_Object:
        Etk_Type *type
        char *name
        Etk_Bool destroy_me
        Etk_Object *prev
        Etk_Object *next
        Evas_Hash *data_hash
        Evas_List *signal_callbacks
        Evas_List *weak_pointers
        Evas_Hash *notification_callbacks
        Etk_Bool should_delete_cbs
        int notifying

    ctypedef struct Etk_Toplevel
    ctypedef void (*Etk_Accumulator)(void *return_value, void *value_to_accum, void *data)
    ctypedef void (*Etk_Constructor)(Etk_Object *object)
    ctypedef void (*Etk_Destructor)(Etk_Object *object)
    ctypedef void (*Etk_Callback)()
    ctypedef void (*Etk_Callback_Swapped)(void *data)
    ctypedef void (*Etk_Marshaller)(Etk_Callback callback, Etk_Object *object, void *data, void *return_value, va_list arguments)


cdef extern from "etk_signal.h":
    ctypedef struct Etk_Signal:
        char *name
        int code
        long handler_offset
        Etk_Marshaller marshaller


cdef extern from "etk_type.h":
    ctypedef void *Etk_Property_Value
    ctypedef struct Etk_Type:
        char *name
        int hierarchy_depth
        Etk_Type **hierarchy
        Etk_Constructor constructor
        Etk_Destructor destructor
        void (*property_set)(Etk_Object *object, int property_id, Etk_Property_Value *value)
        void (*property_get)(Etk_Object *object, int property_id, Etk_Property_Value *value)
        int type_size

        Etk_Signal **signals
        Evas_Hash *properties_hash


cdef extern from "etk_theme.h":
    ctypedef struct Etk_Widget # XXX
    Etk_Bool etk_theme_widget_set_from_path(char *theme_path)
    Etk_Bool etk_theme_edje_object_set(Evas_Object *object, char *file,
                                       char *group, char *parent_group)
    Etk_Bool etk_theme_edje_object_set_from_parent(Evas_Object *object,
                                                   char *group,
                                                   Etk_Widget *parent)


include "type.pxd"
include "types.pxd"
include "signal_callback.pxd"
include "object.pxd"
include "signal.pxd"
include "widget.pxd"
include "label.pxd"
include "container.pxd"
include "bin.pxd"
include "toplevel.pxd"
include "window.pxd"
include "embed.pxd"
include "stock.pxd"
include "box.pxd"
include "image.pxd"
include "button.pxd"
include "table.pxd"
include "entry.pxd"
include "combobox.pxd"
include "combobox_entry.pxd"
include "progress_bar.pxd"
include "range.pxd"
include "slider.pxd"
include "frame.pxd"
include "canvas.pxd"
include "toggle_button.pxd"
include "event.pxd"
include "viewport.pxd"
include "scrolled_view.pxd"
include "alignment.pxd"
include "scrollbar.pxd"
include "separator.pxd"
