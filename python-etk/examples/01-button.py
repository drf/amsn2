#!/usr/bin/python

import etk

counter = 0
msg = "Button clicked %d times"
b = etk.Button(label=msg % counter)
w = etk.Window(title="Button", size_request=(200, 200), child=b)
w.show_all()

def on_clicked(button):
    global counter
    counter += 1
    b.label = msg % counter
    print "button %s clicked" % button
b.connect("clicked", on_clicked)

def on_destroyed(obj):
    etk.main_quit()
w.connect("destroyed", on_destroyed)

etk.main()
