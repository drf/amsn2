# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chatWindow.ui'
#
# Created: Mon Jun 16 01:58:34 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ChatWindow(object):
    def setupUi(self, ChatWindow):
        ChatWindow.setObjectName("ChatWindow")
        ChatWindow.resize(QtCore.QSize(QtCore.QRect(0,0,559,445).size()).expandedTo(ChatWindow.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(ChatWindow)
        self.vboxlayout.setObjectName("vboxlayout")

        self.splitter_2 = QtGui.QSplitter(ChatWindow)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")

        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")

        self.textEdit = QtGui.QTextEdit(self.splitter)
        self.textEdit.setObjectName("textEdit")

        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.layoutWidget)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.vboxlayout1.addWidget(self.label)

        spacerItem = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout1.addItem(spacerItem)

        self.widget = QtGui.QWidget(self.splitter_2)
        self.widget.setObjectName("widget")

        self.vboxlayout2 = QtGui.QVBoxLayout(self.widget)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.toolBar = QtGui.QToolBar(self.widget)
        self.toolBar.setMinimumSize(QtCore.QSize(0,32))
        self.toolBar.setMaximumSize(QtCore.QSize(16777215,32))
        self.toolBar.setSizeIncrement(QtCore.QSize(0,32))
        self.toolBar.setBaseSize(QtCore.QSize(0,32))
        self.toolBar.setAcceptDrops(True)
        self.toolBar.setMovable(False)
        self.toolBar.setObjectName("toolBar")
        self.vboxlayout2.addWidget(self.toolBar)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.inputWidget = QtGui.QTextEdit(self.widget)
        self.inputWidget.setEnabled(True)
        self.inputWidget.setMinimumSize(QtCore.QSize(0,0))
        self.inputWidget.setBaseSize(QtCore.QSize(0,40))
        self.inputWidget.setObjectName("inputWidget")
        self.hboxlayout.addWidget(self.inputWidget)

        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.hboxlayout.addWidget(self.label_2)
        self.vboxlayout2.addLayout(self.hboxlayout)
        self.vboxlayout.addWidget(self.splitter_2)

        self.actionInsert_Emoticon = QtGui.QAction(ChatWindow)
        self.actionInsert_Emoticon.setObjectName("actionInsert_Emoticon")

        self.actionNudge = QtGui.QAction(ChatWindow)
        self.actionNudge.setObjectName("actionNudge")
        self.toolBar.addAction(self.actionInsert_Emoticon)
        self.toolBar.addAction(self.actionNudge)

        self.retranslateUi(ChatWindow)
        QtCore.QMetaObject.connectSlotsByName(ChatWindow)

    def retranslateUi(self, ChatWindow):
        ChatWindow.setWindowTitle(QtGui.QApplication.translate("ChatWindow", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ChatWindow", "Something here...", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("ChatWindow", "Quick Actions", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ChatWindow", "Contact image", None, QtGui.QApplication.UnicodeUTF8))
        self.actionInsert_Emoticon.setText(QtGui.QApplication.translate("ChatWindow", "Insert Emoticon", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNudge.setText(QtGui.QApplication.translate("ChatWindow", "Nudge", None, QtGui.QApplication.UnicodeUTF8))

