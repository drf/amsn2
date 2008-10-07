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
    
class aMSNSplashScreen(QSplashScreen, base.aMSNSplashScreen):

    def __init__(self, amsn_core, parent):
        QSplashScreen.__init__(self, parent)

    def show(self):
        self.setVisible(True)
        qApp.processEvents()
    
    def hide(self):
        self.setVisible(False)
        qApp.processEvents()
    
    def setText(self, text):
        self.showMessage(text)
        qApp.processEvents()
        
    def setImage(self, image):
        self.setPixmap(image)
        qApp.processEvents()
