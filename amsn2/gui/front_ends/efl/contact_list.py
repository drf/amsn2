
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
    def __init__(self, core, parent):
        base.aMSNContactListWindow.__init__(self, core, parent)
        self._core = core
        self._evas = parent._evas
        self._parent = parent
        self._skin = core._skin_manager.skin
        elementary.Box.__init__(self, parent)
        self.size_hint_weight_set(1.0, 1.0)
        self.size_hint_align_set(-1.0, -1.0)
        self.homogenous_set(False)
        self._parent.resize_object_add(self)
        self.show()

        """ Personal Info """
        self._personal_info = PersonalInfoWidget(self._core, self._parent)
        self._personal_info.size_hint_weight_set(1.0, 0.0)
        self._personal_info.size_hint_align_set(-1.0, 1.0)
        self.pack_start(self._personal_info)
        self._personal_info.show()

        """ ContactList Widget """
        self._clwidget = aMSNContactListWidget(self._core, self._parent)
        self._clwidget.size_hint_weight_set(1.0, 1.0)
        self._clwidget.size_hint_align_set(-1.0, -1.0)
        self.pack_end(self._clwidget)
        self._clwidget.show()

        self._parent.show()

    def setTitle(self, text):
        self._parent.setTitle(text)

    def setMenu(self, menu):
        self._parent.setMenu(menu)

    def myInfoUpdated(self, view):
        self._personal_info.myInfoUpdated(view)


class PersonalInfoWidget(elementary.Layout):
    def __init__(self, amsn_core, parent):
        self._core = amsn_core
        self._parent = parent
        self._personal_info_view = None
        elementary.Layout.__init__(self, self._parent)
        self.file_set(THEME_FILE, "personal_info")

        self._dp = elementary.Button(self._parent)
        self._dp.label_set("pouet")
        self._dp.size_hint_weight_set(1.0, 1.0)
        self.content_set("dp", self._dp);
        self._dp.show()

        self._presence = elementary.Hoversel(self._parent)
        self._presence.hover_parent_set(self._parent)
        for key in self._core.p2s:
            name = self._core.p2s[key]
            _, path = self._core._theme_manager.get_statusicon("buddy_%s" % name)
            if name == 'offline': continue
            def cb(data, hoversel, it):
                hoversel.label_set(it.label_get())
                (icon_file, icon_group, icon_type) = it.icon_get()
                ic = elementary.Icon(hoversel)
                ic.scale_set(0, 1)
                if icon_type == elementary.ELM_ICON_FILE:
                    ic.file_set(icon_file, icon_group)
                else:
                    ic.standart_set(icon_file)
                hoversel.icon_set(ic)
                ic.show()
                #TODO
            self._presence.item_add(name, path, elementary.ELM_ICON_FILE, cb,
                                   key)
        self.content_set("presence", self._presence);
        self._presence.show()

        sc = elementary.Scroller(self._parent)
        sc.content_min_limit(0, 1)
        sc.policy_set(elementary.ELM_SCROLLER_POLICY_OFF,
                      elementary.ELM_SCROLLER_POLICY_OFF);
        sc.size_hint_weight_set(1.0, 0.0)
        sc.size_hint_align_set(-1.0, 0.0)
        self.content_set("nick", sc)
        self._nick = elementary.Entry(self._parent)
        self._nick.single_line_set(True)
        self._nick.size_hint_weight_set(1.0, 0.0)
        self._nick.size_hint_align_set(-1.0, 0.0)
        sc.content_set(self._nick)
        self._nick.show()
        sc.show()

        sc = elementary.Scroller(self._parent)
        sc.content_min_limit(0, 1)
        sc.policy_set(elementary.ELM_SCROLLER_POLICY_OFF,
                      elementary.ELM_SCROLLER_POLICY_OFF);
        sc.size_hint_weight_set(1.0, 0.0)
        sc.size_hint_align_set(-1.0, -1.0)
        self.content_set("psm", sc);
        self._psm = elementary.Entry(self._parent)
        self._psm.single_line_set(True)
        self._psm.size_hint_weight_set(1.0, 0.0)
        self._psm.size_hint_align_set(-1.0, -1.0)
        sc.content_set(self._psm)
        self._psm.show()
        sc.show()

        sc = elementary.Scroller(self._parent)
        sc.content_min_limit(0, 1)
        sc.policy_set(elementary.ELM_SCROLLER_POLICY_OFF,
                      elementary.ELM_SCROLLER_POLICY_OFF)
        sc.size_hint_weight_set(1.0, 0.0)
        sc.size_hint_align_set(-1.0, -1.0)
        self.content_set("current_media", sc)
        self._cm = elementary.Entry(self._parent)
        self._cm.single_line_set(True)
        self._cm.size_hint_weight_set(1.0, 0.0)
        self._cm.size_hint_align_set(-1.0, -1.0)
        sc.content_set(self._cm)
        self._cm.show()
        sc.show()

    def myInfoUpdated(self, view):
        print "myInfoUpdated: view=%s" %(view,)
        self._personal_info_view = view

        #TODO
        self._dp.show()
        self._presence.show()

        self._nick.entry_set("nick is"+str(view.nick));
        self._nick.show()

        self._psm.entry_set("psm is "+str(view.psm));
        self._psm.show()

        self._cm.entry_set("cm is "+str(view.current_media));
        self._cm.show()

        self.show()

class aMSNContactListWidget(elementary.Box, base.aMSNContactListWidget):
    def __init__(self, core, parent):
        base.aMSNContactListWidget.__init__(self, core, parent)
        elementary.Box.__init__(self, parent)
        self._core = core
        self._evas = parent._evas
        self._skin = core._skin_manager.skin

        self.homogenous_set(False)
        self.size_hint_weight_set(1.0, 1.0)
        self.size_hint_align_set(-1.0, -1.0)
        self.show()

        self._sc = elementary.Scroller(parent)
        self._sc.size_hint_weight_set(1.0, 1.0)
        self._sc.size_hint_align_set(-1.0, -1.0)
        self._sc.policy_set(elementary.ELM_SCROLLER_POLICY_OFF,
                            elementary.ELM_SCROLLER_POLICY_AUTO)
        self.pack_start(self._sc)
        self._sc.show()

        self.group_holder = GroupHolder(self._evas, self, self._skin)
        self._sc.content_set(self.group_holder)
        self.group_holder.show()


    def contactUpdated(self, contact):
        for gi in self.group_holder.group_items_list:
            if contact.uid in gi.contact_holder.contacts_dict:
                gi.contact_holder.contact_updated(contact)

    def groupUpdated(self, group):
        if group.uid in self.group_holder.group_items_dict:
            self.group_holder.group_items_dict[group.uid].group_updated(group)


    def contactListUpdated(self, clview):
        self.group_holder.viewUpdated(clview)


class ContactHolder(elementary.Box):
    def __init__(self, parent):
        elementary.Box.__init__(self, parent)
        self.contacts_dict = {}
        self.contacts_list = []
        self._skin = parent._skin
        self._parent = parent
        self.size_hint_weight_set(1.0, 1.0)
        self.size_hint_align_set(-1.0, -1.0)

    def contact_updated(self, contactview):
        #TODO : clean :)
        try:
            c = self.contacts_dict[contactview.uid]
        except KeyError:
            return
        c.edje_get().part_text_set("contact_data", str(contactview.name))

        if DP_IN_CL:
            # add the dp
            dp = Image(self._skin, self.evas_get(), contactview.dp)
            c.content_set("buddy_icon", dp)
        else:
            # add the buddy icon
            # Remove the current icon
            icon = Image(self._skin, self.evas_get(), contactview.icon)
            c.content_set("buddy_icon", icon)

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
        c.show()
        print c.size_hint_min_get()


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

    def add_contact(self, uid):
        new_contact = elementary.Layout(self)
        new_contact.file_set(THEME_FILE, "contact_item")
        new_contact.data['uid'] = uid
        new_contact.data['on_click'] = None
        self.contacts_list.append(new_contact)
        self.contacts_dict[uid] = new_contact
        self.pack_end(new_contact)
        new_contact.size_hint_weight_set(1.0, 1.0)
        new_contact.size_hint_align_set(-1.0, -1.0)


    def remove_contact(self, uid):
        #TODO: remove from box
        try:
            ci = self.contacts_dict[uid]
            del self.contacts_dict[uid]
            try:
                self.contacts_list.remove(ci)
            except ValueError:
                pass
            del ci
        except KeyError:
            pass

    def num_contacts(self):
        return len(self.contacts_list)

class GroupItem(elementary.Layout):
    def __init__(self, parent, uid):
        elementary.Layout.__init__(self, parent)
        self.file_set(THEME_FILE, "group_item")
        self._parent = parent
        self._skin = parent._skin
        self.expanded = True
        self.uid = uid
        self.contact_holder = ContactHolder(self)
        self.content_set("contacts", self.contact_holder);
        self.contact_holder.show()

        self.edj = self.edje_get()
        self.edj.signal_callback_add("collapsed", "*", self.__collapsed_cb)
        self.edj.signal_callback_add("expanded", "*", self.__expanded_cb)

        self.size_hint_weight_set(1.0, 0.0)
        self.size_hint_align_set(-1.0, -1.0)

    def num_contacts(self):
        if self.expanded == False:
            return 0
        else:
            return self.contact_holder.num_contacts()

    def group_updated(self, groupview):
        self.edj.part_text_set("group_name", str(groupview.name))
        self.contact_holder.groupViewUpdated(groupview)

    # Private methods
    def __expanded_cb(self, edje_obj, signal, source):
        self.expanded = True
        print "expand"
        print self.size_hint_min_get()
        print self.contact_holder.size_hint_min_get()
        self.contact_holder.hide()

    def __collapsed_cb(self, edje_obj, signal, source):
        self.expanded = False
        print "collapse"
        print self.size_hint_min_get()
        print self.contact_holder.size_hint_min_get()
        self.contact_holder.show()

class GroupHolder(elementary.Box):
    def __init__(self, ecanvas, parent, skin):
        elementary.Box.__init__(self, parent)
        self.group_items_list = []
        self.group_items_dict = {}
        self._parent = parent
        self._skin = skin
        self.size_hint_weight_set(1.0, 1.0)
        self.size_hint_align_set(-1.0, -1.0)

    def add_group(self, uid):
        new_group = GroupItem(self, uid)
        self.group_items_list.append(new_group)
        self.group_items_dict[uid] = new_group
        self.pack_end(new_group)
        new_group.show()

    def remove_group(self, uid):
        #TODO: remove from box
        try:
            gi = self.group_items_dict[uid]
            del self.group_items_dict[uid]
            try:
                self.group_items_list.remove(gi)
            except ValueError:
                pass
            del gi
        except KeyError:
            pass

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

