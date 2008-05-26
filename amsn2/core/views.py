
class StringViewTypes:
    TEXT_ELEMENT = "text"
    COLOR_ELEMENT = "color"
    BACKGROUND_ELEMENT = "bgcolor"
    IMAGE_ELEMENT = "image"
    OPEN_TAG_ELEMENT = "tag"
    CLOSE_TAG_ELEMENT = "-tag"

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
            StringView.StringElement.__init__(self, StringViewTypes.COLOR_ELEMENT, color)
    class BackgroundColorElement(StringElement):
        def __init__(self, color):
            StringView.StringElement.__init__(self, StringViewTypes.BACKGROUND_ELEMENT, color)
    class TextElement(StringElement):
        def __init__(self, text):
            StringView.StringElement.__init__(self, StringViewTypes.TEXT_ELEMENT, text)
    class ImageElement(StringElement):
        def __init__(self, image):
            StringView.StringElement.__init__(self, StringViewTypes.IMAGE_ELEMENT, image)
    class OpenTagElement(StringElement):
        def __init__(self, tag):
            StringView.StringElement.__init__(self, StringViewTypes.OPEN_TAG_ELEMENT, tag)
    class CloseTagElement(StringElement):
        def __init__(self, tag):
            StringView.StringElement.__init__(self, StringViewTypes.CLOSE_TAG_ELEMENT, tag)
            
    def __init__(self, default_background_color, default_color):
        self._elements = []

        self._default_background_color = default_background_color
        self._default_color = default_color
        self.resetColor()
        self.resetBackgroundColor()

    def append(self, type, value):
        self._elements.append(StringElement(type, value))

    def appendText(self, text):
        self._elements.append(StringView.TextElement(text))
    def appendImage(self, image):
        self._elements.append(StringView.ImageElement(image))
    def setColor(self, color):
        self._elements.append(StringView.ColorElement(color))
    def setBackgroundColor(self, color):
        self._elements.append(StringView.BackgroundColorElement(color))
    def openTag(self, tag):
        self._elements.append(StringView.OpenTagElement(tag))
    def closeTag(self, tag):
        self._elements.append(StringView.CloseTagElement(tag))
        
    def resetColor(self):
        self.setColor(self._default_color)
    def resetBackgroundColor(self):
        self.setBackgroundColor(self._default_background_color)

    def toString(self):
        out = ""
        for x in self._elements:
            if x.getType() == StringViewTypes.TEXT_ELEMENT:
                out += x.getValue()
                
        return out

    def __repr__(self):
        out = "{"
        for x in self._elements:
            out += "[" + x.getType() + "=" + str(x.getValue()) + "]"
            
        out += "}"
        return out
        


class GroupView (object):
    groups = {}
    def __init__(self, uid):
        self.uid = uid
        self.icon = None
        self.name = None
        self.contacts = []
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

class ContactView (object):
    contacts = {}
    def __init__(self, uid):
        self.uid = uid
        self.icon = None
        self.name = None 
        self.dp = None
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
