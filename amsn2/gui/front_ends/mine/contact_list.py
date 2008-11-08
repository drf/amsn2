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
        pass

    def show(self):
        """ Show the contact list window """
        pass

    def hide(self):
        """ Hide the contact list window """
        pass

    def setTitle(self, text):
        """ This will allow the core to change the current window's title
        @text : a string
        """
        pass

    def setMenu(self, menu):
        """ This will allow the core to change the current window's main menu
        @menu : a MenuView
        """
        pass

    def myInfoUpdated(self, view):
        """ This will allow the core to change pieces of information about
        ourself, such as DP, nick, psm, the current media being played,...
        @view: the contactView of the ourself (contains DP, nick, psm,
        currentMedia,...)"""
        pass

class aMSNContactListWidget(object):
    """ This interface implements the contact list of the UI """
    def __init__(self, amsn_core, parent):
        clm = amsn_core._contactlist_manager
        clm.register(clm.CLVIEW_UPDATED, self.contactListUpdated)
        clm.register(clm.GROUPVIEW_UPDATED, self.groupUpdated)
        clm.register(clm.CONTACTVIEW_UPDATED, self.contactUpdated)

    def show(self):
        """ Show the contact list widget """
        pass

    def hide(self):
        """ Hide the contact list widget """
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
        pass

    def groupUpdated(self, groupView):
        """ This method will be called to notify the contact list
        that a group has been updated.
        The contact list should update its icon and name
        but also its content (the ContactViews). The order of the contacts
        may be changed, in which case the UI should update itself accordingly.
        A contact can also be added or removed from a group using this method
        """
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
        pass

