from constants import *
import edje
import ecore
import ecore.x
import elementary

from amsn2.gui import base

class aMSNLoginWindow(base.aMSNLoginWindow):
    def __init__(self, amsn_core, parent):
        self._amsn_core = amsn_core
        self._evas = parent._evas
        self._parent = parent

        edje.frametime_set(1.0 / 30)

        try:
            self._edje = edje.Edje(self._evas, file=THEME_FILE,
                                group="login_screen")
        except edje.EdjeLoadError, e:
            raise SystemExit("error loading %s: %s" % (THEME_FILE, e))

        self._parent.resize_object_add(self._edje)
        self._edje.size_hint_weight_set(1.0, 1.0)
        self.show()

        self.password = elementary.Entry(self._edje)
        self.password.single_line_set(1)
        self.password.password_set(1)
        self.password.size_hint_weight_set(1.0, 1.0)
        self.password.show()
        self._edje.part_swallow("login_screen.password", self.password)
        self.password.show()

        #TODO: login_screen.status

        self.username = elementary.Entry(self._edje)
        self.username.single_line_set(1)
        self.username.show()
        self._edje.part_swallow("login_screen.username", self.username)

        if self._edje.part_exists("login_screen.signin"):
           self.signin_b = elementary.Button(self._edje)
           self.signin_b.label_set("Sign in")
           self.signin_b.clicked = self.__signin_button_cb
           self.signin_b.show()
           self._edje.part_swallow("login_screen.signin", self.signin_b)
        else:
           self._edje.signal_callback_add("signin", "*", self.__signin_cb)


        # We start with no profile set up, we let the Core set our starting profile
        self.switch_to_profile(None)


    def show(self):
        self._edje.show()

    def hide(self):
        self._edje.hide()
        #FIXME: those are not hidden by self._edje.hide()
        self.password.hide()
        self.status.hide()
        self.username.hide()
        try:
            getattr(self, "signin_b")
        except AttributeError:
            pass
        else:
            self.signin_b.hide()

    def switch_to_profile(self, profile):
        self.current_profile = profile
        if self.current_profile is not None:
            if self.current_profile.username is None:
                self.username.entry_set("")
            else:
                self.username.entry_set(self.current_profile.username)
            if self.current_profile.password is None:
                self.password.entry_set("")
            else:
                self.password.entry_set(self.current_profile.password)


    def signin(self):
        self.current_profile.username = elementary.Entry.markup_to_utf8(self.username.entry_get())
        self.current_profile.email = self.current_profile.username
        self.current_profile.password = elementary.Entry.markup_to_utf8(self.password.entry_get())
        self._amsn_core.signinToAccount(self, self.current_profile)

    def onConnecting(self, progress, message):
        self._edje.signal_emit("connecting", "")
        msg1 = ""
        msg2 = ""
        try:
            msg1 = message.split("\n")[0]
        except IndexError:
            pass

        try:
            msg2 = message.split("\n")[1]
        except IndexError:
            pass
        self._edje.part_text_set("connection_status", msg1)
        self._edje.part_text_set("connection_status2", msg2)


    def __signin_cb(self, edje_obj, signal, source):
        self.signin()

    def __signin_button_cb(self, button, event, data):
        self.signin()
