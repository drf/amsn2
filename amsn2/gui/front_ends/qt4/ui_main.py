# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Thu Jun 12 21:01:49 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Main(object):
    def setupUi(self, Main):
        Main.setObjectName("Main")
        Main.resize(QtCore.QSize(QtCore.QRect(0,0,226,502).size()).expandedTo(Main.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(Main)
        self.centralwidget.setGeometry(QtCore.QRect(0,25,226,456))
        self.centralwidget.setObjectName("centralwidget")

        self.vboxlayout = QtGui.QVBoxLayout(self.centralwidget)
        self.vboxlayout.setObjectName("vboxlayout")

        spacerItem = QtGui.QSpacerItem(20,173,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)

        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.vboxlayout.addWidget(self.pushButton)

        spacerItem1 = QtGui.QSpacerItem(20,173,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem1)
        Main.setCentralWidget(self.centralwidget)

        self.statusbar = QtGui.QStatusBar(Main)
        self.statusbar.setGeometry(QtCore.QRect(0,481,226,21))
        self.statusbar.setObjectName("statusbar")
        Main.setStatusBar(self.statusbar)

        self.menuBar = QtGui.QMenuBar(Main)
        self.menuBar.setGeometry(QtCore.QRect(0,0,226,25))
        self.menuBar.setObjectName("menuBar")

        self.menuQt_4_GUI = QtGui.QMenu(self.menuBar)
        self.menuQt_4_GUI.setObjectName("menuQt_4_GUI")
        Main.setMenuBar(self.menuBar)

        self.actionComing_soon = QtGui.QAction(Main)
        self.actionComing_soon.setObjectName("actionComing_soon")
        self.menuQt_4_GUI.addAction(self.actionComing_soon)
        self.menuBar.addAction(self.menuQt_4_GUI.menuAction())

        self.retranslateUi(Main)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),Main.close)
        QtCore.QMetaObject.connectSlotsByName(Main)

    def retranslateUi(self, Main):
        Main.setWindowTitle(QtGui.QApplication.translate("Main", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Main", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Arial\'; font-size:9pt; font-weight:600; font-style:normal;\">\n"
        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Coming soon:</p>\n"
        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:400;\">Qt 4 GUI</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Main", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuQt_4_GUI.setTitle(QtGui.QApplication.translate("Main", "Qt 4 GUI", None, QtGui.QApplication.UnicodeUTF8))
        self.actionComing_soon.setText(QtGui.QApplication.translate("Main", "Coming soon...", None, QtGui.QApplication.UnicodeUTF8))

