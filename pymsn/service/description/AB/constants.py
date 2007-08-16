# -*- coding: utf-8 -*-
#
# pymsn - a python client library for Msn
#
# Copyright (C) 2007 Johann Prieur <johann.prieur@gmail.com>
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

__all__ = ['ContactAnnotations', 'ContactEmailType', 'ContactType',
           'ContactPhoneType', 'ContactLocation', 'ContactWebSiteType']

class ContactType(object):
    REGULAR = "Regular"
    LIVE_PENDING = "LivePending"
    LIVE_ACCEPTED = "LiveAccepted"
    LIVE_DROPPED = "LiveDropped"
    YAHOO = "Messenger2"

class ContactAnnotations(object):
    NICKNAME = "AB.NickName"
    JOB_TITLE = "AB.JobTitle"
    SPOUSE = "AB.Spouse"

class ContactEmailType(object):
    BUSINESS = "ContactEmailBusiness"
    MESSENGER = "ContactEmailMessenger"
    OTHER = "ContactEmailOther"
    PERSONAL = "ContactEmailPersonal"
    EXTERNAL = "Messenger2"

class ContactPhoneType(object):
    BUSINESS = "ContactPhoneBusiness"
    FAX = "ContactPhoneFax"
    MOBILE = "ContactPhoneMobile"
    OTHER = "ContactPhoneOther"
    PAGER = "ContactPhonePager"
    PERSONAL = "ContactPhonePersonal"

class ContactLocation(object):
    class Type(object):
        BUSINESS = "ContactLocationBusiness"
        PERSONAL = "ContactLocationPersonal"

    NAME = "name"
    STREET = "street"
    CITY = "city"
    STATE = "state"
    COUNTRY = "country"
    POSTAL_CODE = "postalCode"
    
class ContactWebSiteType(object):
    BUSINESS = "ContactWebSiteBusiness"
    PERSONAL = "ContactWebSitePersonal"

