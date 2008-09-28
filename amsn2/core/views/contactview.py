from base import BaseUIView
from stringview import StringView
from imageview import ImageView

class ContactView (BaseUIView):
    class Updated:
        NONE = 0
        ICON = 1
        DP = 2
        EMBLEM = 4
        STATUS = 8
        ACCOUNT = 16
        NICKNAME = 32
        FRIENDLY_NAME = 64
        PSM = 128
        CURRENT_MEDIA = 512
        HAS_SPACE = 1024
        NAME = 2048


    def __init__(self, core, uid):
        BaseUIView.__init__(self, uid)
        self.icon = ImageView()
        self.dp = ImageView(ImageView.ResourceType.SKIN,"default_dp")
        self.emblem = ImageView()
        self.status = None
        self.account = None
        self.nickname = StringView()
        self.friendly_name = StringView()
        self.psm = StringView()
        self.current_media = None
        self.has_space = None
        self.name = StringView()
        self.pymsn_contact = None
        self.updated = ContactView.Updated.NONE

    @staticmethod
    def getContact(core, uid, pymsn_contact = None, updated = 0):
        contact = BaseUIView.getView(uid)
        if contact is None:
            r = ContactView(core, uid)
        else:
            r = contact
        if pymsn_contact is not None:
            r.__updateView(core, pymsn_contact, updated)
        return r


    def __updateView(self, core, pymsn_contact, updated = 0):

        self.updated = updated
        #check if the status is changed
        if self.updated & ContactView.Updated.STATUS:
            self.status = core.p2s[pymsn_contact.presence]
            #icon
            self.icon.load("Skin","buddy_" + core.p2s[pymsn_contact.presence])
            self.updated |= ContactView.Updated.ICON
            #emblem
            self.emblem.load("Skin","emblem_" + core.p2s[pymsn_contact.presence])
            self.updated |= ContactView.Updated.EMBLEM

        if self.updated & ContactView.Updated.DP:
            pass

        if self.updated & ContactView.Updated.ACCOUNT:
            self.account = pymsn_contact.account

        if self.updated & ContactView.Updated.NICKNAME:
            #TODO: parse...
            self.nickname.reset()
            self.nickname.appendText(pymsn_contact.display_name)

        if self.updated & ContactView.Updated.PSM:
            #TODO: parse...
            self.psm.reset()
            self.psm.appendText(pymsn_contact.personal_message)

        if self.updated & ContactView.Updated.CURRENT_MEDIA:
            self.current_media = pymsn_contact.current_media

        if self.updated & ( ContactView.Updated.NICKNAME
                           | ContactView.Updated.STATUS
                           | ContactView.Updated.PSM ):
            self.updated |= ContactView.Updated.NAME
            self.name.reset() # TODO : default colors
            self.name.openTag("nickname")
            self.name.appendStringView(self.nickname)
            self.name.closeTag("nickname")
            self.name.appendText(" ")
            self.name.openTag("status")
            self.name.appendText("(")
            self.name.appendText(self.status)
            self.name.appendText(")")
            self.name.closeTag("status")
            self.name.appendText(" ")
            self.name.openTag("psm")
            self.name.setItalic()
            self.name.appendStringView(self.psm)
            self.name.unsetItalic()
            self.name.closeTag("psm")

        self.pymsn_contact = pymsn_contact

    def __repr__(self):
        template = "<ContactView uid='%s' name='%s' account='%s'>"
        return template % (self.uid, self.name.toString(), self.account)

