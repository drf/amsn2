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

class Image(gtk.Image, base.aMSNImage):
    def __init__(self, theme_manager, view):
        gtk.Image.__init__(self)
        base.aMSNImage.__init__(self, theme_manager, view)

    def _loadFromFilename(self, filename, view, index):
        # TODO: Implement support for emblems and other embedded images
        if (index != 0): return

        try:
            self.set_from_file(filename)
            self._filename = filename
        except Exception, e:
            print e
            print "Error loading image %s" % filename

    def to_pixbuf(self, width, height):
        #print 'image.py -> to_pixbuf: filename=%s' % self._filename
        try:
            pix = gtk.gdk.pixbuf_new_from_file_at_size(self._filename, 
                width, height)
            return pix
        except:
            print 'Error converting to pixbuf image %s' % self._filename
            return None

