#!/usr/bin/python

import etk

b1 = etk.Button(label="Button #1")
b2 = etk.Button(label="Button #2")

w = etk.Window(title="Swapping buttons", size_request=(200, 50), child=b1)
w.connect("destroyed", lambda x: etk.main_quit())

def show(obj, child):
    print "Added: " + child.label

w.connect("child-added", show)

def swap(obj, other):
    w.child = other
    other.show()

b1.connect("clicked", swap, b2)
b2.connect("clicked", swap, b1)

w.show_all()
etk.main()
