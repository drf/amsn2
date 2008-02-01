from amsn2.gui import base
import pymsn
import curses

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
            

class aMSNContactList(base.aMSNContactList):
    def __init__(self, amsn_core):
        self._amsn_core = amsn_core
        self.groups = {}
        self.contacts = {}
	self._stdscr = self._amsn_core.getMainWindow()._stdscr
        self._win = curses.newwin(100, 100, 3, 3)

    def show(self):
        pass

    def hide(self):
        pass

    def contactStateChange(self, contact):
        for group in contact.groups:
            self.groups[group.id].contacts[contact.id].presence = contact.presence
            
        self.__update_view()

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
        self.groups[group.id].contacts[contact.id] = Contact(contact.display_name, contact.presence)
        self.__update_view()
    
    def contactRemoved(self, group, contact):
        pass

    def contactRenamed(self, contact):
        pass

    def groupRenamed(self, group):
        pass

    def groupAdded(self, group):
        self.groups[group.id] = Group(group.name)
        self.__update_view()

    def groupRemoved(self, group):
        pass

    def configure(self, option, value):
        pass

    def cget(self, option, value):
        pass

        
    def __update_view(self):
        self._win.clear()
        row = 0
        for g in self.groups:
            count = self.groups[g].count()
            self._win.addstr(row, 0, "%s (%d/%d)" % (self.groups[g].name, count[0], count[1]), curses.A_BOLD | curses.A_UNDERLINE)
            row += 1
            for c in self.groups[g].contacts:
                 self._win.addstr(row, 2, "%s (%s)" % (self.groups[g].contacts[c].name, self.groups[g].contacts[c].status()), curses.A_BOLD)
                 row += 1
            row += 1

        self._win.refresh()
                             

