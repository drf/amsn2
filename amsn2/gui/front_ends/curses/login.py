import curses
import curses.textpad


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
	self._stdscr = self._amsn_core.getMainWindow()._stdscr
        self._win = curses.newwin(20, 100, 5, 5)
        
    def show(self):
        self._win.addstr(5, 5, "Account : ", curses.A_BOLD)
        self._username_t = TextBox(self._win, 5, 17, self._username)

        self._win.addstr(8, 5, "Password : ", curses.A_BOLD)
        self._password_t = TextBox(self._win, 8, 17, self._password)
        
        self._win.refresh()
        
        self._username_t.edit()
        self._password_t.edit()

        self.signin()

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
        self.current_profile.username = self._username_t.value()
        self.current_profile.email = self._username_t.value()
        self.current_profile.password = self._password_t.value()
        self._amsn_core.signinToAccount(self, self.current_profile)
        

    def onConnecting(self, progress, message):
        self._username_t = None
        self._password_t = None
        self._win.clear()
        
        self._win.addstr(10, 25, "Connecting...", curses.A_BOLD | curses.A_STANDOUT)
        self._win.refresh()

    def onConnected(self):
        self._username_t = None
        self._password_t = None
        self._win.clear()
        
        self._win.addstr(10, 25, "Connected...", curses.A_BOLD | curses.A_STANDOUT)
        self._win.refresh()

    def onAuthenticating(self):
        self._username_t = None
        self._password_t = None
        self._win.clear()
        
        self._win.addstr(10, 25, "Authenticating...", curses.A_BOLD | curses.A_STANDOUT)
        self._win.refresh()

    def onAuthenticated(self):
        self._username_t = None
        self._password_t = None
        self._win.clear()
        
        self._win.addstr(10, 25, "Authenticated...", curses.A_BOLD | curses.A_STANDOUT)
        self._win.refresh()

    def onSynchronizing(self):
        self._username_t = None
        self._password_t = None
        self._win.clear()
        
        self._win.addstr(10, 25, "Fetching contact list...", curses.A_BOLD | curses.A_STANDOUT)
        self._win.refresh()

    def onSynchronized(self):
        self._username_t = None
        self._password_t = None
        self._win.clear()
        
        self._win.addstr(10, 25, "Synchronized!", curses.A_BOLD | curses.A_STANDOUT)
        self._win.refresh()


