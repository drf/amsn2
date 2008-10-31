
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
        
    def setTitle(self, text):
        self._main_win.set_title(text)

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

class aMSNContactListWidget(base.aMSNContactListWidget, gtk.TreeView):
    def __init__(self, amsn_core, parent):
        """Constructor"""
        base.aMSNContactListWidget.__init__(self, amsn_core, parent)
        gtk.TreeView.__init__(self)
        
        self._amsn_core = amsn_core
        self._main_win = parent
        self.groups = []
        self.contacts = {}
        
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
        self._model = gtk.TreeStore(gtk.gdk.Pixbuf, object, str, str)
        self.model = self._model.filter_new(root=None)
        #self.model.set_visible_func(self._visible_func)

        self._model.set_sort_func(1, self._sort_method)
        self._model.set_sort_column_id(1, gtk.SORT_ASCENDING)
        
        self.set_model(self.model)
        
    def __search_by_id(self, id):
        parent = self._model.get_iter_first()
        
        while (parent is not None):
            obj = self._model.get_value(parent, 3)
            if (obj == id): return parent
            child = self._model.iter_children(parent)
            while (child is not None):
                cobj = self._model.get_value(child, 3)
                if (cobj == id): return child
                child = self._model.iter_next(child)
            parent = self._model.iter_next(parent)
            
        return None
        
    def _sort_method(self, model, iter1, iter2, user_data=None):
        '''callback called to decide the order of the contacts'''

        obj1 = self._model[iter1][1]
        obj2 = self._model[iter2][1]

        return 1

    def show(self):
        """ Show the contact list widget """
        #self.show()
        pass

    def hide(self):
        """ Hide the contact list widget """
        #self.hide()
        pass

    def contactListUpdated(self, clview):
        guids = self.groups
        self.groups = []
        
        # New groups
        for gid in clview.group_ids:
            if (gid == 0): gid = '0'
            if gid not in guids:
                self.groups.append(gid)
                self._model.append(None, [None, None, gid, gid])
                print "Added group %s" % gid
                
        # Remove unused groups
        for gid in guids:
            if gid not in self.groups:
                giter = self.__search_by_id(gid)
                self._model.remove(giter)
                self.groups.remove(gid)
                print "Removed group %s" % gid
        
    def groupUpdated(self, groupview):
        if (groupview.uid == 0): groupview.uid = '0'
        if groupview.uid not in self.groups: return
        
        giter = self.__search_by_id(groupview.uid)
        self._model.set_value(giter, 1, groupview)
        self._model.set_value(giter, 2, common.escape_pango(
            groupview.name.toString()))
        
        try:
            cuids = self.contacts[groupview.uid]
        except:
            cuids = []
        self.contacts[groupview.uid] = []
        
        for cid in groupview.contact_ids:
            if cid not in cuids:
                giter = self.__search_by_id(groupview.uid)
                self.contacts[groupview.uid].append(cid)
                self._model.append(giter, [None, None, cid, cid])
        
        # Remove unused contacts
        for cid in cuids:
            if cid not in self.contacts[groupview.uid]:
                citer = self.__search_by_id(cid)
                self._model.remove(citer)
                self.contacts[groupview.uid].remove(cid)
        

    def contactUpdated(self, contactview):
        citer = self.__search_by_id(contactview.uid)
        if citer is None: return
            
        self._model.set_value(citer, 1, contactview)
        self._model.set_value(citer, 2, common.escape_pango(
            contactview.name.toString()))
        
