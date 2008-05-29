
class aMSNContactList(object):
    """ This interface implements the contact list of the UI """
    def __init__(self, amsn_core):
        raise NotImplementedError

    def show(self):
        """ Show the contact list window """
        raise NotImplementedError

    def hide(self):
        """ Hide the contact list window """
        raise NotImplementedError

    def contactUpdated(self, contact):
        """ This method will be called to notify the contact list that a contact has been updated
        The contact can be in any group drawn and his icon, name or DP should be updated accordingly.
        The position of the contact will not be changed by a call to this function. If the position was changed,
        a groupUpdated call will be made with the new order of the contacts in the affects groups.
        """
        raise NotImplementedError
    
    def groupUpdated(self, group):
        """ This method will be called to notify the contact list that an already added group has been updated
        The contact list should update its icon and name but also its content (the ContactViews). The order of the contacts
        may be changed, in which case the UI should update itself accordingly.
        A contact can also be added or removed from a group using this method
        """
        raise NotImplementedError

    def groupAdded(self, group):
        """ This method will be called when the core wants to notify the contact list
        that a group should be drawn. It will be called initially to feed the contact list with
        the groups that the CL should contain.
        @group : a GroupView containing the icon and name of the group as well as the list of ContactViews for all the contacts
        to show in the group."""
        raise NotImplementedError

    def groupRemoved(self, group):
        """ This method will be called when the core wants to notify the contact list that a group needs to be removed from the CL """
        raise NotImplementedError

    def configure(self, option, value):
        """ This method will be used to configure an option of the contact list """
        raise NotImplementedError

    def cget(self, option):
        """ This method will be used to get the value of an option of the contact list """
        raise NotImplementedError

