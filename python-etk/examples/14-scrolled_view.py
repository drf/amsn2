#!/usr/bin/python

import etk

counter = 0

def do_add(b, box):
    global counter
    counter += 1
    x = etk.Button(label="Yet another button #%d" % counter)
    box.append(x, etk.VBox.START, etk.VBox.FILL, 0)
    x.show()

outer_box = etk.VBox()
box = etk.VBox()

adder = etk.Button(label="New Button")
adder.on_clicked(do_add, box)

sv = etk.ScrolledView()
sv.add_with_viewport(box)

outer_box.append(adder, etk.VBox.START, etk.VBox.FILL, 0)
outer_box.append(sv, etk.VBox.START, etk.VBox.EXPAND_FILL, 0)


w = etk.Window(title="Hello World", size_request=(200, 400), child=outer_box)
w.on_destroyed(lambda x: etk.main_quit())
w.show_all()

etk.main()
