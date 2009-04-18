from __future__ import with_statement
from amsn2.gui import base
import curses
from threading import Thread
from threading import Condition
import time

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
        self._groups_order = []
        self._groups = {}
        self._contacts = {}
        self._win = parent._win
        self._stdscr = parent._stdscr
        self._mod_lock = Condition()
        self._modified = False
        self._thread = Thread(target=self.__thread_run)
        self._thread.daemon = True
        self._thread.setDaemon(True)
        self._thread.start()

    def contactListUpdated(self, clView):
        # Acquire the lock to do modifications
        with self._mod_lock:
            # TODO: Implement it to sort groups
            for g in self._groups_order:
                if g not in clView.group_ids:
                    self._groups.delete(g)
            for g in clView.group_ids:
                if not g in self._groups_order:
                    self._groups[g] = None
            self._groups_order = clView.group_ids
            self._modified = True

            # Notify waiting threads that we modified something
            import sys
            print >> sys.stderr, "Notify from contactListUpdated"
            self._mod_lock.notify()

    def groupUpdated(self, gView):
        # Acquire the lock to do modifications
        with self._mod_lock:
            if self._groups.has_key(gView.uid):
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
                self._modified = True

                # Notify waiting threads that we modified something
                import sys
                print >> sys.stderr, "Notify from groupUpdated"
                self._mod_lock.notify()

    def contactUpdated(self, cView):
        # Acquire the lock to do modifications
        with self._mod_lock:
            if self._contacts.has_key(cView.uid):
                self._contacts[cView.uid]['cView'] = cView
                self._modified = True

                # Notify waiting threads that we modified something
                import sys
                print >> sys.stderr, "Notify from contactUpdated"
                self._mod_lock.notify()

    def __repaint(self):
        import sys
        print >> sys.stderr, "Repainting"
        # Acquire the lock to do modifications
        with self._mod_lock:
            self._win.clear()
            self._win.move(0,0)
            gso = self._groups_order
            gso.reverse()
            for g in gso:
                if self._groups[g] is not None:
                    cids = self._groups[g].contact_ids
                    cids.reverse()
                    for c in cids:
                        if self._contacts.has_key(c) and self._contacts[c]['cView'] is not None:
                            self._win.insstr(" " + self._contacts[c]['cView'].name.toString())
                            self._win.insch(curses.ACS_HLINE)
                            self._win.insch(curses.ACS_HLINE)
                            self._win.insch(curses.ACS_LLCORNER)
                            self._win.insertln()
                    self._win.insstr(self._groups[g].name.toString())
                    self._win.insch(curses.ACS_LLCORNER)
                    self._win.insertln()
            self._win.refresh()
            self._modified = False

        print >> sys.stderr, "Repainted"

    def __thread_run(self):
        while True:
            import sys
            print >> sys.stderr, "at loop start"
            with self._mod_lock:
                t = time.time()
                # We don't want to work before at least half a second has passed
                while time.time() - t < 0.5 or not self._modified:
                    print >> sys.stderr, "Going to sleep\n"
                    self._mod_lock.wait(timeout=1)
                    print >> sys.stderr, "Ok time to see if we must repaint"
                self.__repaint()
                t = time.time()
            print >> sys.stderr, "at loop end"
