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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

from amsn2.gui import base

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from amsn2.core.views import imageview

class Image(QPixmap):
    def __init__(self, theme_manager, view):
        QPixmap.__init__(self)
        self._filename = ""
        self._theme_manager = theme_manager
        self.loader(view)

    def loader(self, view):
        i = 0
        for (resource_type, value) in view.imgs:
            try:
                loadMethod = getattr(self, "_loadFrom%s" % resource_type)
            except AttributeError, e:
                print "From load in qt4/image.py:\n\t(resource_type, value) = (%s, %s)\n\tAttributeError: %s" % (resource_type, value, e)
            else:
                loadMethod(value, view, i)
                i += 1            

    def _loadFromFilename(self, filename, view, index):
        # TODO: Implement support for emblems and other embedded images
        if (index != 0): return

        try:
            self.load(filename)
            self._filename = filename
        except Exception, e:
            print e
            print "Error loading image %s" % filename

    def _loadFromTheme(self, resource_name, view, index):
        # TODO: Implement support for emblems and other embedded images
        if (index != 0): return

        _, filename = self._theme_manager.get_value(resource_name)

        if filename is not None:
            self._loadFromFilename(filename, view, index)
        else:
            print 'Error loading image %s from theme' %resource_name

    def to_size(self, width, height):
        #print 'image.py -> to_pixbuf: filename=%s' % self._filename
        try:
            qpix = self.scaled(width, height)
            return qpix
        except:
            print 'Error converting to qpix image %s' % self._filename
            return None
        
    def _loadFromSkin(self, skin):
        pass

    def _loadFromFileObject(self, obj):
        pass

    def getAsFilename(self):
        return self._filename

    def append(self, resource_name, value):
        """ This method is used to overlap an image on the current image
        Have a look at the documentation of the 'load' method for the meanings of 'resource_name' and 'value'
        """
        if resource_name == "File":
            self.loader(value)

    def prepend(self, resource_name, value):
        """ This method is used to underlap an image under the current image
        Have a look at the documentation of the 'load' method for the meanings of 'resource_name' and 'value'
        """
        if resource_name == "File":
            self.loader(value)