# -*- coding: utf-8 -*-
#===================================================
#
# contact_list.py - This file is part of the amsn2 package
#
# Copyright (C) 2008  Wil Alvarez <wil_alejandro@yahoo.com>
#
# This script is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# This script is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License along with
# this script (see COPYING); if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#===================================================

import gc
import os
import gtk
import pango
import gobject

#import papyon
from image import *
from amsn2.core.views import StringView
from amsn2.core.views import GroupView
from amsn2.core.views import ContactView
from amsn2.core.views import ImageView
from amsn2.core.views import PersonalInfoView
from amsn2.gui import base

import common

class aMSNContactListWindow(base.aMSNContactListWindow, gtk.VBox):
    '''GTK contactlist'''
    def __init__(self, amsn_core, parent):
        '''Constructor'''
        gtk.VBox.__init__(self)
        base.aMSNContactListWindow.__init__(self, amsn_core, parent)

        self._amsn_core = amsn_core
        self._main_win = parent
        self._skin = amsn_core._skin_manager.skin
        self._theme_manager = self._amsn_core._theme_manager
        self._myview = amsn_core._personalinfo_manager._personalinfoview

        self._clwidget = aMSNContactListWidget(amsn_core, self)

        self.__create_controls()
        self.__create_box()

        self._main_win.set_view(self)

        self.show_all()
        self.__setup_window()

    def __create_controls(self):
        ###self.psmlabel.modify_font(common.GUI_FONT)
        # Main Controls
        self.display = gtk.Image()
        self.display.set_size_request(64,64)
        
        self.btnDisplay = gtk.Button()
        self.btnDisplay.set_relief(gtk.RELIEF_NONE)
        self.btnDisplay.add(self.display)
        self.btnDisplay.set_alignment(0,0)
        self.btnDisplay.connect("clicked", self.__onDisplayClicked)
        
        self.nicklabel = gtk.Label()
        self.nicklabel.set_alignment(0, 0)
        self.nicklabel.set_use_markup(True)
        self.nicklabel.set_ellipsize(pango.ELLIPSIZE_END)
        self.nicklabel.set_markup('Loading...')

        self.btnNickname = gtk.Button()
        self.btnNickname.set_relief(gtk.RELIEF_NONE)
        self.btnNickname.add(self.nicklabel)
        self.btnNickname.set_alignment(0,0)
        self.btnNickname.connect("clicked",self.__on_btnNicknameClicked)

        self.psmlabel = gtk.Label()
        self.psmlabel.set_alignment(0, 0)
        self.psmlabel.set_use_markup(True)
        self.psmlabel.set_ellipsize(pango.ELLIPSIZE_END)
        self.psmlabel.set_markup('<i>&lt;Personal message&gt;</i>')

        self.btnPsm = gtk.Button()
        self.btnPsm.add(self.psmlabel)
        self.btnPsm.set_relief(gtk.RELIEF_NONE)
        self.btnPsm.set_alignment(0,0)
        self.btnPsm.connect("clicked", self.__on_btnPsmClicked)

        # status list
        self.status_values = {}
        status_list = gtk.ListStore(gtk.gdk.Pixbuf, str, str)
        for key in self._amsn_core.p2s:
            name = self._amsn_core.p2s[key]
            self.status_values[name] = self._amsn_core.p2s.values().index(name)
            _, path = self._theme_manager.get_statusicon("buddy_%s" % name)
            #if (name == 'offline'): continue
            #iv = ImageView("Skin", "buddy_%s" % name)
            #img = Image(self._skin, iv)
            #icon = img.to_pixbuf(28)
            icon = gtk.gdk.pixbuf_new_from_file(path)
            status_list.append([icon, name, key])
            del icon
            gc.collect()

        iconCell = gtk.CellRendererPixbuf()
        iconCell.set_property('xalign', 0.0)
        txtCell = gtk.CellRendererText()
        txtCell.set_property('xalign', 0.0)

        self.status = gtk.ComboBox()
        self.status.set_model(status_list)
        self.status.set_active(0)
        self.status.pack_start(iconCell, False)
        self.status.pack_start(txtCell, False)
        self.status.add_attribute(iconCell, 'pixbuf',0)
        self.status.add_attribute(txtCell, 'markup',1)
        self.status.connect('changed', self.onStatusChanged)

    def __create_box(self):
        frameDisplay = gtk.Frame()
        frameDisplay.add(self.btnDisplay)
        self.evdisplay = gtk.EventBox()
        self.evdisplay.add(frameDisplay)

        headerLeft = gtk.VBox(False, 0)
        headerLeft.pack_start(self.evdisplay, True, False)

        # Header Right
        boxNick = gtk.HBox(False, 0)
        boxNick.pack_start(self.btnNickname, True, True)

        boxPsm = gtk.HBox(False, 0)
        boxPsm.pack_start(self.btnPsm, True, True)

        headerRight = gtk.VBox(False, 0)
        headerRight.pack_start(boxNick, False, False)
        headerRight.pack_start(boxPsm, False, False)

        # Header pack
        header = gtk.HBox(False, 1)
        header.pack_start(headerLeft, False, False, 0)
        header.pack_start(headerRight, True, True, 0)

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)	
        scrollwindow.add(self._clwidget)

        bottom = gtk.HBox(False, 0)
        bottom.pack_start(self.status, True, True, 0)

        self.pack_start(header, False, False, 2)
        self.pack_start(scrollwindow, True, True, 2)
        self.pack_start(bottom, False, False, 2)

    def __setup_window(self):
        _, filename = self._theme_manager.get_dp('dp_nopic')
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(filename, 64, 64)
        self.display.set_from_pixbuf(pixbuf)
        del pixbuf
        gc.collect()


    def show(self):
        pass

    def hide(self):
        pass

    def setTitle(self, text):
        self._main_win.set_title(text)

    def setMenu(self, menu):
        """ This will allow the core to change the current window's main menu
        @type menu: MenuView
        """
        pass

    def myInfoUpdated(self, view):
        """ This will allow the core to change pieces of information about
        ourself, such as DP, nick, psm, the current media being played,...
        @type view: PersonalInfoView
        @param view: ourself (contains DP, nick, psm, currentMedia,...)
        """
        # TODO: image, ...
        self._myview = view
        nk = view.nick
        self.nicklabel.set_markup(str(nk))
        psm = view.psm
        cm = view.current_media
        message = str(psm)+' '+str(cm)
        self.psmlabel.set_markup('<i>'+message+'</i>')
        self.status.set_active(self.status_values[view.presence])

    def onStatusChanged(self, combobox):
        status = combobox.get_active()
        for key in self.status_values:
            if self.status_values[key] == status:
                break
        # FIXME: changing status to 'offline' will disconnect, so return to login window
        # also fix papyon, gives an error on setting 'offline'
        if key != self._myview.presence:
            self._myview.presence = key

    def __on_btnNicknameClicked(self, source):
        self.__switchToInput(source)
        
    def __on_btnPsmClicked(self, source):
        self.__switchToInput(source)
        
    def __switchToInput(self, source):
        """ Switches the nick button into a text area for editing of the nick
        name."""
        #label = self.btnNickname.get_child()
        source.remove(source.get_child())
        entry = gtk.Entry()
        source.add(entry)
        entry.show()
        entry.grab_focus()
        source.set_relief(gtk.RELIEF_NORMAL) # Add cool elevated effect
        entry.connect("activate", self.__switchFromInput, True)
        entry.connect("key-press-event", self.__handleInput)
        self.focusOutId = entry.connect("focus-out-event", self.__handleInput)
        
    def __handleInput(self, source, event):
        """ Handle various inputs from the nicknameEntry-box """
        if(event.type == gtk.gdk.FOCUS_CHANGE): #user clickd outside textfield
            self.__switchFromInput(source, False)
        elif (event.type == gtk.gdk.KEY_PRESS): #user wrote something, esc perhaps?
            if event.keyval == gtk.keysyms.Escape:
                self.__switchFromInput(source, False)

    def __switchFromInput(self, source, isNew):
        """ When in the editing state of nickname, change back to the uneditable
        label state.
        """
        if(isNew):
            if(source == self.btnNickname.get_child()): 
                newText = source.get_text()
                strv = StringView()
                strv.appendText(newText)
                self._myview.nick = strv
            elif (source == self.btnPsm.get_child()):
                newText = source.get_text()
                strv = StringView()
                strv.appendText(newText)
                self._myview.psm = strv
        else:
            if(source == self.btnNickname.get_child()): # User discards input
                newText = self.nicklabel.get_text() # Old nickname
            if(source == self.btnPsm.get_child()):
                newText = self.psmlabel.get_text()

        parentWidget = source.get_parent()
        currWidget = parentWidget.get_child()
        currWidget.disconnect(self.focusOutId) # Else we trigger focus-out-event; segfault.
        
        parentWidget.remove(currWidget)
        entry = gtk.Label()
        entry.set_markup(newText)
        
        parentWidget.add(entry)
        entry.show()
        parentWidget.set_relief(gtk.RELIEF_NONE) # remove cool elevated effect
        
    def __onDisplayClicked(self, source):
        print "Display clicked!"
        chooser = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_OPEN,
                    buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        
        chooser.set_default_response(gtk.RESPONSE_OK)
        
        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        chooser.add_filter(filter)

        response = chooser.run()
        if(response == gtk.RESPONSE_OK):
            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(chooser.get_filename(), 64, 64)
            self.display.set_from_pixbuf(pixbuf)
            del pixbuf
            gc.collect()
        elif (response == gtk.RESPONSE_CANCEL):
            pass
        chooser.destroy()


    def __on_btnPsmClicked(self, source):
        self.__switchToPsmInput()

    def __switchToPsmInput(self):
        """ Switches the psm button into a text area for editing of the psm."""

        self.btnPsm.get_child().destroy()
        entry = gtk.Entry()
        entry.set_text(str(self._myview.psm))
        self.btnPsm.add(entry)
        entry.show()
        entry.connect("activate", self.__switchFromPsmInput)
        #TODO: If user press ESC then destroy gtk.Entry

    def __switchFromPsmInput(self, source):
        """ When in the editing state of psm, change back to the uneditable
        label state.
        """
        strv = StringView()
        strv.appendText(source.get_text())
        self._myview.psm = strv
        self.btnPsm.get_child().destroy()
        entry = self.psmlabel
        self.btnPsm.add(entry)
        entry.show()

class aMSNContactListWidget(base.aMSNContactListWidget, gtk.TreeView):
    def __init__(self, amsn_core, parent):
        """Constructor"""
        base.aMSNContactListWidget.__init__(self, amsn_core, parent)
        gtk.TreeView.__init__(self)

        self._amsn_core = amsn_core
        self._cwin = parent
        self.groups = []
        self.contacts = {}

        nick = gtk.CellRendererText()
        nick.set_property('ellipsize-set',True)
        nick.set_property('ellipsize', pango.ELLIPSIZE_END)
        pix = gtk.CellRendererPixbuf()

        column = gtk.TreeViewColumn()
        column.set_expand(True)
        column.set_alignment(0.0)
        column.pack_start(pix, False)
        column.pack_start(nick, True)

        #column.add_attribute(pix, 'pixbuf', 0)
        column.set_attributes(pix, pixbuf=0, visible=4)
        column.add_attribute(nick, 'markup', 2)

        exp_column = gtk.TreeViewColumn()
        exp_column.set_max_width(16)

        self.append_column(exp_column)
        self.append_column(column)
        self.set_expander_column(exp_column)

        self.set_search_column(2)
        self.set_headers_visible(False)
        self.set_level_indentation(0)

        # the image (None for groups) the object (group or contact) and
        # the string to display
        self._model = gtk.TreeStore(gtk.gdk.Pixbuf, object, str, str, bool)
        self.model = self._model.filter_new(root=None)
        #self.model.set_visible_func(self._visible_func)

        self.set_model(self.model)
        self.connect("row-activated", self.__on_contact_dblclick)

    def __on_contact_dblclick(self, widget, path, column):
        model, row = widget.get_selection().get_selected()
        if (row is None): return False
        if not (model.get_value(row, 4)): return False

        contactview = model.get_value(row, 1)
        contactview.on_click(contactview.uid)

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

    def show(self):
        pass

    def hide(self):
        pass

    def contactListUpdated(self, clview):
        guids = self.groups
        self.groups = []

        # New groups
        for gid in clview.group_ids:
            if (gid == 0): gid = '0'
            if gid not in guids:
                self.groups.append(gid)
                self._model.append(None, [None, None, gid, gid, False])

        # Remove unused groups
        for gid in guids:
            if gid not in self.groups:
                giter = self.__search_by_id(gid)
                self._model.remove(giter)
                self.groups.remove(gid)

    def groupUpdated(self, groupview):
        if (groupview.uid == 0): groupview.uid = '0'
        if groupview.uid not in self.groups: return

        giter = self.__search_by_id(groupview.uid)
        self._model.set_value(giter, 1, groupview)
        self._model.set_value(giter, 2, '<b>%s</b>' % common.escape_pango(
            str(groupview.name)))

        try:
            cuids = self.contacts[groupview.uid]
        except:
            cuids = []
        self.contacts[groupview.uid] = []

        for cid in groupview.contact_ids:
            if cid not in cuids:
                giter = self.__search_by_id(groupview.uid)
                self.contacts[groupview.uid].append(cid)
                self._model.append(giter, [None, None, cid, cid, True])

        # Remove unused contacts
        for cid in cuids:
            if cid not in self.contacts[groupview.uid]:
                citer = self.__search_by_id(cid)
                self._model.remove(citer)
                self.contacts[groupview.uid].remove(cid)


    def contactUpdated(self, contactview):
        citer = self.__search_by_id(contactview.uid)
        if citer is None: return

        img = Image(self._cwin._theme_manager, contactview.dp)
        #img = Image(self._cwin._theme_manager, contactview.icon)
        dp = img.to_pixbuf(28, 28)

        self._model.set_value(citer, 0, dp)
        self._model.set_value(citer, 1, contactview)
        self._model.set_value(citer, 2, common.escape_pango(
            str(contactview.name)))
        del dp
        gc.collect()

