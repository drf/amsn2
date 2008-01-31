#!/usr/bin/python

import etk
import evas
import ecore.evas
import ecore.x
import edje
import sys
import os

def set_pointer(user_data, pointer):
    if pointer == etk.Embed.POINTER_NONE:
        user_data.x_window_cursor_shape_set(0)
    elif pointer == etk.Embed.POINTER_TEXT_EDIT:
        user_data.x_window_cursor_shape_set(ecore.x.ECORE_X_CURSOR_XTERM)
    else:
        user_data.x_window_cursor_shape_set(ecore.x.ECORE_X_CURSOR_LEFT_PTR)

def get_position(user_data):
    (x, y, w, h) = user_data.geometry_get()
    return (x, y)

ecore_evas = ecore.evas.SoftwareX11()
ecore_evas.title = "ETK Embed demo"

edje_file = os.path.join(os.path.dirname(sys.argv[0]), "06-embed.edj")
edj = edje.Edje(ecore_evas.evas, file=edje_file, group="main")
edj.size = ecore_evas.size
ecore_evas.data["edje"] = edj


# Setup callback for resize
def resize_cb(ee):
    r = ee.evas.rect
    ee.data["edje"].size = r.size

ecore_evas.callback_resize = resize_cb

def item_cb(e):
    print "Item changed in combobox %s into item : %s" % (e, e.active_item)
    return True

ecore_evas.show()
edj.show()

embed1 = etk.Embed(ecore_evas.evas)
entry1 = etk.ComboboxEntry()
embed1.add(entry1)
embed1.show_all()
embed1.pointer_method_set(set_pointer, ecore_evas)
embed1.position_method_set(get_position, ecore_evas)

entry1.item_append("First item")
entry1.item_append("2 item")
entry1.item_append("last item")

embed2 = etk.Embed(ecore_evas.evas)
entry2 = etk.Entry()
entry2.password_mode = True
embed2.add(entry2)
embed2.show_all()

embed2.pointer_method_set(set_pointer, ecore_evas)

edj.part_swallow("entry1", embed1.object)
edj.part_swallow("entry2", embed2.object)

edj.focus = True


def text_changed(o):
    print "Text changed : %s - %s" % (o, o.text)
    return True
entry1.entry.connect("text-changed", text_changed)
entry2.connect("text-changed", text_changed)

ecore.main_loop_begin()

