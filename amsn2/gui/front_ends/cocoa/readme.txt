
aMSN 2 - Cocoa
==============
Thank you for your interest in the Cocoa version of aMSN 2. This Read Me won't explain the architecture of aMSN 2, but is intended to give users/developers an insight into how to build and run aMSN 2 from source.

Building
========
We use NIB files to build our interface, in order to load the NIB's correctly, we require aMSN 2 to be run from inside an application bundle. To build the bundle you need (from macports):

python25
py-openssl (see note)
py25-gobject
py25-pyobjc2-cocoa
	- py25-pyobjc2
	- py25-py2app-devel
		- py25-py2app (see note)

After they have been installed, you will need to run this inside the root folder of amsn2:
$ /opt/local/bin/python2.5 setupCocoa.py py2app -A

This builds the file aMSN2.app into dist. You can now run aMSN2 by double clicking the app, or by running:
$ dist/aMSN2.app/Contents/MacOS/aMSN2

py-openssl - Note
=================
It is recommended to use the 0.7 version of py-openssl. An updated portfile can be found at: http://hosting.notjustanothermacuser.com/macports/py-openssl/Portfiles/0.7_0.tar.gz

py2app - Note
=============
The current py2app on mac ports is out of date, they have 0.3.6, while py25-pyobjc2-cooca requires > 0.4.0. No "official" releases of py2app have been made since 0.3.6, however the current trunk from SVN gives version 0.4.2. If you wish to use macports' python25, and you wish to build the bundle then you will need to update the Portfile for py25-py2app. The updated portfile can be found at: http://hosting.notjustanothermacuser.com/macports/py25-py2app/Portfiles/0.4.2_0.tar.gz

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
