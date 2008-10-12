from views import *
import pymsn



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




    def onContactPresenceChanged(self, pymsn_contact):
        #1st/ update the aMSNContact object
        c = self.getContact(pymsn_contact.id, pymsn_contact)
        c.fill(self._core, pymsn_contact)
        #2nd/ update the ContactView
        cv = ContactView(self._core, c)
        self.emit(self.CONTACTVIEW_UPDATED, cv)

        #TODO: update the group view


    def onCLDownloaded(self, address_book):
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

        contacts = address_book.contacts.search_by_memberships(pymsn.Membership.FORWARD)
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


    def getContact(self, cid, pymsn_contact=None):
        #TODO: should raise UnknownContact or sthg like that
        try:
            return self._contacts[cid]
        except KeyError:
            if pymsn_contact is not None:
                c = aMSNContact(self._core, pymsn_contact)
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
    def __init__(self, core, pymsn_contact):
        self.uid = pymsn_contact.id
        self.fill(core, pymsn_contact)

    def fill(self, core, pymsn_contact):
        self.icon = ImageView()
        self.icon.load("Skin","buddy_" + core.p2s[pymsn_contact.presence])
        self.dp = ImageView()
        #for the moment, use default_dp
        self.dp.load("Skin","default_dp")
        self.emblem = ImageView()
        self.emblem.load("Skin", "emblem_" + core.p2s[pymsn_contact.presence])
        #TODO: PARSE ONLY ONCE
        self.nickname = StringView()
        self.nickname.appendText(pymsn_contact.display_name)
        self.personal_message = StringView()
        self.personal_message.appendText(pymsn_contact.personal_message)
        self.current_media = StringView()
        self.current_media.appendText(pymsn_contact.current_media)
        self.status = StringView()
        self.status.appendText(core.p2s[pymsn_contact.presence])
        #for the moment, we store the pymsn_contact object, but we shouldn't have to
        #TODO: getPymsnContact(self, core...) or _pymsn_contact?
        self._pymsn_contact = pymsn_contact


