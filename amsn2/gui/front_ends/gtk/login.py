# -*- coding: utf-8 -*-
#===================================================
#
# login.py - This file is part of the amsn2 package
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

import os
import gtk
import gobject
import string

from image import *
from amsn2.core.views import ImageView

class aMSNLoginWindow(gtk.VBox, base.aMSNLoginWindow):

    def __init__(self, amsn_core, parent):

        gtk.VBox.__init__(self, spacing=10)

        self._amsn_core = amsn_core
        #self.switch_to_profile(None)
        self._main_win = parent
        self._skin = amsn_core._skin_manager.skin
        self._theme_manager = self._amsn_core._theme_manager
        self.timer = None
        self.anim_phase = 1
        self.last_img = None

        self.status = gtk.Label('')

        self.pgbar = gtk.ProgressBar()
        pgAlign = gtk.Alignment(0.5, 0.5)
        pgAlign.add(self.pgbar)

        # dp
        _, filename = self._theme_manager.get_dp("dp_amsn")
        dpbox = gtk.HBox()
        self.dp = gtk.Image()
        self.dp.set_from_file(filename)
        dpbox.pack_start(self.dp, True, False)

        # user
        userbox = gtk.VBox()
        userlabel = gtk.Label('User:')
        userlabel.set_alignment(0.0, 0.5)
        self.user = gtk.combo_box_entry_new_text()
        self.userListStore = gtk.ListStore(gobject.TYPE_STRING, gtk.gdk.Pixbuf)

        userCompletion = gtk.EntryCompletion()
        self.user.get_children()[0].set_completion(userCompletion)
        userCompletion.set_model(self.userListStore)

        userPixbufCell = gtk.CellRendererPixbuf()
        userCompletion.pack_start(userPixbufCell)

        userCompletion.add_attribute(userPixbufCell, 'pixbuf', 1)
        userCompletion.set_text_column(0)
        #userCompletion.connect('match-selected', self.matchSelected)
        #self.user.connect("changed", self.on_comboxEntry_changed)
        #self.user.connect("key-release-event", self.on_comboxEntry_keyrelease)
        userbox.pack_start(userlabel, False, False)
        userbox.pack_start(self.user, False, False)

        # password
        passbox = gtk.VBox()
        passlabel = gtk.Label('Password:')
        passlabel.set_alignment(0.0, 0.5)
        self.password = gtk.Entry(128)
        self.password.set_visibility(False)
        self.password.connect('activate' , self.__login_clicked)
        passbox.pack_start(passlabel, False, False)
        passbox.pack_start(self.password, False, False)

        # status list
        self.status_values = {}
        status_n = 0
        status_list = gtk.ListStore(gtk.gdk.Pixbuf, str, str)
        for key in self._amsn_core.p2s:
            name = self._amsn_core.p2s[key]
            _, path = self._theme_manager.get_statusicon("buddy_%s" % name)
            if (name == 'offline'): continue
            self.status_values[name] = status_n
            status_n = status_n +1
            icon = gtk.gdk.pixbuf_new_from_file(path)
            name = string.capitalize(name)
            status_list.append([icon, name, key])


        iconCell = gtk.CellRendererPixbuf()
        iconCell.set_property('xalign', 0.0)
        txtCell = gtk.CellRendererText()
        txtCell.set_property('xalign', 0.0)

        # status combobox
        self.statusCombo = gtk.ComboBox()
        self.statusCombo.set_model(status_list)
        self.statusCombo.set_active(4) # Set status to 'online'
        self.statusCombo.pack_start(iconCell, False)
        self.statusCombo.pack_start(txtCell, False)
        self.statusCombo.add_attribute(iconCell, 'pixbuf',0)
        self.statusCombo.add_attribute(txtCell, 'markup',1)

        statuslabel = gtk.Label('Status:')
        statuslabel.set_alignment(0.0, 0.5)

        statusbox = gtk.VBox()
        statusbox.pack_start(statuslabel, False, False)
        statusbox.pack_start(self.statusCombo, False, False)

        # container for user, password and status widgets
        fields = gtk.VBox(True, 5)
        fields.pack_start(userbox, False, False)
        fields.pack_start(passbox, False, False)
        fields.pack_start(statusbox, False, False)

        fields_align = gtk.Alignment(0.5, 0.5, 0.75, 0.0)
        fields_align.add(fields)

        # checkboxes
        checkboxes = gtk.VBox()
        self.rememberMe = gtk.CheckButton('Remember me', True)
        self.rememberPass = gtk.CheckButton('Remember password', True)
        self.autoLogin = gtk.CheckButton('Auto-Login', True)

        checkboxes.pack_start(self.rememberMe, False, False)
        checkboxes.pack_start(self.rememberPass, False, False)
        checkboxes.pack_start(self.autoLogin, False, False)

        # align checkboxes
        checkAlign = gtk.Alignment(0.5, 0.5)
        checkAlign.add(checkboxes)

        # login button
        button_box = gtk.HButtonBox()
        login_button = gtk.Button('Login', gtk.STOCK_CONNECT)
        login_button.connect('clicked', self.__login_clicked)
        button_box.pack_start(login_button, False, False)

        self.pack_start(self.status, True, False)
        self.pack_start(dpbox, False, False)
        self.pack_start(pgAlign, True, False)
        self.pack_start(fields_align, True, False)
        self.pack_start(checkAlign, True, False)
        self.pack_start(button_box, True, False)

        self.show_all()
        self._main_win.set_view(self)
        self.user.grab_focus()
        #self.switch_to_profile(None)

    def __animation(self):
        path = os.path.join("amsn2", "themes", "default", "images",
        "login_screen", "cube")
        name = "cube_%03d.png" % self.anim_phase
        filename = os.path.join(path, name)

        if (os.path.isfile(filename)):
            self.last_img = filename
        else:
            filename = self.last_img

        pix = gtk.gdk.pixbuf_new_from_file_at_size(filename, 96, 96)
        self.dp.set_from_pixbuf(pix)
        self.anim_phase += 1
        del pix

        return True

    def __login_clicked(self, *args):
        self.signin()

    def show(self):
        self.show_all()

    def hide(self):
        if (self.timer is not None):
            gobject.source_remove(self.timer)

    def switch_to_profile(self, profile):
        self.current_profile = profile
        if profile is not None:
            self._username = self.current_profile.username
            self.user.get_children()[0].set_text(self._username)
            self._password = self.current_profile.password
            self.password.set_text(self._password)

    def signin(self):
        self.current_profile.username = self.user.get_active_text()
        self.current_profile.email = self.user.get_active_text()
        self.current_profile.password = self.password.get_text()
        status = self.statusCombo.get_active()
        for key in self.status_values:
            if self.status_values[key] == status:
                break
        self.current_profile.presence = key
        self._amsn_core.signinToAccount(self, self.current_profile)
        self.timer = gobject.timeout_add(40, self.__animation)

    def onConnecting(self, progress, message):
        self.status.set_text(message)
        self.pgbar.set_fraction(progress)

