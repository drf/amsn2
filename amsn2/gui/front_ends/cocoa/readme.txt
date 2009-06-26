
aMSN 2 - Cocoa
==============
Thank you for your interest in the Cocoa version of aMSN 2. This Read Me won't explain the architecture of aMSN 2, but is intended to give users/developers an insight into how to build and run aMSN 2 from source.

Building
========
We use NIB files to build our interface, in order to load the NIB's correctly, we require aMSN 2 to be run from inside an application bundle. To build the bundle you need (from macports):

python25
py25-openssl
py25-gobject
py25-crypto
py25-hashlib
py25-py2app-devel
py25-pyobjc2-cocoa


After they have been installed, you will need to run this inside the root folder of amsn2:
$ /opt/local/bin/python2.5 setupCocoa.py py2app -A

This builds the file aMSN2.app into dist. You can now run aMSN2 by double clicking the app, or by running:
$ dist/aMSN2.app/Contents/MacOS/aMSN2

py-openssl - Note
=================
It is recommended to use the 0.7 version of py-openssl. Last version of Macports is using version 0.7. You can also use an updated portfile that can be found at: http://hosting.notjustanothermacuser.com/macports/py-openssl/Portfiles/0.7_0.tar.gz

py2app - Note
=============
Be sure to use py25-py2app-devel and not py25-py2app from Macports, because py25-py2app is outdated and does not work with pyobjc2-cocoa. 

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

Development
===========
Tech
====
- aMSN2 uses the pyobjc bridge in order to facilitate a Cocoa GUI from python code.

Main Loop
=========
The first challenge was to overcome the dependancy on glib's main loop (as we need to use NSApplication's run: method). Just like the cocoa-gimp project, we have subclassed NSApplication (-> aMSNCocoaNSApplication), and we simply have a method called processEvents: that implements one cycle of the NSApplication run: loop. And hence we can process gevents, and NSEvents.

Support
=======
Currently we only support Mac OS X 10.5.
