#!/usr/bin/python

import etk

def click(o, n, stop=False):
    print n
    if stop:
        print "STOP!"
        return False
    else:
        return True

b1 = etk.Button(label="4 connects")
b1.on_clicked(click, 1)
b1.on_clicked(click, 2)
b1.on_clicked(click, 3)
b1.on_clicked(click, 4)

b2 = etk.Button(label="4 connects w/ a stop in the middle")
b2.on_clicked(click, 1)
b2.on_clicked(click, 2)
b2.on_clicked(click, 3, stop=True)
b2.on_clicked(click, 4)

exit = etk.Button(label="Exit")
exit.on_clicked(lambda x: etk.main_quit())

box = etk.VBox()
box.append(b1, etk.VBox.END, etk.VBox.FILL, 0)
box.append(b2, etk.VBox.END, etk.VBox.FILL, 0)
box.append(exit, etk.VBox.END, etk.VBox.FILL, 0)


w = etk.Window(title="Hello World", child=box)
def delete(o, n, stop=False):
    print "delete-event number #%d" % n
    if stop:
        print "STOP!"
        return False
    else:
        return True

w.on_delete_event(delete, 1)
w.connect_after("delete-event", delete, 2, stop=True)
w.connect_after("delete-event", delete, 3)
w.show_all()

etk.main()
