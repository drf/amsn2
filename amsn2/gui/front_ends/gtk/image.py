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
    
class Image(gtk.Image):
    def __init__(self, skin, view):
        gtk.Image.__init__(self)
        
        self._skin = skin
        '''
        for (resource_type, value) in view.imgs:
            print resource_type, value
            
        print contactview.dp.imgs
        for (resource_type, value) in contactview.dp.imgs:
            print resource_type, value
        '''
        self.load(view)
        
    def load(self, view):
        for (resource_type, value) in view.imgs:
            try:
                loadMethod = getattr(self, "_loadFrom%s" % resource_type)
            except AttributeError, e:
                print "From load in gtk/image.py:\n\t(resource_type, value) = "
                "(%s, %s)\n\tAttributeError: %s" % (resource_type, value, e)
            else:
                loadMethod(value, -1, view)
            
    def _loadFromFilename(self, filename, pos=0, view=None, i=0):
        try:
            self.set_from_file(filename)
            self._filename = filename
        except Exception, e:
            print e
            print "Error loading %s image from file" % filename


    def _loadFromSkin(self, resource_name, pos=0, view=None, i=0):
        res = self._skin.getKey(resource_name)
        if res is not None:
            (type, value) = res
            self._filename = value
            try:
                loadMethod = getattr(self, "_loadFrom%s" % type)
            except AttributeError, e:
                print "From _loadFromSkin in gtk/image.py:\n\t(type, value) = "
                "(%s, %s)\n\tAttributeError: %s" % (type, value, e)
            else:
                loadMethod(value, pos, view, i)

    def _loadFromNone(self, r, pos=0):
        pass
        
    def to_pixbuf(self, size):
        #print 'image.py -> to_pixbuf: filename=%s' % self._filename
        try:
            pix = gtk.gdk.pixbuf_new_from_file_at_size(self._filename, size, size)
            return pix
        except:
            print 'Error converting to pixbuf image %s' % self._filename
            return None
        