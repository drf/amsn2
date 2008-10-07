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
from fadingwidget import FadingWidget
from amsn2.core.views import MenuView, MenuItemView

class aMSNMainWindow(QMainWindow, base.aMSNMainWindow):
    def __init__(self, amsn_core, parent=None):
        QMainWindow.__init__(self, parent)
        self._amsn_core = amsn_core
        self.centralWidget = QWidget(self)
        self.stackedLayout = QStackedLayout()
        #self.stackedLayout.setStackingMode(QStackedLayout.StackAll)
        self.centralWidget.setLayout(self.stackedLayout)
        self.setCentralWidget(self.centralWidget)
        self.opaqLayer = FadingWidget(Qt.white, self)
        self.stackedLayout.addWidget(self.opaqLayer)
        QObject.connect(self.opaqLayer, SIGNAL("fadeInCompleted()"), self.__activateNewWidget)
        QObject.connect(self.opaqLayer, SIGNAL("fadeOutCompleted()"), self.__fadeIn)
        self.resize(230, 550)
        
    def closeEvent(self, event):
        self._amsn_core.quit()

    def fadeIn(self, widget):
        widget.setAutoFillBackground(True)
        self.stackedLayout.addWidget(widget)
        self.stackedLayout.setCurrentWidget(self.opaqLayer)
        # Is there another widget in here?
        if self.stackedLayout.count() > 2:
            self.opaqLayer.fadeOut() # Fade out current active widget
        else:
            self.__fadeIn()

    def __fadeIn(self):
        # Delete old widget(s)
        while self.stackedLayout.count() > 2:
            widget = self.stackedLayout.widget(1)
            self.stackedLayout.removeWidget(widget)
            widget.deleteLater()
        self.opaqLayer.fadeIn()

    def __activateNewWidget(self):
        self.stackedLayout.setCurrentIndex(self.stackedLayout.count()-1)

    def show(self):
        self.setVisible(True)
        self._amsn_core.mainWindowShown()

    def hide(self):
        self.setVisible(False)

    def setTitle(self, title):
        self.setWindowTitle(title)

    def set_view(self, view):
        print "set_view request"
        
    def setMenu(self, menu):
        mb = QMenuBar()
        
        for item in menu.items:
            if item.type == "cascade":
                menu = mb.addMenu(item.label)
                for subitem in item.items:
                    menu.addAction(subitem.label)
                
        self.setMenuBar(mb)