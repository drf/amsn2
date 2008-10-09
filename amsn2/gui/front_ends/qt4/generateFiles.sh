#!/bin/sh

#pyrcc4 -o src/faigaresource_rc.py ui/faigaresource.qrc

pyuic4 -o ui_login.py login.ui
pyuic4 -o ui_contactlist.py contactlist.ui
pyuic4 -o ui_chatwindow.py chatWindow.ui
