import gtk

class TextBox(object):
    def __init__(self, win, y, x, txt):
	self._win = win.derwin(1, 30, y, x)
	self._win.clear()
	self._txtbox = curses.textpad.Textbox(self._win)
	self._txtbox.stripspaces = True

        if txt is not None:
            for x in txt:
                self._txtbox.do_command(x)

    def edit(self):
	return self._txtbox.edit()

    def value(self):
        return self._txtbox.gather()
    
class aMSNLoginWindow(object):
    def __init__(self, amsn_core):
        self._amsn_core = amsn_core
        self.switch_to_profile(None)
        self._main_win = self._amsn_core.getMainWindow()
        
        self.view = gtk.VBox(spacing=10)
        self.status = gtk.Label('')
        self.view.pack_start(self.status, True, False)
        
        fields = gtk.VBox()
        
        # account
        accountbox = gtk.VBox()
        accountlabel = gtk.Label('Account:')
        accountlabel.set_alignment(0.0, 0.5)
        self.account = gtk.Entry()
        accountbox.pack_start(accountlabel, False, False)
        accountbox.pack_start(self.account, False, False)
        fields.pack_start(accountbox, False, False)
        
        # password
        passbox = gtk.VBox()
        passlabel = gtk.Label('Password:')
        passlabel.set_alignment(0.0, 0.5)
        self.password = gtk.Entry()
        self.password.set_visibility(False)
        passbox.pack_start(passlabel, False, False)
        passbox.pack_start(self.password, False, False)
        fields.pack_start(passbox, False, False)
        
        # field alignment
        fields_align = gtk.Alignment(0.5, 0.5, 0.75, 0.0)
        fields_align.add(fields)
        self.view.pack_start(fields_align, True, False)
        
        # login button
        button_box = gtk.HButtonBox()
        login_button = gtk.Button('Login', gtk.STOCK_CONNECT)
        login_button.connect('clicked', self._login_clicked)
        button_box.pack_start(login_button, False, False)
        self.view.pack_start(button_box, True, False)
        
        self.view.show_all()
        self._main_win.set_view(self.view)
        
    def show(self):
        self._main_win.set_title('aMSN 2 - Login')

    def hide(self):
        self._username_t = None
        self._password_t = None
        self._win.clear()
        self._win.refresh()

    def switch_to_profile(self, profile):
        self.current_profile = profile
        if self.current_profile is not None:
            self._username = self.current_profile.username
            self._password = self.current_profile.password

    def signin(self):
        self.current_profile.username = self.account.get_text()
        self.current_profile.email = self.account.get_text()
        self.current_profile.password = self.password.get_text()
        self._amsn_core.signinToAccount(self, self.current_profile)

    def onConnecting(self):
        self.status.set_text("Connecting...")

    def onConnected(self):
        self.status.set_text("Connected...")

    def onAuthenticating(self):
        self.status.set_text("Authenticating...")

    def onAuthenticated(self):
        self.status.set_text("Authenticated...")

    def onSynchronizing(self):
        self.status.set_text("Fetching contact list...")

    def onSynchronized(self):
        self.status.set_text("Synchronized!")

    def _login_clicked(self, *args):
        self.signin()
        
