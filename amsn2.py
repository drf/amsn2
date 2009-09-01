#!/usr/bin/env python
import sys
import os
import optparse
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
sys.path.insert(0, "./papyon")
import locale
locale.setlocale(locale.LC_ALL, '')

from amsn2.core import aMSNCore

if __name__ == '__main__':
    account = None
    passwd = None
    default_front_end = "gtk"

    parser = optparse.OptionParser()
    parser.add_option("-a", "--account", dest="account",
                      default=None, help="The account's username to use")
    parser.add_option("-p", "--password", dest="password",
                      default=None, help="The account's password to use")
    parser.add_option("-f", "--front-end", dest="front_end",
                      default=default_front_end, help="The frontend to use")
    parser.add_option("-d", "--debug-protocol", action="store_true", dest="debug_protocol",
                      default=False, help="Show protocol debug")
    parser.add_option("-D", "--debug-amsn2", action="store_true", dest="debug_amsn2",
                      default=False, help="Show amsn2 debug")
    (options, args) = parser.parse_args()
    
    amsn = aMSNCore(options)
    
    amsn.run()

