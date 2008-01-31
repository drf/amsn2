#!/usr/bin/python

import etk
import ecore
import gc
import math

my_bar = etk.ProgressBar("Progress of Something")
my_slider = etk.HSlider(lower=0, upper=1, step_increment=0.05, page_increment=0.2)
my_timer = None

def stepper(bar, sli):
    f = bar.fraction
    if math.fabs(f - sli.value) < 0.01:
        return True

    if f < sli.value:
        f += 0.005
    else:
        f -= 0.005
    bar.fraction = f
    return True

ecore.timer_add(0.02, stepper, my_bar, my_slider)

box = etk.VBox()
box.append(my_bar, etk.VBox.START, etk.VBox.FILL, 0)
box.append(my_slider, etk.VBox.END, etk.VBox.FILL, 0)

w = etk.Window(title="Hello World", size_request=(300, 100), child=box)
w.on_destroyed(lambda x: etk.main_quit())
w.show_all()

etk.main()
