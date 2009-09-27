# -*- coding: utf-8 -*-
#===================================================
#
# image.py - This file is part of the amsn2 package
#
# Copyright (C) 2008  Wil Alvarez <wil_alejandro@yahoo.com>
#
# This script is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# This script is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License along with
# this script (see COPYING); if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#===================================================

import gtk
from amsn2.gui import base
from amsn2.core.views import imageview
import logging

logger = logging.getLogger("amsn2.gtk.image")

class Image(gtk.Image):
    def __init__(self, theme_manager, view):
        gtk.Image.__init__(self)
        self._theme_manager = theme_manager
        self._filename = None
        self.load(view)

    def load(self, view):
        i = 0
        for (resource_type, value) in view.imgs:
            try:
                loadMethod = getattr(self, "_loadFrom%s" % resource_type)
            except AttributeError, e:
                logger.error("Unable to find the method to load %s image from %s" % (value, resource_type))
            else:
                loadMethod(value, view, i)
                i += 1

    def _loadFromFilename(self, filename, view, index):
        # TODO: Implement support for emblems and other embedded images
        if (index != 0): return

        try:
            self.set_from_file(filename)
            self._filename = filename
        except Exception, e:
            logger.error("Error loading image %s" % filename)

    def _loadFromTheme(self, resource_name, view, index):
        # TODO: Implement support for emblems and other embedded images
        if (index != 0): return

        _, filename = self._theme_manager.get_value(resource_name)

        if filename is not None:
            self._loadFromFilename(filename, view, index)
        else:
            logger.error('Error loading image %s from theme' %resource_name)

    def to_pixbuf(self, width, height):
        #print 'image.py -> to_pixbuf: filename=%s' % self._filename
        try:
            pix = gtk.gdk.pixbuf_new_from_file_at_size(self._filename, 
                width, height)
            return pix
        except:
            logger.error('Error converting to pixbuf image %s' % self._filename)
            return None

