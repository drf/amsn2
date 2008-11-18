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

class aMSNImage(object):
    """ This interface holds the basic methods that must have a Image class in
        any front end
    """
    def __init__(self, theme_manager, view):
        self._theme_manager = theme_manager
        self.load(view)
        
    def load(self, view):
        i = 0
        for (resource_type, value) in view.imgs:
            try:
                loadMethod = getattr(self, "_loadFrom%s" % resource_type)
            except AttributeError, e:
                print "From load in base/image.py:\n\t(resource_type, value) = "
                "(%s, %s)\n\tAttributeError: %s" % (resource_type, value, e)
            else:
                loadMethod(value, view, i)
                i += 1
            
    def _loadFromFilename(self, filename, view, index):
        """ Load an image from a path. This method should be reimplemented """
        pass

    def _loadFromTheme(self, resource_name, view, index):
        """ Load an image from a key stored in aMSNThemeManager"""
        try:
            _, name = self._theme_manager.get_value(resource_name)
        except Exception, e:
            print e
            print "Error loading resource %s" % resource_name
        else:
            self._loadFromFilename(name, view, index)

    def _loadFromNone(self, resource_name, view=None, index=0):
        pass
        