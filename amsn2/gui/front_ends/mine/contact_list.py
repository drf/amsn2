from amsn2.gui import base
import pymsn

class Contact(object):
    def __init__(self, name, presence):
        self.name = name
        self.presence = presence
        self.p2s = {pymsn.Presence.ONLINE:"online",
                    pymsn.Presence.BUSY:"busy",
                    pymsn.Presence.IDLE:"idle",
                    pymsn.Presence.AWAY:"away",
                    pymsn.Presence.BE_RIGHT_BACK:"brb",
                    pymsn.Presence.ON_THE_PHONE:"phone",
                    pymsn.Presence.OUT_TO_LUNCH:"lunch",
                    pymsn.Presence.INVISIBLE:"hidden",
                    pymsn.Presence.OFFLINE:"offline"}
        

    def is_online(self):
        return self.presence != pymsn.Presence.OFFLINE

    def status(self):
        return self.p2s[self.presence]

class Group(object):
    def __init__(self, name):
        self.contacts = {}
        self.name = name

    def count(self):
        online = 0
        total = 0
        for c in self.contacts:
            total += 1
            if self.contacts[c].is_online():
                online +=1

        return (online, total)

class aMSNContactListWindow(base.aMSNContactListWindow):
    def __init__(self, amsn_core,main):
        self._amsn_core = amsn_core
        self.groups = {}
        self.contacts = {}
	self._clwidget = aMSNContactListWidget(amsn_core,main)

    def show(self):
        pass

    def hide(self):
        pass

    def setTitle(self,mess):
        pass

    def setMenu(self,menu):
        pass

    def myInfoUpdated(self,view):
        pass

class aMSNContactListWidget(object):
    def __init__(self, amsn_core,main):
        self._amsn_core = amsn_core
        self.groups = {}
        self.contacts = {}
        clm = amsn_core._contactlist_manager
        clm.register(clm.CLVIEW_UPDATED, self.contactListUpdated)
        clm.register(clm.GROUPVIEW_UPDATED, self.groupUpdated)
        clm.register(clm.CONTACTVIEW_UPDATED, self.contactUpdated)

    def contactListUpdated(self,contactlist):
        print "contactlist"
        
    def groupUpdated(self,group):
        print "group"

    def contactUpdated(self,contactview):
        #print "contact " + contactview.name.toString()
        passh

    def show(self):
        pass

    def hide(self):
        pass

    def groupAdded(self, group):
        self.groups[group.uid] = Group(group.name)
        self.__update_view()

    def __cls(self):
        print "[H[2J"

    def contactStateChange(self, contact):
        for group in contact.groups:
            self.groups[group.uid].contacts[contact.id].presence = contact.presence            
        self.__update_view()

    def contactAdded(self, group, contact):
        self.groups[group.uid].contacts[contact.id] = Contact(contact.display_name, contact.presence)
        self.__update_view()
    
    def __update_view(self):
        self.__cls()
        for g in self.groups:
            count = self.groups[g].count()
            print "|X| %s (%d/%d)" % (self.groups[g].name, count[0], count[1])
            for c in self.groups[g].contacts:
                print "  |=> %s (%s)" % (self.groups[g].contacts[c].name, self.groups[g].contacts[c].status())
            print ""
    

