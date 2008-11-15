# This is a template that has all the basic functions to make a succesfull login.

from amsn2 import gui
import sys

# Here we load the actual front end.
# We need to import the front end module and return it
# so the guimanager can access its classes
def load():
    import mine
    return mine

# Initialize the front end by checking for any
# dependency then register it to the guimanager
try:
    import imp
    gui.GUIManager.registerFrontEnd("mine", sys.modules[__name__])
    
except ImportError:
    pass
        
