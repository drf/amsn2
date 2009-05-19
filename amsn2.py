#!/usr/bin/env python
import sys
import os
import optparse
sys.path.insert(0, "./papyon")
import locale
locale.setlocale(locale.LC_ALL, '')

from amsn2.core import aMSNCore

if __name__ == '__main__':
    account = None
    passwd = None
    default_front_end = "console"

    # Detect graphical toolkit available.
    # Format - 'default_front_end : module name'
    # cocoa > efl > qt4 > gtk > console
    toolkits = {'cocoa' : 'amsn2.gui.front_ends.cocoa',
                'elf' : 'ecore',
                'qt4' : 'PyQt4.QtGui',
                'gtk' : 'gtk',
                'console' : None}
    for toolkit in toolkits:
        try:
            module_name = toolkits[toolkit]
            module = __import__(module_name)
            default_front_end = toolkit
            vars()[module_name] = module
            # Debug
            # print 'Imported toolkit "%s" with module "%s"' % (toolkit, module)
            break
        except ImportError:
        	# Debug
            # print 'Couldn\'t import %s - doesn\'t exist!' % module_name
            pass
        except TypeError:
            pass
        
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

