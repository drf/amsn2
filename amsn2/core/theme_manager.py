# -*- coding: utf-8 -*-
#===================================================
# 
# theme_manager.py - This file is part of the amsn2 package
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

import os

class aMSNThemeManager:
    def __init__(self):
        self._buttons = {}
        self.load()
        
    def load(self):
        # Here aMSNThemeManager should read user's files to know what theme
        # goes to each aspect
        b = ButtonLoader()
        self._buttons = b.load('default')
        
    def get_button(self, key):
        # TODO: evaluate if should be returned None when key is not valid
        if key in self._buttons.keys():
            return self._buttons[key]
        else:
            return None
    
class ButtonLoader:
    def __init__(self):
        self._theme = 'default'
        self._basedir = os.path.join("amsn2", "themes", "buttons")
        self._defaultdir = os.path.join(self._basedir, "default")
        self._keys = ['nudge', 'smile']
        self._dict = {}
        
    def load(self, theme='default'):
        self.theme = theme
        self._theme_dir = os.path.join(self._basedir, theme)
        
        for key in self._keys:
            image = "%s.png" % key
            filepath = os.path.join(self._theme_dir, image)
            print filepath
            # Verificating
            if (not os.path.isfile(filepath)):
                filepath = os.path.join(self._defaultdir, image)
                
            self._dict[key] = ("Filename", filepath)
            
        return self._dict
    