#!/usr/bin/python

import etk

etk.theme_widget_set_from_path("/home/cmarcelo/test.edj")

class RectRenderer(etk.BasicRenderer):
    def __init__(self, *a, **ka):
        etk.BasicRenderer.__init__(self, *a, **ka)

    def create_cell(self, canvas):
        return canvas.Rectangle()

    def update_cell(self, cell, row):
        cell.color = (0, 0, row[self.slot], 255)

    def show_cell(self, cell, x, y, w, h):
        cell.resize(w - 22, h - 30)
        cell.move(x + 10, y + 15)
        cell.show()


def button_clicked(row, msg=None, *a, **ka):
    print "%s - %s" % (row[3], msg)

model = etk.ListModel()
model2 = etk.ListModel()


#lst.freeze()
for i in range(1000):
    model.append(["person #%d" % i, ((i+1) * 27) % 256, ((i+1) * 78) % 256,
                 ((i+1) * 101) % 256, "person #%d" % i, i % 2])
#lst.thaw()


lst = etk.List(model=model, selectable=True, animated_changes=True,
               columns=[
        (100, RectRenderer(slot=1), False),
        (100, etk.TextRenderer(slot=2), False),
        (100, etk.ButtonRenderer(label="Edit", click=button_clicked,
                                 msg="test"), False),
        (100, etk.TextRenderer(slot=0), True),
        ])

#def clack(l, row):
#    print row
#lst.on_row_clicked(clack)

import glob
files = glob.glob("*")
files.sort()
for i, name in enumerate(files):
    model2.append([name, ((i+1) * 13) % 256, ((i+1) * 45) % 256,
                  ((i+1) * 200) % 256, name, 0])

bs = []
def make_button(label, clicked, *a, **ka):
    global bs
    b = etk.Button(label=label)
    b.on_clicked(clicked, *a, **ka)
    bs.append(b)


def swap_model(b, l, m1, m2):
    if l.model == m1:
        l.model = m2
    else:
        l.model = m1
    return True
make_button("Swap model", swap_model, lst, model, model2)


def swap_animated(b, l):
    l.animated_changes = not l.animated_changes
    return True
make_button("Anim", swap_animated, lst)


def goto_selected(b, l, func):
    rows = l.selected_rows
    if rows:
        func(rows[0])
    return True
make_button("Top to", goto_selected, lst, lst.scroll_top_to)
make_button("Middle to", goto_selected, lst, lst.scroll_middle_to)
make_button("Bottom to", goto_selected, lst, lst.scroll_bottom_to)

import random
def make_random_person():
    i = int(random.uniform(0, 8192))
    return ["random person #%d" % i, ((i + 1) * 27) % 256, ((i + 1) * 78) % 256, ((i + 1) * 99) % 256,
            "random person #%d" % i, i % 2]

def prepend_row(b, l):
    l.model.prepend(make_random_person())
    return True
make_button("Prepend person", prepend_row, lst)

def append_row(b, l):
    l.model.append(make_random_person())
    return True
make_button("Append person", append_row, lst)

def add_after_selected(b, l):
    rows = l.selected_rows
    if rows:
        j = l.model.elements.index(rows[0])
        l.model.insert(j+1, make_random_person())
    return True
make_button("Add after selected", add_after_selected, lst)

def add_after_n(b, l, n):
    l.model.insert(n, make_random_person())
    return True
make_button("Add after 2", add_after_n, lst, 2)

def freeze_thaw(b, l):
    if b.label == "Freeze":
        l.freeze()
        b.label = "Thaw"
    else:
        l.thaw()
        b.label = "Freeze"
    return True
make_button("Freeze", freeze_thaw, lst)

def remove(b, l, n):
    rows = l.model.elements
    l.model.remove(rows[n])
    return True
make_button("Remove first", remove, lst, 0)
make_button("Remove last", remove, lst, -1)

def remove_selected(b, l):
    rows = l.selected_rows
    if rows:
        l.model.remove(rows[0])
    return True
make_button("Remove selected", remove_selected, lst)

bsbox = etk.VBox()
for b in bs:
    bsbox.append(b, etk.VBox.START, etk.VBox.FILL, 0)


# Main
box = etk.HBox()

box.append(bsbox, etk.HBox.START, etk.HBox.FILL, 0)
box.append(lst, etk.HBox.START, etk.HBox.EXPAND_FILL, 0)


w = etk.Window(title="Hello World", child=box)
w.on_destroyed(lambda x: etk.main_quit())
w.show_all()

etk.main()
