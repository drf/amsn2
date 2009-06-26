class aMSNLoginWindow(object):
    def __init__(self, amsn_core, main):
        self._main = main
        self._amsn_core = amsn_core
        self.switch_to_profile(None)

    def show(self):
        self._main.send("showLogin",[]);
        self._main.addListener("setUsername",self.setUsername)
        self._main.addListener("setPassword",self.setPassword)
        self._main.addListener("signin",self.signin)

    def hide(self):
        self._main.send("hideLogin",[]);

    def setUsername(self,listU):
        self._username = listU.pop()

    def setPassword(self,listP):
        self._password = listP.pop()

    def switch_to_profile(self, profile):
        self.current_profile = profile
        if self.current_profile is not None:
            self._username = self.current_profile.username
            self._password = self.current_profile.password

    def signin(self,listE):
        self.current_profile.username = self._username
        self.current_profile.email = self._username
        self.current_profile.password = self._password
        self._amsn_core.signinToAccount(self, self.current_profile)

    def onConnecting(self,mess):
        self._main.send("onConnecting",[mess])
