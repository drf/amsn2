
from amsn2 import gui
import sys

# Here we load the actual front end.
# We need to import the front end module and return it
# so the guimanager can access its classes
def load():
    try:
        import efl
        return efl
    except ImportError:
        return None


# Initialize the front end by checking for any
# dependency then register it to the guimanager
try:
    import imp
    imp.find_module("evas")
    imp.find_module("edje")
    imp.find_module("ecore")
    imp.find_module("etk")

    gui.GUIManager.registerFrontEnd("efl", sys.modules[__name__])
    
except ImportError:
    pass
        
