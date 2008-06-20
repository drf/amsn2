from amsn2 import gui
import sys

# Here we load the actual front end.
# We need to import the front end module and return it
# so the guimanager can access its classes
def load():
    try:
        import qt4
        return qt4
    except ImportError:
        return None

# Initialize the front end by checking for any
# dependency then register it to the guimanager
try:
    import imp
    imp.find_module("PyQt4")
    
    gui.GUIManager.registerFrontEnd("qt4", sys.modules[__name__])
except ImportError:
    pass
