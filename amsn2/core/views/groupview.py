
class GroupView (object):
    groups = {}
    def __init__(self, uid):
        self.uid = uid
        self.icon = None
        self.name = None
        self.contacts = []
        self.menu = None
        self.tooltip = None
        GroupView.registerGroup(self.uid, self)

    @staticmethod
    def registerGroup(uid, group):
        GroupView.groups[uid] = group

    @staticmethod
    def getGroup(uid):
        try:
            return GroupView.groups[uid]
        except KeyError:
            return GroupView(uid)
