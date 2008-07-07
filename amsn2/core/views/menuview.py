
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
        
