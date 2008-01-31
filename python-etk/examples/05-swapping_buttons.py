#!/usr/bin/python

import etk

b1 = etk.Button(label="Button #1")
b2 = etk.Button(label="Button #2")

w = etk.Window(title="Swapping buttons", size_request=(200, 50), child=b1)
w.on_destroyed(lambda x: etk.main_quit())

def show(obj, child):
    print "Added: " + child.label
    return True

w.on_child_added(show)

def swap(obj, other):
    w.child = other
    other.show()
    return True

b1.on_clicked(swap, b2)
b2.on_clicked(swap, b1)

w.show_all()
etk.main()
