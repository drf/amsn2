
from amsn2.gui import base
import gtk

class aMSNFileChooserWindow(base.aMSNFileChooserWindow, gtk.FileChooserDialog):
    def __init__(self, filter, directory):
        """
        @type filter: tuple
        @param filter: A tuple containing strings, that will represent the file
        formats to filter.
        @type directory: str
        @param directory: The path to start from.

        This will eventually call the related show() method, so the window is
        displayed when created.
        """
        raise NotImplementedError

class aMSNDPChooser(base.aMSNDPChooser, gtk.Window):
    def __init__(self, default_dps, actions):
        """
        @type default_dps: tuple
        @params default_dps: a tuple containing strings representing the paths of the default dps.
        @type actions: tuple
        @param actions: A tuple containing the options between
        which the user can choose. Every option is a tuple itself, of the form (name, callback),
        where callback is the function that will be called if the option is selected.

        This will eventually call the related show() method, so the window is
        displayed when created.
        """
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        self.child = None
        self.showed = False
        self.set_default_size(550, 450)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_title("aMSN - Choose a Display Picture")
        self.show()

