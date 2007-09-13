#!/usr/bin/python

import etk

l = etk.Label(text="Hello World", alignment=(0.5, 0.5))
w = etk.Window(title="Hello World", size_request=(200, 200), child=l)
w.show_all()

def on_destroyed(obj):
    etk.main_quit()
w.connect("destroyed", on_destroyed)

etk.main()
