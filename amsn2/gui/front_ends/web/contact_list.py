"""TODO:
    * Let the aMSNContactListWidget be selectable to choose contacts to add to a
    conversation... each contact should have a checkbox on front of it
    * Drag contacts through groups
    * Drag groups
    ...
"""


class aMSNContactListWindow(object):
    """ This interface represents the main Contact List Window
        self._clwiget is an aMSNContactListWidget 
    """

    def __init__(self, amsn_core, parent):
        self._main = parent
        self._clwiget = aMSNContactListWidget(amsn_core,self)
        pass

    def show(self):
        """ Show the contact list window """
        self._main.send("showContactListWindow",[])
        pass

    def hide(self):
        """ Hide the contact list window """
        self._main.send("hideContactListWindow",[])
        pass

    def setTitle(self, text):
        """ This will allow the core to change the current window's title
        @text : a string
        """
        self._main.send("setContactListTitle",[text])
        pass

    def setMenu(self, menu):
        """ This will allow the core to change the current window's main menu
        @menu : a MenuView
        """
        self._main.send("setMenu")
        pass

    def myInfoUpdated(self, view):
        """ This will allow the core to change pieces of information about
        ourself, such as DP, nick, psm, the current media being played,...
        @view: the contactView of the ourself (contains DP, nick, psm,
        currentMedia,...)"""
        self._main.send("myInfoUpdated",[view.name.toString()])
        pass

class aMSNContactListWidget(object):
    """ This interface implements the contact list of the UI """
    def __init__(self, amsn_core, parent):
        self._main = parent._main
        self.contacts = {}
        self.groups = {}
        self._main.addListener("contactClicked",self.contactClicked)
        clm = amsn_core._contactlist_manager
        clm.register(clm.CLVIEW_UPDATED, self.contactListUpdated)
        clm.register(clm.GROUPVIEW_UPDATED, self.groupUpdated)
        clm.register(clm.CONTACTVIEW_UPDATED, self.contactUpdated)
        
    def contactClicked(self,uidL):
        uid = uidL.pop()
        try:
            self.contacts[uid].on_click(uid)
        except Exception, inst:
            print inst
        return True

    def show(self):
        """ Show the contact list widget """
        self._main.send("showContactListWidget",[])
        pass

    def hide(self):
        """ Hide the contact list widget """
        self._main.send("hideContactListWidget",[])
        pass

    def contactListUpdated(self, clView):
        """ This method will be called when the core wants to notify
        the contact list of the groups that it contains, and where they
        should be drawn a group should be drawn.
        It will be called initially to feed the contact list with the groups
        that the CL should contain.
        It will also be called to remove any group that needs to be removed.
        @cl : a ContactListView containing the list of groups contained in
        the contact list which will contain the list of ContactViews
        for all the contacts to show in the group."""
        self._main.send("contactListUpdated",clView.group_ids)
        pass

    def groupUpdated(self, groupView):
        """ This method will be called to notify the contact list
        that a group has been updated.
        The contact list should update its icon and name
        but also its content (the ContactViews). The order of the contacts
        may be changed, in which case the UI should update itself accordingly.
        A contact can also be added or removed from a group using this method
        """
        self.groups[groupView.uid]=groupView
        self._main.send("groupUpdated",[groupView.uid,",".join(groupView.contact_ids),groupView.name.toString()])
        pass

    def contactUpdated(self, contactView):
        """ This method will be called to notify the contact list
        that a contact has been updated.
        The contact can be in any group drawn and his icon,
        name or DP should be updated accordingly.
        The position of the contact will not be changed by a call
        to this function. If the position was changed, a groupUpdated
        call will be made with the new order of the contacts
        in the affects groups.
        """
        self.contacts[contactView.uid]=contactView
        self._main.send("contactUpdated",[contactView.uid,contactView.name.toString()])
        pass

