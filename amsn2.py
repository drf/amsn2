#!/usr/bin/env python
import sys
import os
import optparse
sys.path.insert(0, "./pymsn")

from amsn2.core import aMSNCore

if __name__ == '__main__':
    account = None
    passwd = None
    system = os.uname()[0]
    default_front_end = "console"

    if system == "Linux":
        default_front_end = "efl"
    elif system == "Darwin":
        default_front_end = "cocoa"

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

