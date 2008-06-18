import gtk
import gobject

class aMSNLoginWindow(gtk.VBox):
    def __init__(self, amsn_core):
        
        gtk.VBox.__init__(self, spacing=10)
        
        self._amsn_core = amsn_core
        self.switch_to_profile(None)
        self._main_win = self._amsn_core.getMainWindow()
        
        self.status = gtk.Label('')
        self.pack_start(self.status, True, False)
        
        # container for user, password and status widgets
        fields = gtk.VBox(True, 5)
        
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
        fields.pack_start(userbox, False, False)
        
        # password
        passbox = gtk.VBox()
        passlabel = gtk.Label('Password:')
        passlabel.set_alignment(0.0, 0.5)
        self.password = gtk.Entry(128)
        self.password.set_visibility(False)
        self.password.connect('activate' , self._login_clicked)
        passbox.pack_start(passlabel, False, False)
        passbox.pack_start(self.password, False, False)
        fields.pack_start(passbox, False, False)
        
        # status combobox
        self.statusListStore = gtk.ListStore(gtk.gdk.Pixbuf, 
                                              gobject.TYPE_STRING,
                                              gobject.TYPE_STRING)
        statusbox = gtk.VBox()
        self.statusCombo = gtk.ComboBox(self.statusListStore)
        #statusPixbufCell = gtk.CellRendererPixbuf()
        statusTextCell = gtk.CellRendererText()
        #statusCombo.pack_start(statusPixbufCell, False)
        self.statusCombo.pack_start(statusTextCell, False)
        #statusPixbufCell.set_property('xalign', 0.0)
        #statusPixbufCell.set_property('xpad', 5)
        statusTextCell.set_property('xalign', 0.0)
        statusTextCell.set_property('xpad', 5)
        self.statusCombo.add_attribute(statusTextCell, 'text', 2)
        #statusCombo.add_attribute(statusPixbufCell, 'pixbuf', 0)
        statuslabel = gtk.Label('Status:')
        statuslabel.set_alignment(0.0, 0.5)
        statusbox.pack_start(statuslabel, False, False)
        statusbox.pack_start(self.statusCombo, False, False)
        fields.pack_start(statusbox, False, False)
        
        # fill status combo
        for status in ['Online', 'Busy', 'Away', 'Show offline']:
            self.statusListStore.append( [None, 0, status] )
        self.statusCombo.set_active(0)
        
        # align fields
        fields_align = gtk.Alignment(0.5, 0.5, 0.75, 0.0)
        fields_align.add(fields)
        self.pack_start(fields_align, True, False)
        
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
        self.pack_start(checkAlign, True, False)
        
        # login button
        button_box = gtk.HButtonBox()
        login_button = gtk.Button('Login', gtk.STOCK_CONNECT)
        login_button.connect('clicked', self._login_clicked)
        button_box.pack_start(login_button, False, False)
        self.pack_start(button_box, True, False)
        
        self.show_all()
        self._main_win.set_view(self)
        self.user.grab_focus()
        
        self.switch_to_profile(None)
        
        
    def show(self):
        self._main_win.set_title('aMSN 2 - Login')

    def hide(self):
        pass

    def switch_to_profile(self, profile):
        self.current_profile = profile
        if self.current_profile is not None:
            self._username = self.current_profile.username
            self._password = self.current_profile.password

    def signin(self):
        self.current_profile.username = self.user.get_active_text()
        self.current_profile.email = self.user.get_active_text()
        self.current_profile.password = self.password.get_text()
        self._amsn_core.signinToAccount(self, self.current_profile)

    def onConnecting(self, message):
        self.status.set_text(message)

    def _login_clicked(self, *args):
        self.signin()
        
