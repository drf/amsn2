from constants import *
import edje
import ecore
import ecore.x
import etk

from amsn2.gui import base

class aMSNLoginWindow(base.aMSNLoginWindow):
    def __init__(self, amsn_core, parent):
        self._amsn_core = amsn_core
        self._evas = parent._evas
        self._parent = parent

        edje.frametime_set(1.0 / 30)

        mainChild = etk.EvasObject()

        try:
            self._edje = edje.Edje(self._evas, file=THEME_FILE,
                                group="login_screen")
        except edje.EdjeLoadError, e:
            raise SystemExit("error loading %s: %s" % (THEME_FILE, e))

        mainChild.evas_object = self._edje

        self.password = etk.Entry()
        embed = etk.Embed(self._evas)
        embed.add(self.password)
        embed.show_all()
        self.password.password_mode = True
        self._edje.part_swallow("login_screen.password", embed.object)

        self.status = etk.Entry()
        embed = etk.Embed(self._evas)
        embed.add(self.status)
        embed.show_all()
        self._edje.part_swallow("login_screen.status", embed.object)

        self.username = etk.Entry()
        embed = etk.Embed(self._evas)
        embed.add(self.username)
        embed.show_all()
        self._edje.part_swallow("login_screen.username", embed.object)

        if self._edje.part_exists("login_screen.signin"):
           self.signin_b = etk.Button()
           embed = etk.Embed(self._evas)
           embed.add(self.signin_b)
           embed.show_all()
           self._edje.part_swallow("login_screen.signin", embed.object)
           self.signin_b.label = "Sign in"
           self.signin_b.connect("clicked", self.__signin_button_cb)
        else:
           self._edje.signal_callback_add("signin", "*", self.__signin_cb)


        # We start with no profile set up, we let the Core set our starting profile
        self.switch_to_profile(None)

        parent.setChild(mainChild)

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
            self.username.text = self.current_profile.username
            self.password.text = self.current_profile.password


    def signin(self):
        # TODO : get/set the username/password and other options from the login screen
        self.current_profile.username = self.username.text
        self.current_profile.email = self.username.text
        self.current_profile.password = self.password.text
        self._amsn_core.signinToAccount(self, self.current_profile)

    def onConnecting(self, message):
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

    def __signin_button_cb(self, button):
        print "clicked %s - %s" % (self, button)
        self.signin()
