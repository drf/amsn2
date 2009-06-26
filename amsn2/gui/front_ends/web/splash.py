
class aMSNSplashScreen(object):
    """ This interface will represent the splashscreen of the UI"""
    def __init__(self, amsn_core, parent):
        """Initialize the interface. You should store the reference to the core in here
        as well as a reference to the window where you will show the splash screen
        """
        self._amsn_core=amsn_core
        self._main=parent
        pass

    def show(self):
        """ Draw the splashscreen """
        self._main.send("showSplashScreen",[])
        pass

    def hide(self):
        """ Hide the splashscreen """
        self._main.send("hideSplashScreen",[])
        pass

    def setText(self, text):
        """ Shows a different text inside the splashscreen """
        self._main.send("setTextSplashScreen",[text])
        pass

    def setImage(self, image):
        """ Set the image to show in the splashscreen. This is an ImageView object """
        self._main.send("setImageSplashScreen",["..."])
        pass



