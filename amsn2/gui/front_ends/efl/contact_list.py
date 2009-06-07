
from constants import *
import evas
import edje
import ecore
import ecore.evas
import elementary

from image import *

from amsn2.core.views import StringView
from amsn2.gui import base
import papyon

class aMSNContactListWindow(elementary.Box, base.aMSNContactListWindow):
    def __init__(self, amsn_core, parent):
        self._core = amsn_core
        self._evas = parent._evas
        self._parent = parent
        self._skin = amsn_core._skin_manager.skin
        elementary.Box.__init__(self, parent)
        self._clwidget = aMSNContactListWidget(amsn_core, self)
        self._parent.resize_object_add(self)
        self.size_hint_weight_set(1.0, 1.0)
        self.pack_start(self._clwidget)
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


class aMSNContactListWidget(elementary.Scroller, base.aMSNContactListWidget):
    def __init__(self, amsn_core, parent):
        base.aMSNContactListWidget.__init__(self, amsn_core, parent)
        self._core = amsn_core
        self._evas = parent._evas
        self._skin = parent._skin
        elementary.Scroller.__init__(self, parent)

        edje.frametime_set(1.0 / 30)
        try:
            self._edje = edje.Edje(self._evas, file=THEME_FILE,
                                group="contact_list")
        except edje.EdjeLoadError, e:
            raise SystemExit("error loading %s: %s" % (THEME_FILE, e))


        self.group_holder = GroupHolder(self._evas, self)


        self._edje.part_swallow("groups", self.group_holder);
        #elementary.Scroller.resize_object_add(self._edje)
        self._edje.size_hint_weight_set(1.0, 1.0)
        self.content_set(self._edje)
        self._edje.show()


    def contactUpdated(self, contact):
        for gi in self.group_holder.group_items_list:
            if contact.uid in gi.contact_holder.contacts_dict:
                gi.contact_holder.contact_updated(contact)

    def groupUpdated(self, group):
        if group.uid in self.group_holder.group_items_dict:
            self.group_holder.group_items_dict[group.uid].group_updated(group)


    def contactListUpdated(self, clview):
        self.group_holder.viewUpdated(clview)



    def size_request_set(self, w,h):
       self.size_hint_request_set(w,h)


class ContactHolder(evas.SmartObject):

    def __init__(self, ecanvas, parent):
        evas.SmartObject.__init__(self, ecanvas)
        self.evas_obj = ecanvas
        self.contacts_dict = {}
        self.contacts_list = []
        self._skin = parent._skin
        self._parent = parent

    def contact_updated(self, contactview):
        #TODO : clean :)
        try:
            c = self.contacts_dict[contactview.uid]
        except KeyError:
            return
        c.part_text_set("contact_data", str(contactview.name))

        if DP_IN_CL:
            # add the dp
            # Remove the current dp
            obj_swallowed = c.part_swallow_get("buddy_icon")
            if obj_swallowed is not None:
                # Delete ?
                obj_swallowed.hide()
            dp = Image(self._skin, self.evas_obj, contactview.dp)
            c.part_swallow("buddy_icon", dp)
        else:
            # add the buddy icon
            # Remove the current icon
            obj_swallowed = c.part_swallow_get("buddy_icon")
            if obj_swallowed is not None:
                # Delete ?
                obj_swallowed.hide()
            icon = Image(self._skin, self.evas_obj, contactview.icon)
            c.part_swallow("buddy_icon", icon)

        if contactview.on_click is not None:
            def cb_(obj,event):
                contactview.on_click(obj.data['uid'])
            if c.data['on_click'] is not None:
                c.on_mouse_down_del(c.data['on_click'])
            c.data['on_click'] = cb_
            c.on_mouse_down_add(cb_)
        else:
            if c.data['on_click'] is not None:
                c.on_mouse_down_del(c.data['on_click'])
                c.data['on_click'] = None



    def groupViewUpdated(self, groupview):
        contact_items = self.contacts_list
        cuids = [c.uid for g in contact_items]
        self.contact_items = []
        for cid in groupview.contact_ids:
            if cid in cuids:
                self.contacts_list.append(self.contacts_dict[gid])
            else:
                #New contact
                self.add_contact(cid)

        #Remove unused contacts
        for cid in cuids:
            if cid not in self.contacts_dict:
                self.remove_contact(cid)

        #Now, we can redraw it
        self.show()



    def add_contact(self, uid):
        new_contact = edje.Edje(self.evas_obj, file=THEME_FILE,
                                group="contact_item")
        new_contact.data['uid'] = uid
        new_contact.data['on_click'] = None
        self.contacts_list.append(new_contact)
        self.contacts_dict[uid] = new_contact
        self.member_add(new_contact)

    def remove_contact(self, uid):
        try:
            ci = self.contacts_dict[uid]
            del self.contacts_dict[uid]
            try:
                self.contacts_list.remove(ci)
            except ValueError:
                pass
            self.member_del(ci)
            del ci
        except KeyError:
            pass

    def clip_set(self, obj):
        for c in self.contacts_list:
            c.clip_set(obj)

    def clip_unset(self):
        for c in self.contacts_list:
            c.clip_unset()

    def show(self):
        for c in self.contacts_list:
            c.show()

    def hide(self):
        for c in self.contacts_list:
            c.hide()

    def resize(self, w, h):
        self.update_widget(w, h)

    def update_widget(self, w, h):
        x = self.top_left[0]
        y = self.top_left[1]
        if len(self.contacts_list) > 0:
            spacing = 5
            total_spacing = spacing * len(self.contacts_list)
            item_height = (h - total_spacing) / len(self.contacts_list)
            for c in self.contacts_list:
                c.move(x, y)
                c.size = (w, item_height)
                y += item_height + spacing
        self._parent.show()

    def num_contacts(self):
        return len(self.contacts_list)



class GroupItem(edje.Edje):
    def __init__(self, parent, evas_obj, uid):
        self.evas_obj = evas_obj
        self._parent = parent
        self._skin = parent._skin
        self.expanded = True
        self.uid = uid
        self._edje = edje.Edje.__init__(self, self.evas_obj, file=THEME_FILE, group="group_item")
        self.contact_holder = ContactHolder(self.evas_obj, self)
        self.part_swallow("contacts", self.contact_holder);

        self.signal_callback_add("collapsed", "*", self.__collapsed_cb)
        self.signal_callback_add("expanded", "*", self.__expanded_cb)

    def num_contacts(self):
        if self.expanded == False:
            return 0
        else:
            return self.contact_holder.num_contacts()

    def group_updated(self, groupview):
        self.part_text_set("group_name", str(groupview.name))
        self.contact_holder.groupViewUpdated(groupview)

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

    def __init__(self, ecanvas, parent):
        evas.SmartObject.__init__(self, ecanvas)
        self.evas_obj = ecanvas
        self.group_items_list = []
        self.group_items_dict = {}
        self._parent = parent
        self._skin = parent._skin

    def add_group(self, uid):
        new_group = GroupItem(self, self.evas_obj, uid)
        self.group_items_list.append(new_group)
        self.group_items_dict[uid] = new_group
        self.member_add(new_group)

    def remove_group(self, uid):
        try:
            gi = self.group_items_dict[uid]
            del self.group_items_dict[uid]
            try:
                self.group_items_list.remove(gi)
            except ValueError:
                pass
            self.member_del(gi)
            del gi
        except KeyError:
            pass

    def resize(self, w, h):
        self.update_widget(w, h)

    def show(self):
        #FIXME:
        #ugly fix to get the correct clip
        self.clip_set(self._parent._edje.clip_get())
        self.update_widget(self.size[0], self.size[1])
        for g in self.group_items_list:
            g.show()

    def hide(self):
        for g in self.group_items_list:
            g.hide()

    def viewUpdated(self, clview):
        group_items = self.group_items_list
        guids = [g.uid for g in group_items]
        self.group_items = []
        for gid in clview.group_ids:
            if gid in guids:
                self.group_items_list.append(self.group_items_dict[gid])
            else:
                #New group
                self.add_group(gid)

        #Remove unused groups
        for gid in guids:
            if gid not in self.group_items_dict:
                self.remove_group(gid)

        #Now, we can redraw it
        self.show()

    def update_widget(self, w, h):
        x = self.top_left[0]
        y = self.top_left[1]
        if len(self.group_items_list) > 0:
            spacing = 5
            total_spacing = spacing * len(self.group_items_list)
            for i in self.group_items_list:
                item_height = 40 + (29 * i.num_contacts()) - 5
                i.move(x, y)
                i.size = (w, item_height)
                y += item_height + spacing
        self._parent.size_request_set(w,y)

    def clip_set(self, obj):
        for g in self.group_items_list:
            g._clip_set(obj)

    def clip_unset(self):
        for g in self.group_items_list:
            g._clip_unset()


