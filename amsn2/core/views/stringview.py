
class StringView (object):
    TEXT_ELEMENT = "text"
    COLOR_ELEMENT = "color"
    BACKGROUND_ELEMENT = "bgcolor"
    IMAGE_ELEMENT = "image"
    OPEN_TAG_ELEMENT = "tag"
    CLOSE_TAG_ELEMENT = "-tag"
    ITALIC_ELEMENT = "italic"
    BOLD_ELEMENT = "bold"
    UNDERLINE_ELEMENT = "underline"
    FONT_ELEMENT = "font"

    # padding ? 

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
            StringView.StringElement.__init__(self, StringView.COLOR_ELEMENT, color)
    class BackgroundColorElement(StringElement):
        def __init__(self, color):
            StringView.StringElement.__init__(self, StringView.BACKGROUND_ELEMENT, color)
    class TextElement(StringElement):
        def __init__(self, text):
            StringView.StringElement.__init__(self, StringView.TEXT_ELEMENT, text)
    class ImageElement(StringElement):
        def __init__(self, image):
            StringView.StringElement.__init__(self, StringView.IMAGE_ELEMENT, image)
    class OpenTagElement(StringElement):
        def __init__(self, tag):
            StringView.StringElement.__init__(self, StringView.OPEN_TAG_ELEMENT, tag)
    class CloseTagElement(StringElement):
        def __init__(self, tag):
            StringView.StringElement.__init__(self, StringView.CLOSE_TAG_ELEMENT, tag)
    class FontElement(StringElement):
        def __init__(self, font):
            StringView.StringElement.__init__(self, StringView.FONT_ELEMENT, font)
    class BoldElement(StringElement):
        def __init__(self, bold):
            StringView.StringElement.__init__(self, StringView.BOLD_ELEMENT, bold)
    class ItalicElement(StringElement):
        def __init__(self, italic):
            StringView.StringElement.__init__(self, StringView.ITALIC_ELEMENT, italic)
    class UnderlineElement(StringElement):
        def __init__(self, underline):
            StringView.StringElement.__init__(self, StringView.UNDERLINE_ELEMENT, underline)
            
    def __init__(self, default_background_color = None, default_color = None, default_font = None):
        self._elements = []

        self._default_background_color = default_background_color
        self._default_color = default_color
        self._default_font = default_font
        
        if default_color is not None:
            self.resetColor()
        if default_background_color is not None:
            self.resetBackgroundColor()
        if default_font is not None:
            self.resetFont()

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
    def setFont(self, font):
        self._elements.append(StringView.FontElement(font))
    def openTag(self, tag):
        self._elements.append(StringView.OpenTagElement(tag))
    def closeTag(self, tag):
        self._elements.append(StringView.CloseTagElement(tag))
        
    def setBold(self):
        self._elements.append(StringView.BoldElement(True))
    def unsetBold(self):
        self._elements.append(StringView.BoldElement(False))
    def setItalic(self):
        self._elements.append(StringView.ItalicElement(True))
    def unsetItalic(self):
        self._elements.append(StringView.ItalicElement(False))
    def setUnderline(self):
        self._elements.append(StringView.UnderlineElement(True))
    def unsetUnderline(self):
        self._elements.append(StringView.UnderlineElement(False))
        
    def resetColor(self):
        self.setColor(self._default_color)
    def resetBackgroundColor(self):
        self.setBackgroundColor(self._default_background_color)
    def resetFont(self):
        self.setFont(self._default_font)

    def toString(self):
        out = ""
        for x in self._elements:
            if x.getType() == StringView.TEXT_ELEMENT:
                out += x.getValue()
                
        return out

    def __str__(self):
        return self.toString()

    def __repr__(self):
        out = "{"
        for x in self._elements:
            out += "[" + x.getType() + "=" + str(x.getValue()) + "]"
            
        out += "}"
        return out
        
