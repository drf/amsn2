#!/usr/bin/python

import etk


entry = etk.Entry()

def clear(e):
    print "Text was: \"%s\"" % e.text
    e.text = ""

def click(b, e):
    clear(e)

entry.text = 'some text'
entry.on_text_activated(clear)

bye = etk.Button(label="Click")
bye.on_clicked(click, entry)

box = etk.VBox()
box.append(entry, etk.VBox.START, etk.VBox.FILL, 0)
box.append(bye, etk.VBox.END, etk.VBox.NONE, 0)

w = etk.Window(title="Hello World", size_request=(300, 300), child=box)
w.on_destroyed(lambda x: etk.main_quit())
w.show_all()

etk.main()
