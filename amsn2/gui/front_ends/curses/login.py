import curses
import curses.textpad


class TextBox(object):
    def __init__(self, win, y, x, txt):
        self._win = win.derwin(1, 30, y, x)
        self._win.bkgd(' ', curses.color_pair(0))
        self._win.clear()
        self._txtbox = curses.textpad.Textbox(self._win)
        self._txtbox.stripspaces = True

        if txt is not None:
            self._insert(txt)

    def edit(self):
        return self._txtbox.edit()

    def value(self):
        return self._txtbox.gather()

    def _insert(self, txt):
        for ch in txt:
            self._txtbox.do_command(ch)

class PasswordBox(TextBox):
    def __init__(self, win, y, x, txt):
        super(PasswordBox, self).__init__(win, y, x, txt)
        self._password = ''

    def edit(self, cb=None):
        return self._txtbox.edit(self._validateInput)

    def value(self):
        return self._password

    def _validateInput(self, ch):
        if ch in (curses.KEY_BACKSPACE, curses.ascii.BS):
            self._password = self._password[0:-1]
            return ch
        elif curses.ascii.isprint(ch):
            self._password += chr(ch)
            return '*'
        else:
            return ch

    def _insert(self, str):
        for ch in str:
            self._password += ch
            self._txtbox.do_command('*')
    
class aMSNLoginWindow(object):
    def __init__(self, amsn_core, parent):
        self._amsn_core = amsn_core
        self.switch_to_profile(None)
        self._stdscr = parent._stdscr

        (y, x) = self._stdscr.getmaxyx()
        wy = int(y * 0.8)
        wx = int(x * 0.8)
        sy = int((y - wy)/2)
        sx = int((x - wx)/2)
        self._win = curses.newwin(wy, wx, sy, sx)
        
    def show(self):
        self._win.border()
        self._win.bkgd(' ', curses.color_pair(1))
        self._win.addstr(5, 5, "Account : ", curses.A_BOLD)
        self._username_t = TextBox(self._win, 5, 17, self._username)

        self._win.addstr(8, 5, "Password : ", curses.A_BOLD)
        self._password_t = PasswordBox(self._win, 8, 17, self._password)
        
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
        
        self._win.addstr(10, 25, message, curses.A_BOLD | curses.A_STANDOUT)
        self._win.refresh()
