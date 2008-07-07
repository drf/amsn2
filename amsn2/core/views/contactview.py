
class ContactView (object):
    contacts = {}
    def __init__(self, uid):
        self.uid = uid
        self.icon = None
        self.name = None 
        self.dp = None
        self.menu = None
        self.tooltip = None
        ContactView.registerContact(self.uid, self)


    @staticmethod
    def registerContact(uid, contact):
        ContactView.contacts[uid] = contact

    @staticmethod
    def getContact(uid):
        try:
            return ContactView.contacts[uid]
        except KeyError:
            return ContactView(uid)

