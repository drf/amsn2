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
        self._statusicons = {}
        self._displaypic = {}
        self._emblems = {}

        self.load()

    def __get(self, var, key):
        # TODO: evaluate if should be returned None when key is not valid
        if key in var.keys():
            return var[key]
        else:
            return (None, None)

    def load(self):
        # Here aMSNThemeManager should read user's files to know what theme
        # will be loaded to each aspect
        self._buttons = aMSNButtonLoader().load('default')
        self._statusicons = aMSNStatusIconLoader().load('default')
        self._displaypic = aMSNDisplayPicLoader().load('default')
        self._emblems = aMSNEmblemLoader().load('default')

    def get_value(self, key):
        if (key.startswith('button_')):
            return self.get_button(key)
        elif (key.startswith('buddy_')):
            return self.get_statusicon(key)
        elif (key.startswith('dp_')):
            return self.get_dp(key)
        elif (key.startswith('emblem_')):
            return self.get_emblem(key)
        else:
            # TODO: This should raise a exception
            return (None, None)

    def get_button(self, key):
        return self.__get(self._buttons, key)

    def get_statusicon(self, key):
        return self.__get(self._statusicons, key)

    def get_dp(self, key):
        return self.__get(self._displaypic, key)

    def get_emblem(self, key):
        return self.__get(self._emblems, key)

class aMSNGenericLoader:
    def __init__(self, basedir):
        self._theme = 'default'
        self._basedir = os.path.join("amsn2", "themes", basedir)
        self._defaultdir = os.path.join(self._basedir, "default")
        # Keys holds a pair (key,filename)
        # Should be initialized after creating the class
        self._keys = []
        self._dict = {}

    def load(self, theme='default'):
        self.theme = theme
        self._theme_dir = os.path.join(self._basedir, theme)

        for key in self._keys.keys():
            image = self._keys[key]
            filepath = os.path.join(self._theme_dir, image)

            # Verificating
            if (not os.path.isfile(filepath)):
                filepath = os.path.join(self._defaultdir, image)

            self._dict[key] = ("Filename", filepath)

        return self._dict

class aMSNButtonLoader(aMSNGenericLoader):
    def __init__(self):
        aMSNGenericLoader.__init__(self, "buttons")
        self._keys = {
            'button_nudge': 'nudge.png',
            'button_smile': 'smile.png',
        }

class aMSNStatusIconLoader(aMSNGenericLoader):
    def __init__(self):
        aMSNGenericLoader.__init__(self, "status_icons")
        self._keys = {
            'buddy_online': 'online.png',
            'buddy_away': 'away.png',
            'buddy_brb': 'away.png',
            'buddy_idle': 'away.png',
            'buddy_lunch': 'away.png',
            'buddy_busy': 'busy.png',
            'buddy_phone': 'phone.png',
            'buddy_offline': 'offline.png',
            'buddy_hidden': 'offline.png',
            'buddy_blocked': 'blocked.png',
            'buddy_blocked_off': 'blocked_off.png',
            'buddy_webmsn': 'webmsn.png',
        }

class aMSNDisplayPicLoader(aMSNGenericLoader):
    def __init__(self):
        aMSNGenericLoader.__init__(self, "displaypic")
        self._keys = {
            'dp_amsn': 'amsn.png', 
            'dp_female': 'female.png',
            'dp_loading': 'loading.png',
            'dp_male': 'male.png',
            'dp_nopic': 'nopic.png',
        }

class aMSNEmblemLoader(aMSNGenericLoader):
    def __init__(self):
        aMSNGenericLoader.__init__(self, "emblems")
        self._keys = {
            'emblem_online': 'plain_emblem.png',
            'emblem_away': 'away_emblem.png',
            'emblem_brb': 'away_emblem.png',
            'emblem_idle': 'away_emblem.png',
            'emblem_lunch': 'away_emblem.png',
            'emblem_busy': 'busy_emblem.png',
            'emblem_phone': 'busy_emblem.png',
            'emblem_offline': 'offline_emblem.png',
            'emblem_hidden': 'offline_emblem.png',
            'emblem_blocked': 'blocked_emblem.png',
        }
