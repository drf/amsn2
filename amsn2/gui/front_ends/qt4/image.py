from amsn2.gui import base

from PyQt4.QtCore import *
from PyQt4.QtGui import *
    
class Image(QPixmap, base.Image):
    def __init__(self, amsn_core, parent):
        QPixmap.__init__(self)
        self.core = amsn_core

    def load(self, resource_name, value):
        """ This method is used to load an image using the name of a resource and a value for that resource
            resource_name can be :
                - 'File', value is the filename
                - 'Skin', value is the skin key
                - some more :)
        """
        if resource_name == "File":
            QPixmap.load(self, value)

    def append(self, resource_name, value):
        """ This method is used to overlap an image on the current image
            Have a look at the documentation of the 'load' method for the meanings of 'resource_name' and 'value'
        """
        if resource_name == "File":
            self.load(value)

    def prepend(self, resource_name, value):
        """ This method is used to underlap an image under the current image
            Have a look at the documentation of the 'load' method for the meanings of 'resource_name' and 'value'
        """
        if resource_name == "File":
            self.load(value)
            
