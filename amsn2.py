#!/usr/bin/env python
import sys
import os
import optparse
sys.path.insert(0, "./pymsn")

from amsn2.core import aMSNCore

if __name__ == '__main__':
    account = None
    passwd = None
    default_front_end = "console"

    if os.name == "posix":
        system = os.uname()[0]
        if system == "Linux":
            
            """ Here we are trying to import some base modules for the GUI
            interfaces to get a working default frontend. EFL is the first one,
            then come the others.
            
            Suggestion/TODO: we can avoid OS detection through this method.
            I think it makes more sense creating a priority list, something like
            that one:
            
            cocoa > efl > qt4 > gtk > console
            
            As you can imagine, the OS you're using no longer matters: IMHO
            this list (except for qt & gtk, didn't know what to put first) is
            the right way to do it, since it tries to be as native as possible.
            There are some even better ways to do it, especially on gtk/qt side.
            For example, we can use DBus to know what DE is running.
            
            So, my thoughts on how to do it:
            Try cocoa, try Efl. If both went bad, try to see if DBus is running.
            If not, we're probably not on Linux, so give priority to Qt. If it is,
            check for kded service or for a GNOME service and choose that toolkit.
            When all else fails, console will be our friend.
            
            This way we'll have the best default possible, and as you can see
            from the first implementation, it's really easy to do.
            """
            
            try:
                import ecore
                default_front_end = "efl"
            except ImportError: # Efl not available
                try:
                    import PyQt4.QtGui
                    default_front_end = "qt4"
                except ImportError: # Qt not available
                    try:
                        import gtk
                        default_front_end = "gtk"
                    except ImportError: # GTK not available
                        print "No graphical toolkits detected, falling back to console..."
                        default_front_end = "console"
                        
        elif system == "Darwin":
            default_front_end = "cocoa"
    elif os.name == "nt":
        default_front_end = "qt4"
            

    parser = optparse.OptionParser()
    parser.add_option("-a", "--account", dest="account",
                      default=None, help="The account's username to use")
    parser.add_option("-p", "--password", dest="password",
                      default=None, help="The account's password to use")
    parser.add_option("-f", "--front-end", dest="front_end",
                      default=default_front_end, help="The frontend to use")
    parser.add_option("-d", "--debug", action="store_true", dest="debug",
                      default=False, help="Show protocol debug")
    (options, args) = parser.parse_args()
    
    amsn = aMSNCore(options)
    
    amsn.run()

