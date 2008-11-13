
from nibs import CocoaLoginView, CocoaLoggingInView
import main

class aMSNLoginWindow(object):
    loginView = None
    loggingInView = None
    
    def __init__(self, amsn_core, parent):
        self.amsn_core = amsn_core
        self.parent = parent
        
        self.switch_to_profile(None)
        
        # Save the cocoa views that can be loaded in the main window.
        self.loginView = CocoaLoginView.getView()
        self.loggingInView = CocoaLoggingInView.getView()
        
        # Save a call back method for when the cocoa login: message is sent.
        self.loginView.setParent(self)
        self.loggingInView.setParent(self)
        
    def show(self):
        # Load the login view into the main window.
        self.parent._loadView(self.loginView)
    
    # Call back method.
    def login(self, username, password):
        self._username = username
        self._password = password
        
        # Load loggingInView into main window.
        self.parent._loadView(self.loggingInView)
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
        self.amsn_core.signinToAccount(self, self.current_profile)
        
    # Set the status message in the login window.
    def onConnecting(self, pcent_pg, message):
        self.loggingInView.setStatus(message)

