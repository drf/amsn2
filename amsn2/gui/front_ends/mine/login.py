
class aMSNLoginWindow(object):
    def __init__(self, amsn_core, main):
        self._amsn_core = amsn_core
        self.switch_to_profile(None)

    def show(self):
        if self._username is not None and self._username != "":
            print "Account : %s" % (self._username)
        else:
            self._username = raw_input("Account : ")

        if self._password is not None and self._password != "":
            print "Password : ******"
        else:
            import getpass
            self._password = getpass.getpass('Password: ')

        self.signin()

    def hide(self):
        pass

    def switch_to_profile(self, profile):
        self.current_profile = profile
        if self.current_profile is not None:
            self._username = self.current_profile.username
            self._password = self.current_profile.password

    def signin(self):
        self.current_profile.username = self._username
        self.current_profile.email = self._username
        self.current_profile.password = self._password
        self._amsn_core.signinToAccount(self, self.current_profile)


    def onConnecting(self,mess):
        print mess

    def onConnected(self,mess):
        print mess

    def onAuthenticating(self,mess):
        print mess

    def onAuthenticated(self,mess):
        print mess

    def onSynchronizing(self,mess):
        print mess

    def onSynchronized(self,mess):
        print mess

