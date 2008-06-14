# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'contactlist.ui'
#
# Created: Sat Jun 14 19:47:17 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ContactList(object):
    def setupUi(self, ContactList):
        ContactList.setObjectName("ContactList")
        ContactList.resize(206,421)
        self.verticalLayout = QtGui.QVBoxLayout(ContactList)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(ContactList)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.list = QtGui.QTreeWidget(ContactList)
        self.list.setStyleSheet("""         QTreeView {
             show-decoration-selected: 1;
         }

         QTreeView::item {
             border: 1px solid #d9d9d9;
             border-top-color: transparent;
             border-bottom-color: transparent;
         }

         QTreeView::item:hover {
             background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1);
             border: 1px solid #bfcde4;
         }

         QTreeView::item:selected {
             border: 1px solid #567dbc;
         }

         QTreeView::item:selected:active{
             background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6ea1f1, stop: 1 #567dbc);
         }

         QTreeView::item:selected:!active {
             background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6b9be8, stop: 1 #577fbf);
         }
         QTreeView::branch {
                 background: palette(base);
         }

         QTreeView::branch:has-siblings:!adjoins-item {
                 background: cyan;
         }

         QTreeView::branch:has-siblings:adjoins-item {
                 background: red;
         }

         QTreeView::branch:!has-children:!has-siblings:adjoins-item {
                 background: blue;
         }

         QTreeView::branch:closed:has-children:has-siblings {
                 background: pink;
         }

         QTreeView::branch:has-children:!has-siblings:closed {
                 background: gray;
         }

         QTreeView::branch:open:has-children:has-siblings {
                 image: downarrow-icon;
         }

         QTreeView::branch:open:has-children:!has-siblings {
                 image: downarrow-icon;
         }
         QTreeView::branch:has-siblings:!adjoins-item {
             border-image: url(vline.png) 0;
         }

         QTreeView::branch:has-siblings:adjoins-item {
             border-image: url(branch-more.png) 0;
         }

         QTreeView::branch:!has-children:!has-siblings:adjoins-item {
             border-image: url(branch-end.png) 0;
         }

         QTreeView::branch:has-children:!has-siblings:closed,
         QTreeView::branch:closed:has-children:has-siblings {
                 border-image: none;
                 image: downarrow-icon;
         }

         QTreeView::branch:open:has-children:!has-siblings,
         QTreeView::branch:open:has-children:has-siblings  {
                 border-image: none;
                 image: downarrow-icon;
         }""")
        self.list.setSortingEnabled(True)
        self.list.setAnimated(True)
        self.list.setHeaderHidden(True)
        self.list.setObjectName("list")
        self.verticalLayout.addWidget(self.list)

        self.retranslateUi(ContactList)
        QtCore.QMetaObject.connectSlotsByName(ContactList)

    def retranslateUi(self, ContactList):
        ContactList.setWindowTitle(QtGui.QApplication.translate("ContactList", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ContactList", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Welcome!</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This is just a test!</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.list.headerItem().setText(0,QtGui.QApplication.translate("ContactList", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.list.clear()
        item = QtGui.QTreeWidgetItem(self.list)
        item.setText(0,QtGui.QApplication.translate("ContactList", "Group 4", None, QtGui.QApplication.UnicodeUTF8))
        item1 = QtGui.QTreeWidgetItem(item)
        item1.setText(0,QtGui.QApplication.translate("ContactList", "User 5", None, QtGui.QApplication.UnicodeUTF8))
        item2 = QtGui.QTreeWidgetItem(item)
        item2.setText(0,QtGui.QApplication.translate("ContactList", "User 4", None, QtGui.QApplication.UnicodeUTF8))
        item3 = QtGui.QTreeWidgetItem(item)
        item3.setText(0,QtGui.QApplication.translate("ContactList", "User 3", None, QtGui.QApplication.UnicodeUTF8))
        item4 = QtGui.QTreeWidgetItem(item)
        item4.setText(0,QtGui.QApplication.translate("ContactList", "User 2", None, QtGui.QApplication.UnicodeUTF8))
        item5 = QtGui.QTreeWidgetItem(item)
        item5.setText(0,QtGui.QApplication.translate("ContactList", "User 1", None, QtGui.QApplication.UnicodeUTF8))
        item6 = QtGui.QTreeWidgetItem(self.list)
        item6.setText(0,QtGui.QApplication.translate("ContactList", "Group 3", None, QtGui.QApplication.UnicodeUTF8))
        item7 = QtGui.QTreeWidgetItem(self.list)
        item7.setText(0,QtGui.QApplication.translate("ContactList", "Group 2", None, QtGui.QApplication.UnicodeUTF8))
        item8 = QtGui.QTreeWidgetItem(item7)
        item8.setText(0,QtGui.QApplication.translate("ContactList", "User 2", None, QtGui.QApplication.UnicodeUTF8))
        item9 = QtGui.QTreeWidgetItem(item7)
        item9.setText(0,QtGui.QApplication.translate("ContactList", "User 1", None, QtGui.QApplication.UnicodeUTF8))
        item10 = QtGui.QTreeWidgetItem(self.list)
        item10.setText(0,QtGui.QApplication.translate("ContactList", "Group 1", None, QtGui.QApplication.UnicodeUTF8))
        item11 = QtGui.QTreeWidgetItem(item10)
        item11.setText(0,QtGui.QApplication.translate("ContactList", "User 1", None, QtGui.QApplication.UnicodeUTF8))

