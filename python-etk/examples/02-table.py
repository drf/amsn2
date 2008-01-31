#!/usr/bin/python

import etk

cols = 3
rows = 3

t = etk.Table(cols=cols, rows=rows, homogeneous=etk.Table.HOMOGENEOUS)

def on_clicked(button):
    print button.label
    return True

pos = 0
for name in ['One', 'Two', 'Three', 'Four', 'Five', 'Six']:
    b = etk.Button(label=name)
    b.connect("clicked", on_clicked)
    row = pos / cols
    col = pos % cols
    t.attach_default(b, col, col, row, row)
    pos += 1

bye = etk.Button(label="Hello World")
bye.connect("clicked", lambda x: etk.main_quit())
t.attach_default(bye, 0, 2, 2, 2)

w = etk.Window(title="Hello World", size_request=(300, 300), child=t)
w.show_all()

def on_destroyed(obj):
    etk.main_quit()
w.connect("destroyed", on_destroyed)


etk.main()
