#!/usr/bin/python

import etk

counter = 0
msg = "Button clicked %d times"
b = etk.Button(label=msg % counter)
w = etk.Window(title="Button", size_request=(200, 200), child=b)
w.show_all()

def count(button):
    global counter
    counter += 1
    b.label = msg % counter
    print "button %s clicked" % button
    return True
b.on_clicked(count)

def quit(obj):
    etk.main_quit()
w.on_destroyed(quit)

etk.main()
