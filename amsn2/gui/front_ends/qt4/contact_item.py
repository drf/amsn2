from PyQt4.QtGui import *
from PyQt4.QtCore import *

class ContactItem(QStandardItem):
    def __init__(self):
        QStandardItem.__init__(self)
        
    def setContactName(self, name):
        self.setText(name)