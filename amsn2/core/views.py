
class StringView (object):
    class StringElement(object):
        def __init__(self, type, value):
            self._type = type
            self._value = value

        def getType(self):
            return self._type

        def getValue(self):
            return self._value

    class TextElement(StringElement):
        def __init__(self, text):
            StringElement.__init__(self, "text", text)


    class ColorElement(StringElement):
        def __init__(self, color):
            StringElement.__init__(self, "color", color)

            
    def __init__(self):
        self._elements = []

    def parse(self, str):
        # TODO : actually do parse the string
        self._elements = []
        if str is not None:
            self._elements.append(TextElement(str))

    @staticmethod
    def buildFromString(str):
        ret = StringEx()
        ret.parse(str)
        return ret


class GroupView (object):
    groups = {}
    def __init__(self, uid):
        self._uid = uid
        self._expanded = False
        self._name = None
        self._parsed_name = StringView.buildFromString(self._name)
        self._active_contacts = 0
        self._total_contacts = 0
        self._visible_contacts = []
        self._total_contacts = []
        GroupView.registerGroup(key, self)

    def isExpanded(self):
        return self._expanded

    def isCollapsed(self):
        return not self._expanded

    @staticmethod
    def registerGroup(uid, group):
        GroupView.groups[uid] = group

    @staticmethod
    def getGroup(uid):
        try:
            return GroupView.groups[key]
        except KeyError:
            return None
