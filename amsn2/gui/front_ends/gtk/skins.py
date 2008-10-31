# -*- coding: utf-8 -*-
#===================================================
# 
# contact_list.py - This file is part of the amsn2 package
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

class Skin(object):
    def __init__(self, core, path):
        self._path = path
        self._dict = {}
        #TODO : remove, it's just here for test purpose
        #TODO : explain a bit :D
        self.setKey("buddy_online", ("Filename", os.path.join("amsn2", 
            "themes", "default", "images", "online.png")))
        #self.setKey("emblem_online", ("Filename", "amsn2/themes/default/images/contact_list/plain_emblem.png"))

        self.setKey("buddy_away", ("Filename", os.path.join("amsn2", 
            "themes", "default", "images", "away.png")))
            
        #self.setKey("emblem_away", ("Filename", "amsn2/themes/default/images/contact_list/away_emblem.png"))
        self.setKey("buddy_brb", ("Filename", os.path.join("amsn2", 
            "themes", "default", "images", "away.png")))
        #self.setKey("emblem_brb", ("Filename", "amsn2/themes/default/images/contact_list/away_emblem.png"))
        self.setKey("buddy_idle", ("Filename", os.path.join("amsn2", 
            "themes", "default", "images", "away.png")))
        #self.setKey("emblem_idle", ("Filename", "amsn2/themes/default/images/contact_list/away_emblem.png"))
        self.setKey("buddy_lunch", ("Filename", os.path.join("amsn2", 
            "themes", "default", "images", "away.png")))
        #self.setKey("emblem_lunch", ("Filename", "amsn2/themes/default/images/contact_list/away_emblem.png"))

        # Just to show you can use an image from the edj file
        self.setKey("buddy_busy", ("Filename", os.path.join("amsn2", 
            "themes", "default", "images","busy.png")))
        #self.setKey("emblem_busy", ("Filename", "amsn2/themes/default/images/contact_list/busy_emblem.png"))
        self.setKey("buddy_phone", ("Filename", os.path.join("amsn2", 
            "themes", "default", "images", "busy.png")))
        #self.setKey("emblem_phone", ("Filename", "amsn2/themes/default/images/contact_list/busy_emblem.png"))

        self.setKey("buddy_offline", ("Filename", os.path.join("amsn2", 
            "themes", "default", "images", "offline.png")))
        
        #self.setKey("emblem_offline", ("Filename", "amsn2/themes/default/images/contact_list/offline_emblem.png"))
        self.setKey("buddy_hidden", ("Filename", os.path.join("amsn2", 
            "themes", "default", "images", "offline.png")))
        #self.setKey("emblem_hidden", ("Filename", "amsn2/themes/default/images/contact_list/offline_emblem.png"))

        self.setKey("default_dp", ("Filename", os.path.join("amsn2", "themes", 
            "default", "images", "contact_list", "nopic.png")))

    def getKey(self, key, default=None):
        try:
            return self._dict[key]
        except KeyError:
            return default

    def setKey(self, key, value):
        self._dict[key] = value


class SkinManager(object):
    def __init__(self, core):
        self._core = core
        self.skin = Skin(core, "skins")

    def setSkin(self, name):
        self.skin = Skin(self._core, os.path.join("skins", name))

    def listSkins(self, path):
        pass
