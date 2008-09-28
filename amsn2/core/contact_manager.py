from views import *
import pymsn

#TODO: listeners

class aMSNContactManager:
    def __init__(self, core):
        self._core = core

        #TODO: listeners should be a priority weakref list or smthg like that
        """
            Listeners are objects with the following methods:
                - groupAdded(groupView)
                - contactUpdated(contactView)
            TODO: listeners should return the views they were given (so they
            change it, useful for plugins...)
        """
        self._listeners = []

    #Events

    def onContactPresenceChanged(self, c):
        #Maybe we need to change the name of the groupView
        for l in self._listeners:
            l.contactUpdated(c)

    def onCLDownloaded(self, address_book):
        #contacts are new. Need to fill the ContactView
        contact_updated = (ContactView.Updated.ACCOUNT
                           | ContactView.Updated.STATUS
                           | ContactView.Updated.NICKNAME
                           | ContactView.Updated.PSM
                           | ContactView.Updated.CURRENT_MEDIA)
        for group in address_book.groups:
            contacts = address_book.contacts.search_by_groups(group)
            groupV = self.buildGroupView(group, 0, len(contacts))
            groupV.contacts = []

            for contact in contacts:
                contactV = ContactView.getContact(self._core, contact.id,
                                                  contact, contact_updated)
                groupV.contacts.append(contactV)

            for l in self._listeners:
                l.groupAdded(groupV)

        groupV = self.buildGroupView(None, 0, 0)
        groupV.contacts = []

        contacts = address_book.contacts.search_by_memberships(pymsn.Membership.FORWARD)
        for contact in contacts:
            if len(contact.groups) == 0:
                contactV = ContactView.getContact(self._core, contact.id,
                                                  contact, contact_updated)
                groupV.contacts.append(contactV)

        if len(groupV.contacts) > 0:
            groupV = self.buildGroupView(None, 0, len(groupV.contacts))

            for l in self._listeners:
                l.groupAdded(groupV)

    def register(self, obj, priority = 0):
        #TODO: priority
        self._listeners.append(obj)

    def unregister(self, obj):
        if obj in self._listeners:
            self._listeners.remove(obj)


    def buildGroupView(self, group, active, total):
        groupV = GroupView.getGroup(group.id if group else 0)
        groupV.icon = None # TODO : expanded/collapsed icon
        groupV.name = StringView() # TODO : default color from skin/settings
        groupV.name.appendText(group.name if group else "No Group") # TODO : parse or translation
        groupV.name.appendText("(" + str(active) + "/" + str(total) + ")")

        return groupV

