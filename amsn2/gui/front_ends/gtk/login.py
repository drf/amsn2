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
from amsn2.core.views import AccountView, ImageView

class aMSNLoginWindow(gtk.VBox, base.aMSNLoginWindow):

    def __init__(self, amsn_core, parent):

        gtk.VBox.__init__(self, spacing=10)

        self._amsn_core = amsn_core
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
        self.user.connect("key-press-event", self.__on_user_comboxEntry_changed)
        #FIXME: focus-out-event not working, i don't know why
        self.user.connect("focus-out-event", self.__on_user_comboxEntry_changed)
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
        self.password.connect("changed", self.__on_passwd_comboxEntry_changed)
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

        self.rememberMe.connect("toggled", self.__on_toggled_cb)
        self.rememberPass.connect("toggled", self.__on_toggled_cb)
        self.autoLogin.connect("toggled", self.__on_toggled_cb)

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

    def __switch_to_account(self, email):
        print "Switching to account", email

        accv = [accv for accv in self._account_views if accv.email == email]

        if not accv:
            accv = AccountView()
            accv.email = email
        else:
            accv = accv[0]

        self.user.get_children()[0].set_text(accv.email)
        if accv.password:
            self.password.set_text(accv.password)

        self.rememberMe.set_active(accv.save)
        self.rememberPass.set_active(accv.save_password)
        self.autoLogin.set_active(accv.autologin)

    def setAccounts(self, accountviews):
        self._account_views = accountviews

        for accv in self._account_views:
            self.user.append_text(accv.email)

        if len(accountviews)>0 :
            # first in the list, default
            self.__switch_to_account(self._account_views[0].email)

            if self._account_views[0].autologin:
                self.signin()

    def signin(self):
        email = self.user.get_active_text()
        accv = [accv for accv in self._account_views if accv.email == email]
        if not accv:
            accv = AccountView()
            accv.email = email
        else:
            accv = accv[0]

        accv.password = self.password.get_text()
        status = self.statusCombo.get_active()
        for key in self.status_values:
            if self.status_values[key] == status:
                break
        accv.presence = key

        self._amsn_core.signinToAccount(self, accv)
        self.timer = gobject.timeout_add(40, self.__animation)

    def onConnecting(self, progress, message):
        self.status.set_text(message)
        self.pgbar.set_fraction(progress)

    def __on_user_comboxEntry_changed(self, entry, event):
        if event.type == gtk.gdk.FOCUS_CHANGE or \
            (event.type == gtk.gdk.KEY_PRESS and event.keyval == gtk.keysyms.Tab):
            self.__switch_to_account(entry.get_active_text())

    def __on_passwd_comboxEntry_changed(self, entry):
        if len(entry.get_text()) == 0:
            self.rememberPass.set_sensitive(False)
            self.autoLogin.set_sensitive(False)
        else:
            self.rememberPass.set_sensitive(True)
            self.autoLogin.set_sensitive(True)

    def __on_toggled_cb(self, source):

        accv = [accv for accv in self._account_views if accv.email == self.user.get_active_text()]

        if not accv:
            accv = AccountView()
            accv.email = self.user.get_active_text()
        else:
            accv = accv[0]

        if source is self.rememberMe:
            accv.save = source.get_active()
            self.rememberPass.set_sensitive(source.get_active())
            self.autoLogin.set_sensitive(source.get_active())
        elif source is self.rememberPass:
            accv.save_password = source.get_active()
            self.autoLogin.set_sensitive(source.get_active())
        elif source is self.autoLogin:
            accv.autologin = source.get_active()
