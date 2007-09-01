#!/usr/bin/env python
import sys
sys.path.append("./pymsn.devel")

from amsn2.core import aMSNCore

def main():
    import sys
    import optparse
    account = ""
    passwd = ""

    if len(sys.argv) >= 2:
        account = sys.argv[1]
    if len(sys.argv) >=3:
        passwd = sys.argv[2]

    parser = optparse.OptionParser()
    parser.add_option("-d", "--debug", action="store_true", dest="debug", default=False,
                  help="Show protocol debug")
    parser.add_option("-c", "--cocoa",
                  action="store_true", dest="use_cocoa", default=False,
                  help="Use the Cocoa front end")
    (options, args) = parser.parse_args()
    print "Options parsed : debug = %s - cocoa = %s", (options.debug, options.use_cocoa)

    amsn = aMSNCore(options)

    if account != "":
        profile = amsn.addProfile(account)
        profile.password = passwd

    if options.use_cocoa is True:
        from amsn2.gui.cocoa import aMSNGUI_Cocoa
        gui = aMSNGUI_Cocoa(amsn)
    else:
        from amsn2.gui.efl import aMSNGUI_EFL
        gui = aMSNGUI_EFL(amsn)
    gui.launch()

    # Should become as simple as :
    # aMSNGUI_EFL(aMSNCore()).launch()

if __name__ == '__main__':
    main()
