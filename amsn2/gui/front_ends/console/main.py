
from amsn2.gui import base

import curses
class aMSNMainWindow(base.aMSNMainWindow):
    def __init__(self, amsn_core):
        self._amsn_core = amsn_core

    def show(self):
	self._stdscr = curses.initscr()
	curses.noecho()
	curses.cbreak()
	self._stdscr.keypad(1)
        self._stdscr.box()
        self._stdscr.refresh()
        self._amsn_core.idlerAdd(self.__on_show)
        
    def hide(self):
	curses.nocbreak()
	self._stdscr.keypad(0)
	curses.echo()
	curses.endwin()
    
    def __on_show(self):
        self._amsn_core.mainWindowShown()
       
