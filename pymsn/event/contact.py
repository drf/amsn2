# -*- coding: utf-8 -*-
#
# Copyright (C) 2007  Ali Sabil <ali.sabil@gmail.com>
# Copyright (C) 2007  Ole André Vadla Ravnås <oleavr@gmail.com>
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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#

from base import BaseEventInterface

__all__ = ["ContactEventInterface"]

class ContactEventInterface(BaseEventInterface):
    def __init__(self, client):
        BaseEventInterface.__init__(self, client)

    def on_contact_presence_changed(self, contact):
        pass

    def on_contact_display_name_changed(self, contact):
        pass

    def on_contact_personal_message_changed(self, contact):
        pass

    def on_contact_current_media_changed(self, contact):
        pass

    def on_contact_display_picture_changed(self, contact):
        pass

    def on_contact_client_capabilities_changed(self, contact):
        pass

    def on_contact_details_changed(self, contact, details_flag):
        pass
