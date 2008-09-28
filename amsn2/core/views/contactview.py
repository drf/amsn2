from base import BaseUIView
from stringview import StringView

class ContactView (BaseUIView):
    class Updated:
        NONE = 0
        ICON = 1
        DP = 2
        EMBLEM = 4
        STATUS = 8
        NICK = 16
        FRIENDLY_NAME = 32
        PSM = 64
        CURRENT_MEDIA = 128
        HAS_SPACE = 256
        NAME = 512


    def __init__(self, uid):
        BaseUIView.__init__(self, uid)
        self.icon = None
        self.dp = None
        self.emblem = None
        self.status = None
        self.nick = None
        self.friendly_name = None
        self.psm = None
        self.current_media = None
        self.has_space = None
        self.name = None
        self.pymsn_contact = None
        self.updated = self.Updated.NONE

    @staticmethod
    def getContact(core, uid, pymsn_contact = None):
        contact = BaseUIView.getView(uid)
        if contact is None:
            r = ContactView(uid)
        else:
            r = contact
        if pymsn_contact is not None:
            r.__updateView(core, pymsn_contact)
        return r


    def __updateView(self, core, pymsn_contact):
        #TODO:

        self.updated = self.Updated.NONE

        self.icon = core._gui.gui.Image(core, core._main)
        self.icon.load("Skin","buddy_" + core.p2s[pymsn_contact.presence])
        self.dp = core._gui.gui.Image(core, core._main)
        self.dp.load("Skin","default_dp")
        self.name = StringView() # TODO : default colors
        self.name.openTag("nickname")
        self.name.appendText(pymsn_contact.display_name) # TODO parse
        self.name.closeTag("nickname")
        self.name.appendText(" ")
        self.name.openTag("status")
        self.name.appendText("(")
        self.name.appendText(core.p2s[pymsn_contact.presence])
        self.name.appendText(")")
        self.name.closeTag("status")
        self.name.appendText(" ")
        self.name.openTag("psm")
        self.name.setItalic()
        self.name.appendText(pymsn_contact.personal_message)
        self.name.unsetItalic()
        self.name.closeTag("psm")

        self.pymsn_contact = pymsn_contact

