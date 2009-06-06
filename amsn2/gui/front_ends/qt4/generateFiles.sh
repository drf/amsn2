#!/bin/sh

#pyrcc4 -o src/faigaresource_rc.py ui/faigaresource.qrc

which pyuic4>/dev/null
if [ $? != 0 ]; then
 echo >&2 "This script requires pyuic4 installed."
 exit 255
fi

pyuic4 -o ui_login.py login.ui
pyuic4 -o ui_contactlist.py contactlist.ui
pyuic4 -o ui_chatWindow.py chatWindow.ui
