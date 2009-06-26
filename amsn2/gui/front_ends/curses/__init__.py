
from amsn2 import gui
import sys

# Here we load the actual front end.
# We need to import the front end module and return it
# so the guimanager can access its classes
def load():
    import curses_
    return curses_

# Initialize the front end by checking for any
# dependency then register it to the guimanager
try:
    import imp

    imp.find_module("curses")
    gui.GUIManager.registerFrontEnd("curses", sys.modules[__name__])

except ImportError:
    pass

