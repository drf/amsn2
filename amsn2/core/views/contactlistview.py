from base import BaseUIView

class ContactListView (BaseUIView):
    def __init__(self, uid):
        BaseUIView.__init__(self, uid)
        self.groups = []
