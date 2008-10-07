# -*- coding: utf-8 -*-
#
# amsn - a python client for the WLM Network
#
# Copyright (C) 2008 Dario Freddi <drf54321@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from amsn2.gui import base

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from contact_model import ContactModel
from contact_item import ContactItem
from ui_contactlist import Ui_ContactList
from styledwidget import StyledWidget
from amsn2.core.views import StringView, ContactView
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
        StyledWidget.__init__(self, parent._parent)
        self._amsn_core = amsn_core
        self.ui = Ui_ContactList()
        self.ui.setupUi(self)
        self._parent = parent
        self._mainWindow = parent._parent
        self._model = QStandardItemModel(self)
        self._proxyModel = QSortFilterProxyModel(self)
        self._proxyModel.setSourceModel(self._model)
        self.ui.cList.setModel(self._proxyModel)
        self._contactDict = dict()
        
        self._proxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self._proxyModel.setFilterKeyColumn(-1)
        
        self.connect(self.ui.searchLine, SIGNAL('textChanged(QString)'),
                     self._proxyModel, SLOT('setFilterFixedString(QString)'))
        QObject.connect(self.ui.nickName, SIGNAL('textChanged(QString)'),
                        self.__slotChangeNick)

    def show(self):
        self._mainWindow.fadeIn(self)

    def hide(self):
        pass
    
    def __slotChangeNick(self):
        sv = StringView()
        sv.appendText(str(self.ui.nickName.text()))
        self._amsn_core._profile.client.changeNick(sv)
    
    def contactUpdated(self, contact):
        print unicode("Contact Updated: " + QString.fromUtf8(contact.name.toString()))
        l = self._model.findItems("*", Qt.MatchWildcard | Qt.MatchRecursive)
        
        for itm in l:
            if itm.data(40).toString() == contact.uid:
                itm.setText(QString.fromUtf8(contact.name.toString()))
                break

    def groupUpdated(self, group):
        print "GroupUpdated"
        l = self._model.findItems("*", Qt.MatchWildcard)
        
        for itm in l:
            
            if itm.data(40).toString() == group.uid:
                
                itm.setText(QString.fromUtf8(group.name.toString()))
            
                for contact in group.contacts:
                    
                    for ent in l:
                        
                        if ent.data(40).toString() == contact.uid:
                            itm.setText(QString.fromUtf8(contact.name.toString()))
                            continue
                        
                    print "  * " + contact.name.toString()
            
                    contactItem = ContactItem()
                    contactItem.setContactName(QString.fromUtf8(contact.name.toString()))
                    contactItem.setData(QVariant(contact.uid), 40)
            
                    itm.appendRow(contactItem)

                break

    def groupRemoved(self, group):
        l = self._model.findItems("", Qt.MatchWildcard)
        
        for itm in l:
            if itm.data(40) == group.uid:
                row = self._model.indexFromItem(itm)
                self._model.takeRow(row)
                break

    def configure(self, option, value):
        pass

    def cget(self, option, value):
        pass

    def size_request_set(self, w,h):
        pass

    def setContactCallback(self, cb):
        self._callback = cb
        if cb is not None:
            self.connect(self.ui.cList, SIGNAL('doubleClicked(QModelIndex)'),
                         self.__slotContactCallback)

    def __slotContactCallback(self, index):
        data = str(index.data(40).toString())
        if self._callback is not None:
            self._callback(self._contactDict[data])

    def setContactContextMenu(self, cb):
        #TODO:
        pass

    def groupAdded(self, group):
        print group.name.toString()
        
        pi = self._model.invisibleRootItem();
        
        # Adding Group Item
        
        groupItem = QStandardItem()
        groupItem.setText(QString.fromUtf8(group.name.toString()))
        groupItem.setData(QVariant(group.uid), 40)
        pi.appendRow(groupItem)
        
        for contact in group.contacts:
            print "  * " + contact.name.toString()
            
            contactItem = ContactItem()
            contactItem.setContactName(QString.fromUtf8(contact.name.toString()))
            contactItem.setData(QVariant(contact.uid), 40)
            contactItem.setData(QVariant(contact), 41)
            
            groupItem.appendRow(contactItem)
            
            self._contactDict[contact.uid] = contact
