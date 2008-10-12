from stringview import *

class GroupView:
    def __init__(self, uid, name, contact_ids=[], active=0):
        self.uid = uid
        self.contact_ids = contact_ids
        self.icon = None # TODO: expanded/collapsed icon
        self.name = StringView() # TODO: default color from skin/settings
        self.name.appendText(name) #TODO: parse for smileys
        active = 0 #TODO
        total = len(self.contact_ids)
        self.name.appendText("(" + str(active) + "/" + str(total) + ")")

        self.on_click = None #TODO: collapse, expand
        self.on_double_click = None
        self.tooltip = None
        self.context_menu = None


    #TODO: @roproperty: context_menu, tooltip

