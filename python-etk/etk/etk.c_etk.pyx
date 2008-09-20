cimport python
import sys

def init():
    cdef int argc, argc_orig, i, arg_len, ret
    cdef char **argv, **argv_copy, *arg
    argc_orig = argc = len(sys.argv)
    argv = <char **>python.PyMem_Malloc(argc * sizeof(char *))
    argv_copy = <char **>python.PyMem_Malloc(argc * sizeof(char *))
    for i from 0 <= i < argc:
        arg = sys.argv[i]
        arg_len = len(sys.argv[i])
        argv[i] = <char *>python.PyMem_Malloc(arg_len + 1)
        argv_copy[i] = argv[i]
        python.memcpy(argv[i], arg, arg_len + 1)

    ret = etk_init(argc, argv)

    for i from 0 <= i < argc_orig:
        python.PyMem_Free(argv_copy[i])
    python.PyMem_Free(argv_copy)
    python.PyMem_Free(argv)

    return ret

def shutdown():
    return etk_shutdown()

def main():
    python.Py_BEGIN_ALLOW_THREADS
    etk_main()
    python.Py_END_ALLOW_THREADS

def main_iterate():
    python.Py_BEGIN_ALLOW_THREADS
    etk_main_iterate()
    python.Py_END_ALLOW_THREADS

def main_quit():
    etk_main_quit()


# Mapping from Etk_Type name to correct Python class
cdef object object_mapping
object_mapping = dict()

def _object_mapping_register(char *name, cls):
    if name in object_mapping:
        raise ValueError("object type name '%s' already registered." % name)
    object_mapping[name] = cls

def _object_mapping_unregister(char *name):
    del object_mapping[name]


class EtkMeta(type):
    def __init__(cls, name, bases, dict_):
        type.__init__(cls, name, bases, dict_)
        cls._register_etk_type()

    def _register_etk_type(cls):
        if hasattr(cls, "_etk_type"):
            etk_type = getattr(cls, "_etk_type")
            try:
                _object_mapping_register(etk_type, cls)
            except ValueError:
                pass  # only register stuff with new _etk_type name


cdef Object Object_from_instance(Etk_Object *obj):
    cdef void *data
    cdef Object o
    cdef Etk_Type *t

    if obj == NULL:
        return None

    data = etk_object_data_get(obj, 'python-etk')
    if data != NULL:
        return <Object>data
    else:
        t = etk_object_object_type_get(obj)
        cls = object_mapping.get(t.name, Object)
        o = cls.__new__(cls)
        return o._set_obj(obj)

def _Object_from_instance(long ptr):
    return Object_from_instance(<Etk_Object*>ptr)

def theme_widget_set_from_path(path):
    etk_theme_widget_set_from_path(path)


def theme_edje_object_set_from_parent(evas.c_evas.Object obj, group,
                                      Widget parent):
    cdef Etk_Widget *p
    if parent is None:
        p = NULL
    else:
        p = <Etk_Widget*>parent.obj
    etk_theme_edje_object_set_from_parent(obj.obj, group, p)

def theme_edje_object_set(evas.c_evas.Object obj, file, group,
                          parent_group=""):
    cdef char *cfile
    if file is None:
        cfile = NULL
    else:
        cfile = file
    return etk_theme_edje_object_set(obj.obj, cfile, group, parent_group)



include "core/object.pxi"
include "core/type.pxi"
include "core/widget.pxi"
include "core/label.pxi"
include "core/container.pxi"
include "core/bin.pxi"
include "core/toplevel.pxi"
include "core/window.pxi"
include "core/embed.pxi"
include "core/box.pxi"
include "core/image.pxi"
include "core/button.pxi"
include "core/table.pxi"
include "core/entry.pxi"
include "core/combobox.pxi"
include "core/combobox_entry.pxi"
include "core/progress_bar.pxi"
include "core/range.pxi"
include "core/slider.pxi"
include "core/frame.pxi"
include "core/canvas.pxi"
include "core/toggle_button.pxi"
include "core/event.pxi"
include "core/viewport.pxi"
include "core/scrolled_view.pxi"
include "core/alignment.pxi"
include "core/scrollbar.pxi"
include "core/separator.pxi"
include "core/filechooser_widget.pxi"
include "core/check_button.pxi"
include "core/spinner.pxi"
include "core/popup_window.pxi"
include "core/menu.pxi"
include "core/menu_shell.pxi"
include "core/menu_bar.pxi"
include "core/menu_item.pxi"
include "core/evas_object.pxi"
include "core/string.pxi"
include "core/text.pxi"
include "core/paned.pxi"
