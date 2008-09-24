from QtGui import *
from QtCore import *

class ContactDelegate(QItemDelegate):
    def __init__(self, parent):
        QStandardItemModel.__init__(parent)