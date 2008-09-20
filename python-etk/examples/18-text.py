import etk

v = etk.VPaned()
h = etk.HBox()

out_tv = etk.TextView()
in_tv = etk.TextView()

out_tb = out_tv.textblock_get()
in_tb = in_tv.textblock_get()
iter_out = etk.TextblockIter(out_tb)
iter_out.forward_end()

b = etk.Button(label="Send")

#e = etk.Entry()
h.append(in_tv, etk.HBox.START, etk.HBox.EXPAND_FILL, 0)
#h.append(e, etk.HBox.START, etk.HBox.EXPAND_FILL, 0)
h.append(b, etk.HBox.END, etk.HBox.FILL, 0)


w = etk.Window(title="Testing TextView!", child=v)
v.child2_set(h,1)
v.child1_set(out_tv,1)

def sendButton_cb(button):
    text = in_tb.text_get(0)
    in_tb.clear()
    #text = e.text
    #e.text = ""
    print text
    out_tb.insert(iter_out, text)
b.on_clicked(sendButton_cb)

def on_destroyed(obj):
    etk.main_quit()
w.connect("destroyed", on_destroyed)

w.show_all()
w.resize(600,600)
v.position = 420




etk.main()
