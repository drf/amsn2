
import gtk
import gobject
import pango

import pymsn
from amsn2.core.views import StringView
from amsn2.core.views import GroupView
from amsn2.core.views import ContactView
from amsn2.gui import base

import common

class aMSNContactListWindow(base.aMSNContactListWindow, gtk.VBox):
    '''GTK contactlist'''
    def __init__(self, amsn_core, parent):
        '''Constructor'''
        
        gtk.VBox.__init__(self)
        
        self._amsn_core = amsn_core
        self._main_win = parent
        
        self._clwidget = aMSNContactListWidget(amsn_core, parent)
        
        self.__create_controls()
        header = self.__create_box()
        
        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)	
        scrollwindow.add(self._clwidget)
        
        self.pack_start(header, False, False)
        self.pack_start(scrollwindow, True, True)
        self.show_all()
        
        #self._main_win.set_view(self.view)
        self._main_win.set_view(self)
        
    def __create_controls(self):
        # Main Controls
        self.display = gtk.Image()
        self.display.set_size_request(64,64)
        
        self.nickname = gtk.Label()
        self.nickname.set_alignment(0, 0)
        self.nickname.set_use_markup(True)
        self.nickname.set_ellipsize(pango.ELLIPSIZE_END)
        self.nickname.set_markup('Loading...')
        
        self.btnNickname = gtk.Button()
        self.btnNickname.set_relief(gtk.RELIEF_NONE)
        self.btnNickname.add(self.nickname)
        
        self.psm = gtk.Entry()
        self.psm.modify_font(common.GUI_FONT)
        
        self.psmlabel = gtk.Label()
        self.psmlabel.set_use_markup(True)
        self.psmlabel.set_ellipsize(pango.ELLIPSIZE_END)
        self.psmlabel.modify_font(common.GUI_FONT)
        
        self.btnPsm = gtk.Button()
        self.btnPsm.add(self.psmlabel)
        self.btnPsm.set_relief(gtk.RELIEF_NONE)
        self.btnPsm.set_alignment(0,0.5)
        
        self.cs = gtk.Label()
        self.cs.set_use_markup(True)
        self.cs.set_markup('')
        self.cs.set_alignment(0,0.5)
        self.cs.set_ellipsize(pango.ELLIPSIZE_END)
        
    def __create_box(self):
        frameDisplay = gtk.Frame()
        frameDisplay.add(self.display)
        self.evdisplay = gtk.EventBox()
        self.evdisplay.add(frameDisplay)

        headerLeft = gtk.VBox(False, 0)
        headerLeft.pack_start(self.evdisplay, True, False)

        # Header Right
        boxNick = gtk.HBox(False, 0)
        boxNick.pack_start(self.btnNickname, True, True)

        boxPsm = gtk.HBox(False, 0)
        boxPsm.pack_start(self.psm, True, True)
        boxPsm.pack_start(self.btnPsm, True, True)

        boxCs = gtk.HBox(False, 2)
        boxCs.pack_start(self.cs, True, True)

        headerRight = gtk.VBox(False, 0)
        headerRight.pack_start(boxNick, True, False)
        headerRight.pack_start(boxPsm, False, False)
        headerRight.pack_start(boxCs, False, False, 3)

        # Header pack
        header = gtk.HBox(False, 5)
        header.pack_start(headerRight, True, True, 0)
        header.pack_start(headerLeft, False, False, 0)
        return header

    def show(self):
        pass 

    def hide(self):
        pass 

    def contactUpdated(self, contact):
        contact_data = (None, contact, common.stringvToHtml(contact.name))
        for row in self._model:
            obj = row[1]
            if type(obj) == GroupView:
                for contact_row in row.iterchildren():
                    con = contact_row[1]
                    if con.uid == contact.uid:
                        self._model[contact_row.iter] = contact_data
                        #self.groupUpdated(obj)
            elif type(obj) == ContactView and obj.account == contact.account:
                self._model[row.iter] = contact_data

    def groupUpdated(self, group):
        print 'group updated...'
        raise NotImplementedError
    
    def groupAdded(self, group):
        group_data = (None, group, self.format_group(group))
        iter = self._model.append(None, group_data)
        
        for contact in group.contacts:
            contact_data = (None, contact, common.stringvToHtml(contact.name))
            self._model.append(iter, contact_data)
            
        path = self._model.get_path(iter)
        self.expand_row(path, False)

    def format_group(self, group):
        return '<b>' + group.name.toString() + '</b>'

    def groupRemoved(self, group):
        pass

    def configure(self, option, value):
        pass

    def cget(self, option, value):
        pass

class aMSNContactListWidget(base.aMSNContactListWidget, gtk.TreeView):
    def __init__(self, amsn_core, parent):
        """Constructor"""
        gtk.TreeView.__init__(self)
        
        self._amsn_core = amsn_core
        self._main_win = parent
        
        crt = gtk.CellRendererText()
        column = gtk.TreeViewColumn()
        column.set_expand(True)
        
        exp_column = gtk.TreeViewColumn()
        exp_column.set_max_width(16)       
        
        self.append_column(exp_column)
        self.append_column(column)
        self.set_expander_column(exp_column)
        
        column.pack_start(crt)
        column.add_attribute(crt, 'markup', 2)
        
        self.set_search_column(2)
        self.set_headers_visible(False)
        
        # the image (None for groups) the object (group or contact) and 
        # the string to display
        self._model = gtk.TreeStore(gtk.gdk.Pixbuf, object, str)
        self.model = self._model.filter_new(root=None)
        #self.model.set_visible_func(self._visible_func)

        self._model.set_sort_func(1, self._sort_method)
        self._model.set_sort_column_id(1, gtk.SORT_ASCENDING)
        
        self.set_model(self.model)
        
    def _sort_method(self, model, iter1, iter2, user_data=None):
        '''callback called to decide the order of the contacts'''

        obj1 = self._model[iter1][1]
        obj2 = self._model[iter2][1]

        return 1
        #if type(obj1) == Group and type(obj2) == Group:
        #    return self.compare_groups(obj1, obj2)
        #elif type(obj1) == Contact and type(obj2) == Contact:
        #    return self.compare_contacts(obj1, obj2)
        #elif type(obj1) == Group and type(obj2) == Contact:
        #    return -1
        #else:
        #    return 1

    def show(self):
        """ Show the contact list widget """
        self.show()

    def hide(self):
        """ Hide the contact list widget """
        self.hide()

    def contactListUpdated(self, clView):
        """ This method will be called when the core wants to notify
        the contact list of the groups that it contains, and where they
        should be drawn a group should be drawn.
        It will be called initially to feed the contact list with the groups
        that the CL should contain.
        It will also be called to remove any group that needs to be removed.
        @cl : a ContactListView containing the list of groups contained in
        the contact list which will contain the list of ContactViews
        for all the contacts to show in the group."""
        raise NotImplementedError
        
    def groupAdded(self, group):
        gi = self._model.append(None, [None, group, common.escape_pango(
                group.name.toString())])
        for c in group.contacts:
            self._model.append(gi, [None, c, common.escape_pango(
                c.name.toString())])
        
    def groupUpdated(self, groupView):
        """ This method will be called to notify the contact list
        that a group has been updated.
        The contact list should update its icon and name
        but also its content (the ContactViews). The order of the contacts
        may be changed, in which case the UI should update itself accordingly.
        A contact can also be added or removed from a group using this method
        """
        raise NotImplementedError

    def contactUpdated(self, contactView):
        """ This method will be called to notify the contact list
        that a contact has been updated.
        The contact can be in any group drawn and his icon,
        name or DP should be updated accordingly.
        The position of the contact will not be changed by a call
        to this function. If the position was changed, a groupUpdated
        call will be made with the new order of the contacts
        in the affects groups.
        """
        pass #raise NotImplementedError

    def setContactCallback(self, cb):
        """ Set the callback when a contact is clicked or double clicked (choice
        is given to the front-end developer)
        If cb is None, the callback should be removed
        Expected signature: function(cid)
        cid is the contact id of the contact actionned
        """
        self.callback = cb

    def setContactContextMenu(self, cb):
        """ Set the callback when a context menu for a contact should be
        displayed (choice is given to the front-end developer, usually on right
        click)
        If cb is None, the callback should be removed
        Expected signature: function(cid)
        cid is the contact id of the contact actionned
        That function must return a MenuView
        """
        raise NotImplementedError

    def setGroupCallback(self, cb):
        """ Set the callback when a group is clicked or double clicked (choice
        is given to the front-end developer)
        If cb is None, the callback should be removed
        Expected signature: function(gid)
        gid is the group id of the group actionned
        """
        raise NotImplementedError

    def setContactContextMenu(self, cb):
        """ Set the callback when a context menu for a group should be
        displayed (choice is given to the front-end developer, usually on right
        click)
        If cb is None, the callback should be removed
        Expected signature: function(gid)
        gid is the group id of the group actionned
        That function must return a MenuView
        """
        raise NotImplementedError