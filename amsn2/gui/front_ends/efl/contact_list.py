
from constants import *
import evas
import edje
import ecore
import ecore.evas

from amsn2.core.views import StringView
from amsn2.gui import base
import pymsn

class aMSNContactList(base.aMSNContactList):
    def __init__(self, amsn_core, parent):
        self._amsn_core = amsn_core
        self._evas = parent._evas

        edje.frametime_set(1.0 / 30)
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

    def show(self):
        self._edje.show()

    def hide(self):
        self._edje.hide()

    def contactUpdated(self, contact):
        for gid in self.group_holders:
            gi = self.group_holders[gid]
            if contact in gi.group.contacts:
                gi.contact_holder.contact_updated(contact)

    def groupUpdated(self, group):
        raise NotImplementedError
    
    def groupAdded(self, group):
        gi = self.groups.add_group(group)
        self.group_holders[group.uid] = gi
        for c in group.contacts:
            gi.add_contact(c)

    def groupRemoved(self, group):
        pass

    def configure(self, option, value):
        pass

    def cget(self, option, value):
        pass


    # Private methods
    def __on_key_down(self, obj, event):
        if event.keyname in ("F6", "f"):
            self._evas.fullscreen = not self._evas.fullscreen
        elif event.keyname == "b":
            self._evas.borderless = not self._evas.borderless

class ContactHolder(evas.SmartObject):

    def __init__(self, ecanvas):
        evas.SmartObject.__init__(self, ecanvas.evas)
        self.evas_obj = ecanvas
        self.contacts = {}

    def contact_updated(self, contact):
        self.contacts[contact.uid].\
            part_text_set("contact_data", contact.name.toString())

        status = ""
        found = False
        for x in contact.name._elements:
            if x.getType() == StringView.OPEN_TAG_ELEMENT and \
                   x.getValue() == "status":
                found = True
            if found and x.getType() == StringView.TEXT_ELEMENT:
                status += x.getValue()
            if x.getType() == StringView.CLOSE_TAG_ELEMENT and \
                   x.getValue() == "status":
                found = False
        if status != "":
            self.contacts[contact.uid].signal_emit("state_changed", status.strip("()"))

    def add_contact(self, contact):
        new_contact = edje.Edje(self.evas_obj.evas, file=THEME_FILE,
                                group="contact_item")
        self.contacts[contact.uid] = new_contact
        self.contact_updated(contact)
        
        self.member_add(new_contact)

        new_contact.show()
        return new_contact
        
    def show(self):
        self.update_widget(self.size[0], self.size[1])
        
    def hide(self):
        self.update_widget(self.size[0], self.size[1])

    def clip_set(self, obj):
        pass

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
                self.contacts[i].move(x, y)
                self.contacts[i].size = (w, item_height)
                y += item_height + spacing
            
    def num_contacts(self):
        return len(self.contacts)

class GroupItem(edje.Edje):
    def __init__(self, parent, evas_obj, group):
        self.evas_obj = evas_obj
        self._parent = parent
        self.expanded = True
        self.group = group
        self._edje = edje.Edje.__init__(self, self.evas_obj.evas, file=THEME_FILE, group="group_item")
        self.contact_holder = ContactHolder(self.evas_obj)
        self.part_text_set("group_name", group.name.toString())
        self.part_swallow("contacts", self.contact_holder);

        self.signal_callback_add("collapsed", "*", self.__collapsed_cb)
        self.signal_callback_add("expanded", "*", self.__expanded_cb)
        

    def add_contact(self, contact):
        c = self.contact_holder.add_contact(contact)
        c.clip_set(self._edje)
        self.__update_parent()

    def contact_presence_changed(self, contact):
        self.contact_holder.contact_presence_changed(contact)

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

    def show(self):
        self.update_widget(self.size[0], self.size[1])
        
    def hide(self):
        self.update_widget(self.size[0], self.size[1])

    def update_widget(self,w, h):
        x = self.top_left[0]
        y = self.top_left[1]
        h = h +100
        if len(self.groups) > 0:
            spacing = 5
            total_spacing = spacing * len(self.groups)
            item_height = (h - total_spacing) / len(self.groups)
            for i in self.groups:
                item_height = 40 + (24 * i.num_contacts())
                i.move(x, y)
                i.size = (w, item_height)
                y += item_height + spacing
