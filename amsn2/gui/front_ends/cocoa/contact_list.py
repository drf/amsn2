
from amsn2.gui import base

from amsn2.core.views import StringView
from amsn2.core.views import GroupView
from amsn2.core.views import ContactView
            

class aMSNContactList(base.aMSNContactListWindow):
    def __init__(self, amsn_core, parent):
		pass

    def show(self):
        pass

    def hide(self):
        pass

    def contactStateChange(self, contact):
		pass

    def contactNickChange(self, contact):
        pass
        
    def contactPSMChange(self, contact):
        pass
    
    def contactAlarmChange(self, contact):
        pass

    def contactDisplayPictureChange(self, contact):
        pass

    def contactSpaceChange(self, contact):
        pass
    
    def contactSpaceFetched(self, contact):
        pass

    def contactBlocked(self, contact):
        pass

    def contactUnblocked(self, contact):
        pass

    def contactMoved(self, from_group, to_group, contact):
        pass

    def contactAdded(self, group, contact):
        pass
    
    def contactRemoved(self, group, contact):
        pass

    def contactRenamed(self, contact):
        pass

    def groupRenamed(self, group):
        pass

    def groupAdded(self, group):
        pass

    def groupRemoved(self, group):
        pass

    def configure(self, option, value):
        pass

    def cget(self, option, value):
        pass
