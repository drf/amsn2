
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

    def myInfoUpdated(self, view):
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


        self.group_holder = GroupHolder(self._evas, self)
        self.group_items = {}

        self._etk_evas_object.evas_object = self._edje
        self.add_with_viewport(self._etk_evas_object)

        self._edje.part_swallow("groups", self.group_holder);

        self._edje.focus = True

        self._edje.show()
        self._etk_evas_object.show()


    def contactUpdated(self, contact):
        for gid in self.group_items:
            gi = self.group_items[gid]
            if contact.uid in gi.contact_holder.contacts:
                gi.contact_holder.contact_updated(contact)

    def groupUpdated(self, group):
        raise NotImplementedError

    def groupAdded(self, group):
        gi = self.group_holder.add_group(group)
        self.group_items[group.uid] = gi
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

    def setContactCallback(self, cb):
        #cb is func(contactview)
        self.group_holder.setContactCallback(cb)

    def setContactContextMenu(self, cb):
        #TODO:
        pass



class ContactHolder(evas.SmartObject):

    def __init__(self, ecanvas, parent, cb = None):
        evas.SmartObject.__init__(self, ecanvas)
        self.evas_obj = ecanvas
        self.contacts = {}
        self._parent = parent
        self._callback = cb

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
            contact.dp.repeat_events = True
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
        new_contact.data["view"] = contact
        self.contacts[contact.uid] = new_contact
        self.contact_updated(contact)

        self.member_add(new_contact)

        if self._callback is not None:
            def cb_(obj,event):
                self._callback(obj.data["view"])
            new_contact.on_mouse_down_add(cb_)


        new_contact.show()
        return new_contact

    def clip_set(self, obj):
        for i in self.contacts:
            self.contacts[i].clip_set(obj)

    def clip_unset(self):
        for i in self.contacts:
            self.contacts[i].clip_unset()

    def show(self):
        for i in self.contacts:
            self.contacts[i].show()

    def hide(self):
        for i in self.contacts:
            self.contacts[i].hide()


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

    def setCallback(self, cb):
        self._callback = cb
        for cid in self.contacts:
            c = self.contacts[cid]
            if cb is not None:
                def cb_(obj,event):
                    cb(obj.data["view"])
                c.on_mouse_down_add(cb_)
            else:
                c.on_mouse_down_del()


class GroupItem(edje.Edje):
    def __init__(self, parent, evas_obj, group, ccb = None):
        self.evas_obj = evas_obj
        self._parent = parent
        self.expanded = True
        self.group = group
        self._edje = edje.Edje.__init__(self, self.evas_obj, file=THEME_FILE, group="group_item")
        self.contact_holder = ContactHolder(self.evas_obj, self, cb = ccb)
        self.part_text_set("group_name", group.name.toString())
        self.part_swallow("contacts", self.contact_holder);

        self.signal_callback_add("collapsed", "*", self.__collapsed_cb)
        self.signal_callback_add("expanded", "*", self.__expanded_cb)

    def setContactCallback(self, ccb):
        self.contact_holder.setCallback(ccb)

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

    def _clip_set(self, obj):
        self.clip_set(obj)
        self.contact_holder.clip_set(obj)

    def _clip_unset(self):
        self.clip_unset()
        self.contact_holder.clip_unset()

class GroupHolder(evas.SmartObject):

    def __init__(self, ecanvas, parent, ccb = None):
        evas.SmartObject.__init__(self, ecanvas)
        self.evas_obj = ecanvas
        self.group_items = []
        self._parent = parent
        self._ccb = ccb

    def add_group(self, group):
        new_group = GroupItem(self, self.evas_obj, group, ccb = self._ccb)
        new_group.show()
        self.group_items.append(new_group)
        self.member_add(new_group)
        self.update_widget(self.size[0], self.size[1])
        return new_group

    def setContactCallback(self, ccb):
        self._ccb = ccb
        for gi in self.group_items:
            gi.setContactCallback(ccb)

    def resize(self, w, h):
        self.update_widget(w, h)

    def show(self):
        #FIXME:
        #ugly fix to get the correct clip
        self.clip_set(self._parent._edje.clip_get())
        for g in self.group_items:
            g.show()

    def hide(self):
        for g in self.group_items:
            g.hide()

    def update_widget(self, w, h):
        x = self.top_left[0]
        y = self.top_left[1]
        if len(self.group_items) > 0:
            spacing = 5
            total_spacing = spacing * len(self.group_items)
            for i in self.group_items:
                item_height = 40 + (29 * i.num_contacts()) - 5
                i.move(x, y)
                i.size = (w, item_height)
                y += item_height + spacing
        self._parent.size_request_set(w,y)

    def clip_set(self, obj):
        for g in self.group_items:
            g._clip_set(obj)

    def clip_unset(self):
        for g in self.group_items:
            g._clip_unset()


