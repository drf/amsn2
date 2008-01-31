#!/usr/bin/env python
import sys
sys.path.append("./pymsn")

from amsn2.core import aMSNCore

def main():
    import optparse
    account = ""
    passwd = ""

    parser = optparse.OptionParser()
    parser.add_option("-d", "--debug", action="store_true", dest="debug", default=False,
                  help="Show protocol debug")
    parser.add_option("-c", "--cocoa",
                  action="store_true", dest="use_cocoa", default=False,
                  help="Use the Cocoa front end")
    (options, args) = parser.parse_args()
    print "Options parsed : debug = %s - cocoa = %s - args : %s" % (options.debug, options.use_cocoa, args)

    amsn = aMSNCore(options)

    if len(args) >= 1:
        account = args[0]
    if len(args) >=2:
        passwd = args[1]

    print "default profile set to %s:%s" % (account, passwd)
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
