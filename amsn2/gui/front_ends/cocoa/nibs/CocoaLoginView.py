
import os
from objc import *
from Foundation import *
from AppKit import *

loginView = None
def getView():
    global loginView
    return loginView

# This is a view that we can load into the main window.
class aMSNCocoaLoginView(NSView):
    loginCallback = None
    
    loginButton =       IBOutlet('loginButton')         # loginButton fires the login: action.
    usernameField =     IBOutlet('usernameField')       # Text field with user/profile name.
    usernameLabel =     IBOutlet('usernameLabel')       # Text label next to usernameField.
    passwordField =     IBOutlet('passwordField')       # Secure text field with password.
    passwordLabel =     IBOutlet('passwordLabel')       # Text label next to passwordField.
    rememberMe =        IBOutlet('rememberMe')          # Check box for save profile.
    rememberPassword =  IBOutlet('rememberPassword')    # Check box for save password.
    
    def awakeFromNib(self):
        global loginView
        loginView = self
    
    def login_(self):
        username = str(self.usernameField.stringValue())
        password = str(self.passwordField.stringValue())
        self.loginCallback(username, password)
    
    def registerLoginCallback(self, function):
        self.loginCallback = function

NSBundle.loadNibNamed_owner_('aMSNCocoaLoginView', NSApplication.sharedApplication())
