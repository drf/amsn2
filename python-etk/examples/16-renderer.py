#!/usr/bin/python

import etk
import edje

etk.theme_widget_set_from_path("/home/cmarcelo/test.edj")

class MyMultiImageRenderer(etk.KineticRenderer):
    def __init__(self, images=[], state_slot=0, click=None, align=(0.0, 0.5)):
        if not images:
            raise ValueError("must supply images")
        etk.KineticRenderer.__init__(self)
        self.images = images
        self.state_slot = state_slot
        if not callable(click):
            raise ValueError("click must be callable")
        self.click_cb = click
        self.align = align

    def create_cell(self, canvas):
        cell = canvas.FilledImage()
        return cell

    def update_cell(self, cell, row):
        state = row[self.state_slot]
        file, key = self.images[state]
        cell.file_set(file, key)

    def show_cell(self, cell, x, y, w, h):
        iw, ih = cell.image_size
        ix = x + self.align[0] * (w - iw)
        iy = y + self.align[1] * (h - ih)
        cell.resize(iw, ih)
        cell.move(int(ix), int(iy))
        cell.show()

    def click(self, cell, row):
        self.click_cb(row)


def action(row):
    next = (row[2] + 1) % 3
    print "I was in state %d and going to state %d" % (row[2], next)
    row[2] = next

def text_clicked(row):
    print "Clicked in item", row


mir = MyMultiImageRenderer(images=[("07-image/icon.png", None),
                                   ("07-image/icon2.png", None),
                                   ("07-image/icon3.png", None)],
                           state_slot=2, click=action)

ktr = etk.KineticTextRenderer(slot=1, click=text_clicked)

model = etk.ListModel()
lst = etk.List(model=model, selectable=False, animated_changes=False,
               row_height=150, columns=[
        #(100, ImageRenderer(file_slot=0), False),
        (200, ktr, True),
        (175, mir, False),
        ])

lst.freeze()
for i in range(50):
    model.append(["07-image/icon.png", "User #%d" % i, 0])
lst.thaw()

# Main
box = etk.VBox()

box.append(lst, etk.VBox.START, etk.VBox.EXPAND_FILL, 0)


w = etk.Window(title="Hello World", child=box)
w.on_destroyed(lambda x: etk.main_quit())
w.show_all()

etk.main()
