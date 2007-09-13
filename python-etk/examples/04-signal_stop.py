#!/usr/bin/python

import etk

def click(o, n, stop):
    print n
    if stop:
        etk.signal_stop()
        print "STOP!"

b1 = etk.Button(label="4 connects")
b1.connect("clicked", click, 1, False)
b1.connect("clicked", click, 2, False)
b1.connect("clicked", click, 3, False)
b1.connect("clicked", click, 4, False)

b2 = etk.Button(label="4 connects w/ a stop in the middle")
b2.connect("clicked", click, 1, False)
b2.connect("clicked", click, 2, False)
b2.connect("clicked", click, 3, True)
b2.connect("clicked", click, 4, False)

box = etk.VBox()
box.append(b1, etk.VBox.END, etk.VBox.FILL, 0)
box.append(b2, etk.VBox.END, etk.VBox.FILL, 0)

w = etk.Window(title="Hello World", child=box)
w.connect("destroyed", lambda x: etk.main_quit())
w.show_all()

etk.main()
