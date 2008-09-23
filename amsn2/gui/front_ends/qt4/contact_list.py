from amsn2.gui import base

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_contactlist import Ui_ContactList
from styledwidget import StyledWidget
from amsn2.core.views import StringView
from amsn2.gui import base

class aMSNContactListWindow(base.aMSNContactListWindow):
    def __init__(self, amsn_core, parent):
        self._amsn_core = amsn_core
        self._parent = parent
        self._clwidget = aMSNContactListWidget(amsn_core, self)
        self._clwidget.show()

    def show(self):
        self._clwidget.show()
    
    def hide(self):
        self._clwidget.hide()

    def setTitle(self, text):
        self._parent.setTitle(text)

    def setMenu(self, menu):
        self._parent.setMenu(menu)

    def topCLUpdated(self, contactView):
        pass #TODO

    
            
class aMSNContactListWidget(StyledWidget, base.aMSNContactListWidget):
    def __init__(self, amsn_core, parent):
        """ Should we consider switching the contact view to a Model+View
        instead of a QTreeWidget? This can surely give us some advantages... """
        StyledWidget.__init__(self, parent._parent)
        self._amsn_core = amsn_core
        self.ui = Ui_ContactList()
        self.ui.setupUi(self)
        self._parent = parent
        self._mainWindow = parent._parent
        self.ui.cList.clear()

    def show(self):
        self._mainWindow.fadeIn(self)

    def hide(self):
        pass
    
    def groupAdded(self, group):
        groupItem = QTreeWidgetItem(self.ui.cList)
        groupItem.setText(0, group.name.toString())
        for contact in group.contacts:
            contactItem = QTreeWidgetItem(groupItem)
            contactItem.setText(0, contact.name.toString())

    def groupAdded(self, group):
        print group.name.toString()
        groupItem = QTreeWidgetItem(self.ui.cList)
        groupItem.setText(0, QString.fromUtf8(group.name.toString()))
        for contact in group.contacts:
            print "  * " + contact.name.toString()
            contactItem = QTreeWidgetItem(groupItem)
            contactItem.setText(0, QString.fromUtf8(contact.name.toString()))
