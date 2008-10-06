# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'contactlist.ui'
#
# Created: Mon Oct  6 02:07:09 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ContactList(object):
    def setupUi(self, ContactList):
        ContactList.setObjectName("ContactList")
        ContactList.resize(206, 429)
        ContactList.setStyleSheet("#ContactList { background-color: white; }")
        self.verticalLayout = QtGui.QVBoxLayout(ContactList)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(0, 3, 0, 3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pixUser = QtGui.QLabel(ContactList)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pixUser.sizePolicy().hasHeightForWidth())
        self.pixUser.setSizePolicy(sizePolicy)
        self.pixUser.setMinimumSize(QtCore.QSize(100, 100))
        self.pixUser.setStyleSheet("""#pixUser {
color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(175, 175, 175, 255));
font-weight: bold;
font-size: 20px;
border: 3px solid gray;
border-radius: 10px;
background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(80, 92, 115, 255), stop:1 rgba(0, 0, 0, 255));
}
#pixUser:hover {
background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(80, 92, 115, 255));
}""")
        self.pixUser.setAlignment(QtCore.Qt.AlignCenter)
        self.pixUser.setObjectName("pixUser")
        self.horizontalLayout.addWidget(self.pixUser)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.nickName = QtGui.QLabel(ContactList)
        self.nickName.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextEditable|QtCore.Qt.TextEditorInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.nickName.setObjectName("nickName")
        self.verticalLayout.addWidget(self.nickName)
        self.statusMessage = QtGui.QLabel(ContactList)
        self.statusMessage.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextEditable|QtCore.Qt.TextEditorInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.statusMessage.setObjectName("statusMessage")
        self.verticalLayout.addWidget(self.statusMessage)
        self.label = QtGui.QLabel(ContactList)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.searchLine = QtGui.QLineEdit(ContactList)
        self.searchLine.setObjectName("searchLine")
        self.verticalLayout.addWidget(self.searchLine)
        self.cList = QtGui.QTreeView(ContactList)
        self.cList.setStyleSheet("""         QTreeView {
             show-decoration-selected: 1;
             background-color: white;
             border: none;
         }



         QTreeView::item:hover {
             background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1);
         }


         QTreeView::item:selected:active{
             background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6ea1f1, stop: 1 #567dbc);
         }

         QTreeView::item:selected:!active {
             background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6b9be8, stop: 1 #577fbf);
         }
""")
        self.cList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.cList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.cList.setSortingEnabled(True)
        self.cList.setAnimated(True)
        self.cList.setHeaderHidden(True)
        self.cList.setObjectName("cList")
        self.verticalLayout.addWidget(self.cList)

        self.retranslateUi(ContactList)
        QtCore.QMetaObject.connectSlotsByName(ContactList)

    def retranslateUi(self, ContactList):
        ContactList.setWindowTitle(QtGui.QApplication.translate("ContactList", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.pixUser.setText(QtGui.QApplication.translate("ContactList", "aMSN", None, QtGui.QApplication.UnicodeUTF8))
        self.nickName.setText(QtGui.QApplication.translate("ContactList", "Nick here", None, QtGui.QApplication.UnicodeUTF8))
        self.statusMessage.setText(QtGui.QApplication.translate("ContactList", "Status message here", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ContactList", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Welcome!</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This is just a test!</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

