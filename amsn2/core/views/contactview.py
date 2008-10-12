from stringview import *

""" a view of a contact on the contact list """
class ContactView:
    def __init__(self, core, amsn_contact):

        self.uid = amsn_contact.uid

        self.icon = amsn_contact.icon
        #TODO: apply emblem on dp
        self.dp = amsn_contact.dp
        #self.emblem = amsn_contact.emblem
        self.name = StringView
        self.name = StringView() # TODO : default colors
        self.name.openTag("nickname")
        self.name.appendStringView(amsn_contact.nickname) # TODO parse
        self.name.closeTag("nickname")
        self.name.appendText(" ")
        self.name.openTag("status")
        self.name.appendText("(")
        self.name.appendStringView(amsn_contact.status)
        self.name.appendText(")")
        self.name.closeTag("status")
        self.name.appendText(" ")
        self.name.openTag("psm")
        self.name.setItalic()
        self.name.appendStringView(amsn_contact.personal_message)
        self.name.unsetItalic()
        self.name.closeTag("psm")
        #TODO:
        def startConversation_cb(c_uid):
            core._conversation_manager.newConversation([c_uid])
        self.on_click = startConversation_cb
        self.on_double_click = None
        self.tooltip = None
        self.context_menu = None

    #TODO: @roproperty: context_menu, tooltip




