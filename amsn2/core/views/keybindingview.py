
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
    
