from base import BaseUIView

class ContactView (BaseUIView):
    def __init__(self, uid):
        BaseUIView.__init__(self, uid)
        self.icon = None
        self.dp = None
        self.emblem = None
        self.name = None

    @staticmethod
    def getContact(uid):
        contact = BaseUIView.getView(uid)
        if contact is None:
            return ContactView(uid)
        else:
            return contact
