
from amsn2.gui import base
from amsn2.core import views
import gtk
import logging

logger = logging.getLogger('amsn2.gtk.utility')

class aMSNErrorWindow(base.aMSNErrorWindow, gtk.Dialog):
    def __init__(self, error_text):
        gtk.Dialog.__init__(self, "aMSN Error", None, gtk.DIALOG_NO_SEPARATOR,
                            (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        label = gtk.Label(error_text)
        self.get_content_area().set_spacing(5)
        self.get_content_area().pack_start(label)
        label.show()
        self.connect("response", self.onResponse)
        self.show()

    def onResponse(self, dialog, id):
        self.destroy()

class aMSNNotificationWindow(base.aMSNNotificationWindow, gtk.Dialog):
    def __init__(self, notification_text):
        gtk.Dialog.__init__(self, "aMSN Notification", None, gtk.DIALOG_NO_SEPARATOR,
                            (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        label = gtk.Label(notification_text)
        self.get_content_area().set_spacing(5)
        self.get_content_area().pack_start(label)
        label.show()
        self.connect("response", self.onResponse)
        self.show()

    def onResponse(self, dialog, id):
        self.destroy()

class aMSNDialogWindow(base.aMSNDialogWindow, gtk.Dialog):
    def __init__(self, message, actions):
        gtk.Dialog.__init__(self, "aMSN Dialog", None, gtk.DIALOG_NO_SEPARATOR, None)

        label = gtk.Label(message)
        ca = self.get_content_area()
        ca.pack_start(label)

        id = -1
        self._cbs = {}
        for act in actions:
            name, cb = act
            self.add_button(name, id)
            self._cbs[id] = cb
            id = id - 1

        self.connect("response", self.onResponse)
        label.show()
        self.show()

    def onResponse(self, dialog, id):
        try:
            self._cbs[id]()
        except KeyError:
            logger.warning("Unknown dialog choice, id %s" % id)
        self.destroy()

class aMSNContactInputWindow(base.aMSNContactInputWindow, gtk.Dialog):
    def __init__(self, message, callback, groups):
        gtk.Dialog.__init__(self, "aMSN Contact Input", None, gtk.DIALOG_NO_SEPARATOR,
                            (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                             gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
        self._callback = callback

        label = gtk.Label(message[0])
        self._name = gtk.Entry()
        ca = self.get_content_area()
        ca.set_spacing(5)
        ca.pack_start(label)
        ca.pack_start(self._name)

        # TODO: build list of existing groups
        label2 = gtk.Label(message[1])
        ca.pack_start(label2)
        self._message = gtk.Entry()
        ca.pack_start(self._message)
        label2.show()
        self._message.show()

        self.connect("response", self.onResponse)
        label.show()
        self._name.show()
        self.show()

    def onResponse(self, dialog, id):
        if id == gtk.RESPONSE_ACCEPT:
            name = self._name.get_text()
            msg = self._message.get_text()
            self._callback(name, msg)
        elif id == gtk.RESPONSE_REJECT:
            pass
        self.destroy()


class aMSNGroupInputWindow(base.aMSNGroupInputWindow, gtk.Dialog): 
    def __init__(self, message, callback, contacts):
        gtk.Dialog.__init__(self, "aMSN Group Input", None, gtk.DIALOG_NO_SEPARATOR,
                            (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                             gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
        self._callback = callback

        label = gtk.Label(message[0])
        self._name = gtk.Entry()
        ca = self.get_content_area()
        ca.set_spacing(5)
        ca.pack_start(label)
        ca.pack_start(self._name)

        # TODO: build list of existing contacts
        label2 = gtk.Label(message[1])
        ca.pack_start(label2)
        self._message = gtk.Entry()
        ca.pack_start(self._message)
        label2.show()
        self._message.show()

        self.connect("response", self.onResponse)
        label.show()
        self._name.show()
        self.show()

    def onResponse(self, dialog, id):
        if id == gtk.RESPONSE_ACCEPT:
            name = self._name.get_text()
            self._callback(name)
        elif id == gtk.RESPONSE_REJECT:
            pass
        self.destroy()

class aMSNContactDeleteWindow(base.aMSNContactDeleteWindow, gtk.Dialog): 
    def __init__(self, message, callback, contacts):
        gtk.Dialog.__init__(self, "aMSN Contact Input", None, gtk.DIALOG_NO_SEPARATOR,
                            (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                             gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
        self._callback = callback

        label = gtk.Label(message)
        self._name = gtk.Entry()
        ca = self.get_content_area()
        ca.set_spacing(5)
        ca.pack_start(label)
        ca.pack_start(self._name)

        self.connect("response", self.onResponse)
        label.show()
        self._name.show()
        self.show()

    def onResponse(self, dialog, id):
        if id == gtk.RESPONSE_ACCEPT:
            name = self._name.get_text()
            self._callback(name)
        elif id == gtk.RESPONSE_REJECT:
            pass
        self.destroy()

class aMSNGroupDeleteWindow(base.aMSNGroupDeleteWindow, gtk.Dialog): 
    def __init__(self, message, callback, groups):
        gtk.Dialog.__init__(self, "aMSN Group Input", None, gtk.DIALOG_NO_SEPARATOR,
                            (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                             gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
        self._callback = callback

        label = gtk.Label(message)
        self._name = gtk.Entry()
        ca = self.get_content_area()
        ca.set_spacing(5)
        ca.pack_start(label)
        ca.pack_start(self._name)

        self.connect("response", self.onResponse)
        label.show()
        self._name.show()
        self.show()

    def onResponse(self, dialog, id):
        if id == gtk.RESPONSE_ACCEPT:
            name = self._name.get_text()
            self._callback(name)
        elif id == gtk.RESPONSE_REJECT:
            pass
        self.destroy()

