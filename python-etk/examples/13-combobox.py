#!/usr/bin/python

import etk

# Combobox
combo = etk.Combobox(columns=[
    (etk.Combobox.IMAGE, 50, etk.Combobox.FILL, 0.0),
    (etk.Combobox.LABEL, 50, etk.Combobox.FILL, 1.0),
    (etk.Combobox.OTHER, 20, etk.Combobox.FILL, 0.0)])
combo.items_height = 50

def show(b, text):
    print text

for i, v in enumerate(["XXX", "ABCABC", "P", "JJJJJ"]):
    f = etk.Image()
    f.set_from_file('07-image/icon.png')
    b = etk.Button(label="?")
    b.on_clicked(show, "I don't know what is %s" % v)
    combo.item_append(f, v, b)

def show_item(c, i):
    print i.field_get(1)

combo.on_item_activated(show_item)


# ComboboxEntry
ce = etk.ComboboxEntry()

for t in ["Alpha", "Beta", "Gamma"]:
    ce.item_append(t)

def show_active_item(c):
    print c.active_item.field_get(0)

ce.on_active_item_changed(show_active_item)

# Main
box = etk.VBox()
box.append(combo, etk.VBox.START, etk.VBox.FILL, 0)
box.append(ce, etk.VBox.END, etk.VBox.FILL, 0)

w = etk.Window(title="Hello World", size_request=(300, 200), child=box)
w.on_destroyed(lambda x: etk.main_quit())
w.show_all()

etk.main()
