from constants import *
import edje
import ecore
import ecore.x
import etk

from amsn2.gui import base

class aMSNLoginWindow(base.aMSNLoginWindow):
    def __init__(self, amsn_core):
        self._amsn_core = amsn_core
        self._amsn_gui = self._amsn_core.getMainWindow()
        self._evas = self._amsn_gui._evas

        edje.frametime_set(1.0 / 30)
        try:
            self._edje = edje.Edje(self._evas.evas, file=THEME_FILE,
                                group="login_screen")
        except edje.EdjeLoadError, e:
            raise SystemExit("error loading %s: %s" % (THEME_FILE, e))

        self._edje.size = self._evas.size
        self._evas.data["login_window"] = self._edje
        
        self._edje.on_key_down_add(self.__on_key_down)

        self.password = etk.Entry()
        embed = etk.Embed(self._evas.evas)
        embed.add(self.password)
        embed.show_all()
        self.password.password_mode = True
        self._edje.part_swallow("login_screen.password", embed.object)

        self.status = etk.Entry()
        embed = etk.Embed(self._evas.evas)
        embed.add(self.status)
        embed.show_all()
        self._edje.part_swallow("login_screen.status", embed.object)

        self.username = etk.Entry()
        embed = etk.Embed(self._evas.evas)
        embed.add(self.username)
        embed.show_all()
        self._edje.part_swallow("login_screen.username", embed.object)
        
        if self._edje.part_exists("login_screen.signin"):
           self.signin_b = etk.Button()
           embed = etk.Embed(self._evas.evas)
           embed.add(self.signin_b)
           embed.show_all()
           self._edje.part_swallow("login_screen.signin", embed.object)
           self.signin_b.label = "Sign in"
           self.signin_b.connect("clicked", self.__signin_button_cb)
        else:
           self._edje.signal_callback_add("signin", "*", self.__signin_cb)

        self._edje.focus = True

        # We start with no profile set up, we let the Core set our starting profile
        self.switch_to_profile(None)

    def show(self):
        self._edje.show()
    
    def hide(self):
        self._edje.hide()

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

    def onConnecting(self):
        self._edje.signal_emit("connecting", "")
        self._edje.part_text_set("connection_status", "Connecting to server...")

    def onConnected(self):
        self._edje.signal_emit("connecting", "")
        self._edje.part_text_set("connection_status", "Connected...")
        self._edje.part_text_set("connection_status2", "")

    def onAuthenticating(self):
        self._edje.signal_emit("connecting", "")
        self._edje.part_text_set("connection_status", "Authenticating...")
        self._edje.part_text_set("connection_status2", "")

    def onAuthenticated(self):
        self._edje.signal_emit("connecting", "")
        self._edje.part_text_set("connection_status", "Password accepted...")
        self._edje.part_text_set("connection_status2", "")

    def onSynchronizing(self):
        self._edje.signal_emit("connecting", "")
        self._edje.part_text_set("connection_status", "Please wait while your contact list")
        self._edje.part_text_set("connection_status2", "is being downloaded...")

    def onSynchronized(self):
        self._edje.signal_emit("connecting", "")
        self._edje.part_text_set("connection_status", "Contact list downloaded successfully")
        self._edje.part_text_set("connection_status2", "Happy Chatting")

    # Private methods
    def __on_key_down(self, obj, event):
        if event.keyname in ("F6", "f"):
            self._evas.fullscreen = not self._evas.fullscreen
        elif event.keyname == "b":
            self._evas.borderless = not self._evas.borderless
        elif event.keyname == "Escape":
            self._amsn_core.quit()

    def __signin_cb(self, edje_obj, signal, source):
        self.signin()

    def __signin_button_cb(self, button):
        print "clicked %s - %s" % (self, button)
        self.signin()
