#!/usr/bin/python

import etk

class MyButton(etk.Button):
    def _size_request(self):
        return (500, 500)

    def _theme_signal_emit(self, signal, size_recalc):
        print "signal=\"%s\"    size_recalc=%d" % (signal, size_recalc)

new = MyButton(label="lalalla")

w = etk.Window(title="Hello World", child=new)
w.show_all()

def quit(obj):
    etk.main_quit()
w.on_destroyed(quit)

etk.main()
