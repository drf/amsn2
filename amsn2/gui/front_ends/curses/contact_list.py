from amsn2.gui import base
import curses

class aMSNContactListWindow(base.aMSNContactListWindow):
    def __init__(self, amsn_core, parent):
        self._amsn_core = amsn_core
        self._stdscr = parent._stdscr
        (y,x) = self._stdscr.getmaxyx()
        # TODO: Use a pad instead
        self._win = curses.newwin(y, int(0.25*x), 0, 0)
        self._win.bkgd(curses.color_pair(0))
        self._win.border()
        self._clwidget = aMSNContactListWidget(amsn_core, self)

    def show(self):
        self._win.refresh()

    def hide(self):
        self._stdscr.clear()
        self._stdscr.refresh()

    def configure(self, option, value):
        pass

    def cget(self, option, value):
        pass

class aMSNContactListWidget(base.aMSNContactListWidget):

    def __init__(self, amsn_core, parent):
        super(aMSNContactListWidget, self).__init__(amsn_core, parent)
        self._groups = {}
        self._contacts = {}
        self._win = parent._win
        self._stdscr = parent._stdscr

    def contactListUpdated(self, clView):
        # TODO: Implement it to sort groups
        for g in self._groups:
            if g not in clView.group_ids:
                self._groups.delete(g)
        for g in clView.group_ids:
            if not self._groups.has_key(g):
                self._groups[g] = None

    def groupUpdated(self, gView):
        if not self._groups.has_key(gView.uid):
            return

        if self._groups[gView.uid] is not None:
            #Delete contacts
            for c in self._groups[gView.uid].contact_ids:
                if c not in gView.contact_ids:
                    if self._contacts[c]['refs'] == 1:
                        self._contacts.delete(c)
                    else:
                        self._contacts[c]['refs'] -= 1
        #Add contacts
        for c in gView.contact_ids:
            if not self._contacts.has_key(c):
                self._contacts[c] = {'cView': None, 'refs': 1}
                continue
            #If contact wasn't already there, increment reference count
            if self._groups[gView.uid] is None or c not in self._groups[gView.uid].contact_ids:
                self._contacts[c]['refs'] += 1
        self._groups[gView.uid] = gView
        self.__updateGroups()

    def contactUpdated(self, cView):
        if not self._contacts.has_key(cView.uid):
            return
        self._contacts[cView.uid]['cView'] = cView
        self.__updateGroups()

    def __updateGroups(self):
        self._win.clear()
        self._win.move(0,0)
        for g in self._groups:
            if self._groups[g] is not None:
                self._win.insstr(self._groups[g].name.toString())
                self._win.insch(curses.ACS_LLCORNER)
                self._win.insertln()
                for c in self._groups[g].contact_ids:
                    if self._contacts.has_key(c) and self._contacts[c]['cView'] is not None:
                        self._win.insstr(self._contacts[c]['cView'].name.toString())
                        self._win.insch(curses.ACS_HLINE)
                        self._win.insch(curses.ACS_HLINE)
                        self._win.insch(curses.ACS_LLCORNER)
                        self._win.insertln()
        self._win.refresh()
