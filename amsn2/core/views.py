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

class TooltipView (object):
    def __init__(self):
        self.name = None
        self.icon = None

    
class KeyBindingView(object):
    BACKSPACE = "Backspace"
    TAB = "Tab"
    ENTER = "Enter"
    ESCAPE = "Escape"
    HOME = "Home"
    END = "End"
    LEFT = "Left"
    RIGHT = "Right"
    UP = "Up"
    DOWN = "Down"
    PAGEUP = "PageUp"
    PAGEDOWN = "PageDown"
    INSERT = "Insert"
    DELETE = "Delete"
    
    def __init__(self, key = None, control = False, alt = False, shift = False):
        self.key = key
        self.control = control
        self.alt = alt
        self.shift = shift
        
    def __repr__(self):
        out = ""
        if self.control:
            out += "Ctrl-"
        if self.alt:
            out += "Alt-"
        if self.shift:
            out += "Shift-"
        out += self.key
        
        return out
    
class MenuItemView(object):
    CASCADE_MENU = "cascade"
    CHECKBUTTON = "checkbutton"
    RADIOBUTTON = "radiobutton"
    SEPARATOR = "separator"
    COMMAND = "command"
    
    def __init__(self, type, label = None, icon = None, accelerator = None,
                 radio_value = None, check_onvalue = None, check_offvalue = None,
                 disabled = False,  command = None, menu = None):
        """ Create a new MenuItemView
        @type : the type of item, can be cascade, checkbutton, radiobutton, separator or command
        @label : the label for the item, unused for separator items
        @accelerator : the accelerator (KeyBindingView) to access this item.
                       If None, an '&' preceding a character of the menu label will set that key with Ctrl- as an accelerator
        @icon : an optional icon to show next to the menu item, unused for separator items
        @radio_value : the value to set when the radiobutton is enabled
        @check_onvalue : the value to set when the checkbutton is enabled
        @check_offvalue : the value to set when the checkbutton is disabled
        @disabled : true if the item's state should be disabled
        @command : the command to call for setting the value for checkbutton and radiobutton items, or the command in case of a 'command' item
        @menu : the MenuView for a cascade item
        """

        if ((type is MenuItemView.SEPARATOR and
             (label is not None or
              icon is not None or
              accelerator is not None or
              radio_value is not None or
              check_onvalue is not None or
              check_offvalue is not None or
              disabled is True or
              command is not None or
              menu is not None)) or
            (type is MenuItemView.CHECKBUTTON and
             (radio_value is not None or
              command is None or
              menu is not None)) or
            (type is MenuItemView.RADIOBUTTON and
             (check_onvalue is not None or
              check_offvalue is not None or
              command is None or
              menu is not None)) or
            (type is MenuItemView.COMMAND and
             (radio_value is not None or
              check_onvalue is not None or
              check_offvalue is not None or
              command is None or
              menu is not None)) or
            (type is MenuItemView.CASCADE_MENU and
             (radio_value is not None or
              check_onvalue is not None or
              check_offvalue is not None or
              command is not None or
              menu is None))):              
            raise ValueError, InvalidArgument

        new_label = label
        if accelerator is None and label is not None:
            done = False
            idx = 0
            new_label = ""
            while not done:
                part = label.partition('&')
                new_label += part[0]
                if part[1] == '&':
                    if part[2].startswith('&'):
                        new_label += '&'
                        label = part[2][1:]
                    elif len(part[2]) > 0:
                        if accelerator is None:
                            accelerator = KeyBindingView(key = part[2][0], control = True)
                        label = part[2]
                    else:
                        done = True
                else:
                    done = True
        

        self.type = type
        self.label = new_label
        self.icon = icon
        self.accelerator = accelerator
        self.radio_value = radio_value
        self.check_onvalue = check_onvalue
        self.check_offvalue = check_offvalue
        self.disabled = disabled
        self.command = command
        self.menu = menu
             
            
        
        
        
class MenuView (object):
    def __init__(self):
        self.items = []

    def addItem(self, item):
        self.items.append(item)
        
