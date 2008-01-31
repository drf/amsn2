#!/usr/bin/python

import etk

counter = 0
msg = "Button clicked %d times"
b = etk.Button(label=msg % counter)
b_block = etk.Button(label="Block action")
b_block_false = etk.Button(label="Block other action")
b_unblock = etk.Button(label="Unblock action")

v = etk.VBox()
v.append(b, etk.VBox.END, etk.VBox.NONE, 0)
v.append(b_block, etk.VBox.END, etk.VBox.NONE, 0)
v.append(b_block_false, etk.VBox.END, etk.VBox.NONE, 0)
v.append(b_unblock, etk.VBox.END, etk.VBox.NONE, 0)

w = etk.Window(title="Button", size_request=(200, 200), child=v)
w.show_all()

def count(b, a):
    global counter
    counter += 1
    b.label = msg % counter
    print "button %s clicked" % b
    return True
b.on_clicked(count, 13)

def do_block(button, b):
    b.block("clicked", count, 13)
    return True
b_block.on_clicked(do_block, b)

def do_block_false(button, b):
    try:
        b.block("clicked", count, 1)
    except ValueError:
        print "can't block if it's not connected"
    return True
b_block_false.on_clicked(do_block_false, b)

def do_unblock(button, b):
    b.unblock("clicked", count, 13)
    return True
b_unblock.on_clicked(do_unblock, b)

def quit(obj):
    etk.main_quit()
w.on_destroyed(quit)

etk.main()
