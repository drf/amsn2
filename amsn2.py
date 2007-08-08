#!/usr/bin/env python

import evas
import edje
import ecore
import ecore.evas
import sys
import os
import time

WIDTH = 800
HEIGHT = 480
MIN_WIDTH = 100
MIN_HEIGHT = 150
THEME_FILE = "themes/default.edj"
TITLE = "aMSN 2"
WM_NAME = "aMSN2"
WM_CLASS = "main"

class ResizableImage(evas.SmartObject):
    def __init__(self, ecanvas):
        evas.SmartObject.__init__(self, ecanvas)
        self.image_object = evas.Image(ecanvas)
        self.member_add(self.image_object)

    def file_set(self, filename):
        self.image_object.file_set(filename)
        self.image_object.show()

    def resize(self, w, h):
        self.image_object.size = (w, h)
        self.image_object.fill_set(0, 0, w, h)

    def color_set(self, r, g, b, a):
        self.image_object.color_set(r, g, b, a)


class GroupHolder(evas.SmartObject):

    def __init__(self, ecanvas):
        evas.SmartObject.__init__(self, ecanvas)
        self.evas_obj = ecanvas
        self.groups = []
        self.x = 0
        self.y = 0

    def add_group(self, group_name):
        new_group = edje.Edje(self.evas_obj, file=THEME_FILE,
                                   group="group_item")
        new_group.part_text_set("group_name", group_name)
        new_group.show()
        self.groups.append(new_group)
        self.member_add(new_group)
        
    def resize(self, w, h):
        x = self.top_left[0]
        y = self.top_left[1]
        spacing = 5
        total_spacing = spacing * len(self.groups)
        item_height = (h - total_spacing) / len(self.groups)
        for i in self.groups:
            i.move(x, y)
            i.size = (w, item_height)
            y += item_height + spacing
            
        
class MainWindow(object):
    def __init__(self, evas_canvas):
        self.evas_obj = evas_canvas.evas_obj
        try:
            self.cl = edje.Edje(self.evas_obj.evas, file=THEME_FILE,
                                group="contact_list")
        except edje.EdjeLoadError, e:
            raise SystemExit("error loading %s: %s" % (f, e))

        self.cl.size = self.evas_obj.evas.size
        self.evas_obj.data["contact_list"] = self.cl
        
        self.cl.show()

        self.cl.on_key_down_add(self.on_key_down)

        self.cl.focus = True
    
        self.groups = GroupHolder(self.evas_obj.evas)
        self.groups.add_group("test group 1");
        self.groups.add_group("Group with long name, very long, very very long name");
        self.groups.add_group("Yet another test group"); 
        
        self.cl.part_swallow("groups", self.groups);
        self.groups.show();

    def on_key_down(self, obj, event):
        if event.keyname in ("F6", "f"):
            self.evas_obj.fullscreen = not self.evas_obj.fullscreen
        elif event.keyname == "Escape":
            ecore.main_loop_quit()


class EvasCanvas(object):
    def __init__(self, fullscreen, engine, width, height):
        if engine == "x11":
            self.evas_obj = ecore.evas.SoftwareX11(w=width, h=height)
        elif engine == "x11-16":
            if ecore.evas.engine_type_supported_get("software_x11_16"):
                self.evas_obj = ecore.evas.SoftwareX11_16(w=width, h=height)
            else:
                print "warning: x11-16 is not supported, fallback to x11"
                self.evas_obj = ecore.evas.SoftwareX11(w=width, h=height)

        self.evas_obj.callback_delete_request = self.on_delete_request
        self.evas_obj.callback_resize = self.on_resize

        self.evas_obj.title = TITLE
        self.evas_obj.name_class = (WM_NAME, WM_CLASS)
        self.evas_obj.fullscreen = fullscreen
        self.evas_obj.size = (width, height)
        self.evas_obj.size_min_set(MIN_WIDTH, MIN_HEIGHT)
        self.evas_obj.show()

    def on_resize(self, evas_obj):
        x, y, w, h = evas_obj.evas.viewport
        size = (w, h)
        for key in evas_obj.data.keys():
            evas_obj.data[key].size = size

    def on_delete_request(self, evas_obj):
        ecore.main_loop_quit()


if __name__ == "__main__":
    from optparse import OptionParser

    def parse_geometry(option, opt, value, parser):
        try:
            w, h = value.split("x")
            w = int(w)
            h = int(h)
        except Exception, e:
            raise optparse.OptionValueError("Invalid format for %s" % option)
        parser.values.geometry = (w, h)

    usage = "usage: %prog [options]"
    op = OptionParser(usage=usage)
    op.add_option("-e", "--engine", type="choice",
                  choices=("x11", "x11-16"), default="x11",
                  help=("which display engine to use (x11, x11-16), "
                        "default=%default"))
    op.add_option("-z", "--fullscreen", action="store_true", default=False,
                  help="do not launch in fullscreen")
    op.add_option("-g", "--geometry", type="string", metavar="WxH",
                  action="callback", callback=parse_geometry,
                  default=(800, 480),
                  help="use given window geometry")
    op.add_option("-f", "--fps", type="int", default=50,
                  help="frames per second to use, default=%default")

    # Handle options and create output window
    options, args = op.parse_args()
    edje.frametime_set(1.0 / options.fps)
    canvas = EvasCanvas(fullscreen=options.fullscreen,
                        engine=options.engine,
                        width=options.geometry[0],
                        height=options.geometry[1])

    view = MainWindow(canvas)
    ecore.main_loop_begin()
