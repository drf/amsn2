
from amsn2.gui import base
from amsn2.core import views
import gtk

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
        """
        @type message: str
        @type actions: tuple
        @param actions: A tuple containing the options between
        which the user can choose. Every option is a tuple itself, of the form (name, callback),
        where callback is the function that will be called if the option is selected.

        This will eventually call the related show() method, so the window is
        displayed when created.
        """
        gtk.Dialog.__init__(self, "aMSN Dialog", None, gtk.DIALOG_NO_SEPARATOR, None)

        id = -1
        for name, cb in actions:
            dialog.add_button(name, id)
            self._cbs[id] = cb
            id = id - 1

        self.connect("response", self.onResponse)
        self.show()

    def onResponse(self, dialog, id):
        try:
            self._cbs[id]()
        except ValueError:
            print "Unknown dialog choice, id %s" % id
        self.destroy()

# TODO: build contactinput, groupinput, contactremove, groupremove instead of one window for all, and change the base API too
class aMSNInputWindow(base.aMSNInputWindow, gtk.Dialog):
    def __init__(self, message, type, callback, params):
        """
        @type message: str
        @type type: ContactView or GroupView
        @param type: contains the view to fill.
        @type callback: function
        @param callback: The function that will be called when the view has been filled.
        The prototype is callback(view), where view is the ContactView or the Grouview
        filled, or None if the input has been canceled.
        @type params: tuple
        @param params: a list of existing contacts or groups
        """
        gtk.Dialog.__init__(self, "aMSN Input", None, gtk.DIALOG_NO_SEPARATOR,
                            (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                             gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
        self._callback = callback
        self._view , going_to_add = type

        label = gtk.Label(message)
        self._name = gtk.Entry()
        ca = self.get_content_area()
        ca.set_spacing(5)
        ca.pack_start(label)
        ca.pack_start(self._name)

        # TODO: build list of existing contacts/groups if going_to_add a group or a contact
        if isinstance(type[0], views.ContactView):
            if going_to_add:
                label2 = gtk.Label("Message: ")
                ca.pack_start(label2)
                self._message = gtk.Entry()
                ca.pack_start(self._message)
                label2.show()
                self._message.show()
        elif isinstance(type[0], views.GroupView):
            pass
        else:
            # TODO: get the string from the core
            aMSNErrorWindow("Can't build an input window of type %s" % type[0])
            self.destroy()
            return

        self.connect("response", self.onResponse)
        label.show()
        self._name.show()
        self.show()

    def onResponse(self, dialog, id):
        if id == gtk.RESPONSE_ACCEPT:
            self._view.account = self._name.get_text()
            if self._view.account:
                self._callback(self._view)
            else:
                # TODO: get the string from the core
                aMSNErrorWindow("The input can't be empty")
        elif id == gtk.RESPONSE_REJECT:
            self._callback(None)
        self.destroy()
