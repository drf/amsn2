
class BaseUIView (object):
    views = {}
    def __init__(self, uid):
        self.uid = uid
        self.icon = None
        self.name = None
        self.menu = None
        self.tooltip = None
        if self.uid != None:
            BaseUIView.registerView(self.uid, self)

    @staticmethod
    def registerView(uid, view):
        BaseUIView.views[uid] = view

    @staticmethod
    def getView(uid):
        try:
            return BaseUIView.views[uid]
        except KeyError:
            return None
