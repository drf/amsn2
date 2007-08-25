#!/usr/bin/env python
import sys
sys.path.append("./pymsn.devel")

from amsn2.core import aMSNCore
from amsn2.gui.efl import aMSNGUI_EFL

def main():
    import sys
    use_cocoa = False

    if len(sys.argv) < 3:
        print "Usage : %s username password" % (sys.argv[0])
        return
    else:
        account = sys.argv[1]
        passwd = sys.argv[2]

    amsn = aMSNCore()
    profile = amsn.addProfile(account)
    profile.password = passwd

    if use_cocoa is True:
        gui = aMSNGUI_Cocoa(amsn)
    else:
        gui = aMSNGUI_EFL(amsn)
    gui.launch()

    # Should become as simple as :
    # aMSNGUI_EFL(aMSNCore()).launch()

if __name__ == '__main__':
    main()
