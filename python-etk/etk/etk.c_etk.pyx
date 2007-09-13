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

    for i from 0 <= i < argc_orig:
        python.PyMem_Free(argv_copy[i])
    python.PyMem_Free(argv_copy)
    python.PyMem_Free(argv)

    ret = etk_init(&argc, &argv)
    return ret

def shutdown():
    return etk_shutdown()

def main():
    etk_main()

def main_iterate():
    etk_main_iterate()

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

cdef Object Object_from_instance(Etk_Object *obj):
    cdef void *data
    cdef Object o
    cdef Etk_Type *t

    if obj == NULL:
        return None

    data = etk_object_data_get(obj, 'python-etk')
    if data != NULL:
        o = <Object>data
    else:
        t = etk_object_object_type_get(obj)
        cls = object_mapping.get(t.name, Object)
        o = cls.__new__(cls)
        o._set_obj(obj)

    return o

def _Object_from_instance(long ptr):
    return Object_from_instance(<Etk_Object*>ptr)

def theme_widget_set_from_path(path):
    etk_theme_widget_set_from_path(path)

include "object.pxi"
include "type.pxi"
include "widget.pxi"
include "label.pxi"
include "container.pxi"
include "bin.pxi"
include "toplevel.pxi"
include "window.pxi"
include "embed.pxi"
include "box.pxi"
include "image.pxi"
include "button.pxi"
include "table.pxi"
include "entry.pxi"
include "combobox.pxi"
include "combobox_entry.pxi"
include "progress_bar.pxi"
include "range.pxi"
include "slider.pxi"
include "frame.pxi"
include "canvas.pxi"
include "toggle_button.pxi"
include "event.pxi"
