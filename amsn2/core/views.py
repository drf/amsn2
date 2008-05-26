
class StringViewTypes:
    TEXT_ELEMENT = "text"
    COLOR_ELEMENT = "color"
    BACKGROUND_ELEMENT = "bgcolor"
    IMAGE_ELEMENT = "image"

# Font ? padding ? underline/bold/italic ?

class StringView (object):
    class StringElement(object):
        def __init__(self, type, value):
            self._type = type
            self._value = value

        def getType(self):
            return self._type

        def getValue(self):
            return self._value

    class ColorElement(StringElement):
        def __init__(self, color):
            StringElement.__init__(self, COLOR_ELEMENT, color)
    class BackgroundColorElement(StringElement):
        def __init__(self, color):
            StringElement.__init__(self, BACKGROUND_ELEMENT, color)
    class TextElement(StringElement):
        def __init__(self, text):
            StringElement.__init__(self, TEXT_ELEMENT, text)
    class ImageElement(StringElement):
        def __init__(self, image):
            StringElement.__init__(self, IMAGE_ELEMENT, image)
            
    def __init__(self, default_background_color, default_color):
        self._elements = []

        self._default_background_color = default_background_color
        self._default_color = default_color
        self.resetColor()
        self.resetBackgroundColor()

    def append(self, type, value):
        self._elements.append(StringElement(type, value))

    def appendText(self, text):
        self._elements.append(TextElement(text))
    def appendImage(self, image):
        self._elements.append(ImageElement(image))
    def setColor(self, color):
        self._elements.append(ColorElement(color))
    def setBackgroundColor(self, color):
        self._elements.append(BackgroundColorElement(color))
        
    def resetColor(self):
        self.setColor(self._default_color)
    def resetBackgroundColor(self):
        self.setBackgroundColor(self._default_background_color)


class GroupView (object):
    groups = {}
    def __init__(self, uid):
        self._uid = uid
        self._expanded = False
        self._name = StringView(None, None)
        self._active_contacts = 0
        self._total_contacts = 0
        self._visible_contacts = []
        self._contacts = []
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

class ContactView (object):
    contacts = {}
    def __init__(self, uid):
        self._uid = uid
        self._blocked = False
        self._name = StringView(None, None)
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
