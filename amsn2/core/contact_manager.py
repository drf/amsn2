from views import *
import pymsn

#TODO: listeners

class aMSNContactManager:
    def __init__(self, core):
        self._core = core

        #TODO: cl_listeners should be a weakref list
        """
            Listeners are objects with the following methods:
                - groupAdded(groupView)
                - contactUpdated(contactView)
            TODO: listeners should return the views they were given (so they
            change it, useful for plugins...)
        """
        self._cl_listeners = []

    #Events

    def onContactPresenceChanged(self, contact):
        c = self.buildContactView(contact)
        for l in self._cl_listeners:
            l.contactUpdated(c)

    def onCLDownloaded(self, address_book):
        for group in address_book.groups:
            contacts = address_book.contacts.search_by_groups(group)
            groupV = self.buildGroupView(group, 0, len(contacts))
            groupV.contacts = []
            
            for contact in contacts:
                contactV = self.buildContactView(contact)
                groupV.contacts.append(contactV)
            
            for l in self._cl_listeners:
                l.groupAdded(groupV)

        groupV = self.buildGroupView(None, 0, 0)
        groupV.contacts = []
            
        contacts = address_book.contacts.search_by_memberships(pymsn.Membership.FORWARD)
        for contact in contacts:
            if len(contact.groups) == 0:
                contactV = self.buildContactView(contact)
                groupV.contacts.append(contactV)
                            
        if len(groupV.contacts) > 0:
            groupV = self.buildGroupView(None, 0, len(groupV.contacts))
            
            for l in self._cl_listeners:
                l.groupAdded(groupV)


    def buildGroupView(self, group, active, total):
        groupV = GroupView.getGroup(group.id if group else 0)
        groupV.icon = None # TODO : expanded/collapsed icon
        groupV.name = StringView() # TODO : default color from skin/settings
        groupV.name.appendText(group.name if group else "No Group") # TODO : parse or translation
        groupV.name.appendText("(" + str(active) + "/" + str(total) + ")")
        
        return groupV
    
    def buildContactView(self, contact):
        contactV = ContactView.getContact(contact.id)
        contactV.icon = self._core._gui.gui.Image(self._core, self._core._main)
        contactV.icon.load("Skin","buddy_" + self._core.p2s[contact.presence])
        contactV.dp = self._core._gui.gui.Image(self._core, self._core._main)
        contactV.dp.load("Skin","default_dp")
        contactV.name = StringView() # TODO : default colors
        contactV.name.openTag("nickname")
        contactV.name.appendText(contact.display_name) # TODO parse
        contactV.name.closeTag("nickname")
        contactV.name.appendText(" ")
        contactV.name.openTag("status")
        contactV.name.appendText("(")
        contactV.name.appendText(self._core.p2s[contact.presence])
        contactV.name.appendText(")")
        contactV.name.closeTag("status")
        contactV.name.appendText(" ")
        contactV.name.openTag("psm")
        contactV.name.setItalic()
        contactV.name.appendText(contact.personal_message)
        contactV.name.unsetItalic()
        contactV.name.closeTag("psm")
        
        return contactV
        
