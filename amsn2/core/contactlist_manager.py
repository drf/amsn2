from views import *
import os
import tempfile
import papyon


class aMSNContactListManager:
    def __init__(self, core):
        self._core = core

        #TODO: have only one event manager?
        #TODO: describe the events:
        self.CONTACTVIEW_UPDATED = 0
        self.GROUPVIEW_UPDATED = 1
        self.CLVIEW_UPDATED = 2
        self.AMSNCONTACT_UPDATED = 3
        self._events_cbs = [[], [], [], []]

        self._contacts = {}
        self._groups = {}
        self._papyon_addressbook = None

    #TODO: sorting contacts & groups

    def emit(self, event, *args):
        """ emit the event """
        for cb in self._events_cbs[event]:
            #TODO: try except
            cb(*args)

    def register(self, event, callback, pos=None):
        """ register a callback for an event """
        #TODO: try except
        if pos is None:
            self._events_cbs[event].append(callback)
        else:
            self._events_cbs[event].insert(pos,callback)

    def unregister(self, event, callback):
        """ unregister a callback for an event """
        #TODO: try except
        self._events_cbs[event].remove(callback)




    def onContactPresenceChanged(self, papyon_contact):
        #1st/ update the aMSNContact object
        c = self.getContact(papyon_contact.id, papyon_contact)
        c.fill(self._core, papyon_contact)
        #2nd/ update the ContactView
        cv = ContactView(self._core, c)
        self.emit(self.CONTACTVIEW_UPDATED, cv)

        #TODO: update the group view

        #Request the DP...
        if (papyon_contact.presence is not papyon.Presence.OFFLINE and
            papyon_contact.msn_object):
                self._core._profile.client._msn_object_store.request(papyon_contact.msn_object,
                                                                     (self.onDPdownloaded,
                                                                      papyon_contact.id))

    def onCLDownloaded(self, address_book):
        self._papyon_addressbook = address_book
        grpviews = []
        cviews = []
        clv = ContactListView()

        for group in address_book.groups:
            contacts = address_book.contacts.search_by_groups(group)

            for contact in contacts:
                c = self.getContact(contact.id, contact)
                cv = ContactView(self._core, c)
                cviews.append(cv)

            cids = [c.id for c in contacts]
            gv = GroupView(group.id, group.name, cids)
            grpviews.append(gv)
            clv.group_ids.append(group.id)

        contacts = address_book.contacts.search_by_memberships(papyon.Membership.FORWARD)
        no_group_ids= []
        for contact in contacts:
            if len(contact.groups) == 0:
                c = self.getContact(contact.id, contact)
                cv = ContactView(self._core, c)
                cviews.append(cv)
                no_group_ids.append(contact.id)

        if len(no_group_ids) > 0:
            gv = GroupView(0, "NoGroup", no_group_ids)
            grpviews.append(gv)
            clv.group_ids.append(0)

        #Emit the events
        self.emit(self.CLVIEW_UPDATED, clv)
        for g in grpviews:
            self.emit(self.GROUPVIEW_UPDATED, g)
        for c in cviews:
            self.emit(self.CONTACTVIEW_UPDATED, c)

    def onDPdownloaded(self, msn_object, uid):
        #1st/ update the aMSNContact object
        c = self.getContact(uid)
        ##c.dp.load("FileObject", msn_object._data)
        (fno, tf) = tempfile.mkstemp()
        f = os.fdopen(fno, 'w+b')
        f.write(msn_object._data.read())
        f.close()
        c.dp.load("Filename", tf)
        self.emit(self.AMSNCONTACT_UPDATED, c)
        #2nd/ update the ContactView
        cv = ContactView(self._core, c)
        self.emit(self.CONTACTVIEW_UPDATED, cv)


    def getContact(self, cid, papyon_contact=None):
        #TODO: should raise UnknownContact or sthg like that
        try:
            return self._contacts[cid]
        except KeyError:
            if papyon_contact is not None:
                c = aMSNContact(self._core, papyon_contact)
                self._contacts[cid] = c
                self.emit(self.AMSNCONTACT_UPDATED, c)
                return c
            else:
                raise ValueError


""" A few things used to describe a contact
    They are stored in that structure so that there's no need to create them
    everytime
"""
class aMSNContact():
    def __init__(self, core, papyon_contact):
        self.uid = papyon_contact.id
        self.fill(core, papyon_contact)

    def fill(self, core, papyon_contact):
        self.icon = ImageView()
        self.icon.load("Theme","buddy_" + core.p2s[papyon_contact.presence])
        self.dp = ImageView()
        #TODO: for the moment, use default dp
        self.dp.load("Theme", "dp_nopic")
        self.emblem = ImageView()
        self.emblem.load("Theme", "emblem_" + core.p2s[papyon_contact.presence])
        #TODO: PARSE ONLY ONCE
        self.nickname = StringView()
        self.nickname.appendText(papyon_contact.display_name)
        self.personal_message = StringView()
        self.personal_message.appendText(papyon_contact.personal_message)
        self.current_media = StringView()
        self.current_media.appendText(papyon_contact.current_media)
        self.status = StringView()
        self.status.appendText(core.p2s[papyon_contact.presence])
        #for the moment, we store the papyon_contact object, but we shouldn't have to
        #TODO: getPapyonContact(self, core...) or _papyon_contact?
        self._papyon_contact = papyon_contact


