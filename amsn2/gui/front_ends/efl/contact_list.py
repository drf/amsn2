
from constants import *
import evas
import edje
import ecore
import ecore.evas
import etk

from amsn2.core.views import StringView
from amsn2.gui import base
import pymsn

class aMSNContactListWindow(base.aMSNContactListWindow):
    def __init__(self, amsn_core, parent):
        self._amsn_core = amsn_core
        self._evas = parent._evas
        self._parent = parent
        self._clwidget = aMSNContactListWidget(amsn_core, self)
        parent.setChild(self._clwidget)
        self._clwidget.show()

    def show(self):
        self._clwidget.show()
    
    def hide(self):
        self._clwidget.hide()

    def setTitle(self, text):
        self._parent.setTitle(text)

    def setMenu(self, menu):
        self._parent.setMenu(menu)

    def topCLUpdated(self, contactView):
        pass #TODO


class aMSNContactListWidget(etk.ScrolledView, base.aMSNContactListWidget):
    def __init__(self, amsn_core, parent):
        self._amsn_core = amsn_core
        self._evas = parent._evas

        self._etk_evas_object = etk.EvasObject()
        etk.ScrolledView.__init__(self)

        edje.frametime_set(1.0 / 30)
        try:
            self._edje = edje.Edje(self._evas, file=THEME_FILE,
                                group="contact_list")
        except edje.EdjeLoadError, e:
            raise SystemExit("error loading %s: %s" % (THEME_FILE, e))

    
        self.groups = GroupHolder(self._evas, self)
        self.group_holders = {}
                
        self._etk_evas_object.evas_object = self._edje
        self.add_with_viewport(self._etk_evas_object)

        self._edje.part_swallow("groups", self.groups);
        
        self._edje.focus = True

        self._edje.show()
        self._etk_evas_object.show()

    def contactUpdated(self, contact):
        pass
        for gid in self.group_holders:
            gi = self.group_holders[gid]
            if contact in gi.group.contacts:
                gi.contact_holder.contact_updated(contact)

    def groupUpdated(self, group):
        raise NotImplementedError
    
    def groupAdded(self, group):
        pass
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

    def size_request_set(self, w,h):
        self._etk_evas_object.size_request_set(w,h)

class ContactHolder(evas.SmartObject):

    def __init__(self, ecanvas):
        evas.SmartObject.__init__(self, ecanvas)
        self.evas_obj = ecanvas
        self.contacts = {}

    def contact_updated(self, contact):
        #TODO : clean :)
        self.contacts[contact.uid].\
            part_text_set("contact_data", contact.name.toString())
       
        if DP_IN_CL:
            # add the dp
            # Remove the current dp
            obj_swallowed = self.contacts[contact.uid].\
                part_swallow_get("buddy_icon")
            if obj_swallowed is not None:
                # Delete ?
                obj_swallowed.hide()
            #add emblem on dp
            #shouldn't be done there, but in the core...
            contact.dp.append("Skin","emblem_busy") #yeah, everyone is busy!!
            self.contacts[contact.uid].\
                part_swallow("buddy_icon", contact.dp)
        else:
            # add the buddy icon
            # Remove the current icon
            obj_swallowed = self.contacts[contact.uid].\
                part_swallow_get("buddy_icon")
            if obj_swallowed is not None:
                # Delete ?
                obj_swallowed.hide()
            self.contacts[contact.uid].\
                part_swallow("buddy_icon", contact.icon)
        

    def add_contact(self, contact):
        new_contact = edje.Edje(self.evas_obj, file=THEME_FILE,
                                group="contact_item")
        self.contacts[contact.uid] = new_contact
        self.contact_updated(contact)
        
        self.member_add(new_contact)

        new_contact.show()
        return new_contact
    
    def clip_set(self, obj):
        for c in self.contacts:
            c.clip_set(obj)

    def clip_unset(self):
        for c in self.contacts:
            c.clip_unset

    def show(self):
        self.update_widget(self.size[0], self.size[1])
        
    def hide(self):
        self.update_widget(self.size[0], self.size[1])


    def resize(self, w, h):
        self.update_widget(w, h)

    def update_widget(self, w, h):
        x = self.top_left[0]
        y = self.top_left[1]
        if len(self.contacts) > 0:
            spacing = 5
            total_spacing = spacing * len(self.contacts)
            item_height = 24
            for i in self.contacts:
                self.contacts[i].move(x, y)
                self.contacts[i].size = (w, item_height)
                y += item_height + spacing
            
    def num_contacts(self):
        return len(self.contacts)

    def clip_unset(self):
        pass

class GroupItem(edje.Edje):
    def __init__(self, parent, evas_obj, group):
        self.evas_obj = evas_obj
        self._parent = parent
        self.expanded = True
        self.group = group
        self._edje = edje.Edje.__init__(self, self.evas_obj, file=THEME_FILE, group="group_item")
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

    def __init__(self, ecanvas, parent):
        evas.SmartObject.__init__(self, ecanvas)
        self.evas_obj = ecanvas
        self.groups = []
        self._parent = parent

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

    def update_widget(self, w, h):
        x = self.top_left[0]
        y = self.top_left[1]
        if len(self.groups) > 0:
            spacing = 5
            total_spacing = spacing * len(self.groups)
            for i in self.groups:
                item_height = 40 + (29 * i.num_contacts()) - 5
                i.move(x, y)
                i.size = (w, item_height)
                y += item_height + spacing
        self._parent.size_request_set(w,y)

    def clip_set(self, obj):
        for g in self.groups:
            g.clip_set(obj)

    def clip_unset(self):
        for g in self.groups:
            g.clip_unset()
