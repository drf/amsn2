
from nibs import CocoaLoginView, CocoaLoggingInView
import main

class aMSNLoginWindow(object):
    loginView = None
    loggingInView = None
    
    def __init__(self, amsn_core):
        self._amsn_core = amsn_core
        self.switch_to_profile(None)
        self._mainWin = self._amsn_core.getMainWindow()
        
        # Save the cocoa views that can be loaded in the main window.
        self.loginView = CocoaLoginView.getView()
        self.loggingInView = CocoaLoggingInView.getView()
        
        # Save a call back method for when the cocoa login: message is sent.
        self.loginView.registerLoginCallback(self.login)
        
    def show(self):
        # Load the login view into the main window.
        self._mainWin.setTitle(u'aMSN 2 - Login')
        self._mainWin._loadView(self.loginView)
    
    # Call back method.
    def login(self, username, password):
        self._username = username
        self._password = password
        
        # Load loggingInView into main window (no resize).
        self._mainWin._loadView(self.loggingInView, False)
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
        
    # Set the status message in the login window.
    def onConnecting(self, message):
        self.loggingInView.setStatus(message)

