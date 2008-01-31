#!/usr/bin/python

import etk

icon = etk.Image()
icon.set_from_file('icon.png')

box = etk.VBox()
box.append(icon, etk.VBox.START, etk.VBox.FILL, 0)

w = etk.Window(title="Hello World", size_request=(300, 300), child=box)
w.on_destroyed(lambda x: etk.main_quit())
w.show_all()

etk.main()
