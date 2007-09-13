#!/usr/bin/python

import etk


entry = etk.Entry()

def click(o):
    global entry
    print entry.text

entry.text = 'some text'
entry.connect("text-changed", click)

bye = etk.Button(label="Click")
bye.connect("clicked", click)

box = etk.VBox()
box.append(entry, etk.VBox.START, etk.VBox.FILL, 0)
box.append(bye, etk.VBox.END, etk.VBox.NONE, 0)

w = etk.Window(title="Hello World", size_request=(300, 300), child=box)
w.connect("destroyed", lambda x: etk.main_quit())
w.show_all()

etk.main()
