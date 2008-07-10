from base import BaseUIView

class GroupView (BaseUIView):
    def __init__(self, uid):
        BaseUIView.__init__(self, uid)
        self.contacts = []

    @staticmethod
    def getGroup(uid):
        group = BaseUIView.getView(uid)
        if group is None:
            return GroupView(uid)
        else:
            return group
