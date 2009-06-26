# -*- encoding: utf-8 -*-
from __future__ import with_statement
import curses
import sys
from threading import Thread
from threading import Condition
import locale

class CommandLine(object):
    def __init__(self, screen, ch_cb):
        self._stdscr = screen
        self._on_char_cb = ch_cb
        self._cb_cond = Condition()
        self._thread = Thread(target=self._get_key)
        self._thread.daemon = True
        self._thread.setDaemon(True)
        self._thread.start()

    def setCharCb(self, ch_cb):
        with self._cb_cond:
            self._on_char_cb = ch_cb
            if ch_cb is not None:
                self._cb_cond.notify()

    def _get_key(self):
        while( True ):
            with self._cb_cond:
                if self._on_char_cb is None:
                    self._cb_cond.wait()
                print >> sys.stderr, "Waiting for char"
                ch = self._stdscr.getkey()
                first = True
                while True:
                    try:
                        ch = ch.decode(locale.getpreferredencoding())
                        self._stdscr.nodelay(0)
                        break
                    except (UnicodeEncodeError, UnicodeDecodeError), e:
                        self._stdscr.nodelay(1)
                        try:
                            ch += self._stdscr.getkey()
                        except:
                            if not first:
                                ch = None
                                self._stdscr.nodelay(0)
                                break
                if ch is not None:
                    self._on_char_cb(ch)
