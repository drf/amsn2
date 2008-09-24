from PyQt4.QtGui import *
from PyQt4.QtCore import *

class ContactModel(QStandardItemModel):
    def __init__(self, parent):
        QStandardItemModel.__init__(self, parent)
        
    def test(self):
        self.test = "test"        
