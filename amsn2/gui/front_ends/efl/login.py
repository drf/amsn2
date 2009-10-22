from constants import *
import edje
import ecore
import ecore.x
import elementary

from amsn2.gui import base
from amsn2.core.views import accountview

#TODO: del
#TODO: switch to elm_layout?
class aMSNLoginWindow(base.aMSNLoginWindow):
    def __init__(self, amsn_core, parent):
        self._core = amsn_core
        self._evas = parent._evas
        self._parent = parent
        self._account_views = []

        edje.frametime_set(1.0 / 30)

        try:
            self._edje = edje.Edje(self._evas, file=THEME_FILE,
                                group="login_screen")
        except edje.EdjeLoadError, e:
            raise SystemExit("error loading %s: %s" % (THEME_FILE, e))

        self._parent.resize_object_add(self._edje)
        self._edje.size_hint_weight_set(1.0, 1.0)
        self.show()

        sc = elementary.Scroller(self._edje)
        sc.content_min_limit(0, 1)
        sc.policy_set(elementary.ELM_SCROLLER_POLICY_OFF,
                      elementary.ELM_SCROLLER_POLICY_OFF);
        sc.size_hint_weight_set(1.0, 0.0)
        sc.size_hint_align_set(-1.0, -1.0)
        self._edje.part_swallow("login_screen.username", sc)
        self.username = elementary.Entry(self._edje)
        self.username.single_line_set(1)
        self.username.size_hint_weight_set(1.0, 0.0)
        self.username.size_hint_align_set(-1.0, -1.0)
        sc.content_set(self.username)
        self.username.show()
        sc.show()

        sc = elementary.Scroller(self._edje)
        sc.content_min_limit(0, 1)
        sc.policy_set(elementary.ELM_SCROLLER_POLICY_OFF,
                      elementary.ELM_SCROLLER_POLICY_OFF);
        sc.size_hint_weight_set(1.0, 0.0)
        sc.size_hint_align_set(-1.0, -1.0)
        self._edje.part_swallow("login_screen.password", sc)
        self.password = elementary.Entry(self._edje)
        self.password.single_line_set(1)
        self.password.password_set(1)
        self.password.size_hint_weight_set(1.0, 1.0)
        self.password.size_hint_align_set(-1.0, -1.0)
        sc.content_set(self.password)
        self.password.show()
        sc.show()

        self.presence = elementary.Hoversel(self._edje)
        self.presence.hover_parent_set(self._parent)
        for key in self._core.p2s:
            name = self._core.p2s[key]
            _, path = self._core._theme_manager.get_statusicon("buddy_%s" % name)
            if name == 'offline': continue
            def cb(data, hoversel, it):
                hoversel.label_set(it.label_get())
                (icon_file, icon_group, icon_type) = it.icon_get()
                ic = elementary.Icon(hoversel)
                ic.scale_set(0, 1)
                if icon_type == elementary.ELM_ICON_FILE:
                    ic.file_set(icon_file, icon_group)
                else:
                    ic.standart_set(icon_file)
                hoversel.icon_set(ic)
                ic.show()
                self.presence_key = data

            self.presence.item_add(name, path, elementary.ELM_ICON_FILE, cb,
                                   key)

        self.presence_key = self._core.Presence.ONLINE
        self.presence.label_set(self._core.p2s[self.presence_key])
        ic = elementary.Icon(self.presence)
        ic.scale_set(0, 1)
        _, path = self._core._theme_manager.get_statusicon("buddy_%s" %
                            self._core.p2s[self.presence_key])
        ic.file_set(path)
        self.presence.icon_set(ic)
        ic.show()
        self.presence.size_hint_weight_set(0.0, 0.0)
        self.presence.size_hint_align_set(0.5, 0.5)
        self._edje.part_swallow("login_screen.presence", self.presence)
        self.presence.show()

        self.save = elementary.Check(self._edje)
        self.save.label_set("Remember Me")
        def cb(obj, event_info, data):
            if obj.state_get():
                self.save_password.disabled_set(False)
            else:
                self.save_password.disabled_set(True)
                self.save_password.state_set(False)
                self.autologin.disabled_set(True)
                self.autologin.state_set(False)
        self.save._callback_add("changed", cb)
        self._edje.part_swallow("login_screen.remember_me", self.save)
        self.save.show()

        self.save_password = elementary.Check(self._edje)
        self.save_password.label_set("Remember Password")
        self.save_password.disabled_set(True)
        def cb(obj, event_info, data):
            if obj.state_get():
                self.autologin.disabled_set(False)
            else:
                self.autologin.disabled_set(True)
                self.autologin.state_set(False)
        self.save_password._callback_add("changed", cb)
        self._edje.part_swallow("login_screen.remember_password",
                                self.save_password)
        self.save_password.show()

        self.autologin = elementary.Check(self._edje)
        self.autologin.label_set("Auto Login")
        self.autologin.disabled_set(True)
        self._edje.part_swallow("login_screen.auto_login", self.autologin)
        self.autologin.show()

        if self._edje.part_exists("login_screen.signin"):
           self.signin_b = elementary.Button(self._edje)
           self.signin_b.label_set("Sign in")
           self.signin_b.clicked = self.__signin_button_cb
           self.signin_b.show()
           self._edje.part_swallow("login_screen.signin", self.signin_b)
        else:
           self._edje.signal_callback_add("signin", "*", self.__signin_cb)


    def show(self):
        self._parent.resize_object_add(self._edje)
        self._edje.show()

    def hide(self):
        self._parent.resize_object_del(self._edje)
        self._edje.hide()
        #FIXME: those are not hidden by self._edje.hide()
        self.password.hide()
        self.username.hide()
        try:
            getattr(self, "signin_b")
        except AttributeError:
            pass
        else:
            self.signin_b.hide()


    def setAccounts(self, accountviews):
        #TODO: support more than just 1 account...
        self._account_views = accountviews
        if accountviews:
            #Only select the first one
            acc = accountviews[0]
            self.username.entry_set(acc.email)
            self.password.entry_set(acc.password)

            self.presence_key = acc.presence
            self.presence.label_set(self._core.p2s[self.presence_key])
            ic = elementary.Icon(self.presence)
            ic.scale_set(0, 1)
            _, path = self._core._theme_manager.get_statusicon("buddy_%s" %
                                self._core.p2s[self.presence_key])
            ic.file_set(path)
            self.presence.icon_set(ic)
            ic.show()

            self.save.state_set(acc.save)
            if acc.save:
                self.save_password.disabled_set(False)
            else:
                self.save_password.disabled_set(True)
            self.save_password.state_set(acc.save_password)
            if acc.save_password:
                self.autologin.disabled_set(False)
            else:
                self.autologin.disabled_set(True)
            self.autologin.state_set(acc.autologin)


    def signin(self):
        email = elementary.Entry.markup_to_utf8(self.username.entry_get()).strip()
        password = elementary.Entry.markup_to_utf8(self.password.entry_get()).strip()

        accv = [accv for accv in self._account_views if accv.email == email]
        if not accv:
            accv = AccountView()
            accv.email = email
        else:
            accv = accv[0]
        accv.password = password

        accv.presence = self.presence_key

        accv.save = self.save.state_get()
        accv.save_password = self.save_password.state_get()
        accv.autologin = self.autologin.state_get()

        self._core.signinToAccount(self, accv)

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

    def __signin_button_cb(self, button, event, *args, **kargs):
        self.signin()
