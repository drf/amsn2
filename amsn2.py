#!/usr/bin/env python
import sys
sys.path.append("./pymsn.devel")

import evas
import edje
import ecore
import ecore.evas
import sys
import os
import time
import logging

import pymsn
import pymsn.event

logging.basicConfig(level=logging.DEBUG)

WIDTH = 400
HEIGHT = 600
MIN_WIDTH = 100
MIN_HEIGHT = 150
THEME_FILE = "themes/default.edj"
TITLE = "aMSN 2"
WM_NAME = "aMSN2"
WM_CLASS = "main"


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
        self.update_widget()
        
    def resize(self, w, h):
        self.update_widget()

    def update_widget(self):
        x = self.top_left[0]
        y = self.top_left[1]
        (w, h) = self.size
        if len(self.groups) > 0:
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
        
        self.cl.part_swallow("groups", self.groups);
        self.groups.show();

    def add_group(self, group_name):
        self.groups.add_group(group_name)

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

class ClientEvents(pymsn.event.ClientEventInterface):
    def on_client_state_changed(self, state):
        if state == pymsn.event.ClientState.CLOSED:
            self._client.quit()
        elif state == pymsn.event.ClientState.OPEN:
            self._client.profile.display_name = "aMSN2"
            self._client.profile.presence = pymsn.Presence.ONLINE
            self._client.profile.current_media = ("I listen to", "Nothing")
            self._client.profile.personal_message = "Testing aMSN2!"
            ecore.idler_add(self._client.fill_gui)

    def on_client_error(self, error_type, error):
        print "ERROR :", error_type, " ->", error


class Client(pymsn.Client):
    def __init__(self, account, quit,gui):
        server = ('messenger.hotmail.com', 1863)
        self.quit = quit
        self.account = account
        self.gui = gui
        pymsn.Client.__init__(self, server)

        ClientEvents(self)
        ecore.idler_add(self._connect)

    def _connect(self):
        self.login(*self.account)
        return False

    def fill_gui(self):
        groups = self.address_book.groups
        for group in groups.values():
            self.gui.add_group(group.name)
        return False

def main():
    import sys
    import getpass
    import signal
    import thread
    import gobject

    if len(sys.argv) < 3:
        print "Usage : %s username password" % (sys.argv[0])
        return
    else:
        account = sys.argv[1]
        passwd = sys.argv[2]

    mainloop = gobject.MainLoop(is_running=True)
    context = mainloop.get_context()
  
    def glib_context_iterate():
        while context.pending():
            context.iteration()
        return True

    def quit():
        ecore.main_loop_quit()

    def sigterm_cb():
        ecore.idle_add(quit)

        
 
    edje.frametime_set(1.0 / 30)
    canvas = EvasCanvas(fullscreen=False,
                        engine="x11",
                        width=WIDTH,
                        height=HEIGHT)

    view = MainWindow(canvas)

    n = Client((account, passwd), quit, view)

    # Every 100ms, call an iteration of the glib main context loop
    ecore.timer_add(0.1, glib_context_iterate)

    ecore.main_loop_begin()


if __name__ == '__main__':
    main()
