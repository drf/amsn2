from stringview import *

class MessageView:
    MESSAGE_INCOMING = 0
    MESSAGE_OUTGOING = 1
    def __init__(self):
        self.msg = StringView()
        self.sender = StringView()
        self.sender_icon = None
        self.message_type = MessageView.MESSAGE_INCOMING


    #TODO: toMessageStyle or sthg like that

    def toStringView(self):
        strv = StringView()
        strv.appendStringView(self.sender)
        strv.appendText(" says:\n")
        strv.appendStringView(self.msg)
        strv.appendText("\n")

        return strv

