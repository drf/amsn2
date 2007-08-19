

import evas
import edje
import ecore
import ecore.evas

from amsn2.gui import *
from amsn2.core import *

WIDTH = 400
HEIGHT = 600
MIN_WIDTH = 100
MIN_HEIGHT = 150

THEME_FILE = "amsn2/themes/default.edj"
TITLE = "aMSN 2"
WM_NAME = "aMSN2"
WM_CLASS = "main"

class aMSNGUI_EFL(aMSNGUI):
    def __init__(self, amsn_core):     
        self._amsn_core = amsn_core
        self._amsn_core.setGUI(self)

        edje.frametime_set(1.0 / 30)
        self._evas = ecore.evas.SoftwareX11(w=WIDTH, h=HEIGHT)
        self._evas.callback_delete_request = self.__on_delete_request
        self._evas.callback_resize = self.__on_resize
        self._evas.callback_show = self.__on_show
        self._evas.title = TITLE
        self._evas.name_class = (WM_NAME, WM_CLASS)
        self._evas.fullscreen = False
        self._evas.size = (WIDTH, HEIGHT)
        self._evas.size_min_set(MIN_WIDTH, MIN_HEIGHT)


    def createLoginWindow(self):
        self._login = aMSNLoginWindow_EFL(self._amsn_core)
        return self._login

    def createContactList(self, profile):
        cl = aMSNContactList_EFL(self._amsn_core)
        return cl

    def launch(self):
        import gobject
        mainloop = gobject.MainLoop(is_running=True)
        context = mainloop.get_context()

        def glib_context_iterate():
            while context.pending():
                context.iteration()
            return True

        # Every 100ms, call an iteration of the glib main context loop
        # to allow the protocol context loop to work
        ecore.timer_add(0.1, glib_context_iterate)

        self._evas.show()
        ecore.main_loop_begin()

    def idler_add(self, func):
        ecore.idler_add(func)

    def timer_add(self, delay, func):
        ecore.timer_add(delay, func)

       
    # Private methods
    def __on_show(self, evas_obj):
        self._amsn_core.mainWindowShown()

    def __on_resize(self, evas_obj):
        x, y, w, h = evas_obj.evas.viewport
        size = (w, h)
        for key in evas_obj.data.keys():
            evas_obj.data[key].size = size

    def __on_delete_request(self, evas_obj):
        ecore.main_loop_quit()


class aMSNLoginWindow_EFL(aMSNLoginWindow):
    def __init__(self, amsn_core):
        self._amsn_core = amsn_core
        self._amsn_gui = self._amsn_core.gui
        self._evas = self._amsn_gui._evas

        try:
            self._edje = edje.Edje(self._evas.evas, file=THEME_FILE,
                                group="login_screen")
        except edje.EdjeLoadError, e:
            raise SystemExit("error loading %s: %s" % (THEME_FILE, e))

        self._edje.size = self._evas.size
        self._evas.data["login_window"] = self._edje
        
        self._edje.on_key_down_add(self.__on_key_down)
        self._edje.signal_callback_add("signin", "*", self.__signin_cb)

        self._edje.focus = True

        # We start with no profile set up, we let the Core set our starting profile
        self.switch_to_profile(None)

    def show_window(self):
        self._edje.show()
    
    def hide_window(self):
        self._edje.hide()

    def switch_to_profile(self, profile):
        self.current_profile = profile
        if self.current_profile is not None:
            self._edje.part_text_set("user_name", self.current_profile.username)
            self._edje.part_text_set("password",  ''.join(["*" for i in range(len(self.current_profile.password))]))


    def signin(self):
        # TODO : get/set the username/password and other options from the login screen
        self._amsn_core.signin_to_account( self, self.current_profile)

    def onConnecting(self):
        self._edje.signal_emit("connecting", "")
        self._edje.part_text_set("connection_status", "Connecting to server...")

    def onConnected(self):
        self._edje.signal_emit("connecting", "")
        self._edje.part_text_set("connection_status", "Connected...")
        self._edje.part_text_set("connection_status2", "")

    def onAuthenticating(self):
        self._edje.signal_emit("connecting", "")
        self._edje.part_text_set("connection_status", "Authenticating...")
        self._edje.part_text_set("connection_status2", "")

    def onAuthenticated(self):
        self._edje.signal_emit("connecting", "")
        self._edje.part_text_set("connection_status", "Password accepted...")
        self._edje.part_text_set("connection_status2", "")

    def onSynchronizing(self):
        self._edje.signal_emit("connecting", "")
        self._edje.part_text_set("connection_status", "Please wait while your contact list")
        self._edje.part_text_set("connection_status2", "is being downloaded...")

    def onSynchronized(self):
        self._edje.signal_emit("connecting", "")
        self._edje.part_text_set("connection_status", "Contact list downloaded successfully")
        self._edje.part_text_set("connection_status2", "Happy Chatting")

    # Private methods
    def __on_key_down(self, obj, event):
        if event.keyname in ("F6", "f"):
            self.evas_obj.fullscreen = not self.evas_obj.fullscreen
        elif event.keyname == "Escape":
            ecore.main_loop_quit()

    def __signin_cb(self, edje_obj, signal, source):
        self.signin()


class aMSNContactList_EFL(object):
    def __init__(self, amsn_core):
        self._amsn_core = amsn_core
        self._amsn_gui = self._amsn_core.gui
        self._evas = self._amsn_gui._evas

        try:
            self._edje = edje.Edje(self._evas.evas, file=THEME_FILE,
                                group="contact_list")
        except edje.EdjeLoadError, e:
            raise SystemExit("error loading %s: %s" % (THEME_FILE, e))

        self._edje.size = self._evas.size
        self._evas.data["contact_list"] = self._edje 

        self._edje.on_key_down_add(self.__on_key_down)

        self._edje.focus = True
    
        self.groups = GroupHolder(self._evas)
        self.group_holders = {}
        
        self._edje.part_swallow("groups", self.groups);
        self.groups.show();

    def show_window(self):
        self._edje.show()

    def hide_window(self):
        self._edje.hide()

    def contactStateChange(self, contact):
        pass

    def contactNickChange(self, contact):
        pass
        
    def contactPSMChange(self, contact):
        pass
    
    def contactAlarmChange(self, contact):
        pass

    def contactDisplayPictureChange(self, contact):
        pass

    def contactSpaceChange(self, contact):
        pass
    
    def contactSpaceFetched(self, contact):
        pass

    def contactBlocked(self, contact):
        pass

    def contactUnblocked(self, contact):
        pass

    def contactMoved(self, from_group, to_group, contact):
        pass

    def contactAdded(self, group, contact):
        self.group_holders[group.id].add_contact(contact)
    
    def contactRemoved(self, group, contact):
        pass

    def contactRenamed(self, contact):
        pass

    def groupRenamed(self, group):
        pass

    def groupAdded(self, group):
        gi = self.groups.add_group(group)
        self.group_holders[group.id] = gi

    def groupRemoved(self, group):
        pass

    def configure(self, option, value):
        pass

    def cget(self, option, value):
        pass


    # Private methods
    def __on_key_down(self, obj, event):
        if event.keyname in ("F6", "f"):
            self.evas_obj.fullscreen = not self.evas_obj.fullscreen
        elif event.keyname == "Escape":
            ecore.main_loop_quit()

class ContactHolder(evas.SmartObject):

    def __init__(self, ecanvas):
        evas.SmartObject.__init__(self, ecanvas.evas)
        self.evas_obj = ecanvas
        self.contacts = []
        self.p2s = {pymsn.Presence.ONLINE:"online",
                    pymsn.Presence.BUSY:"busy",
                    pymsn.Presence.IDLE:"idle",
                    pymsn.Presence.AWAY:"away",
                    pymsn.Presence.BE_RIGHT_BACK:"brb",
                    pymsn.Presence.ON_THE_PHONE:"phone",
                    pymsn.Presence.OUT_TO_LUNCH:"lunch",
                    pymsn.Presence.INVISIBLE:"hidden",
                    pymsn.Presence.OFFLINE:"offline"}

    def add_contact(self, contact):
        new_contact = edje.Edje(self.evas_obj.evas, file=THEME_FILE,
                                group="contact_item")
        new_contact.part_text_set("contact_data", 
                                  "<%s><nickname>%s</nickname> <status>(%s)</status> <psm>%s</psm></%s>"
                                  % (contact.presence, contact.display_name, 
                                     self.p2s[contact.presence], contact.personal_message, 
                                     contact.presence) )
        new_contact.signal_emit("state_changed", self.p2s[contact.presence])
        new_contact.show()
        self.contacts.append(new_contact)
        self.member_add(new_contact)
        self.update_widget(self.size[0], self.size[1])
        

    def resize(self, w, h):
        self.update_widget(w, h)

    def update_widget(self, w, h):
        x = self.top_left[0]
        y = self.top_left[1]
        if len(self.contacts) > 0:
            spacing = 5
            total_spacing = spacing * len(self.contacts)
            item_height = (h - total_spacing) / len(self.contacts)
            for i in self.contacts:
                i.move(x, y)
                i.size = (w, item_height)
                y += item_height + spacing
            
    def num_contacts(self):
        return len(self.contacts)

class GroupItem(edje.Edje):
    def __init__(self, parent, evas_obj, group):
        self.evas_obj = evas_obj
        self._parent = parent
        self.expanded = True
        edje.Edje.__init__(self, self.evas_obj.evas, file=THEME_FILE, group="group_item")
        self.contact_holder = ContactHolder(self.evas_obj)
        self.part_text_set("group_name", group.name)
        self.part_swallow("contacts", self.contact_holder);

        self.signal_callback_add("collapsed", "*", self.__collapsed_cb)
        self.signal_callback_add("expanded", "*", self.__expanded_cb)
        

    def add_contact(self, contact):
        self.contact_holder.add_contact(contact)
        self.__update_parent()

    def num_contacts(self):
        if self.expanded == False:
            return 0
        else:
            return self.contact_holder.num_contacts()
        

    # Private methods
    def __update_parent(self):
        self._parent.update_widget(self._parent.size[0], self._parent.size[1])
        
    def __expanded_cb(self, edje_obj, signal, source):
        self.expanded = True
        self.__update_parent()

    def __collapsed_cb(self, edje_obj, signal, source):
        self.expanded = False
        self.__update_parent()

class GroupHolder(evas.SmartObject):

    def __init__(self, ecanvas):
        evas.SmartObject.__init__(self, ecanvas.evas)
        self.evas_obj = ecanvas
        self.groups = []

    def add_group(self, group):
        new_group = GroupItem(self, self.evas_obj, group)
        new_group.show()
        self.groups.append(new_group)
        self.member_add(new_group)
        self.update_widget(self.size[0], self.size[1])
        return new_group
        
    def resize(self, w, h):
        self.update_widget(w, h)

    def update_widget(self,w, h):
        x = self.top_left[0]
        y = self.top_left[1]
        h = h +100
        if len(self.groups) > 0:
            spacing = 5
            total_spacing = spacing * len(self.groups)
            #item_height = (h - total_spacing) / len(self.groups)
            for i in self.groups:
                item_height = 36 + (24 * i.num_contacts())
                i.move(x, y)
                i.size = (w, item_height)
                y += item_height + spacing
