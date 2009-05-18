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
from amsn2.core.views import imageview

class Image(QPixmap):
    def __init__(self):
        QPixmap.__init__(self)

    def load(self, resource_name, value):
        """ This method is used to load an image using the name of a resource and a value for that resource
            resource_name can be :
                - 'File', value is the filename
                - 'Skin', value is the skin key
                - some more :)
        """
        if resource_name == "File":
            self._loadFromFilename(value)

    def loadFromImageView(self, view):
        for (resource_type, value) in view.imgs:
            try:
                loadMethod = getattr(self, "_loadFrom%s" % resource_type)
            except AttributeError, e:
                print "From append in qt4/image.py:\n\t(resource_type, value) = (%s, %s)\n\tAttributeError: %s" % (resource_type, value, e)
            else:
                loadMethod(value)

    def getAsFilename(self):
        return self._fileName

    def append(self, resource_name, value):
        """ This method is used to overlap an image on the current image
            Have a look at the documentation of the 'load' method for the meanings of 'resource_name' and 'value'
        """
        if resource_name == "File":
            self.load(value)

    def prepend(self, resource_name, value):
        """ This method is used to underlap an image under the current image
            Have a look at the documentation of the 'load' method for the meanings of 'resource_name' and 'value'
        """
        if resource_name == "File":
            self.load(value)

    def _loadFromFilename(self, filename):
        QPixmap.load(self, filename)
        self._fileName = filename

    def _loadFromSkin(self, skin):
        pass

    def _loadFromFileObject(self, obj):
        pass


