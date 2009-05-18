
from amsn2.core.views import StringView
import gobject, pango

GUI_FONT = pango.FontDescription('normal 8')

def stringvToHtml(stringv):
    out = ''
    for x in stringv._elements:
        if x.getType() == StringView.TEXT_ELEMENT:
            out += x.getValue()
        elif x.getType() == StringView.ITALIC_ELEMENT:
            if x.getValue():
                out += '<i>'
            else:
                out += '</i>'
    return out

def escape_pango(str):
    str = gobject.markup_escape_text(str)
    str = str.replace('\n',' ')
    return str
